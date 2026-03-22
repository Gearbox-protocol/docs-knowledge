# Borrowing: Credit Account Lifecycle

Open a Credit Account through CreditFacadeV3, borrow underlying from a Gearbox pool, manage collateral, and close — all via batched multicall transactions. Every user operation flows through CreditFacadeV3, never directly to the Credit Account contract (FACT-003, FACT-004).

| Concept | Mechanism |
|---------|-----------|
| **Credit Account** | Isolated smart contract per borrower (FACT-003). Holds collateral + borrowed funds in a single on-chain address. |
| **Multicall batching** | All state changes are encoded as `MultiCall[]` arrays and executed atomically (FACT-004). |
| **Check-on-exit** | Health factor is validated **once** at the end of the multicall — not per operation. Enables atomic deposit + borrow + swap in a single tx. |
| **Health Factor** | `HF = TWV / Total Debt` (FACT-050). Account is liquidatable when `HF < 1`. |
| **TWV** | `sum(Balance_i × Price_i × LT_i)` for all enabled collateral tokens (FACT-051). |
| **Total Debt** | `Principal + BaseInterest + QuotaInterest + Fees` (FACT-052). |
| **Debt limits** | Every account's debt must stay between `minDebt` and `maxDebt` (`debtLimits()`). |

**Contracts:** [`CreditFacadeV3.sol`](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/credit/CreditFacadeV3.sol) · [`ICreditFacadeV3.sol`](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/interfaces/ICreditFacadeV3.sol) · [`ICreditFacadeV3Multicall.sol`](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/interfaces/ICreditFacadeV3Multicall.sol)

---

## Credit Manager Discovery

Locate active Credit Manager and Facade addresses before interacting with borrowing.

### Option A: ContractsRegister (On-Chain Enumeration)

`ContractsRegister.getCreditManagers()` returns all active Credit Manager addresses. Each Credit Manager has exactly one CreditFacadeV3.

**TypeScript**

```typescript
import { ethers } from "ethers";

const register = new ethers.Contract(contractsRegisterAddress, [
  "function getCreditManagers() view returns (address[])",
], provider);

const creditManagers = await register.getCreditManagers();
// creditManagers: string[] — e.g., ["0xabc...", "0xdef..."]
```

**Solidity**

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

import {IContractsRegister} from "@gearbox-protocol/core-v3/contracts/interfaces/IContractsRegister.sol";

contract CreditManagerFinder {
    function listCreditManagers(IContractsRegister register) external view returns (address[] memory) {
        return register.getCreditManagers();
    }
}
```

### Option B: CreditAccountCompressor (Aggregated Data)

`CreditAccountCompressor` returns full position data — debt, collateral, health factor, enabled tokens — in a single call. Useful for dashboards and monitoring.

```typescript
const compressor = new ethers.Contract(creditAccountCompressorAddress, [
  "function getCreditAccountData(address creditManager, address creditAccount) view returns (tuple)",
], provider);

const accountData = await compressor.getCreditAccountData(creditManagerAddress, creditAccountAddress);
```

### Option C: SDK (High-Level)

```typescript
import { GearboxSDK } from "@gearbox-protocol/sdk";

const sdk = new GearboxSDK({ /* provider config */ });
const creditManagers = sdk.market.creditManagers;
// CreditManagerSuite[] — each has .address, .facade, .underlying
```

---

## Setup

Instantiate the CreditFacadeV3 contract and define multicall helper types. All subsequent examples reference these instances.

**TypeScript (ethers.js)**

```typescript
import { ethers } from "ethers";

const FACADE_ABI = [
  // Lifecycle
  "function openCreditAccount(address onBehalfOf, (address target, bytes callData)[] calls, uint256 referralCode) returns (address)",
  "function closeCreditAccount(address creditAccount, (address target, bytes callData)[] calls)",
  "function multicall(address creditAccount, (address target, bytes callData)[] calls)",
  // View
  "function creditManager() view returns (address)",
  "function underlying() view returns (address)",
  "function debtLimits() view returns (uint128 minDebt, uint128 maxDebt)",
  "function expirationDate() view returns (uint40)",
  "function paused() view returns (bool)",
  "function forbiddenTokenMask() view returns (uint256)",
  // Events
  "event OpenCreditAccount(address indexed creditAccount, address indexed onBehalfOf, address indexed caller, uint256 referralCode)",
  "event CloseCreditAccount(address indexed creditAccount, address indexed owner)",
  "event StartMultiCall(address indexed creditAccount, address indexed caller)",
  "event FinishMultiCall()",
];

const facade = new ethers.Contract(facadeAddress, FACADE_ABI, provider);
const facadeWrite = new ethers.Contract(facadeAddress, FACADE_ABI, signer);
```

```typescript
// Multicall helper — encode internal facade calls
const MULTICALL_ABI = [
  "function addCollateral(address token, uint256 amount)",
  "function withdrawCollateral(address token, uint256 amount, address to)",
  "function increaseDebt(uint256 amount)",
  "function decreaseDebt(uint256 amount)",
  "function updateQuota(address token, int96 quotaChange, uint96 minQuota)",
];

const multicallIface = new ethers.Interface(MULTICALL_ABI);

function facadeCall(method: string, args: any[]) {
  return { target: facadeAddress, callData: multicallIface.encodeFunctionData(method, args) };
}
```

```typescript
const ERC20_ABI = [
  "function approve(address spender, uint256 amount) returns (bool)",
  "function allowance(address owner, address spender) view returns (uint256)",
  "function balanceOf(address) view returns (uint256)",
];

const CREDIT_MANAGER_ABI = [
  "function calcDebtAndCollateral(address creditAccount, uint8 task) view returns (tuple)",
  "function getBorrowerOrRevert(address creditAccount) view returns (address)",
  "function enabledTokensMaskOf(address creditAccount) view returns (uint256)",
];
```

**Solidity**

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

import {ICreditFacadeV3} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditFacadeV3.sol";
import {ICreditFacadeV3Multicall} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditFacadeV3Multicall.sol";
import {ICreditManagerV3} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditManagerV3.sol";
import {MultiCall} from "@gearbox-protocol/core-v2/contracts/libraries/MultiCall.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

/// @notice Base contract for credit account interactions.
contract CreditIntegration {
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

## Open a Credit Account

Allocate an isolated Credit Account, deposit collateral, and borrow in a single atomic transaction (FACT-010).

### Method Variants

| Method | Description | When to use |
|--------|-------------|-------------|
| `openCreditAccount(address onBehalfOf, MultiCall[] calls, uint256 referralCode)` | Opens account for `onBehalfOf`, executes `calls`, returns new Credit Account address | Standard open flow |

### Step 1: Identify

Verify the facade accepts new accounts and check debt limits.

**Pre-conditions:**

- ✅ Facade is not paused — `paused()` returns `false`
- ✅ Facade has not expired — `expirationDate()` is `0` or in the future
- ✅ Intended borrow amount is between `minDebt` and `maxDebt` — call `debtLimits()`
- ✅ ERC-20 approval granted — collateral token approved to the **Credit Manager** address (not the facade)
- ✅ Collateral token is allowed by this Credit Manager

**TypeScript**

```typescript
// using facade from Setup section
const isPaused = await facade.paused();
const expiry = await facade.expirationDate();
const [minDebt, maxDebt] = await facade.debtLimits();
const cmAddress = await facade.creditManager();

const borrowAmount = 5000_000000n; // 5000 USDC (6 decimals)
console.log(`Debt limits: ${minDebt} — ${maxDebt}`);
console.log(`Borrow ${borrowAmount} valid: ${borrowAmount >= minDebt && borrowAmount <= maxDebt}`);
```

**Solidity**

```solidity
// Inside a contract inheriting CreditIntegration from Setup
function checkCanOpen(uint256 borrowAmount) external view returns (bool) {
    (uint128 minDebt, uint128 maxDebt) = facade.debtLimits();
    require(!facade.paused(), "facade paused");
    require(borrowAmount >= minDebt && borrowAmount <= maxDebt, "debt out of range");
    return true;
}
```

### Step 2: Prepare

Approve collateral to the Credit Manager, then build the multicall array. The typical open flow: `addCollateral` → `increaseDebt` → optional adapter calls.

**TypeScript**

```typescript
// using facade, facadeCall, ERC20_ABI from Setup section
const cmAddress = await facade.creditManager();
const collateralToken = new ethers.Contract(usdcAddress, ERC20_ABI, signer);

const collateralAmount = 1000_000000n; // 1000 USDC
const allowance = await collateralToken.allowance(signerAddress, cmAddress);
if (allowance < collateralAmount) {
  const tx = await collateralToken.approve(cmAddress, collateralAmount);
  await tx.wait();
}
```

```typescript
// Build multicall: deposit collateral + borrow
const borrowAmount = 5000_000000n; // 5000 USDC — 5x leverage
const calls = [
  facadeCall("addCollateral", [usdcAddress, collateralAmount]),
  facadeCall("increaseDebt", [borrowAmount]),
];
```

**Solidity**

```solidity
// Inside a contract inheriting CreditIntegration from Setup
function buildOpenCalls(uint256 collateral, uint256 debt) internal view returns (MultiCall[] memory calls) {
    calls = new MultiCall[](2);
    calls[0] = MultiCall({
        target: address(facade),
        callData: abi.encodeCall(ICreditFacadeV3Multicall.addCollateral, (address(underlying), collateral))
    });
    calls[1] = MultiCall({
        target: address(facade),
        callData: abi.encodeCall(ICreditFacadeV3Multicall.increaseDebt, (debt))
    });
}
```

### Step 3: Execute

Call `openCreditAccount` and capture the new Credit Account address from the return value or event.

**TypeScript**

```typescript
// using facadeWrite, calls from Prepare step
const referralCode = 0n;
const tx = await facadeWrite.openCreditAccount(signerAddress, calls, referralCode);
const receipt = await tx.wait();

// Parse the CreditAccount address from OpenCreditAccount event
const openEvent = receipt.logs.find((log: any) => {
  try { return facade.interface.parseLog(log)?.name === "OpenCreditAccount"; } catch { return false; }
});
const creditAccountAddress = facade.interface.parseLog(openEvent).args.creditAccount;
console.log(`Opened credit account: ${creditAccountAddress}`);
```

**Solidity**

```solidity
// Inside a contract inheriting CreditIntegration from Setup
function openAccount(uint256 collateral, uint256 debt) external returns (address creditAccount) {
    underlying.approve(address(creditManager), collateral);
    MultiCall[] memory calls = buildOpenCalls(collateral, debt);
    creditAccount = facade.openCreditAccount(address(this), calls, 0);
}
```

**Events emitted:** `OpenCreditAccount(address indexed creditAccount, address indexed onBehalfOf, address indexed caller, uint256 referralCode)`, `StartMultiCall`, `FinishMultiCall`

**Error cases:**

| Condition | Revert |
|-----------|--------|
| Facade is paused | Pausable revert |
| Facade has expired | `NotAllowedAfterExpirationException` |
| Whitelisted mode and caller not whitelisted | `ForbiddenInWhitelistedModeException` |
| Debt below `minDebt` or above `maxDebt` | Debt limit revert |
| Insufficient ERC-20 approval to Credit Manager | `transferFrom` revert |
| Total new debt this block exceeds `maxDebtPerBlockMultiplier` limit | Debt limit revert |
| HF < 1 after multicall execution | `fullCollateralCheck` revert |

---

## Manage Position (Multicall)

Modify an existing Credit Account — add/withdraw collateral, borrow/repay, swap via adapters — in a single atomic transaction (FACT-012).

### Method Variants

| Method | Description | When to use |
|--------|-------------|-------------|
| `multicall(address creditAccount, MultiCall[] calls)` | Owner batches operations on an existing account | Standard position management |
| `botMulticall(address creditAccount, MultiCall[] calls)` | Authorized bot executes permitted operations | Automated strategies, rebalancing |

### Available Multicall Operations

| Operation | Signature | Effect |
|-----------|-----------|--------|
| Add collateral | `addCollateral(address token, uint256 amount)` | Transfer token into the Credit Account |
| Withdraw collateral | `withdrawCollateral(address token, uint256 amount, address to)` | Transfer token out (HF checked after) |
| Borrow more | `increaseDebt(uint256 amount)` | Borrow additional underlying from pool |
| Repay debt | `decreaseDebt(uint256 amount)` | Repay underlying back to pool |
| Update quota | `updateQuota(address token, int96 quotaChange, uint96 minQuota)` | Adjust quota for a collateral token |
| Set bot permissions | `setBotPermissions(address bot, uint192 permissions)` | Delegate specific operations to a bot |
| Slippage guard (begin) | `storeExpectedBalances(BalanceDelta[] balanceDeltas)` | Snapshot expected post-swap balances |
| Slippage guard (end) | `compareBalances()` | Revert if balances fell below expectations |
| Adapter call | External call to an allowed adapter address | Swap on Uniswap, deposit to Curve, stake on Convex, wrap on Lido |

### Ordering

Operation order within the multicall array matters. Borrow before swap — `increaseDebt` must precede any adapter call that spends the borrowed funds. The check-on-exit phase runs only after all calls complete.

Multicall execution follows 4 phases:
1. **State Initialization** — captures `enabledTokensMask`, snapshots forbidden token balances
2. **Sequential Execution** — iterates `MultiCall[]`; internal calls dispatch to `ICreditFacadeV3Multicall`, external calls go through adapters
3. **Finalization** — unsets active account, emits `FinishMultiCall`
4. **Check-on-Exit** — forbidden token checks + `fullCollateralCheck` (HF ≥ `minHealthFactor`)

### Step 1: Identify

Read current position state to decide what operations to perform.

**TypeScript**

```typescript
// using facade, CREDIT_MANAGER_ABI from Setup section
const cmAddress = await facade.creditManager();
const cm = new ethers.Contract(cmAddress, CREDIT_MANAGER_ABI, provider);

// CollateralCalcTask.DEBT_COLLATERAL_WITHOUT_WITHDRAWALS = 1
const positionData = await cm.calcDebtAndCollateral(creditAccountAddress, 1);
console.log(`Current debt: ${positionData.totalDebtUSD}`);
```

### Step 2: Prepare — Increase Leverage

Build a multicall that borrows more underlying and swaps to a collateral token via an adapter.

**TypeScript**

```typescript
// using facadeCall from Setup section
const additionalBorrow = 2000_000000n; // 2000 USDC

// Encode adapter call (e.g., Uniswap V3 swap USDC → WETH)
const uniAdapterIface = new ethers.Interface([
  "function exactInputSingle((address,address,uint24,address,uint256,uint256,uint160)) returns (uint256)",
]);
const swapCalldata = uniAdapterIface.encodeFunctionData("exactInputSingle", [
  [usdcAddress, wethAddress, 3000, creditAccountAddress, additionalBorrow, 0n, 0n],
]);

const calls = [
  facadeCall("increaseDebt", [additionalBorrow]),
  { target: uniswapAdapterAddress, callData: swapCalldata },
];
```

### Step 2: Prepare — Reduce Leverage

Build a multicall that swaps collateral back to underlying and repays.

**TypeScript**

```typescript
// using facadeCall from Setup section
const swapBack = uniAdapterIface.encodeFunctionData("exactInputSingle", [
  [wethAddress, usdcAddress, 3000, creditAccountAddress, wethAmount, 0n, 0n],
]);

const calls = [
  { target: uniswapAdapterAddress, callData: swapBack },
  facadeCall("decreaseDebt", [1000_000000n]), // repay 1000 USDC
];
```

### Step 3: Execute

**TypeScript**

```typescript
// using facadeWrite from Setup section
const tx = await facadeWrite.multicall(creditAccountAddress, calls);
const receipt = await tx.wait();
console.log(`Multicall executed: ${receipt.hash}`);
```

**Solidity**

```solidity
// Inside a contract inheriting CreditIntegration from Setup
function increaseLeverage(address creditAccount, uint256 borrowMore) external {
    MultiCall[] memory calls = new MultiCall[](1);
    calls[0] = MultiCall({
        target: address(facade),
        callData: abi.encodeCall(ICreditFacadeV3Multicall.increaseDebt, (borrowMore))
    });
    facade.multicall(creditAccount, calls);
}
```

**Events emitted:** `StartMultiCall(address indexed creditAccount, address indexed caller)`, `FinishMultiCall()`

**Error cases:**

| Condition | Revert |
|-----------|--------|
| Caller is not the Credit Account owner | `CallerNotCreditAccountOwnerException` |
| Debt modified twice in the same block | `DebtUpdatedTwiceInOneBlockException` |
| HF < 1 after all operations | `fullCollateralCheck` revert |
| Forbidden token balance increased while borrowing/withdrawing | Forbidden token revert |
| Resulting debt below `minDebt` or above `maxDebt` | Debt limit revert |
| Facade is paused | Pausable revert |
| Adapter call targets a non-allowed contract | Adapter check revert |

---

## Check Position Health

Read the full debt and collateral breakdown for a Credit Account using `calcDebtAndCollateral` on the Credit Manager (FACT-102).

### Method Variants

| Method | Description | When to use |
|--------|-------------|-------------|
| `calcDebtAndCollateral(address creditAccount, CollateralCalcTask task)` | Full position valuation with configurable detail level | Health monitoring, pre-trade checks |
| `getBorrowerOrRevert(address creditAccount)` | Returns owner address (FACT-100) | Verify ownership |
| `enabledTokensMaskOf(address creditAccount)` | Bitmask of enabled collateral tokens (FACT-101) | List active collateral |

### Health Factor Formula

```
HF = TWV / Total Debt                                    (FACT-050)
TWV = Σ (Balance_i × Price_i × LT_i)                     (FACT-051)
Total Debt = Principal + BaseInterest + QuotaInterest + Fees  (FACT-052)
```

| Field | Meaning |
|-------|---------|
| **Principal** | Original borrowed amount |
| **BaseInterest** | Accrued interest from the pool's base rate |
| **QuotaInterest** | Accrued interest from quota fees on specific collateral tokens |
| **Fees** | Protocol fees on interest |
| **TWV** | Total Weighted Value — collateral value discounted by Liquidation Thresholds |
| **HF ≥ 1** | Healthy — no liquidation risk |
| **HF < 1** | Liquidatable — anyone can call `liquidateCreditAccount` |

### Step 1: Identify

Determine the Credit Manager address from the facade.

**TypeScript**

```typescript
// using facade, CREDIT_MANAGER_ABI from Setup section
const cmAddress = await facade.creditManager();
const cm = new ethers.Contract(cmAddress, CREDIT_MANAGER_ABI, provider);
```

### Step 2: Prepare

Select the `CollateralCalcTask` enum value based on the query purpose.

| Task Value | Name | Description |
|------------|------|-------------|
| `0` | `GENERIC_PARAMS` | Basic debt parameters only |
| `1` | `DEBT_COLLATERAL_WITHOUT_WITHDRAWALS` | Full valuation, no withdrawal simulation |
| `2` | `DEBT_COLLATERAL_CANCEL_WITHDRAWALS` | Full valuation, cancel pending withdrawals |
| `3` | `DEBT_COLLATERAL_FORCE_CANCEL_WITHDRAWALS` | Force cancel + full valuation |

### Step 3: Execute

**TypeScript**

```typescript
// using cm from Step 1
const task = 1; // DEBT_COLLATERAL_WITHOUT_WITHDRAWALS
const result = await cm.calcDebtAndCollateral(creditAccountAddress, task);

const healthFactor = result.twvUSD * 10000n / result.totalDebtUSD;
console.log(`HF: ${Number(healthFactor) / 10000}`);
console.log(`Debt: ${result.totalDebtUSD}, TWV: ${result.twvUSD}`);
```

**Solidity**

```solidity
// Inside a contract inheriting CreditIntegration from Setup
function getHealthFactor(address creditAccount) external view returns (uint256 hf) {
    // CollateralCalcTask.DEBT_COLLATERAL_WITHOUT_WITHDRAWALS = 1
    CollateralDebtData memory data = creditManager.calcDebtAndCollateral(creditAccount, 1);
    // HF in basis points: 10000 = 1.0
    hf = data.twvUSD * 10000 / data.totalDebtUSD;
}
```

---

## Close Position

Repay all outstanding debt and return the Credit Account to the factory (FACT-011). Partial close is not possible — all debt must be repaid to zero.

### Method Variants

| Method | Description | When to use |
|--------|-------------|-------------|
| `closeCreditAccount(address creditAccount, MultiCall[] calls)` | Repay debt, withdraw remainder, return account | Clean exit |

### Typical Close Flow

1. Swap all non-underlying collateral to the underlying token (via adapter calls)
2. `decreaseDebt(type(uint256).max)` — repay all outstanding debt
3. `withdrawCollateral(underlying, type(uint256).max, to)` — withdraw remaining balance

### Step 1: Identify

Verify position state and ensure sufficient underlying balance to cover total debt after swaps.

**Pre-conditions:**

- ✅ Caller is the Credit Account owner — `getBorrowerOrRevert(creditAccount)` returns caller
- ✅ After multicall execution, debt is exactly zero — any remainder reverts
- ✅ All collateral swapped to underlying, or sufficient underlying to repay

**TypeScript**

```typescript
// using cm from Check Position Health section
const owner = await cm.getBorrowerOrRevert(creditAccountAddress);
console.log(`Account owner: ${owner}`);

const result = await cm.calcDebtAndCollateral(creditAccountAddress, 1);
console.log(`Total debt to repay: ${result.totalDebtUSD}`);
```

### Step 2: Prepare

Build the close multicall — swap all collateral tokens to underlying, repay all debt, withdraw.

**TypeScript**

```typescript
// using facadeCall from Setup section
// Assume all collateral already swapped to underlying via adapter calls
const calls = [
  // Adapter swap calls would go here first (e.g., WETH → USDC)
  facadeCall("decreaseDebt", [ethers.MaxUint256]),  // repay all
  facadeCall("withdrawCollateral", [usdcAddress, ethers.MaxUint256, signerAddress]),
];
```

**Solidity**

```solidity
// Inside a contract inheriting CreditIntegration from Setup
function buildCloseCalls(address to) internal view returns (MultiCall[] memory calls) {
    calls = new MultiCall[](2);
    calls[0] = MultiCall({
        target: address(facade),
        callData: abi.encodeCall(ICreditFacadeV3Multicall.decreaseDebt, (type(uint256).max))
    });
    calls[1] = MultiCall({
        target: address(facade),
        callData: abi.encodeCall(ICreditFacadeV3Multicall.withdrawCollateral, (address(underlying), type(uint256).max, to))
    });
}
```

### Step 3: Execute

**TypeScript**

```typescript
// using facadeWrite from Setup section
const tx = await facadeWrite.closeCreditAccount(creditAccountAddress, calls);
const receipt = await tx.wait();
console.log(`Account closed: ${receipt.hash}`);
```

**Solidity**

```solidity
// Inside a contract inheriting CreditIntegration from Setup
function closeAccount(address creditAccount, address to) external {
    MultiCall[] memory calls = buildCloseCalls(to);
    facade.closeCreditAccount(creditAccount, calls);
}
```

**Events emitted:** `CloseCreditAccount(address indexed creditAccount, address indexed owner)`, `StartMultiCall`, `FinishMultiCall`

**Error cases:**

| Condition | Revert |
|-----------|--------|
| Caller is not the account owner | `CallerNotCreditAccountOwnerException` |
| Debt not fully repaid after multicall | `CloseAccountWithNonZeroDebtException` |
| Swap slippage leaves insufficient underlying | `CloseAccountWithNonZeroDebtException` |
| Facade is paused | Pausable revert |

---

## Expiration

Some Credit Facades have an expiration date that restricts operations after a set timestamp.

### Checking Expiration

**TypeScript**

```typescript
// using facade from Setup section
const expiry = await facade.expirationDate(); // uint40 timestamp
if (expiry === 0n) {
  console.log("No expiration — facade accepts accounts indefinitely");
} else {
  const now = BigInt(Math.floor(Date.now() / 1000));
  console.log(expiry > now ? `Expires: ${new Date(Number(expiry) * 1000)}` : "EXPIRED");
}
```

**Solidity**

```solidity
// Inside a contract inheriting CreditIntegration from Setup
function isExpired() external view returns (bool) {
    uint40 expiry = facade.expirationDate();
    if (expiry == 0) return false; // no expiry set
    return block.timestamp >= expiry;
}
```

### Post-Expiration Behavior

| Operation | After Expiry |
|-----------|-------------|
| `openCreditAccount` | Reverts with `NotAllowedAfterExpirationException` |
| `increaseDebt` (within multicall) | Reverts with `NotAllowedAfterExpirationException` |
| `multicall` (no new borrowing) | Allowed — can still manage, repay, withdraw |
| `closeCreditAccount` | Allowed — accounts must close or face liquidation |
| Liquidation | Allowed — expired accounts with debt become liquidatable at post-expiry fee rates |

---

## Gotchas

### 1. Approve the Credit Manager, Not the Facade

ERC-20 `approve` for collateral tokens must target the **Credit Manager** address, not the CreditFacadeV3. The Credit Manager executes `transferFrom` during `addCollateral`. Call `facade.creditManager()` to get the correct approval target.

### 2. Debt Cannot Be Modified Twice in One Block

`increaseDebt` and `decreaseDebt` set a timestamp flag. A second debt modification in the same block reverts with `DebtUpdatedTwiceInOneBlockException`. This means: open + immediate manage in the same block is impossible if both modify debt. Plan transactions across blocks.

### 3. Debt Limits Are Enforced Per Account

Every account's total debt must stay between `minDebt` and `maxDebt` (from `debtLimits()`). Partial repayment that drops debt below `minDebt` reverts — either repay to zero (close) or stay above `minDebt`. There is also a `maxDebtPerBlockMultiplier` that limits total new borrowing across all accounts per block.

### 4. Check-on-Exit Means Order Is Flexible (Within Limits)

Health factor is validated once at the end of the multicall, not per operation. This enables temporarily unhealthy intermediate states — e.g., withdraw collateral then add different collateral. However, operation order still matters: `increaseDebt` must precede adapter calls that spend the borrowed funds, because the funds must exist in the Credit Account for the adapter call to succeed.

### 5. Forbidden Tokens Restrict Borrowing

If a Credit Account holds tokens in the `forbiddenTokenMask()`, those tokens still count toward TWV (FACT-051), but the account enters restricted mode. While forbidden tokens are enabled, `increaseDebt` and `withdrawCollateral` (for non-forbidden tokens) are blocked unless forbidden token balances are non-increasing. Swap out of forbidden tokens before borrowing more.

### 6. One Account Per Address Per Credit Manager

A single address can own at most one Credit Account per Credit Manager. Opening a second account on the same Credit Manager with the same `onBehalfOf` address reverts. Different Credit Managers allow separate accounts.

### 7. Multicall Targets Must Be Allowed

External calls within a multicall must target **allowed adapter addresses**, not arbitrary contracts. The Credit Manager maintains a mapping of allowed adapters. Calling a non-allowed target reverts. Internal calls (targeting the facade address) dispatch to `ICreditFacadeV3Multicall` functions.

### 8. `closeCreditAccount` Requires Zero Debt

The close function reverts with `CloseAccountWithNonZeroDebtException` if any debt remains after executing the multicall. This includes accrued interest and fees (FACT-052). Use `decreaseDebt(type(uint256).max)` to repay all debt, and ensure the Credit Account holds enough underlying after swaps.

### 9. Bot Permissions Use a Bitmask

`setBotPermissions(address bot, uint192 permissions)` grants granular access: bit 0 = add collateral, bit 1 = increase debt, bit 2 = decrease debt, bit 5 = withdraw collateral, bit 6 = update quota, bit 16 = external calls. The `SET_BOT_PERMISSIONS_PERMISSION` (bit 8) is owner-only — bots cannot grant permissions to other bots.

### 10. Slippage Protection via Balance Checks

Use `storeExpectedBalances` + `compareBalances` to enforce minimum output from adapter swaps. Call `storeExpectedBalances` with expected deltas before the swap, then `compareBalances` after. If any balance falls below the expected minimum, the entire multicall reverts. This is critical for protecting against MEV sandwich attacks.

---

**Related:** [Lending: Pool Deposit & Withdrawal →](./01-lending.md) · [Strategies & Adapters →](./03-strategies.md) · [Liquidation →](./04-liquidation.md) · [CreditFacadeV3.sol](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/credit/CreditFacadeV3.sol) · [ICreditFacadeV3Multicall.sol](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/interfaces/ICreditFacadeV3Multicall.sol)
