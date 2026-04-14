# Frontend Applications

Build dashboards, portfolio trackers, and trading UIs that display Gearbox protocol data and let users manage positions.

## Overview

Frontend applications typically need to:

1. Display pool and market data
2. Show collateral exposure and limits
3. Monitor credit account health
4. Enable position management

This guide maps each requirement to specific SDK methods.

***

## Pool Display

**WHY:** Users want to see pool health, yields, and utilization before depositing or borrowing.

### Data Requirements

| Display             | SDK Source    | Field                                              |
| ------------------- | ------------- | -------------------------------------------------- |
| Underlying token    | `market.pool` | `underlying.symbol`, `underlying.address`          |
| Total supplied      | `market.pool` | `totalAssets`                                      |
| Available liquidity | `market.pool` | `availableLiquidity`                               |
| Utilization         | Calculated    | `(totalAssets - availableLiquidity) / totalAssets` |
| Supply APY          | `market.pool` | `supplyRate` (RAY scaled)                          |
| Borrow APR          | `market.pool` | `baseInterestRate` (RAY scaled)                    |
| Share price         | `market.pool` | `dieselRate` (RAY scaled)                          |

### How to Fetch

```typescript
import { GearboxSDK } from '@gearbox-protocol/sdk';

const sdk = await GearboxSDK.attach({ client, marketConfigurators: [] });

// Find market by pool address
const market = sdk.marketRegister.findByPool(poolAddress);
const pool = market.pool;

// Display data
const RAY = 10n ** 27n;

console.log(`Underlying: ${pool.underlying.symbol}`);
console.log(`Total Supplied: ${pool.totalAssets}`);
console.log(`Available: ${pool.availableLiquidity}`);

// Calculate utilization
const borrowed = pool.totalAssets - pool.availableLiquidity;
const utilization = Number(borrowed * 10000n / pool.totalAssets) / 100;
console.log(`Utilization: ${utilization.toFixed(2)}%`);

// Convert RAY rates to percentages
const supplyAPY = Number(pool.supplyRate * 10000n / RAY) / 100;
const borrowAPR = Number(pool.baseInterestRate * 10000n / RAY) / 100;
console.log(`Supply APY: ${supplyAPY.toFixed(2)}%`);
console.log(`Borrow APR: ${borrowAPR.toFixed(2)}%`);
```

### Where Data Comes From

The SDK caches market data on initialization via `GearboxSDK.attach()`. This data comes from the `MarketCompressor` contract. For real-time updates, either:

* Re-initialize the SDK periodically
* Call compressors directly (see [Real-Time Updates](frontend-applications.md#real-time-updates))

***

## Collateral Exposure

**WHY:** Users want to see what collaterals the pool is exposed to and current utilization against limits.

### Data Requirements

| Display               | SDK Source               | Field               |
| --------------------- | ------------------------ | ------------------- |
| Quoted tokens         | `MarketData.quotaKeeper` | `tokens[]`          |
| Token quota limit     | `quotaKeeper.tokens[]`   | `limit`             |
| Current quoted amount | `quotaKeeper.tokens[]`   | `totalQuoted`       |
| Quota rate            | `quotaKeeper.tokens[]`   | `rate` (RAY scaled) |

### How to Fetch

For quota data, use the `MarketCompressor` directly:

```typescript
import {
  marketCompressorAbi,
  AP_MARKET_COMPRESSOR,
  VERSION_RANGE_310,
} from '@gearbox-protocol/sdk';

// Get compressor address
const [compressor] = sdk.addressProvider.mustGetLatest(
  AP_MARKET_COMPRESSOR,
  VERSION_RANGE_310
);

// Fetch market data with quota keeper
const marketData = await client.readContract({
  address: compressor,
  abi: marketCompressorAbi,
  functionName: 'getMarketData',
  args: [poolAddress],
});

// QuotaKeeper token data
for (const token of marketData.quotaKeeper.tokens) {
  const utilizationPct = Number(token.totalQuoted * 10000n / token.limit) / 100;

  console.log(`Token: ${token.token}`);
  console.log(`  Limit: ${token.limit}`);
  console.log(`  Quoted: ${token.totalQuoted}`);
  console.log(`  Utilization: ${utilizationPct.toFixed(2)}%`);
  console.log(`  Rate: ${token.rate}`); // RAY scaled
}
```

### Gotcha: Quota Limits

Before letting users open positions with a specific collateral, check that `totalQuoted < limit`. If the limit is reached, new positions with that collateral will fail.

***

## Credit Manager Configuration

**WHY:** Users need to know debt limits, collateral requirements, and fees before opening positions.

### Data Requirements

| Display               | SDK Source           | Field                                 |
| --------------------- | -------------------- | ------------------------------------- |
| Min debt              | `creditManager`      | `minDebt`                             |
| Max debt              | `creditManager`      | `maxDebt`                             |
| Collateral tokens     | `creditManager`      | `collateralTokens[]`                  |
| Liquidation threshold | `collateralTokens[]` | `liquidationThreshold` (basis points) |
| Fees                  | `creditManager`      | `fees`                                |
| Liquidation premium   | `creditManager`      | `liquidationPremium`                  |

### How to Fetch

```typescript
const market = sdk.marketRegister.findByCreditManager(cmAddress);

for (const cm of market.creditManagers) {
  console.log(`Credit Manager: ${cm.address}`);
  console.log(`Credit Facade: ${cm.creditFacade}`);

  // Debt limits
  console.log(`Min Debt: ${cm.minDebt}`);
  console.log(`Max Debt: ${cm.maxDebt}`);

  // Collateral configuration
  console.log('Allowed Collaterals:');
  for (const token of cm.collateralTokens) {
    // LT is in basis points (10000 = 100%)
    const ltPct = Number(token.liquidationThreshold) / 100;
    console.log(`  ${token.symbol}: LT ${ltPct.toFixed(1)}%`);
  }
}
```

### Understanding Liquidation Threshold

The liquidation threshold (LT) determines how much each collateral contributes to the weighted collateral value:

```
Weighted Value = Token Balance * Token Price * LT
Health Factor = Total Weighted Value / Total Debt
```

A lower LT means the protocol values that collateral more conservatively.

***

## Credit Account Monitoring

**WHY:** Users need to track their position health, collateral values, and accrued interest.

### Data Requirements

| Display          | SDK Source          | Field                        |
| ---------------- | ------------------- | ---------------------------- |
| Account address  | `CreditAccountData` | `addr`                       |
| Owner            | `CreditAccountData` | `owner`                      |
| Total debt       | `CreditAccountData` | `debt`                       |
| Health factor    | `CreditAccountData` | `healthFactor` (10000 = 1.0) |
| Is liquidatable  | `CreditAccountData` | `isLiquidatable`             |
| Token balances   | `CreditAccountData` | `tokens[]`                   |
| Token values     | `tokens[]`          | `balanceInUnderlying`        |
| Accrued interest | `CreditAccountData` | `cumulativeQuotaInterest`    |
| Quota fees       | `CreditAccountData` | `quotaFees`                  |

### How to Fetch

```typescript
import { createCreditAccountService } from '@gearbox-protocol/sdk';

const service = createCreditAccountService(sdk, 310);

// Get user's accounts
const accounts = await service.getCreditAccounts(
  {
    creditManager: cmAddress,
    owner: userAddress,
  },
  sdk.currentBlock
);

for (const account of accounts) {
  // Health factor: 10000 = 1.0
  const hf = Number(account.healthFactor) / 10000;

  console.log(`Account: ${account.addr}`);
  console.log(`Health Factor: ${hf.toFixed(4)}`);
  console.log(`Liquidatable: ${account.isLiquidatable}`);

  // Debt breakdown
  console.log(`Total Debt: ${account.debt}`);
  console.log(`Accrued Interest: ${account.cumulativeQuotaInterest}`);
  console.log(`Quota Fees: ${account.quotaFees}`);

  // Token positions
  console.log('Positions:');
  for (const token of account.tokens) {
    if (token.balance > 0n) {
      console.log(`  ${token.symbol}:`);
      console.log(`    Balance: ${token.balance}`);
      console.log(`    Value (underlying): ${token.balanceInUnderlying}`);
      console.log(`    LT: ${token.lt / 100}%`);
    }
  }
}
```

### Interest Breakdown

Credit account debt consists of:

* **Principal:** Original borrowed amount
* **Base interest:** Accrues on principal based on pool utilization
* **Quota interest:** Per-collateral rate for non-underlying tokens
* **Quota fees:** Fixed fee component for quotas

```typescript
// Total debt = principal + base interest + quota interest + quota fees
const principal = account.borrowedAmount;
const quotaInterest = account.cumulativeQuotaInterest;
const quotaFees = account.quotaFees;
const baseInterest = account.debt - principal - quotaInterest - quotaFees;
```

### Health Factor Thresholds

Display appropriate warnings based on health factor:

```typescript
function getHealthStatus(hf: number): string {
  if (hf < 1.0) return 'LIQUIDATABLE';
  if (hf < 1.05) return 'CRITICAL';
  if (hf < 1.1) return 'WARNING';
  return 'HEALTHY';
}

const status = getHealthStatus(Number(account.healthFactor) / 10000);
```

***

## Price Feed Information

**WHY:** Users want to understand which oracles determine their collateral values.

### How to Fetch

```typescript
import {
  priceFeedCompressorAbi,
  AP_PRICE_FEED_COMPRESSOR,
  VERSION_RANGE_310,
} from '@gearbox-protocol/sdk';

// Get price feed compressor
const [priceFeedCompressor] = sdk.addressProvider.mustGetLatest(
  AP_PRICE_FEED_COMPRESSOR,
  VERSION_RANGE_310
);

// Get all price feeds for a price oracle
const feeds = await client.readContract({
  address: priceFeedCompressor,
  abi: priceFeedCompressorAbi,
  functionName: 'getUpdatablePriceFeeds',
  args: [priceOracleAddress],
});

for (const feed of feeds) {
  console.log(`Token: ${feed.token}`);
  console.log(`  Feed: ${feed.priceFeed}`);
  console.log(`  Needs Update: ${feed.needsUpdate}`);
}
```

***

## Position Management

**WHY:** Users take actions on their positions (add collateral, borrow, repay, etc.).

### Linking to Operations

Position management uses multicalls. Link to the appropriate operation guide:

| User Action        | Operation Guide                                                              |
| ------------------ | ---------------------------------------------------------------------------- |
| Deposit collateral | [Adding Collateral](../multicalls/multicalls/adding-collateral.md)           |
| Borrow more        | [Debt Management](../multicalls/multicalls/debt-management.md)               |
| Repay debt         | [Debt Management](../multicalls/multicalls/debt-management.md)               |
| Update quota       | [Updating Quotas](../multicalls/multicalls/updating-quotas.md)               |
| Withdraw           | [Withdrawing Collateral](../multicalls/multicalls/withdrawing-collateral.md) |
| Swap collateral    | [Making External Calls](../multicalls/multicalls/making-external-calls.md)   |

### Pre-Operation Data Checks

Before letting users perform operations, validate:

```typescript
// Before addCollateral: Check token is allowed
const isAllowed = market.creditManagers[0].collateralTokens
  .some(t => t.address === tokenAddress);

// Before increaseDebt: Check against max debt
const newDebt = account.debt + borrowAmount;
const isWithinLimit = newDebt <= cm.maxDebt;

// Before updateQuota: Check quota capacity
const quotaToken = marketData.quotaKeeper.tokens
  .find(t => t.token === tokenAddress);
const hasCapacity = quotaToken && quotaToken.totalQuoted < quotaToken.limit;

// Before any operation: Estimate health factor impact
// (Use simulation or calculate locally)
```

***

## Real-Time Updates

**WHY:** UI needs to stay current as blockchain state changes.

### Option 1: Poll Compressors

For most dashboards, polling every few seconds is sufficient:

```typescript
const POLL_INTERVAL = 5000; // 5 seconds

async function pollMarketData() {
  const marketData = await client.readContract({
    address: compressor,
    abi: marketCompressorAbi,
    functionName: 'getMarketData',
    args: [poolAddress],
  });

  // Update UI state
  setPoolData(marketData.pool);
  setQuotaData(marketData.quotaKeeper);
}

// Start polling
setInterval(pollMarketData, POLL_INTERVAL);
```

### Option 2: Watch Events

For specific state changes, watch contract events:

```typescript
import { parseAbiItem } from 'viem';

// Watch for credit account state changes
const unwatch = client.watchContractEvent({
  address: creditManagerAddress,
  abi: creditManagerAbi,
  eventName: 'ExecuteOrder',
  onLogs: (logs) => {
    // Refresh account data for affected accounts
    for (const log of logs) {
      refreshAccountData(log.args.creditAccount);
    }
  },
});

// Cleanup on unmount
return () => unwatch();
```

### Recommendation

Use **polling** for:

* General market data
* Pool state (rates, liquidity)
* Quota utilization

Use **events** for:

* User's own account changes
* Critical health factor alerts

***

## Complete Example: Dashboard Component

```typescript
import { GearboxSDK, createCreditAccountService, marketCompressorAbi } from '@gearbox-protocol/sdk';
import { createPublicClient, http } from 'viem';
import { mainnet } from 'viem/chains';

interface DashboardData {
  pool: {
    underlying: string;
    totalAssets: bigint;
    availableLiquidity: bigint;
    supplyAPY: number;
    borrowAPR: number;
  };
  userAccounts: Array<{
    address: string;
    healthFactor: number;
    debt: bigint;
    isLiquidatable: boolean;
  }>;
}

async function fetchDashboardData(
  poolAddress: `0x${string}`,
  cmAddress: `0x${string}`,
  userAddress: `0x${string}`
): Promise<DashboardData> {
  const client = createPublicClient({
    chain: mainnet,
    transport: http(),
  });

  const sdk = await GearboxSDK.attach({
    client,
    marketConfigurators: [],
  });

  const RAY = 10n ** 27n;

  // Pool data
  const market = sdk.marketRegister.findByPool(poolAddress);
  const pool = market.pool;

  // User accounts
  const service = createCreditAccountService(sdk, 310);
  const accounts = await service.getCreditAccounts(
    { creditManager: cmAddress, owner: userAddress },
    sdk.currentBlock
  );

  return {
    pool: {
      underlying: pool.underlying.symbol,
      totalAssets: pool.totalAssets,
      availableLiquidity: pool.availableLiquidity,
      supplyAPY: Number(pool.supplyRate * 10000n / RAY) / 100,
      borrowAPR: Number(pool.baseInterestRate * 10000n / RAY) / 100,
    },
    userAccounts: accounts.map(a => ({
      address: a.addr,
      healthFactor: Number(a.healthFactor) / 10000,
      debt: a.debt,
      isLiquidatable: a.isLiquidatable,
    })),
  };
}
```

***

## Next Steps

* [Multicall Operations](../multicalls/multicalls/) - Implement position management
* [Backend Services](backend-services.md) - If you also need historical data
* [Compressors Reference](../../utilities/compressors.md) - Complete compressor API
