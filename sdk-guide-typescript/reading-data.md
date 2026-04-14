# Reading Data

Query market state, pool data, and credit account information using the SDK.

> For Solidity pool operations, see [Pool Operations](../solidity-guide/pool-operations.md).

## Market Data via marketRegister

The `marketRegister` provides cached access to all Gearbox markets:

```typescript
import { GearboxSDK } from '@gearbox-protocol/sdk';

const sdk = await GearboxSDK.attach({ client, marketConfigurators: [] });

// All markets
const markets = sdk.marketRegister.markets;

// Find specific market
const market = sdk.marketRegister.findByPool(poolAddress);
// or
const market = sdk.marketRegister.findByCreditManager(cmAddress);

// Access market components
console.log(`Pool: ${market.pool.address}`);
console.log(`Available liquidity: ${market.pool.availableLiquidity}`);
console.log(`Diesel rate: ${market.pool.dieselRate}`);
console.log(`Supply rate: ${market.pool.supplyRate}`);
console.log(`Credit managers: ${market.creditManagers.length}`);
```

## Pool State

Access pool data through the market object:

```typescript
const market = sdk.marketRegister.findByPool(poolAddress);
const pool = market.pool;

// Core metrics
console.log(`Underlying: ${pool.underlying.symbol}`);
console.log(`Total assets: ${pool.totalAssets}`);
console.log(`Available liquidity: ${pool.availableLiquidity}`);

// Interest rates (RAY = 27 decimals)
const RAY = 10n ** 27n;
const supplyAPY = Number(pool.supplyRate * 10000n / RAY) / 100;
const borrowAPR = Number(pool.baseInterestRate * 10000n / RAY) / 100;
console.log(`Supply APY: ${supplyAPY}%`);
console.log(`Borrow APR: ${borrowAPR}%`);

// Share price
const dieselRate = pool.dieselRate;
console.log(`Diesel rate: ${dieselRate}`);
```

## Credit Manager Data

Access credit manager configuration:

```typescript
const market = sdk.marketRegister.findByCreditManager(cmAddress);

for (const cm of market.creditManagers) {
  console.log(`Credit Manager: ${cm.address}`);
  console.log(`Credit Facade: ${cm.creditFacade}`);

  // Debt limits
  console.log(`Min debt: ${cm.minDebt}`);
  console.log(`Max debt: ${cm.maxDebt}`);

  // Allowed tokens
  for (const token of cm.collateralTokens) {
    console.log(`  ${token.symbol}: LT ${token.liquidationThreshold}`);
  }
}
```

## Real-Time Data via Compressors

The SDK caches data on initialization. For real-time data, use compressors directly:

```typescript
import {
  GearboxSDK,
  marketCompressorAbi,
  AP_MARKET_COMPRESSOR,
  VERSION_RANGE_310,
} from '@gearbox-protocol/sdk';

const sdk = await GearboxSDK.attach({ client, marketConfigurators: [] });

// Get compressor address
const [compressor] = sdk.addressProvider.mustGetLatest(
  AP_MARKET_COMPRESSOR,
  VERSION_RANGE_310
);

// Fetch fresh market data
const freshData = await client.readContract({
  address: compressor,
  abi: marketCompressorAbi,
  functionName: 'getMarketData',
  args: [poolAddress],
});

console.log(`Fresh available liquidity: ${freshData.pool.availableLiquidity}`);
```

## Filtering Markets

Query markets by criteria:

```typescript
// All USDC markets
const usdcMarkets = sdk.marketRegister.markets.filter(
  m => m.pool.underlying.symbol === 'USDC'
);

// Markets with high liquidity
const liquidMarkets = sdk.marketRegister.markets.filter(
  m => m.pool.availableLiquidity > 1_000_000n * 10n ** 6n // > 1M
);

// Markets by configurator
const curatedMarkets = sdk.marketRegister.markets.filter(
  m => m.configurator === curatorAddress
);
```

## Price Oracle Data

Access price information through the market:

```typescript
const market = sdk.marketRegister.findByCreditManager(cmAddress);

// Price oracle address
const priceOracle = market.priceOracle;

// Token prices are available through market data
for (const token of market.tokens) {
  console.log(`${token.symbol}: ${token.price} USD`);
}
```

## Complete Example

```typescript
import { GearboxSDK } from '@gearbox-protocol/sdk';
import { createPublicClient, http } from 'viem';
import { mainnet } from 'viem/chains';

async function getMarketOverview() {
  const client = createPublicClient({
    chain: mainnet,
    transport: http(),
  });

  const sdk = await GearboxSDK.attach({
    client,
    marketConfigurators: [],
  });

  const RAY = 10n ** 27n;

  for (const market of sdk.marketRegister.markets) {
    const pool = market.pool;

    console.log(`\n=== ${pool.underlying.symbol} Market ===`);
    console.log(`Pool: ${pool.address}`);
    console.log(`Total assets: ${pool.totalAssets}`);
    console.log(`Available: ${pool.availableLiquidity}`);

    const supplyAPY = Number(pool.supplyRate * 10000n / RAY) / 100;
    console.log(`Supply APY: ${supplyAPY.toFixed(2)}%`);

    console.log(`Credit Managers: ${market.creditManagers.length}`);
  }
}

getMarketOverview().catch(console.error);
```

## Next Steps

* [Credit Accounts](credit-accounts.md) - Query and manage credit accounts
* [Multicalls](multicalls/) - Build and execute multicalls

For architectural background, see [Pool Architecture](../concepts/pools.md).
