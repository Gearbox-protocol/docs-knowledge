# Liquidation: Detection & Execution

Detect unhealthy or expired Credit Accounts, execute full or partial liquidations via CreditFacadeV3, and extract the liquidation premium — all permissionless (FACT-056).

| Concept | Mechanism |
|---------|-----------|
| **Health Factor** | `HF = TWV / Total Debt` (FACT-050). Account is liquidatable when `HF < 1`. |
| **TWV** | `sum(Balance_i × Price_i × LT_i)` — collateral value discounted by per-token Liquidation Thresholds (FACT-051). |
| **Total Debt** | `Principal + BaseInterest + QuotaInterest + Fees` (FACT-052). |
| **Full Liquidation** | `liquidateCreditAccount` closes the account entirely — liquidator swaps assets via multicall, pool is repaid, remainder sent to `to` (FACT-014). |
| **Partial Liquidation** | `partiallyLiquidateCreditAccount` repays a portion of debt, seizes discounted collateral — account stays open if HF recovers (FACT-015, FACT-060). |
| **Liquidation Premium** | `1 - LiquidationDiscount` — profit margin paid to the liquidator from collateral value (FACT-053). |
| **Liquidation Fee** | Percentage of collateral value taken by the protocol Treasury (FACT-054). |
| **Expiry Liquidation** | Separate (usually lower) fee/discount parameters for expired accounts (FACT-055). |
| **Loss Policy** | `AliasedLossPolicyV3` re-checks solvency with TWAP-based alias price feeds before allowing bad debt liquidation (FACT-059). |

**Contracts:** [`CreditFacadeV3.sol`](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/credit/CreditFacadeV3.sol) · [`ICreditFacadeV3.sol`](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/interfaces/ICreditFacadeV3.sol) · [`CreditManagerV3.sol`](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/credit/CreditManagerV3.sol) · [`ICreditManagerV3.sol`](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/interfaces/ICreditManagerV3.sol)

---

## Account Scanning

Identify liquidatable accounts by iterating Credit Accounts and checking health factors per block.

### Scan Approaches

| Approach | Method | When to use |
|----------|--------|-------------|
| On-chain enumeration | `CreditAccountCompressor.getCreditAccountData()` per account | Full-node access, custom filtering |
| SDK | `GearboxSDK` market scanning | Rapid prototyping, dashboard monitoring |
| Event indexing | Index `OpenCreditAccount` / `CloseCreditAccount` events, maintain live set | High-performance bots, reduced RPC load |

### Check Liquidatability

Two methods on CreditManagerV3:

| Method | Signature | Returns |
|--------|-----------|---------|
| Health check | `isLiquidatable(address creditAccount, uint16 minHealthFactor)` (FACT-103) | `bool` — true when `HF < minHealthFactor / 10000` |
| Full breakdown | `calcDebtAndCollateral(address creditAccount, CollateralCalcTask task)` (FACT-102) | Struct with `totalDebtUSD`, `twvUSD`, per-token balances |

Pass `minHealthFactor = 10000` (= 1.0) to detect all liquidatable accounts.

**TypeScript**

```typescript
// using cm from Setup section
const accounts = await getActiveCreditAccounts(); // from indexer or compressor

for (const account of accounts) {
  const liquidatable = await cm.isLiquidatable(account, 10000);
  if (liquidatable) {
    const data = await cm.calcDebtAndCollateral(account, 1);
    console.log(`Liquidatable: ${account}`);
    console.log(`  Debt: ${data.totalDebtUSD}, TWV: ${data.twvUSD}`);
  }
}
```

**Solidity**

```solidity
// Inside a contract with ICreditManagerV3 creditManager
function checkLiquidatable(address creditAccount) external view returns (bool) {
    return creditManager.isLiquidatable(creditAccount, 10000);
}
```

---

## Setup

Instantiate CreditFacadeV3 and CreditManagerV3 with liquidation-specific ABIs. All subsequent examples reference these instances.

**TypeScript (ethers.js)**

```typescript
import { ethers } from "ethers";

const FACADE_ABI = [
  // Liquidation
  "function liquidateCreditAccount(address creditAccount, address to, (address target, bytes callData)[] calls, bytes lossPolicyData)",
  "function partiallyLiquidateCreditAccount(address creditAccount, address token, uint256 repaidAmount, uint256 minSeizedAmount, address to, (address token, bytes data)[] priceUpdates) returns (uint256)",
  // View
  "function creditManager() view returns (address)",
  "function underlying() view returns (address)",
  "function debtLimits() view returns (uint128 minDebt, uint128 maxDebt)",
  "function expirationDate() view returns (uint40)",
  "function paused() view returns (bool)",
  // Events
  "event LiquidateCreditAccount(address indexed creditAccount, address indexed liquidator, address to, uint256 remainingFunds)",
  "event PartiallyLiquidateCreditAccount(address indexed creditAccount, address indexed token, address indexed liquidator, uint256 repaidAmount, uint256 seizedAmount, uint256 feeAmount)",
];

const facade = new ethers.Contract(facadeAddress, FACADE_ABI, provider);
const facadeWrite = new ethers.Contract(facadeAddress, FACADE_ABI, signer);
```

```typescript
const CREDIT_MANAGER_ABI = [
  "function calcDebtAndCollateral(address creditAccount, uint8 task) view returns (tuple)",
  "function isLiquidatable(address creditAccount, uint16 minHealthFactor) view returns (bool)",
  "function liquidationThresholds(address token) view returns (uint16)",
  "function getBorrowerOrRevert(address creditAccount) view returns (address)",
  "function enabledTokensMaskOf(address creditAccount) view returns (uint256)",
  "function fees() view returns (uint16, uint16, uint16, uint16, uint16)",
];

const cmAddress = await facade.creditManager();
const cm = new ethers.Contract(cmAddress, CREDIT_MANAGER_ABI, provider);
```

```typescript
const ERC20_ABI = [
  "function approve(address spender, uint256 amount) returns (bool)",
  "function allowance(address owner, address spender) view returns (uint256)",
  "function balanceOf(address) view returns (uint256)",
];

// Multicall helper for liquidation swaps
const MULTICALL_ABI = [
  "function addCollateral(address token, uint256 amount)",
  "function withdrawCollateral(address token, uint256 amount, address to)",
];
const multicallIface = new ethers.Interface(MULTICALL_ABI);
```

**Solidity**

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

import {ICreditFacadeV3} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditFacadeV3.sol";
import {ICreditManagerV3} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditManagerV3.sol";
import {MultiCall} from "@gearbox-protocol/core-v2/contracts/libraries/MultiCall.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

/// @notice Base contract for liquidation bot integration.
contract LiquidationBot {
    ICreditFacadeV3 public immutable facade;
    ICreditManagerV3 public immutable creditManager;
    IERC20 public immutable underlying;

    constructor(ICreditFacadeV3 _facade) {
        facade = _facade;
        creditManager = ICreditManagerV3(_facade.creditManager());
        underlying = IERC20(_facade.underlying());
    }
}
```

---

## Full Liquidation

Close an unhealthy or expired Credit Account entirely. The liquidator executes multicall swaps to convert account assets to underlying, the pool is repaid, the Treasury takes a fee, and remaining funds go to the `to` address (FACT-014).

### Method Variants

| Method | Description | When to use |
|--------|-------------|-------------|
| `liquidateCreditAccount(address creditAccount, address to, MultiCall[] calls, bytes lossPolicyData)` | Full liquidation — close account, repay pool, claim remainder | Account `HF < 1` or expired |

### Step 1: Identify

Confirm the account is liquidatable and gather position data for swap planning.

**Pre-conditions:**

- ✅ Account `HF < 1` — `isLiquidatable(creditAccount, 10000)` returns `true` (FACT-103)
- ✅ OR account is expired — `expirationDate()` is non-zero and in the past (FACT-055)
- ✅ Facade is not paused — OR caller holds Emergency Liquidator role (FACT-057)
- ✅ If the account has bad debt — caller holds Loss Liquidator role and passes valid `lossPolicyData` (FACT-058)

**TypeScript**

```typescript
// using facade, cm from Setup section
const isLiquidatable = await cm.isLiquidatable(creditAccountAddress, 10000);
const expiry = await facade.expirationDate();
const now = BigInt(Math.floor(Date.now() / 1000));
const isExpired = expiry > 0n && now >= expiry;

console.log(`Liquidatable: ${isLiquidatable}, Expired: ${isExpired}`);

const positionData = await cm.calcDebtAndCollateral(creditAccountAddress, 1);
console.log(`Debt: ${positionData.totalDebtUSD}, TWV: ${positionData.twvUSD}`);
```

**Solidity**

```solidity
// Inside a contract inheriting LiquidationBot from Setup
function canLiquidate(address creditAccount) external view returns (bool) {
    return creditManager.isLiquidatable(creditAccount, 10000);
}
```

### Step 2: Prepare

Build the multicall array to swap all non-underlying collateral tokens to the underlying token via adapter calls. The liquidator does not need ERC-20 approvals — swaps execute within the Credit Account itself.

**TypeScript**

```typescript
// using facade from Setup section
// Build adapter swap calls — e.g., swap WETH → USDC via Uniswap adapter
const uniAdapterIface = new ethers.Interface([
  "function exactInputSingle((address,address,uint24,address,uint256,uint256,uint160)) returns (uint256)",
]);

const swapCalldata = uniAdapterIface.encodeFunctionData("exactInputSingle", [
  [wethAddress, usdcAddress, 3000, creditAccountAddress, wethBalance, minOut, 0n],
]);

const calls = [
  { target: uniswapAdapterAddress, callData: swapCalldata },
  // Add more swap calls for each non-underlying token
];

const lossPolicyData = "0x"; // empty for standard liquidations
```

**Solidity**

```solidity
// Inside a contract inheriting LiquidationBot from Setup
function buildSwapCalls() internal view returns (MultiCall[] memory calls) {
    calls = new MultiCall[](1);
    // Example: adapter call to swap collateral → underlying
    calls[0] = MultiCall({
        target: uniswapAdapterAddress,
        callData: abi.encodeCall(ISwapRouter.exactInputSingle, (params))
    });
}
```

### Step 3: Execute

Submit the liquidation transaction. On success, the pool is repaid and remaining funds are sent to `to`.

**TypeScript**

```typescript
// using facadeWrite, calls, lossPolicyData from Prepare step
const tx = await facadeWrite.liquidateCreditAccount(
  creditAccountAddress,
  signerAddress,   // `to` — receives remaining funds
  calls,
  lossPolicyData
);
const receipt = await tx.wait();

const liqEvent = receipt.logs.find((log: any) => {
  try { return facade.interface.parseLog(log)?.name === "LiquidateCreditAccount"; }
  catch { return false; }
});
const parsed = facade.interface.parseLog(liqEvent);
console.log(`Remaining funds: ${parsed.args.remainingFunds}`);
```

**Solidity**

```solidity
// Inside a contract inheriting LiquidationBot from Setup
function executeLiquidation(address creditAccount) external {
    MultiCall[] memory calls = buildSwapCalls();
    facade.liquidateCreditAccount(creditAccount, address(this), calls, "");
}
```

**Events emitted:** `LiquidateCreditAccount(address indexed creditAccount, address indexed liquidator, address to, uint256 remainingFunds)` (FACT-022)

**Error cases:**

| Condition | Revert |
|-----------|--------|
| HF ≥ 1 and account not expired | `CreditAccountNotLiquidatableException` |
| Bad debt present, caller lacks Loss Liquidator role | `CreditAccountNotLiquidatableWithLossException` |
| Bad debt present, loss policy rejects via TWAP check | `CreditAccountNotLiquidatableWithLossException` |
| Facade is paused and caller lacks Emergency Liquidator role | Pausable revert |
| Multicall swap fails (slippage, insufficient liquidity) | Adapter-level revert |

---

## Partial Liquidation

Repay a specific amount of debt and receive a discounted quantity of a chosen collateral token. The account remains open if the health factor recovers above 1 after the repayment (FACT-015, FACT-060).

### Method Variants

| Method | Description | When to use |
|--------|-------------|-------------|
| `partiallyLiquidateCreditAccount(address creditAccount, address token, uint256 repaidAmount, uint256 minSeizedAmount, address to, PriceUpdate[] priceUpdates)` | Partial liquidation — repay debt portion, seize discounted collateral | Account slightly unhealthy, full liquidation unnecessary |

### Step 1: Identify

Determine which collateral token to seize and how much debt to repay.

**Pre-conditions:**

- ✅ Account `HF < 1` — `isLiquidatable(creditAccount, 10000)` returns `true` (FACT-103)
- ✅ Target `token` is not the underlying asset — `UnderlyingIsNotLiquidatableException` otherwise
- ✅ Target `token` has a non-zero balance in the Credit Account
- ✅ Liquidator holds sufficient underlying to cover `repaidAmount`
- ✅ Liquidator has approved the Credit Manager for `repaidAmount` of underlying

**TypeScript**

```typescript
// using facade, cm from Setup section
const isLiquidatable = await cm.isLiquidatable(creditAccountAddress, 10000);
const positionData = await cm.calcDebtAndCollateral(creditAccountAddress, 1);
const lt = await cm.liquidationThresholds(targetTokenAddress);

console.log(`Liquidatable: ${isLiquidatable}`);
console.log(`Target token LT: ${lt} bps`);
```

**Solidity**

```solidity
// Inside a contract inheriting LiquidationBot from Setup
function checkPartialLiquidation(address creditAccount, address token) external view returns (uint16 lt) {
    require(creditManager.isLiquidatable(creditAccount, 10000), "not liquidatable");
    lt = creditManager.liquidationThresholds(token);
}
```

### Step 2: Prepare

Approve the underlying token to the Credit Manager and calculate the minimum seized amount.

**TypeScript**

```typescript
// using cm, ERC20_ABI from Setup section
const underlyingAddress = await facade.underlying();
const underlyingToken = new ethers.Contract(underlyingAddress, ERC20_ABI, signer);
const repaidAmount = 1000_000000n; // 1000 USDC

const allowance = await underlyingToken.allowance(signerAddress, cmAddress);
if (allowance < repaidAmount) {
  const tx = await underlyingToken.approve(cmAddress, repaidAmount);
  await tx.wait();
}

// Calculate minimum seized amount with slippage tolerance
// seizedAmount ≈ repaidAmount × (1 + liquidationDiscount) / tokenPrice
const minSeizedAmount = expectedSeized * 99n / 100n; // 1% slippage
```

**Solidity**

```solidity
// Inside a contract inheriting LiquidationBot from Setup
function preparePartialLiquidation(uint256 repaidAmount) internal {
    underlying.approve(address(creditManager), repaidAmount);
}
```

### Step 3: Execute

Call `partiallyLiquidateCreditAccount`. The function transfers `repaidAmount` of underlying from the liquidator to repay debt, and transfers `seizedAmount` of the collateral token to `to`.

**TypeScript**

```typescript
// using facadeWrite from Setup section
const priceUpdates: any[] = []; // empty if no pull-oracle updates needed

const tx = await facadeWrite.partiallyLiquidateCreditAccount(
  creditAccountAddress,
  targetTokenAddress,  // collateral token to seize
  repaidAmount,
  minSeizedAmount,
  signerAddress,       // `to` — receives seized collateral
  priceUpdates
);
const receipt = await tx.wait();

const partialEvent = receipt.logs.find((log: any) => {
  try { return facade.interface.parseLog(log)?.name === "PartiallyLiquidateCreditAccount"; }
  catch { return false; }
});
const parsed = facade.interface.parseLog(partialEvent);
console.log(`Seized: ${parsed.args.seizedAmount}, Fee: ${parsed.args.feeAmount}`);
```

**Solidity**

```solidity
// Inside a contract inheriting LiquidationBot from Setup
function executePartialLiquidation(
    address creditAccount,
    address token,
    uint256 repaidAmount,
    uint256 minSeizedAmount
) external {
    underlying.approve(address(creditManager), repaidAmount);
    PriceUpdate[] memory updates = new PriceUpdate[](0);
    facade.partiallyLiquidateCreditAccount(
        creditAccount, token, repaidAmount, minSeizedAmount, address(this), updates
    );
}
```

**Events emitted:** `PartiallyLiquidateCreditAccount(address indexed creditAccount, address indexed token, address indexed liquidator, uint256 repaidAmount, uint256 seizedAmount, uint256 feeAmount)` (FACT-023)

**Error cases:**

| Condition | Revert |
|-----------|--------|
| HF ≥ 1 | `CreditAccountNotLiquidatableException` |
| `token` is the underlying asset | `UnderlyingIsNotLiquidatableException` |
| Seized amount < `minSeizedAmount` | `SeizedLessThanRequiredException` |
| Insufficient underlying approval to Credit Manager | `transferFrom` revert |
| Insufficient collateral token balance in the account | Arithmetic underflow |

---

## Liquidation Economics

### Fee Parameters

Retrieve liquidation fee parameters from the Credit Manager via `fees()`.

| Parameter | Description | Typical range |
|-----------|-------------|---------------|
| `feeLiquidation` | Fee percentage taken by Treasury on undercollateralized liquidation | 100–200 bps |
| `liquidationDiscount` | Discount at which liquidator acquires collateral (premium = `1 - discount`) | 9500–9700 bps |
| `feeLiquidationExpired` | Treasury fee for expired account liquidation (FACT-055) | 50–100 bps |
| `liquidationDiscountExpired` | Discount for expired account liquidation — usually lower premium | 9800–9900 bps |

**TypeScript**

```typescript
// using cm from Setup section
const fees = await cm.fees();
console.log(`Liquidation fee: ${fees[0]} bps`);
console.log(`Liquidation discount: ${fees[1]} bps`);
console.log(`Expired fee: ${fees[2]} bps`);
console.log(`Expired discount: ${fees[3]} bps`);
```

### Full Liquidation Math

The liquidator's profit derives from the spread between total collateral value and the repayment amount.

```
Total Value     = sum(Balance_i × Price_i)                           — raw collateral value
Amount to Pool  = Total Debt                                         — full debt repayment
Treasury Fee    = Total Value × feeLiquidation / 10000               — protocol cut
Remaining Funds = Total Value - Amount to Pool - Treasury Fee        — sent to `to`
Liquidator Profit = Remaining Funds - Gas Cost                       (FACT-053)
```

The liquidation premium equals the difference between total collateral value and debt plus fees. When `Total Value < Total Debt`, the account has bad debt — the pool absorbs the loss.

### Partial Liquidation Math

The liquidator repays `repaidAmount` of underlying and receives a discounted quantity of the chosen collateral token (FACT-060).

```
seizedAmount = repaidAmount × (10000 + liquidationPremiumBps) / tokenPrice    (FACT-053)
feeAmount    = repaidAmount × feeLiquidation / 10000                          (FACT-054)
```

The `seizedAmount` and `feeAmount` are reported in the `PartiallyLiquidateCreditAccount` event (FACT-023). The liquidator's profit:

```
Liquidator Profit = seizedAmount × tokenPrice - repaidAmount - Gas Cost
```

### Worked Example: Full Liquidation

| Parameter | Value |
|-----------|-------|
| Total collateral value | $100,000 |
| Total debt | $95,000 |
| `feeLiquidation` | 150 bps (1.5%) |
| `liquidationDiscount` | 9600 bps (96%) |

```
Treasury Fee    = $100,000 × 150 / 10000 = $1,500
Amount to Pool  = $95,000
Remaining Funds = $100,000 - $95,000 - $1,500 = $3,500
```

The liquidator receives $3,500 minus gas costs. If the liquidator executed swaps within the multicall at market prices, the full $3,500 is realized profit.

### Worked Example: Partial Liquidation

| Parameter | Value |
|-----------|-------|
| `repaidAmount` | 10,000 USDC |
| Target token (WETH) price | $3,000 |
| Liquidation premium | 400 bps (4%) |
| `feeLiquidation` | 150 bps |

```
seizedAmount = 10,000 × (10000 + 400) / 10000 / 3000 = 3.4667 WETH
feeAmount    = 10,000 × 150 / 10000 = 150 USDC
Liquidator Profit = 3.4667 × $3,000 - $10,000 = $400 (minus gas)
```

---

## Loss Policy & Bad Debt

When total collateral value falls below total debt (`TWV < Total Debt`), the account has bad debt. Standard liquidation reverts with `CreditAccountNotLiquidatableWithLossException` unless the loss policy approves the liquidation (FACT-058).

### AliasedLossPolicyV3

The `AliasedLossPolicyV3` contract re-checks account solvency using TWAP-based alias price feeds instead of spot prices before allowing a bad debt liquidation (FACT-059). This prevents manipulation of spot oracles to create artificial bad debt.

| Component | Role |
|-----------|------|
| Loss Liquidator role | Address authorized to call `liquidateCreditAccount` when bad debt is present (FACT-058) |
| `lossPolicyData` parameter | ABI-encoded data passed to the loss policy contract for validation |
| TWAP alias feeds | Time-weighted average prices used by `AliasedLossPolicyV3` for re-validation |

### Encoding lossPolicyData

For `AliasedLossPolicyV3`, encode the data expected by the policy contract:

**TypeScript**

```typescript
// Standard liquidation (no bad debt) — pass empty bytes
const lossPolicyData = "0x";

// Bad debt liquidation via AliasedLossPolicyV3
const lossPolicyData = ethers.AbiCoder.defaultAbiCoder().encode(
  ["address"],  // alias oracle address, or other policy-specific params
  [aliasOracleAddress]
);
```

**Solidity**

```solidity
// Standard liquidation
bytes memory lossPolicyData = "";

// Bad debt liquidation — encode policy-specific data
bytes memory lossPolicyData = abi.encode(aliasOracleAddress);
```

### Bad Debt Flow

1. The liquidator detects `TWV < Total Debt` via `calcDebtAndCollateral` (FACT-102)
2. Standard `liquidateCreditAccount` reverts — `CreditAccountNotLiquidatableWithLossException`
3. A Loss Liquidator calls `liquidateCreditAccount` with valid `lossPolicyData`
4. `AliasedLossPolicyV3` re-checks solvency using TWAP alias prices (FACT-059)
5. If TWAP-based check confirms bad debt, the liquidation proceeds
6. The pool absorbs the shortfall — loss is socialized across LPs

⚠️ If TWAP prices diverge from spot (e.g., during rapid market moves), the loss policy may reject the liquidation. The liquidator must wait until TWAP catches up to spot.

---

## Bot Infrastructure

### Permission Model

| Role | Access | When |
|------|--------|------|
| Any address | `liquidateCreditAccount`, `partiallyLiquidateCreditAccount` | Account `HF < 1` or expired, facade not paused (FACT-056) |
| Emergency Liquidator | `liquidateCreditAccount` | Facade is paused — can still execute liquidations (FACT-057) |
| Loss Liquidator | `liquidateCreditAccount` with `lossPolicyData` | Account has bad debt (FACT-058) |
| Authorized bot | `botMulticall` — deleverage before liquidation triggers | Account owner granted permissions via `setBotPermissions` |

### Emergency Liquidator Role

When the CreditFacadeV3 is paused (circuit breaker, exploit mitigation), standard liquidation calls revert. Addresses holding the Emergency Liquidator role bypass the pause check and can execute `liquidateCreditAccount` (FACT-057).

- The role is granted by governance via the ACL contract
- Emergency liquidators cannot call `partiallyLiquidateCreditAccount` while paused
- The multicall within the liquidation still executes normally

### Bot Permission Bitmask

Account owners can grant bots specific permissions for proactive position management (deleveraging before liquidation triggers):

| Permission | Bit | Description |
|------------|-----|-------------|
| `ADD_COLLATERAL_PERMISSION` | `1 << 0` | Allow adding assets |
| `INCREASE_DEBT_PERMISSION` | `1 << 1` | Allow borrowing more |
| `DECREASE_DEBT_PERMISSION` | `1 << 2` | Allow repaying debt |
| `WITHDRAW_COLLATERAL_PERMISSION` | `1 << 5` | Allow removing assets |
| `EXTERNAL_CALLS_PERMISSION` | `1 << 16` | Allow DeFi protocol interaction via adapters |

A deleverage bot with bits `1 << 2 | 1 << 16` (= `0x10004`) can repay debt and execute adapter swaps on behalf of the account owner — enabling automated risk reduction before `HF` drops below 1.

**TypeScript**

```typescript
// Grant bot permissions (called by account owner)
const DECREASE_DEBT = 1n << 2n;
const EXTERNAL_CALLS = 1n << 16n;
const permissions = DECREASE_DEBT | EXTERNAL_CALLS;

const setBotCall = multicallIface.encodeFunctionData("setBotPermissions", [
  botAddress, permissions
]);
```

---

## Practical Bot Architecture

### Scanning Strategy

| Component | Implementation |
|-----------|---------------|
| Account set | Index `OpenCreditAccount` / `CloseCreditAccount` / `LiquidateCreditAccount` events to maintain a live set of active accounts |
| Health check frequency | Every block for high-value accounts; every N blocks for smaller positions |
| Priority queue | Sort accounts by HF ascending — lowest HF first, highest profit potential |
| Multi-CM scanning | Iterate all Credit Managers from `ContractsRegister.getCreditManagers()` |

### Oracle Monitoring

Pull-based oracles (Pyth, RedStone) require price updates to be bundled with the liquidation transaction via the `PriceUpdate[]` parameter in `partiallyLiquidateCreditAccount`.

| Oracle type | Handling |
|-------------|----------|
| Push-based (Chainlink) | No action — prices update independently |
| Pull-based (Pyth, RedStone) | Include `PriceUpdate[]` with fresh signed prices in the liquidation call |
| Stale oracle | Check `updatedAt` timestamp; stale prices may cause `calcDebtAndCollateral` to return incorrect HF values |

### Gas Optimization

- Estimate gas before submission — `estimateGas` catches most revert conditions
- Bundle oracle updates + liquidation in a single transaction
- Pre-simulate using `eth_call` to verify profitability before broadcasting
- Monitor base fee and priority fee — liquidation profit must exceed gas cost

**TypeScript**

```typescript
// Pre-simulate liquidation profitability
try {
  const gasEstimate = await facadeWrite.liquidateCreditAccount.estimateGas(
    creditAccountAddress, signerAddress, calls, "0x"
  );
  const gasCost = gasEstimate * gasPrice;
  console.log(`Gas cost: ${gasCost}, Expected profit: ${expectedProfit}`);
  if (expectedProfit <= gasCost) console.log("Unprofitable — skip");
} catch (e) {
  console.log(`Simulation failed: ${e.message}`);
}
```

### MEV Protection

- Submit liquidation transactions via private mempools (Flashbots Protect, MEV Blocker) to prevent front-running
- Use `minSeizedAmount` in partial liquidations as a slippage guard against sandwich attacks
- Monitor for competing liquidators — if another bot liquidates first, the transaction reverts with `CreditAccountNotLiquidatableException`
- Consider Flashbots bundles to atomically combine oracle updates + liquidation

---

## Key Function Reference

CreditManagerV3 and CreditFacadeV3 functions used in liquidation workflows.

### CreditManagerV3 View Functions

| Function | Signature | Returns | Description |
|----------|-----------|---------|-------------|
| `fees` | `fees()` | `(uint16 feeLiquidation, uint16 liquidationDiscount, uint16 feeLiquidationExpired, uint16 liquidationDiscountExpired, uint16 feeInterest)` | Returns the fee parameters governing liquidation premium, discount, and interest fee in bps. |
| `calcDebtAndCollateral` | `calcDebtAndCollateral(address creditAccount, uint8 task)` | `CollateralDebtData` | Computes aggregated debt and weighted collateral values for a credit account according to the specified task type (FACT-102). |
| `isLiquidatable` | `isLiquidatable(address creditAccount, uint16 minHealthFactor)` | `bool` | Returns `true` if the account's health factor is below `minHealthFactor`, indicating eligibility for liquidation (FACT-103). |
| `liquidationThresholds` | `liquidationThresholds(address token)` | `uint16` | Returns the liquidation threshold for `token` in basis points, used to weight collateral in health factor computation (FACT-104). |
| `getBorrowerOrRevert` | `getBorrowerOrRevert(address creditAccount)` | `address` | Returns the borrower address associated with the credit account, reverting if the account does not exist (FACT-100). |
| `enabledTokensMaskOf` | `enabledTokensMaskOf(address creditAccount)` | `uint256` | Returns the bitmask of currently enabled collateral tokens on the credit account (FACT-101). |

### CreditFacadeV3 Liquidation Functions

| Function | Signature | Returns | Description |
|----------|-----------|---------|-------------|
| `liquidateCreditAccount` | `liquidateCreditAccount(address creditAccount, address to, MultiCall[] calldata calls, bytes memory lossPolicyData)` | — | Performs full liquidation of a credit account, converting all collateral and sending remaining funds to `to` (FACT-014). |
| `partiallyLiquidateCreditAccount` | `partiallyLiquidateCreditAccount(address creditAccount, address token, uint256 repaidAmount, uint256 minSeizedAmount, address to, PriceUpdate[] calldata priceUpdates)` | `uint256 seizedAmount` | Seizes a single collateral `token` in exchange for repaying `repaidAmount` of underlying debt, returning the amount seized (FACT-015). |

### Events

| Event | Signature | Emitted when |
|-------|-----------|--------------|
| `LiquidateCreditAccount` | `LiquidateCreditAccount(address indexed creditAccount, address indexed liquidator, address to, uint256 remainingFunds)` | A full liquidation completes successfully. |
| `PartiallyLiquidateCreditAccount` | `PartiallyLiquidateCreditAccount(address indexed creditAccount, address indexed token, address indexed liquidator, uint256 repaidAmount, uint256 seizedAmount, uint256 feeAmount)` | A partial liquidation completes successfully. |

---

## Gotchas

### 1. Anyone Can Liquidate — No Permission Required

`liquidateCreditAccount` and `partiallyLiquidateCreditAccount` are permissionless when the account is unhealthy or expired (FACT-056). Competition is won by gas priority, not by holding a role. The Exception: bad debt liquidation requires the Loss Liquidator role (FACT-058).

### 2. Empty `lossPolicyData` for Standard Liquidations

Pass `"0x"` (empty bytes) for `lossPolicyData` in standard liquidations where `Total Value ≥ Total Debt`. Non-empty data is only required when the loss policy must validate a bad debt liquidation. Passing incorrect `lossPolicyData` when bad debt exists causes `CreditAccountNotLiquidatableWithLossException`.

### 3. Partial Liquidation Cannot Seize the Underlying Token

`partiallyLiquidateCreditAccount` reverts with `UnderlyingIsNotLiquidatableException` if `token` equals the pool's underlying asset. Only non-underlying collateral tokens can be seized. To liquidate an account holding primarily underlying, use full liquidation instead.

### 4. `minSeizedAmount` Is the Slippage Guard

The `minSeizedAmount` parameter in `partiallyLiquidateCreditAccount` protects against oracle price changes between simulation and execution. If the actual seized amount falls below this value, the transaction reverts with `SeizedLessThanRequiredException`. Set this conservatively — too tight causes reverts on volatile tokens; too loose exposes the liquidator to adverse price moves.

### 5. Expired Accounts Have Different Fee Parameters

Expired accounts (past `expirationDate()`) use `feeLiquidationExpired` and `liquidationDiscountExpired` instead of the standard parameters (FACT-055). These are typically lower, yielding smaller liquidation premiums. Check both parameter sets when estimating profitability.

### 6. Emergency Liquidator Bypasses Pause — But Not Loss Policy

The Emergency Liquidator role allows `liquidateCreditAccount` execution when the facade is paused (FACT-057). However, the loss policy check is not bypassed — bad debt liquidation still requires valid `lossPolicyData` and the Loss Liquidator role regardless of pause state.

### 7. Multicall Swaps Execute Inside the Credit Account

During full liquidation, the `MultiCall[] calls` parameter defines adapter swap operations executed within the Credit Account — the liquidator does not receive or send tokens during the multicall phase. Tokens flow to the liquidator only after the multicall completes and remaining funds are calculated. Incorrectly targeting the liquidator's own address in swap calls has no effect.

### 8. Approve the Credit Manager for Partial Liquidation

Partial liquidation requires ERC-20 approval of the underlying token to the **Credit Manager** address, not the CreditFacadeV3 address. The Credit Manager executes `transferFrom` to pull `repaidAmount` from the liquidator. Call `facade.creditManager()` to get the correct approval target.

### 9. Loss Policy TWAP Lag Can Block Liquidation

`AliasedLossPolicyV3` uses TWAP-based prices that lag behind spot prices (FACT-059). During rapid market downturns, spot price may show bad debt while TWAP does not yet reflect the decline — causing the loss policy to reject the liquidation. The liquidator must retry once TWAP catches up. This delay is intentional: it prevents oracle manipulation attacks that create artificial bad debt.

### 10. Gas Estimation Failure ≠ Unprofitable

A reverted `estimateGas` call can indicate either (a) the account is not actually liquidatable (HF recovered), (b) multicall swap parameters are invalid, or (c) loss policy rejection. Distinguish between these by decoding the revert reason: `CreditAccountNotLiquidatableException` means the account recovered; adapter-level reverts indicate swap configuration issues.

---

**Related:** [Lending: Pool Deposit & Withdrawal →](./01-lending.md) · [Borrowing: Credit Account Lifecycle →](./02-borrowing.md) · [Strategies & Adapters →](./03-strategies.md) · [CreditFacadeV3.sol](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/credit/CreditFacadeV3.sol) · [CreditManagerV3.sol](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/credit/CreditManagerV3.sol)
