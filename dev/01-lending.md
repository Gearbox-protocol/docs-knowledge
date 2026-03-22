# Lending: Pool Deposit & Withdrawal

Deposit an underlying token into a Gearbox PoolV3 contract, receive dTokens (shares), and earn yield as borrowers pay interest. (FACT-001) Withdraw by burning shares for the underlying.

PoolV3 is **ERC-4626 compliant**. Standard ERC-4626 tooling works. Deviations from vanilla ERC-4626:

| Deviation | Effect |
|-----------|--------|
| **Withdrawal fee** | A fee in basis points (`withdrawFee()`) is deducted on exit. Callers receive less than `convertToAssets(shares)`. |
| **Pause logic** | When paused, `maxDeposit`/`maxMint` return `0`; state-changing calls revert. |
| **Dead shares** | `1e5` shares minted to `address(0)` at deployment. Prevents ERC-4626 inflation attack. First depositor does not get 1:1. (FACT-037) |
| **Quota revenue** | `supplyRate()` includes quota fees from the PoolQuotaKeeper — not visible in vanilla ERC-4626 vaults. (FACT-040) |
| **Credit Manager borrowing** | Underlying is lent to Credit Accounts via `lendCreditAccount`. Utilization affects withdrawal liquidity. (FACT-001) |

**Contract:** [`PoolV3.sol`](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/pool/PoolV3.sol) · [`IPoolV3.sol`](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/interfaces/IPoolV3.sol)

---

## Pool Discovery

Locate active pool addresses before interacting with deposits or withdrawals.

### Option A: ContractsRegister (On-Chain Enumeration)

`ContractsRegister.getPools()` returns all active pool addresses. Obtain the register address from `AddressProvider`.

**TypeScript**

```typescript
import { ethers } from "ethers";

const register = new ethers.Contract(contractsRegisterAddress, [
  "function getPools() view returns (address[])",
], provider);

const pools = await register.getPools();
// pools: string[] — e.g., ["0xabc...", "0xdef..."]
```

**Solidity**

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

import {IContractsRegister} from "@gearbox-protocol/core-v3/contracts/interfaces/IContractsRegister.sol";

contract PoolFinder {
    function listPools(IContractsRegister register) external view returns (address[] memory) {
        return register.getPools();
    }
}
```

### Option B: MarketCompressor (Aggregated Data)

`MarketCompressor.getMarkets(filter)` returns `MarketData[]` — pool address, underlying token, rates, utilization, and connected Credit Managers in a single call. (FACT-002)

```typescript
const compressor = new ethers.Contract(marketCompressorAddress, [
  "function getMarkets((bool,address[],bool,address[]) filter) view returns (tuple[])",
], provider);

const markets = await compressor.getMarkets({ /* MarketFilter fields */ });
```

### Option C: SDK (High-Level)

```typescript
import { GearboxSDK } from "@gearbox-protocol/sdk";

const sdk = new GearboxSDK({ /* provider config */ });
const pools = sdk.market.pools;
// PoolSuite[] — each has .address, .underlying, .name, .symbol
```

---

## Setup

Instantiate the pool contract once. All subsequent examples reference this instance.

**TypeScript (ethers.js)**

```typescript
import { ethers } from "ethers";

const POOL_ABI = [
  // ERC-4626 core
  "function asset() view returns (address)",
  "function totalAssets() view returns (uint256)",
  "function totalSupply() view returns (uint256)",
  "function balanceOf(address) view returns (uint256)",
  "function convertToAssets(uint256) view returns (uint256)",
  "function convertToShares(uint256) view returns (uint256)",
  // Deposit
  "function deposit(uint256 assets, address receiver) returns (uint256 shares)",
  "function mint(uint256 shares, address receiver) returns (uint256 assets)",
  "function maxDeposit(address) view returns (uint256)",
  "function previewDeposit(uint256) view returns (uint256)",
  // Withdraw
  "function withdraw(uint256 assets, address receiver, address owner) returns (uint256 shares)",
  "function redeem(uint256 shares, address receiver, address owner) returns (uint256 assets)",
  "function maxRedeem(address) view returns (uint256)",
  "function maxWithdraw(address) view returns (uint256)",
  "function previewRedeem(uint256) view returns (uint256)",
  // Pool-specific
  "function supplyRate() view returns (uint256)",
  "function availableLiquidity() view returns (uint256)",
  "function withdrawFee() view returns (uint16)",
  // Events
  "event Deposit(address indexed sender, address indexed owner, uint256 assets, uint256 shares)",
  "event Withdraw(address indexed sender, address indexed receiver, address indexed owner, uint256 assets, uint256 shares)",
  "event Borrow(address indexed creditManager, address indexed creditAccount, uint256 amount)",
  "event Repay(address indexed creditManager, uint256 repaidAmount, uint256 profit, uint256 loss)",
];

// Read-only queries
const pool = new ethers.Contract(poolAddress, POOL_ABI, provider);

// State-changing transactions — attach a signer
const poolWrite = new ethers.Contract(poolAddress, POOL_ABI, signer);

const ERC20_ABI = [
  "function approve(address spender, uint256 amount) returns (bool)",
  "function allowance(address owner, address spender) view returns (uint256)",
];
```

**Solidity**

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

import {IPoolV3} from "@gearbox-protocol/core-v3/contracts/interfaces/IPoolV3.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

/// @notice Base contract for pool interactions.
/// Inherit or deploy with a pool address.
contract PoolIntegration {
    IPoolV3 public immutable pool;
    IERC20 public immutable underlying;

    constructor(IPoolV3 _pool) {
        pool = _pool;
        underlying = IERC20(_pool.asset());
    }
}
```

---

## Deposit

Transfer underlying tokens into the pool and receive dTokens in return.

### Method Variants

| Method | Description | When to use |
|--------|-------------|-------------|
| `deposit(uint256 assets, address receiver)` | Specify exact underlying amount to deposit (FACT-030) | Most common — "deposit 1000 USDC" |
| `mint(uint256 shares, address receiver)` | Specify exact shares to receive | When targeting a specific share count |
| `depositWithReferral(uint256 assets, address receiver, uint256 referralCode)` | Same as `deposit` + emits a `Refer` event | Referral tracking integrations |

### Step 1: Identify

Check that the pool accepts deposits and preview the expected outcome.

**Pre-conditions:**

- ✅ Pool is not paused — `maxDeposit(address)` returns non-zero
- ✅ Deposit amount > 0 — reverts with `AmountCantBeZeroException` otherwise
- ✅ Receiver is not `address(0)` — reverts with `ZeroAddressException`
- ✅ ERC-20 approval granted — underlying token approved to pool address

**TypeScript**

```typescript
// using pool from Setup section
const underlying = await pool.asset();
const maxDeposit = await pool.maxDeposit(depositorAddress);
// maxDeposit returns type(uint256).max when active, 0 when paused

const depositAmount = 1000_000000n; // 1000 USDC (6 decimals)
const expectedShares = await pool.previewDeposit(depositAmount);
```

**Solidity**

```solidity
// Inside a contract inheriting PoolIntegration from Setup
function checkDeposit(uint256 amount) external view returns (uint256 expected) {
    require(pool.maxDeposit(address(this)) > 0, "pool paused");
    expected = pool.previewDeposit(amount);
}
```

### Step 2: Prepare

Approve the underlying token to the pool, then build the deposit call.

**TypeScript**

```typescript
// using pool, ERC20_ABI from Setup section
const underlyingToken = new ethers.Contract(underlyingAddress, ERC20_ABI, signer);

const allowance = await underlyingToken.allowance(depositorAddress, poolAddress);
if (allowance < depositAmount) {
  const tx = await underlyingToken.approve(poolAddress, depositAmount);
  await tx.wait();
}
```

**Solidity**

```solidity
// Inside a contract inheriting PoolIntegration from Setup
function approvePool(uint256 amount) external {
    underlying.approve(address(pool), amount);
}
```

### Step 3: Execute

Call `deposit` and handle the result.

**TypeScript**

```typescript
// using poolWrite from Setup section
const tx = await poolWrite.deposit(depositAmount, depositorAddress);
const receipt = await tx.wait();
console.log(`Deposited ${depositAmount}, tx: ${receipt.hash}`);
```

**Solidity**

```solidity
// Inside a contract inheriting PoolIntegration from Setup
function depositToPool(uint256 amount) external returns (uint256 shares) {
    underlying.approve(address(pool), amount);
    shares = pool.deposit(amount, address(this));
}
```

**Events emitted:** `Deposit(address indexed sender, address indexed owner, uint256 assets, uint256 shares)` (FACT-036)

**Error cases:**

| Condition | Revert |
|-----------|--------|
| `assets == 0` | `AmountCantBeZeroException` |
| `receiver == address(0)` | `ZeroAddressException` |
| Pool is paused | Pausable revert |
| Insufficient ERC-20 approval | `transferFrom` revert |

#### viem Alternative

```typescript
import { createWalletClient, http, parseAbi } from "viem";
import { mainnet } from "viem/chains";

const poolAbi = parseAbi([
  "function asset() view returns (address)",
  "function deposit(uint256 assets, address receiver) returns (uint256 shares)",
]);

const hash = await walletClient.writeContract({
  address: poolAddress,
  abi: poolAbi,
  functionName: "deposit",
  args: [1000_000000n, account.address],
});
```

---

## Check Position & Yield

Read the current deposit position, its value, and pool yield data.

### Pool State Object

The key state a frontend or bot needs from a single pool:

```typescript
// Shape of data returned by reading pool state
interface PoolState {
  underlying: string;           // address of the underlying token (e.g., USDC)
  totalAssets: bigint;          // total underlying managed (including lent-out capital)
  totalSupply: bigint;          // total dTokens in circulation
  availableLiquidity: bigint;   // underlying balance actually in the pool contract (FACT-035)
  supplyRateRay: bigint;        // annualized LP yield in RAY (1e27) (FACT-033)
  withdrawFeeBps: number;       // withdrawal fee in basis points
  baseInterestRate: bigint;     // current base borrow rate in RAY (FACT-034)
}
```

### Reading Share Balance and Value

**TypeScript**

```typescript
// using pool from Setup section
const shares = await pool.balanceOf(accountAddress);
const grossValue = await pool.convertToAssets(shares);
const feeBps = await pool.withdrawFee();
const netValue = grossValue - (grossValue * BigInt(feeBps)) / 10000n;
```

`convertToAssets(shares)` returns the **gross** value. Actual withdrawal proceeds are `grossValue * (10000 - withdrawFee) / 10000`.

### Reading Supply Rate (APR)

**TypeScript**

```typescript
// using pool from Setup section
const RAY = 10n ** 27n;
const supplyRateRay = await pool.supplyRate();
const supplyAPR = Number(supplyRateRay * 10000n / RAY) / 100;
// e.g., 5.25 means 5.25% annualized (APR — no compounding)
```

`supplyRate()` is an **instantaneous** spot rate. (FACT-033) It changes on every deposit, withdrawal, borrow, or repayment. Do not display it as a guaranteed yield.

**Solidity**

```solidity
// Inside a contract inheriting PoolIntegration from Setup
function getSupplyAPR() external view returns (uint256 rateRay) {
    rateRay = pool.supplyRate();
    // Returns RAY (1e27). Divide by 1e25 off-chain for percentage.
}
```

### Exchange Rate (Diesel Rate)

The exchange rate is `totalAssets() / totalSupply()` — how many underlying tokens one dToken is worth. It increases as borrowers pay interest. Some pool versions expose `dieselRate()` directly (returns RAY, 1e27).

### Yield Composition

| Source | Description | Effect on exchange rate |
|--------|-------------|------------------------|
| Base interest | Borrowers pay interest on debt; rate from IRM based on utilization (FACT-043) | Increases `totalAssets` |
| Quota revenue | Borrowers pay annual fees for holding specific collateral; rate set by gauge (FACT-043) | Increases `totalAssets` via PoolQuotaKeeper (FACT-040) |
| Liquidation profit | Surplus from profitable liquidations goes to treasury as shares | Indirect — treasury holds shares |
| Bad debt (loss) | Liquidation shortfall reduces `totalAssets` | **Decreases** exchange rate |

---

## Withdraw

Retrieve underlying tokens from the pool by burning dTokens.

### Method Variants

| Method | Description | When to use |
|--------|-------------|-------------|
| `withdraw(uint256 assets, address receiver, address owner)` | Specify exact underlying amount to receive (FACT-031) | "Withdraw exactly 500 USDC" |
| `redeem(uint256 shares, address receiver, address owner)` | Specify exact shares to burn (FACT-032) | "Exit my full position" — pass full balance |

### Step 1: Identify

Check available liquidity and withdrawal limits before building the transaction.

**Pre-conditions:**

- ✅ Pool is not paused
- ✅ Amount > 0
- ✅ `owner` has sufficient shares
- ✅ If `msg.sender != owner`: dToken allowance granted (allowance on the pool contract, not the underlying)
- ✅ Pool has sufficient `availableLiquidity()` (FACT-035) — capital lent to Credit Accounts is not available

**TypeScript**

```typescript
// using pool from Setup section
const totalShares = await pool.balanceOf(accountAddress);
const maxRedeemable = await pool.maxRedeem(accountAddress);
const maxWithdrawable = await pool.maxWithdraw(accountAddress);
const liquidity = await pool.availableLiquidity();
```

`maxRedeem` / `maxWithdraw` account for both share balance and available liquidity. If `maxRedeemable < totalShares`, the pool has insufficient liquidity for a full exit.

**Solidity**

```solidity
// Inside a contract inheriting PoolIntegration from Setup
function withdrawalLimits(address owner) external view returns (uint256 maxShares, uint256 maxAssets) {
    maxShares = pool.maxRedeem(owner);
    maxAssets = pool.maxWithdraw(owner);
}
```

### Step 2: Prepare

Choose between `withdraw` (exact assets out) or `redeem` (exact shares burned).

For a full exit, use `redeem` with `maxRedeem(owner)`:

```typescript
// using pool from Setup section
const sharesToRedeem = await pool.maxRedeem(accountAddress);
const expectedAssets = await pool.convertToAssets(sharesToRedeem);
// expectedAssets is gross — actual received is net of withdrawal fee
```

For a specific amount, use `withdraw`:

```typescript
// using pool from Setup section
const desiredAssets = 500_000000n; // 500 USDC
const maxAmount = await pool.maxWithdraw(accountAddress);
if (desiredAssets > maxAmount) {
  throw new Error(`Requested ${desiredAssets} exceeds max ${maxAmount}`);
}
```

### Step 3: Execute

**Full exit via `redeem`:**

**TypeScript**

```typescript
// using poolWrite from Setup section
const shares = await pool.maxRedeem(accountAddress);
const tx = await poolWrite.redeem(shares, accountAddress, accountAddress);
const receipt = await tx.wait();
```

**Solidity**

```solidity
// Inside a contract inheriting PoolIntegration from Setup
function redeemAll() external returns (uint256 assets) {
    uint256 shares = pool.maxRedeem(address(this));
    assets = pool.redeem(shares, address(this), address(this));
}
```

**Exact amount via `withdraw`:**

**TypeScript**

```typescript
// using poolWrite from Setup section
const tx = await poolWrite.withdraw(500_000000n, accountAddress, accountAddress);
const receipt = await tx.wait();
```

**Solidity**

```solidity
// Inside a contract inheriting PoolIntegration from Setup
function withdrawExact(uint256 amount) external returns (uint256 sharesBurned) {
    sharesBurned = pool.withdraw(amount, address(this), address(this));
}
```

**Events emitted:** `Withdraw(address indexed sender, address indexed receiver, address indexed owner, uint256 assets, uint256 shares)` (FACT-036)

**Error cases:**

| Condition | Revert |
|-----------|--------|
| `assets == 0` or `shares == 0` | `AmountCantBeZeroException` |
| `receiver == address(0)` | `ZeroAddressException` |
| Pool is paused | Pausable revert |
| Insufficient shares | ERC-20 `burn exceeds balance` |
| Insufficient pool liquidity | `transfer` revert (underlying balance too low) |
| `msg.sender != owner` without dToken allowance | ERC-20 allowance revert |

### Withdrawal Fee

`withdrawFee()` returns a `uint16` in basis points. The fee is applied automatically — `redeem` returns fewer assets, `withdraw` burns more shares. The fee is minted as shares to the treasury.

### Lock-up

Standard PoolV3 has **no lock-up**. Deposits and withdrawals can occur in the same block. On-demand liquidity pools (a separate contract) may have fixed terms, expiry, and KYC requirements.

---

## Monitoring Events

Subscribe to on-chain events for real-time pool activity tracking.

### Event Reference

| Event | Emitted when | Key fields |
|-------|-------------|------------|
| `Deposit(sender, owner, assets, shares)` | `deposit` or `mint` called | `sender` = msg.sender, `owner` = receiver (FACT-036) |
| `Withdraw(sender, receiver, owner, assets, shares)` | `withdraw` or `redeem` called | `assets` is net of withdrawal fee (FACT-036) |
| `Borrow(creditManager, creditAccount, amount)` | Credit Manager borrows from pool | Utilization increased (FACT-036) |
| `Repay(creditManager, repaidAmount, profit, loss)` | Credit Manager repays | `loss > 0` = bad debt event (FACT-036) |

### Live Event Listener

```typescript
// using pool from Setup section
pool.on("Deposit", (sender, owner, assets, shares) => {
  console.log(`Deposit: ${assets} assets → ${shares} shares`);
});

pool.on("Repay", (cm, repaid, profit, loss) => {
  if (loss > 0n) console.warn(`Bad debt: ${loss} loss from CM ${cm}`);
});
```

### Query Historical Events

```typescript
// using pool from Setup section
const deposits = await pool.queryFilter(pool.filters.Deposit(), fromBlock, "latest");
const parsed = deposits.map((e) => ({
  block: e.blockNumber,
  tx: e.transactionHash,
  assets: e.args.assets,
  shares: e.args.shares,
}));
```

---

## Gotchas

### 1. Exchange Rate Can Decrease

The diesel rate (`totalAssets / totalSupply`) increases when borrowers pay interest. It **decreases** when bad debt occurs — when a liquidation shortfall exceeds the treasury's share buffer. The pool calls `repayCreditAccount` with a `loss` parameter; if the treasury cannot cover it, the loss is socialized across all LPs. An `IncurUncoveredLoss` event is emitted.

### 2. `supplyRate()` Is a Spot Rate

The value reflects current utilization and quota revenue at the moment of the call. (FACT-033) Every `deposit`, `withdraw`, `lendCreditAccount`, or `repayCreditAccount` changes utilization, which changes the rate. Do not display it as a fixed APR.

### 3. Dead Shares Exist at Deployment

The pool mints `1e5` (100,000) shares to `address(0)` during construction — standard ERC-4626 inflation attack mitigation. (FACT-037) Consequences:
- `totalSupply()` is never zero after deployment
- The first depositor does not receive shares at 1:1
- Division-by-zero in exchange rate math is impossible

### 4. Withdrawal Fee Reduces Realized Returns

`convertToAssets(shares)` returns the **gross** value. Actual proceeds are lower by `withdrawFee()` basis points. Use `previewRedeem(shares)` for the net value. The fee is minted as new shares to the treasury, marginally diluting remaining LPs.

### 5. Multiple Credit Managers Per Pool

A single pool can serve multiple Credit Managers, each with independent debt limits. (FACT-002) Total utilization is the sum across all CMs. Query `creditManagers()` or the MarketCompressor for the full list.

### 6. Available Liquidity ≠ Total Assets

`availableLiquidity()` returns the **actual ERC-20 balance** in the pool contract. (FACT-035) `totalAssets()` includes outstanding debt plus accrued interest. When utilization is high, `availableLiquidity()` can be a small fraction of `totalAssets()`, limiting withdrawal capacity.

### 7. `maxDeposit` Returns Max or Zero

`maxDeposit(address)` returns `type(uint256).max` when active, `0` when paused. No intermediate values. Pool capacity, if any, is enforced through debt limits on the borrowing side, not on deposits.

### 8. Interest Accrual Is Lazy

The exchange rate is recalculated on-demand via a cumulative index (`_baseInterestIndexLU`) when state-changing functions are called. Between state changes, `totalAssets()` and `convertToAssets()` still return correct values — view functions compute accrued interest using `block.timestamp - lastBaseInterestUpdate`.

### 9. On-Demand Pools Are a Different Contract

On-demand liquidity pools (institutional lending with fixed rates, expiry, KYC) are a separate contract type, not PoolV3. They share interface similarities but have different mechanics for deposits, lock-ups, and rate determination.

### 10. Approval Target Is the Pool Itself

The ERC-20 `approve` for the underlying must target the pool address — the pool pulls tokens via `transferFrom` during `deposit`/`mint`. The pool contract IS the dToken. When calling `withdraw`/`redeem` on behalf of another address (`owner != msg.sender`), the required allowance is on the **dToken** (pool contract), not the underlying.

---

**Related:** [Borrowing: Credit Account Lifecycle →](./02-borrowing.md) · [Strategies & Adapters →](./03-strategies.md) · [Liquidation →](./04-liquidation.md) · [PoolV3.sol](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/pool/PoolV3.sol)
