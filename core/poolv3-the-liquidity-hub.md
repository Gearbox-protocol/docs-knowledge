# PoolV3: The Liquidity Hub

The `PoolV3` is the central vault for a specific underlying asset (e.g., USDC, WETH). It adheres to the [**ERC-4626**](https://docs.openzeppelin.com/contracts/4.x/erc4626) standard, allowing users to deposit assets and receive **Diesel Tokens** (LP tokens, e.g., dUSDC) representing their share of the pool.

Unlike standard lending protocols, users **do not borrow directly** from the pool. Instead, whitelisted **Credit Managers** borrow liquidity on behalf of Credit Accounts to execute leveraged strategies.

## ERC-4626 Compliance

Pool V3 implements the full ERC-4626 tokenized vault standard. This means any tooling built for ERC-4626 vaults works with Gearbox pools out of the box.

**Standard ERC-4626 Functions:**

| Function | Purpose |
|----------|---------|
| `deposit(assets, receiver)` | Deposit underlying, receive shares |
| `mint(shares, receiver)` | Mint exact shares, deposit required assets |
| `withdraw(assets, receiver, owner)` | Withdraw exact assets, burn shares |
| `redeem(shares, receiver, owner)` | Burn exact shares, receive assets |
| `convertToShares(assets)` | Preview shares for asset amount |
| `convertToAssets(shares)` | Preview assets for share amount |
| `maxDeposit(receiver)` | Maximum depositable assets |
| `maxWithdraw(owner)` | Maximum withdrawable assets |

**Gearbox Extensions:**

Beyond ERC-4626, Pool V3 adds:

* `depositWithReferral`: On-chain referral tracking
* `lendCreditAccount` / `repayCreditAccount`: Credit Manager-only borrowing interface
* `dieselRate()`: Share price in RAY (27 decimals) for precision

### Diesel Rate (Share Price)

The `dieselRate` represents how many underlying tokens each diesel token (share) is worth. It starts at 1 RAY (`10^27`) and increases as interest accrues.

```solidity
// Get current share price (in RAY)
uint256 rate = pool.dieselRate();

// Equivalent to ERC-4626 convertToAssets but in RAY precision
// 1 diesel token = rate / 10^27 underlying tokens
```

```typescript
// TypeScript: Reading share price
const dieselRate = await pool.read.dieselRate();

// Convert using ERC-4626 standard functions
const assetsPerShare = await pool.read.convertToAssets([10n ** 18n]); // 1 share in assets
const sharesPerAsset = await pool.read.convertToShares([10n ** 18n]); // 1 asset in shares
```

## Core State & Address Discovery

Each pool is immutable regarding its underlying asset.

| Parameter         | Description                                                                                            |
| ----------------- | ------------------------------------------------------------------------------------------------------ |
| **Underlying**    | The asset held by the pool (e.g., USDC).                                                               |
| **Diesel Token**  | The ERC-20 LP token minted to lenders (e.g., dUSDC). Address of Diesel token is pool's address itself. |
| **Contract Type** | Returns `"POOL"` (or `"POOL::USDT"` for the USDT variant).                                             |

### **Contract Address Discovery (MarketCompressor)**

For developers, the **MarketCompressor** (from the `periphery-v3` repository) is the most efficient discovery tool. It allows you to find pools and fetch their entire state (limits, utilization, connected managers) in a single RPC call using the `getMarkets` method and a `MarketFilter`.

```solidity
struct MarketFilter {
    address[] configurators; // Filter by specific Risk Curators
    address[] pools;          // Lookup specific pool addresses
    address underlying;      // Find the pool for a specific token (e.g., USDC)
}

// Example: Finding the USDC pool address and its data
MarketFilter memory filter;
filter.underlying = 0xA0b8...; // USDC Address

MarketData[] memory results = marketCompressor.getMarkets(filter);
address poolAddr = results[0].pool.baseParams.addr;
```

### **Checking Pool Properties**

Once you have an address, you can verify its core properties directly:

```solidity
// Example: Checking pool properties
IPoolV3 pool = IPoolV3(poolAddr);

address asset = pool.asset();           // Underlying (e.g., USDC)
string memory name = pool.name();       // e.g., "diesel USDC"
string memory symbol = pool.symbol();   // e.g., "dUSDC"
uint8 decimals = pool.decimals();       // Matches underlying decimals
```

***

## Transact with a pool

### Lending (Entry Flows)

Lenders provide liquidity to earn passive yield. This yield comes from two sources:

1. **Base Interest:** Paid by borrowers on the principal debt.
2. **Quota Revenue:** Paid by borrowers for the right to hold specific collateral tokens.

#### Deposit

Deposits `assets` amount of underlying tokens and mints shares to `receiver`.

```solidity
function deposit(uint256 assets, address receiver) external returns (uint256 shares);
```

```typescript
// TypeScript: Deposit to pool
import { getContract } from 'viem';

const pool = getContract({
  address: poolAddress,
  abi: poolV3Abi,
  client: walletClient,
});

// Approve underlying first
await underlying.write.approve([poolAddress, assets]);

// Deposit and receive shares
const shares = await pool.write.deposit([assets, receiverAddress]);

// Preview how many shares you'd receive
const expectedShares = await pool.read.previewDeposit([assets]);
```

* **Pause State:** Reverts if the pool is paused.

#### Deposit with Referral

Gearbox V3 supports on-chain referral tracking. This emits a `Refer` event which can be indexed by off-chain reward systems.

```solidity
function depositWithReferral(
    uint256 assets,
    address receiver,
    uint256 referralCode
) external returns (uint256 shares);
```

```typescript
// TypeScript: Deposit with referral code
const shares = await pool.write.depositWithReferral([
  assets,
  receiverAddress,
  123n, // referralCode
]);
```

### Withdrawal (Exit Flows)

Withdrawals in Gearbox V3 are subject to a **Withdrawal Fee**. This fee is taken from the _interest earned_, effectively keeping the capital principal intact if possible, but computationally it acts as a reduction in the underlying returned.

#### Redeem

Burns a specific amount of `shares` and sends the resulting assets to the `receiver`.

```solidity
function redeem(
    uint256 shares,
    address receiver,
    address owner
) external returns (uint256 assets);
```

```typescript
// TypeScript: Redeem shares for underlying assets
const assets = await pool.write.redeem([
  shares,
  receiverAddress,
  ownerAddress,
]);

// Preview how many assets you'd receive
const expectedAssets = await pool.read.previewRedeem([shares]);
```

#### Withdraw

Withdraws exact `assets` amount, burning the required shares.

```solidity
function withdraw(
    uint256 assets,
    address receiver,
    address owner
) external returns (uint256 shares);
```

```typescript
// TypeScript: Withdraw exact asset amount
const sharesBurned = await pool.write.withdraw([
  assets,
  receiverAddress,
  ownerAddress,
]);
```

**Pause State:** Reverts if the pool is paused.

***

### Credit Manager Interaction

Only whitelisted Credit Managers can borrow from the pool. Regular users cannot call these functions directly.

```solidity
// Credit Manager borrows from pool (CM-only)
function lendCreditAccount(uint256 borrowedAmount, address creditAccount) external;

// Credit Manager repays to pool (CM-only)
function repayCreditAccount(uint256 repaidAmount, uint256 profit, uint256 loss) external;
```

This separation ensures that all borrowed funds flow through Credit Accounts with proper collateral checks.

### Reading Pool State

**Using the SDK (Recommended):**

```typescript
import { GearboxSDK } from '@gearbox-protocol/sdk';

const sdk = await GearboxSDK.attach({ client, marketConfigurators: [] });

// Get pool data via market register
const market = sdk.marketRegister.findByPool(poolAddress);

// Pool state from market register (cached from compressor)
const poolState = market.pool;
console.log(poolState.availableLiquidity);
console.log(poolState.dieselRate);
console.log(poolState.supplyRate);
console.log(poolState.baseInterestRate);

// Or use MarketCompressor directly for real-time data
import { marketCompressorAbi, AP_MARKET_COMPRESSOR } from '@gearbox-protocol/sdk';

const [compressor] = sdk.addressProvider.mustGetLatest(AP_MARKET_COMPRESSOR, VERSION_RANGE_310);
const freshState = await client.readContract({
  address: compressor,
  abi: marketCompressorAbi,
  functionName: 'getPoolState',
  args: [poolAddress],
});
```

**Using raw viem:**

```typescript
// TypeScript: Reading pool state
const underlying = await pool.read.asset();
const totalAssets = await pool.read.totalAssets();
const totalSupply = await pool.read.totalSupply();

// Interest rates (in RAY - 27 decimals)
const supplyRate = await pool.read.supplyRate();   // APY for lenders
const borrowRate = await pool.read.baseInterestRate(); // APR for borrowers

// Calculate utilization
const availableLiquidity = await pool.read.availableLiquidity();
const utilization = (totalAssets - availableLiquidity) * 10000n / totalAssets;
```

> For how interest rates are calculated based on utilization, see [Interest Rate Model](./interest-rate-model.md).

<details>

<summary>Sources</summary>

* [contracts/pool/PoolV3.sol](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/pool/PoolV3.sol)
* [contracts/pool/PoolV3\_USDT.sol](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/pool/PoolV3_USDT.sol)
* [contracts/interfaces/IPoolV3.sol](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/interfaces/IPoolV3.sol)

</details>
