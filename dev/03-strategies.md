# Leveraged Farming: Strategies & Adapters

Deploy borrowed capital into external DeFi protocols — Uniswap, Curve, Convex, Aura, Lido, Yearn, Pendle, Balancer, Beefy, Mellow — through adapter contracts that execute from the Credit Account. A strategy combines opening a Credit Account, borrowing, and depositing into a yield position within a single atomic multicall (FACT-004).

| Concept | Mechanism |
|---------|-----------|
| **Adapter** | Wrapper contract around a target protocol. Mirrors the target's interface but executes from the Credit Account via CreditManager (FACT-003). The adapter handles token approvals, parameter validation, and pool/pair whitelisting. |
| **Strategy** | A sequence of multicall operations: `addCollateral` → `increaseDebt` → adapter deposit calls, all encoded as `MultiCall[]` and executed atomically (FACT-004). |
| **Leverage multiplier** | The Liquidation Threshold (LT) of the resulting collateral token sets the ceiling (FACT-051). With LT = 90%, max leverage ≈ 10× (`1 / (1 - LT)`). |
| **Adapter resolution** | `creditManager.contractToAdapter(targetAddress)` returns the adapter address for a given protocol contract. Reverse: `creditManager.adapterToContract(adapterAddress)`. |
| **Collateral check** | After all multicall operations complete, CreditManager runs `fullCollateralCheck` — HF = TWV / Total Debt must be ≥ 1 (FACT-050). Intermediate states can be temporarily unhealthy. |
| **Unwinding** | Reverse of entry: adapter withdrawal from protocol → swap to underlying → `decreaseDebt(type(uint256).max)` → `withdrawCollateral`. |
| **Quota requirement** | Non-underlying collateral tokens require a quota via `updateQuota` before they contribute to TWV (FACT-040, FACT-042). Without a quota, HF calculation ignores the token balance. |

**Contracts:** [`CreditFacadeV3.sol`](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/credit/CreditFacadeV3.sol) · [`ICreditFacadeV3Multicall.sol`](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/interfaces/ICreditFacadeV3Multicall.sol) · [`IAdapter.sol`](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/interfaces/base/IAdapter.sol) · [`integrations-v3`](https://github.com/Gearbox-protocol/integrations-v3)

---

## Adapter Discovery

Locate adapter addresses for a given Credit Manager before encoding multicall operations.

### Option A: CreditManager On-Chain Lookup

`creditManager.contractToAdapter(targetAddress)` returns the adapter address for a whitelisted protocol contract. Returns `address(0)` if governance has not configured an adapter.

**TypeScript**

```typescript
import { ethers } from "ethers";

const cm = new ethers.Contract(creditManagerAddress, [
  "function contractToAdapter(address) view returns (address)",
  "function adapterToContract(address) view returns (address)",
], provider);

const curveAdapter = await cm.contractToAdapter(curvePoolAddress);
// curveAdapter: "0x..." or ethers.ZeroAddress if not allowed
```

**Solidity**

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

import {ICreditManagerV3} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditManagerV3.sol";

contract AdapterFinder {
    function getAdapter(ICreditManagerV3 cm, address target) external view returns (address) {
        return cm.contractToAdapter(target);
    }
}
```

### Option B: CreditAccountCompressor (Aggregated Data)

`CreditAccountCompressor` returns adapter lists alongside position data in a single call. Frontends use this to enumerate all available adapters for a Credit Manager.

```typescript
const compressor = new ethers.Contract(creditAccountCompressorAddress, [
  "function getCreditAccountData(address creditManager, address creditAccount) view returns (tuple)",
], provider);

const data = await compressor.getCreditAccountData(creditManagerAddress, creditAccountAddress);
```

### Option C: SDK (High-Level)

```typescript
import { GearboxSDK } from "@gearbox-protocol/sdk";

const sdk = new GearboxSDK({ /* provider config */ });
const cmSuite = sdk.market.creditManagers[0];
// cmSuite.adapters — map of protocol name → adapter address
```

---

## Setup

Instantiate adapter interfaces, Credit Facade, and CreditManager. All subsequent examples reference these instances.

**TypeScript (ethers.js)**

```typescript
import { ethers } from "ethers";

const FACADE_ABI = [
  "function openCreditAccount(address onBehalfOf, (address target, bytes callData)[] calls, uint256 referralCode) returns (address)",
  "function closeCreditAccount(address creditAccount, (address target, bytes callData)[] calls)",
  "function multicall(address creditAccount, (address target, bytes callData)[] calls)",
  "function creditManager() view returns (address)",
  "function underlying() view returns (address)",
  "function debtLimits() view returns (uint128 minDebt, uint128 maxDebt)",
  "function paused() view returns (bool)",
  "event OpenCreditAccount(address indexed creditAccount, address indexed onBehalfOf, address indexed caller, uint256 referralCode)",
  "event CloseCreditAccount(address indexed creditAccount, address indexed owner)",
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
// Adapter interface — example for Curve 3pool
const CURVE_ADAPTER_ABI = [
  "function add_liquidity(uint256[] amounts, uint256 min_mint_amount)",
  "function remove_liquidity(uint256[] amounts, uint256 max_burn_amount)",
  "function remove_liquidity_one_coin(uint256 token_amount, int128 i, uint256 min_amount)",
  "function exchange(int128 i, int128 j, uint256 dx, uint256 min_dy)",
];

const curveAdapterIface = new ethers.Interface(CURVE_ADAPTER_ABI);

// Credit Manager for adapter lookups
const CREDIT_MANAGER_ABI = [
  "function contractToAdapter(address) view returns (address)",
  "function adapterToContract(address) view returns (address)",
  "function calcDebtAndCollateral(address creditAccount, uint8 task) view returns (tuple)",
  "function getBorrowerOrRevert(address creditAccount) view returns (address)",
];

const cm = new ethers.Contract(await facade.creditManager(), CREDIT_MANAGER_ABI, provider);
```

```typescript
const ERC20_ABI = [
  "function approve(address spender, uint256 amount) returns (bool)",
  "function allowance(address owner, address spender) view returns (uint256)",
  "function balanceOf(address) view returns (uint256)",
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

/// @notice Base contract for leveraged strategy interactions.
contract StrategyIntegration {
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

## Open a Credit-Backed Position

Deposit collateral, borrow from the pool, and deploy into a yield protocol — all in a single `openCreditAccount` call (FACT-010).

### Method Variants

| Method | Description | When to use |
|--------|-------------|-------------|
| `openCreditAccount(address onBehalfOf, MultiCall[] calls, uint256 referralCode)` (FACT-010) | Opens account, executes multicall (deposit + borrow + adapter calls), returns Credit Account address | Opening a new credit-backed position |

### Step 1: Identify

Verify the facade is active, debt limits are compatible, and the target adapter exists.

**Pre-conditions:**

- ✅ Facade is not paused — `paused()` returns `false`
- ✅ Borrow amount is between `minDebt` and `maxDebt` — call `debtLimits()`
- ✅ Adapter exists for target protocol — `creditManager.contractToAdapter(target)` returns non-zero
- ✅ ERC-20 approval granted — approve collateral token to the **Credit Manager** address (FACT-003)
- ✅ Resulting HF ≥ 1 after all adapter calls complete — the LP token must have sufficient LT

**TypeScript**

```typescript
// using facade, cm from Setup section
const isPaused = await facade.paused();
const [minDebt, maxDebt] = await facade.debtLimits();
const cmAddress = await facade.creditManager();

const curveAdapter = await cm.contractToAdapter(curvePoolAddress);
if (curveAdapter === ethers.ZeroAddress) throw new Error("No adapter for target");

const borrowAmount = 5n * 10n ** 18n; // 5 ETH
console.log(`Adapter: ${curveAdapter}, Debt range: ${minDebt}–${maxDebt}`);
```

**Solidity**

```solidity
// Inside a contract inheriting StrategyIntegration from Setup
function verifyAdapter(address target) external view returns (address adapter) {
    adapter = creditManager.contractToAdapter(target);
    require(adapter != address(0), "no adapter");
    require(!facade.paused(), "facade paused");
}
```

### Step 2: Prepare

Approve collateral to the Credit Manager. Build the multicall array: `addCollateral` → `increaseDebt` → `updateQuota` (for LP token) → adapter deposit.

**TypeScript**

```typescript
// using facadeCall, curveAdapterIface, ERC20_ABI from Setup section
const cmAddress = await facade.creditManager();
const collateral = new ethers.Contract(wethAddress, ERC20_ABI, signer);

const collateralAmount = 1n * 10n ** 18n; // 1 ETH own capital
const allowance = await collateral.allowance(signerAddress, cmAddress);
if (allowance < collateralAmount) {
  const tx = await collateral.approve(cmAddress, collateralAmount);
  await tx.wait();
}
```

```typescript
// Build multicall: deposit 1 ETH + borrow 5 ETH + LP into Curve = 6x leverage
const borrowAmount = 5n * 10n ** 18n;
const lpCalldata = curveAdapterIface.encodeFunctionData("add_liquidity", [
  [6n * 10n ** 18n, 0n], 0n  // deposit 6 ETH into first slot, min LP = 0
]);

const calls = [
  facadeCall("addCollateral", [wethAddress, collateralAmount]),
  facadeCall("increaseDebt", [borrowAmount]),
  facadeCall("updateQuota", [curveLpTokenAddress, ethers.MaxInt256, 0n]),
  { target: curveAdapterAddress, callData: lpCalldata },
];
```

**Solidity**

```solidity
// Inside a contract inheriting StrategyIntegration from Setup
function buildOpenCalls(
    uint256 collateral, uint256 debt, address adapter, bytes memory adapterCalldata, address lpToken
) internal view returns (MultiCall[] memory calls) {
    calls = new MultiCall[](4);
    calls[0] = MultiCall({
        target: address(facade),
        callData: abi.encodeCall(ICreditFacadeV3Multicall.addCollateral, (address(underlying), collateral))
    });
    calls[1] = MultiCall({
        target: address(facade),
        callData: abi.encodeCall(ICreditFacadeV3Multicall.increaseDebt, (debt))
    });
    calls[2] = MultiCall({
        target: address(facade),
        callData: abi.encodeCall(ICreditFacadeV3Multicall.updateQuota, (lpToken, type(int96).max, 0))
    });
    calls[3] = MultiCall({target: adapter, callData: adapterCalldata});
}
```

### Step 3: Execute

Call `openCreditAccount` with the assembled multicall (FACT-010). CreditManager runs `fullCollateralCheck` after all calls complete (FACT-050).

**TypeScript**

```typescript
// using facadeWrite, calls from Prepare step
const tx = await facadeWrite.openCreditAccount(signerAddress, calls, 0n);
const receipt = await tx.wait();

const openEvent = receipt.logs.find((log: any) => {
  try { return facade.interface.parseLog(log)?.name === "OpenCreditAccount"; } catch { return false; }
});
const creditAccountAddress = facade.interface.parseLog(openEvent).args.creditAccount;
console.log(`Position opened: ${creditAccountAddress}`);
```

**Solidity**

```solidity
// Inside a contract inheriting StrategyIntegration from Setup
function openLeveraged(
    uint256 collateral, uint256 debt, address adapter, bytes calldata adapterCalldata, address lpToken
) external returns (address creditAccount) {
    underlying.approve(address(creditManager), collateral);
    MultiCall[] memory calls = buildOpenCalls(collateral, debt, adapter, adapterCalldata, lpToken);
    creditAccount = facade.openCreditAccount(address(this), calls, 0);
}
```

**Events emitted:** `OpenCreditAccount(address indexed creditAccount, address indexed onBehalfOf, address indexed caller, uint256 referralCode)`, `StartMultiCall`, `FinishMultiCall`

**Error cases:**

| Condition | Revert |
|-----------|--------|
| Facade is paused | Pausable revert |
| Adapter target not allowed by CreditManager | Adapter check revert |
| Borrow below `minDebt` or above `maxDebt` | Debt limit revert |
| HF < 1 after adapter deposit (LT too low for debt-to-collateral ratio) | `fullCollateralCheck` revert |
| Insufficient ERC-20 approval to Credit Manager | `transferFrom` revert |
| LP token quota not set before adapter deposit | LP balance ignored in TWV → HF < 1 |
| Total new debt this block exceeds `maxDebtPerBlockMultiplier` | Debt limit revert |

---

## Adjust Exposure

Modify an existing credit-backed position — increase exposure, decrease exposure, or rotate between protocols — via `multicall` (FACT-012).

### Method Variants

| Method | Description | When to use |
|--------|-------------|-------------|
| `multicall(address creditAccount, MultiCall[] calls)` (FACT-012) | Owner batches operations: borrow more, add to position, partially withdraw | Standard exposure adjustment |
| `botMulticall(address creditAccount, MultiCall[] calls)` (FACT-013) | Authorized bot executes permitted operations | Automated rebalancing, compounding rewards |

### Increase Exposure

Borrow additional underlying from the pool and deposit into the yield protocol via the adapter.

**TypeScript**

```typescript
// using facadeCall, curveAdapterIface, facadeWrite from Setup section
const additionalBorrow = 2n * 10n ** 18n; // borrow 2 more ETH
const lpCalldata = curveAdapterIface.encodeFunctionData("add_liquidity", [
  [additionalBorrow, 0n], 0n
]);

const calls = [
  facadeCall("increaseDebt", [additionalBorrow]),
  { target: curveAdapterAddress, callData: lpCalldata },
];

const tx = await facadeWrite.multicall(creditAccountAddress, calls);
await tx.wait();
```

**Solidity**

```solidity
// Inside a contract inheriting StrategyIntegration from Setup
function increaseLeverage(
    address creditAccount, uint256 borrowMore, address adapter, bytes calldata adapterCalldata
) external {
    MultiCall[] memory calls = new MultiCall[](2);
    calls[0] = MultiCall({
        target: address(facade),
        callData: abi.encodeCall(ICreditFacadeV3Multicall.increaseDebt, (borrowMore))
    });
    calls[1] = MultiCall({target: adapter, callData: adapterCalldata});
    facade.multicall(creditAccount, calls);
}
```

### Decrease Exposure

Withdraw from the yield protocol via the adapter, swap back to underlying if needed, and repay debt.

**TypeScript**

```typescript
// using facadeCall, curveAdapterIface, facadeWrite from Setup section
const withdrawCalldata = curveAdapterIface.encodeFunctionData("remove_liquidity_one_coin", [
  lpTokenAmount, 0n, 0n  // burn LP, receive token index 0, min output 0
]);

const calls = [
  { target: curveAdapterAddress, callData: withdrawCalldata },
  facadeCall("decreaseDebt", [repayAmount]),
];

const tx = await facadeWrite.multicall(creditAccountAddress, calls);
await tx.wait();
```

**Solidity**

```solidity
// Inside a contract inheriting StrategyIntegration from Setup
function decreaseLeverage(
    address creditAccount, address adapter, bytes calldata withdrawCalldata, uint256 repayAmount
) external {
    MultiCall[] memory calls = new MultiCall[](2);
    calls[0] = MultiCall({target: adapter, callData: withdrawCalldata});
    calls[1] = MultiCall({
        target: address(facade),
        callData: abi.encodeCall(ICreditFacadeV3Multicall.decreaseDebt, (repayAmount))
    });
    facade.multicall(creditAccount, calls);
}
```

### Rotate Strategy

Exit one protocol and enter another in a single multicall. Example: move from Curve LP to Convex staking.

**TypeScript**

```typescript
// using facadeCall, facadeWrite from Setup section
const exitCurve = curveAdapterIface.encodeFunctionData("remove_liquidity_one_coin", [
  lpAmount, 0n, 0n
]);
const convexAdapterIface = new ethers.Interface([
  "function deposit(uint256 pid, uint256 amount, bool stake)",
]);
const enterConvex = convexAdapterIface.encodeFunctionData("deposit", [
  poolId, depositAmount, true
]);

const calls = [
  { target: curveAdapterAddress, callData: exitCurve },
  facadeCall("updateQuota", [convexTokenAddress, ethers.MaxInt256, 0n]),
  { target: convexAdapterAddress, callData: enterConvex },
];

const tx = await facadeWrite.multicall(creditAccountAddress, calls);
await tx.wait();
```

**Error cases:**

| Condition | Revert |
|-----------|--------|
| Caller is not the Credit Account owner | `CallerNotCreditAccountOwnerException` |
| HF < 1 after adjustment | `fullCollateralCheck` revert |
| Debt modified twice in the same block | `DebtUpdatedTwiceInOneBlockException` |
| Adapter target not whitelisted | Adapter check revert |
| Resulting debt below `minDebt` or above `maxDebt` | Debt limit revert |

---

## Unwind Position

Close the credit-backed position: exit the yield protocol, repay all debt, and withdraw remaining collateral.

### Step 1: Identify

Read position state — current debt, collateral tokens, and adapter addresses for exit calls.

**Pre-conditions:**

- ✅ Caller is the Credit Account owner — `creditManager.getBorrowerOrRevert(creditAccount)` (FACT-100) returns caller
- ✅ The Credit Account holds LP/yield tokens to withdraw from the protocol
- ✅ After swaps and adapter withdrawals, the account holds enough underlying to repay total debt (principal + base interest + quota interest + fees) (FACT-052)

**TypeScript**

```typescript
// using cm, facade from Setup section
const owner = await cm.getBorrowerOrRevert(creditAccountAddress);
const positionData = await cm.calcDebtAndCollateral(creditAccountAddress, 1); // (FACT-102)
console.log(`Total debt: ${positionData.totalDebtUSD}`);
console.log(`TWV: ${positionData.twvUSD}`);
```

**Solidity**

```solidity
// Inside a contract inheriting StrategyIntegration from Setup
function getDebt(address creditAccount) external view returns (uint256) {
    CollateralDebtData memory data = creditManager.calcDebtAndCollateral(creditAccount, 1); // (FACT-102)
    return data.totalDebtUSD;
}
```

### Step 2: Prepare

Build the unwind multicall: adapter withdraw → swap non-underlying tokens to underlying → repay all debt → withdraw remaining balance.

**TypeScript**

```typescript
// using facadeCall, curveAdapterIface from Setup section
const exitCalldata = curveAdapterIface.encodeFunctionData("remove_liquidity_one_coin", [
  lpTokenBalance, 0n, 0n  // burn all LP, receive underlying, min output 0
]);

const calls = [
  { target: curveAdapterAddress, callData: exitCalldata },
  facadeCall("decreaseDebt", [ethers.MaxUint256]),           // repay all debt
  facadeCall("withdrawCollateral", [wethAddress, ethers.MaxUint256, signerAddress]),
];
```

**Solidity**

```solidity
// Inside a contract inheriting StrategyIntegration from Setup
function buildUnwindCalls(
    address adapter, bytes memory exitCalldata, address to
) internal view returns (MultiCall[] memory calls) {
    calls = new MultiCall[](3);
    calls[0] = MultiCall({target: adapter, callData: exitCalldata});
    calls[1] = MultiCall({
        target: address(facade),
        callData: abi.encodeCall(ICreditFacadeV3Multicall.decreaseDebt, (type(uint256).max))
    });
    calls[2] = MultiCall({
        target: address(facade),
        callData: abi.encodeCall(
            ICreditFacadeV3Multicall.withdrawCollateral, (address(underlying), type(uint256).max, to)
        )
    });
}
```

### Step 3: Execute

Call `closeCreditAccount` (FACT-011) to atomically unwind, repay, and return the Credit Account to the factory.

**TypeScript**

```typescript
// using facadeWrite, calls from Prepare step
const tx = await facadeWrite.closeCreditAccount(creditAccountAddress, calls);
const receipt = await tx.wait();
console.log(`Position unwound and account closed: ${receipt.hash}`);
```

**Solidity**

```solidity
// Inside a contract inheriting StrategyIntegration from Setup
function unwind(address creditAccount, address adapter, bytes calldata exitCalldata) external {
    MultiCall[] memory calls = buildUnwindCalls(adapter, exitCalldata, msg.sender);
    facade.closeCreditAccount(creditAccount, calls);
}
```

**Events emitted:** `CloseCreditAccount(address indexed creditAccount, address indexed owner)`, `StartMultiCall`, `FinishMultiCall`

**Error cases:**

| Condition | Revert |
|-----------|--------|
| Caller is not the account owner | `CallerNotCreditAccountOwnerException` |
| Debt not fully repaid after multicall | `CloseAccountWithNonZeroDebtException` |
| Adapter withdrawal returns insufficient underlying | `CloseAccountWithNonZeroDebtException` (debt remains) |
| Slippage on exit leaves residual debt | `CloseAccountWithNonZeroDebtException` |
| Facade is paused | Pausable revert |

---

## Available Strategies

Governance deploys adapters per Credit Manager (FACT-001). The set of available strategies depends on which adapters governance configures. Enumerate available adapters by querying the Credit Manager.

### Supported Protocol Adapters

| Protocol | Adapter Type | Typical Operations |
|----------|-------------|-------------------|
| **Uniswap V2** | DEX swap | `swapExactTokensForTokens`, `swapTokensForExactTokens` |
| **Uniswap V3** | DEX swap | `exactInputSingle`, `exactInput`, `exactOutputSingle` |
| **Curve** | DEX + LP | `exchange`, `add_liquidity`, `remove_liquidity_one_coin` |
| **Convex** | Yield farming | `deposit`, `withdraw`, `getReward` (Booster + BaseRewardPool) |
| **Aura** | Yield farming | `deposit`, `withdraw`, `getReward` (Balancer LP staking) |
| **Lido** | Liquid staking | `submit` (ETH → stETH), `wrap` (stETH → wstETH) |
| **Yearn V2** | Vault | `deposit`, `withdraw` (yVault shares) |
| **Balancer V2** | DEX + LP | `swap`, `joinPool`, `exitPool` |
| **Pendle** | Yield tokenization | `swapExactTokenForPt`, `swapExactPtForToken`, `addLiquiditySingleToken` |
| **Beefy** | Vault | `deposit`, `withdraw` (vault shares) |
| **Mellow** | Vault | `deposit`, `withdraw` (LRT vaults) |

### Key Adapter Function Signatures

Each adapter mirrors the target protocol's interface. The Credit Account is the `msg.sender` for all calls routed through `CreditManager.execute` (FACT-003). Full Solidity signatures for core adapter functions:

#### Uniswap V3 (ISwapRouter)

| Function | Signature |
|----------|-----------|
| `exactInputSingle` | `exactInputSingle(ExactInputSingleParams calldata params) returns (uint256 amountOut)` |
| `exactInput` | `exactInput(ExactInputParams calldata params) returns (uint256 amountOut)` |
| `exactOutputSingle` | `exactOutputSingle(ExactOutputSingleParams calldata params) returns (uint256 amountIn)` |

`ExactInputSingleParams` contains: `tokenIn`, `tokenOut`, `fee`, `recipient`, `deadline`, `amountIn`, `amountOutMinimum`, `sqrtPriceLimitX96`. The adapter overrides `recipient` to the Credit Account address.

#### Curve (ICurvePool)

| Function | Signature |
|----------|-----------|
| `exchange` | `exchange(int128 i, int128 j, uint256 dx, uint256 min_dy) returns (uint256)` |
| `exchange_underlying` | `exchange_underlying(int128 i, int128 j, uint256 dx, uint256 min_dy) returns (uint256)` |
| `add_liquidity` | `add_liquidity(uint256[] calldata amounts, uint256 min_mint_amount) returns (uint256)` |
| `remove_liquidity` | `remove_liquidity(uint256 amount, uint256[] calldata min_amounts) returns (uint256[])` |
| `remove_liquidity_one_coin` | `remove_liquidity_one_coin(uint256 token_amount, int128 i, uint256 min_amount) returns (uint256)` |
| `remove_liquidity_imbalance` | `remove_liquidity_imbalance(uint256[] calldata amounts, uint256 max_burn_amount) returns (uint256)` |

Curve pool indices (`i`, `j`) are zero-based. The adapter resolves token addresses to indices internally for `exchange` calls.

#### Convex (IBooster + IBaseRewardPool)

| Function | Contract | Signature |
|----------|----------|-----------|
| `deposit` | Booster | `deposit(uint256 pid, uint256 amount, bool stake) returns (bool)` |
| `withdraw` | Booster | `withdraw(uint256 pid, uint256 amount) returns (bool)` |
| `getReward` | BaseRewardPool | `getReward(address account, bool claimExtras) returns (bool)` |
| `withdrawAndUnwrap` | BaseRewardPool | `withdrawAndUnwrap(uint256 amount, bool claim) returns (bool)` |
| `stake` | BaseRewardPool | `stake(uint256 amount) returns (bool)` |

`pid` is the Convex pool ID. Setting `stake = true` in `deposit` routes LP tokens directly to the BaseRewardPool.

#### Lido (ILido + IWstETH)

| Function | Contract | Signature |
|----------|----------|-----------|
| `submit` | Lido (stETH) | `submit(address referral) returns (uint256 sharesAmount)` |
| `wrap` | WstETH | `wrap(uint256 stETHAmount) returns (uint256 wstETHAmount)` |
| `unwrap` | WstETH | `unwrap(uint256 wstETHAmount) returns (uint256 stETHAmount)` |

`submit` converts ETH to stETH. `wrap` converts stETH to wstETH (non-rebasing). Credit Accounts hold wstETH as the collateral-recognized token (FACT-040).

#### Yearn V2 (IYVault)

| Function | Signature |
|----------|-----------|
| `deposit` | `deposit(uint256 amount) returns (uint256 shares)` |
| `deposit` (with recipient) | `deposit(uint256 amount, address recipient) returns (uint256 shares)` |
| `withdraw` | `withdraw(uint256 maxShares) returns (uint256 amount)` |
| `withdraw` (with recipient) | `withdraw(uint256 maxShares, address recipient) returns (uint256 amount)` |
| `pricePerShare` | `pricePerShare() external view returns (uint256)` |

The adapter overrides `recipient` to the Credit Account address in overloaded variants.

#### Balancer V2 (IVault)

| Function | Signature |
|----------|-----------|
| `swap` | `swap(SingleSwap calldata singleSwap, FundManagement calldata funds, uint256 limit, uint256 deadline) returns (uint256 amountCalculated)` |
| `joinPool` | `joinPool(bytes32 poolId, address sender, address recipient, JoinPoolRequest calldata request)` |
| `exitPool` | `exitPool(bytes32 poolId, address sender, address recipient, ExitPoolRequest calldata request)` |

The adapter sets `sender` and `recipient` in `FundManagement` / request structs to the Credit Account address.

### Enumerating Adapters for a Credit Manager

**TypeScript**

```typescript
// using cm from Setup section
const protocolContracts = [curvePoolAddress, convexBoosterAddress, lidoAddress];

for (const target of protocolContracts) {
  const adapter = await cm.contractToAdapter(target);
  const status = adapter === ethers.ZeroAddress ? "NOT AVAILABLE" : adapter;
  console.log(`${target} → ${status}`);
}
```

**Solidity**

```solidity
// Inside a contract inheriting StrategyIntegration from Setup
function hasAdapter(address target) external view returns (bool) {
    return creditManager.contractToAdapter(target) != address(0);
}
```

### Adapter Execution Flow (Internal)

1. The integrator encodes `(adapterAddress, callData)` as a `MultiCall` entry
2. `CreditFacadeV3.multicall` dispatches the call to the adapter contract
3. The adapter validates inputs and approves tokens from the Credit Account to the target protocol
4. The adapter passes formed calldata to `CreditManager.execute`
5. `CreditManager` instructs the Credit Account (FACT-003) to execute the call on the target contract
6. After all multicall entries complete: `CreditManager.fullCollateralCheck` verifies HF ≥ 1

⚠️ Adapters do NOT transfer funds to/from the caller. All assets remain inside the Credit Account (FACT-003). The Credit Account is the `msg.sender` seen by the target protocol.

**Revert propagation:** If the target protocol reverts (insufficient liquidity, slippage exceeded, expired deadline), the adapter propagates the revert through `CreditManager.execute` and the entire `multicall` fails atomically. No partial execution occurs — all multicall entries either succeed together or revert together. Check `amountOutMinimum` (Uniswap), `min_dy` (Curve), or equivalent slippage parameters before submission.

---

## Gotchas

### 1. Adapter Address ≠ Target Protocol Address

Multicall entries must use the **adapter address** as the `target`, not the protocol contract address. `creditManager.contractToAdapter(protocolAddress)` returns the correct adapter. Passing the protocol address directly causes CreditFacade to revert — CreditFacade only accepts whitelisted adapter addresses as external call targets.

### 2. Quota Must Be Set Before Adapter Deposit

Non-underlying collateral tokens (LP tokens, vault shares) require a quota via `updateQuota(token, quotaChange, minQuota)` before they contribute to TWV (FACT-040, FACT-042). If the adapter produces an LP token without a quota, the health factor calculation ignores the token's balance, causing `fullCollateralCheck` to revert with HF < 1 (FACT-050). Place `updateQuota` before the adapter deposit call in the multicall array.

### 3. Liquidation Threshold Bounds Maximum Leverage

The maximum safe leverage multiplier for a given LP token is approximately `1 / (1 - LT)` (FACT-051). For LT = 90%, max ≈ 10×. For LT = 80%, max ≈ 5×. Exceeding this causes HF < 1 immediately after the multicall, reverting the transaction. Price impact, fees, and oracle deviations lower the actual limit slightly.

### 4. Slippage Protection Is the Integrator's Responsibility

Adapters pass `min_amount` / `min_dy` parameters directly to the target protocol. Setting these to `0` risks sandwich attacks. Use `storeExpectedBalances` + `compareBalances` within the multicall to enforce minimum outputs, or compute realistic minimums off-chain before encoding the adapter call.

### 5. Adapter Calls Cannot Be Chained Across Credit Managers

Each adapter binds to exactly one CreditManager (FACT-001). An adapter's `creditManager()` returns its bound manager. Attempting to use an adapter from a different CreditManager's multicall reverts — the adapter validates that `msg.sender` matches its configured CreditFacade.

### 6. Reward Claiming Produces Non-Quota Tokens

Calling `getReward()` on Convex/Aura adapters produces reward tokens (CRV, CVX, BAL, AURA). These tokens must have quotas set to contribute to TWV (FACT-040), and may appear on the forbidden token list. If forbidden, the account enters restricted mode — no further `increaseDebt` or `withdrawCollateral` until the forbidden token balance decreases. Swap reward tokens to underlying or allowed tokens within the same multicall.

### 7. `decreaseDebt(type(uint256).max)` Repays Exact Total Debt

When passed `type(uint256).max`, `decreaseDebt` calculates and repays the exact total debt (principal + accrued base interest + quota interest + fees) (FACT-043, FACT-052). The Credit Account must hold at least that much underlying. If the underlying balance falls short, the call reverts — not a partial repayment.

### 8. Adapters Handle Token Approvals

The integrator does NOT need to approve tokens from the Credit Account to the target protocol. The adapter handles all internal approvals before calling the target (FACT-003). Approve collateral to the **Credit Manager** only (for `addCollateral`) — not to adapters or target protocols.

### 9. Check-on-Exit Allows Temporary Insolvency

CreditManager validates HF once after all multicall operations complete (FACT-050). This permits sequences like: withdraw LP (HF drops) → swap to underlying (HF recovers) → repay debt (HF rises). The intermediate HF < 1 after LP withdrawal does not cause a revert. However, if the final state has HF < 1, the entire multicall reverts.

### 10. Bot Permissions Scope Adapter Access

When using `botMulticall` (FACT-013), the bot must have the external calls permission bit (bit 16) set via `setBotPermissions`. Without this bit, the bot can call internal facade operations (`increaseDebt`, `decreaseDebt`, etc.) but cannot execute adapter calls. The `SET_BOT_PERMISSIONS_PERMISSION` (bit 8) remains owner-only — bots cannot grant themselves additional permissions.

---

**Related:** [Lending: Pool Deposit & Withdrawal →](./01-lending.md) · [Borrowing: Credit Account Lifecycle →](./02-borrowing.md) · [Liquidation →](./04-liquidation.md) · [CreditFacadeV3.sol](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/credit/CreditFacadeV3.sol) · [IAdapter.sol](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/interfaces/base/IAdapter.sol) · [integrations-v3](https://github.com/Gearbox-protocol/integrations-v3)
