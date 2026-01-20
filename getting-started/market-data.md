# Market Data

Fetch complete market state with a single call using MarketCompressor.

## Why MarketCompressor

MarketCompressor aggregates the state of all market components into a single RPC call. Instead of querying dozens of contracts individually, get a structured `MarketData` response.

Benefits:
- Single call for complete market state
- Avoids rate limiting on RPC providers
- Consistent snapshot across all fields
- Typed return data for easy parsing

---

## Core Methods

### Get Single Market

```solidity
function getMarketData(address pool) external view returns (MarketData memory);
```

Returns complete state for a specific pool and its connected credit infrastructure.

### Get Multiple Markets

```solidity
function getMarkets(MarketFilter memory filter) external view returns (MarketData[] memory);
```

Returns filtered markets by underlying token or configurator.

---

## Usage

### Solidity

```solidity
import {IMarketCompressor} from "@gearbox-protocol/periphery-v3/contracts/interfaces/IMarketCompressor.sol";
import {MarketData, MarketFilter} from "@gearbox-protocol/periphery-v3/contracts/types/MarketData.sol";

IMarketCompressor compressor = IMarketCompressor(MARKET_COMPRESSOR_ADDRESS);

// Get single market
MarketData memory data = compressor.getMarketData(poolAddress);

// Get all USDC markets
MarketFilter memory filter = MarketFilter({
    underlying: USDC,
    configurators: new address[](0)  // empty = all configurators
});
MarketData[] memory usdcMarkets = compressor.getMarkets(filter);
```

### TypeScript (viem)

```typescript
import { getContract } from 'viem';
import { marketCompressorAbi } from '@gearbox-protocol/sdk';

const marketCompressor = getContract({
  address: MARKET_COMPRESSOR_ADDRESS,
  abi: marketCompressorAbi,
  client: publicClient,
});

// Get single market
const marketData = await marketCompressor.read.getMarketData([poolAddress]);

console.log(`Pool: ${marketData.pool.name}`);
console.log(`Configurator: ${marketData.configurator}`);
console.log(`Credit Managers: ${marketData.creditManagers.length}`);

// Get all USDC markets
const usdcMarkets = await marketCompressor.read.getMarkets([{
  underlying: USDC_ADDRESS,
  configurators: [],
}]);
```

---

## MarketFilter

Filter markets by criteria:

```solidity
struct MarketFilter {
    address underlying;       // Filter by underlying token (0x0 = all)
    address[] configurators;  // Filter by configurators (empty = all)
}
```

### Examples

```solidity
// All markets
MarketFilter memory all = MarketFilter({
    underlying: address(0),
    configurators: new address[](0)
});

// All WETH markets
MarketFilter memory weth = MarketFilter({
    underlying: WETH,
    configurators: new address[](0)
});

// Markets from specific configurator
address[] memory configs = new address[](1);
configs[0] = myConfigurator;
MarketFilter memory byConfig = MarketFilter({
    underlying: address(0),
    configurators: configs
});
```

---

## MarketData Struct

The `MarketData` struct contains the complete state of a Gearbox market. See the [Market Overview](../README.md#understanding-marketdata) for the full field reference table.

Key fields:

| Field | Type | Description |
|-------|------|-------------|
| `pool` | `PoolData` | Core lending pool state |
| `quotaKeeper` | `address` | Quota management contract |
| `interestRateModel` | `address` | IRM contract address |
| `priceOracle` | `address` | Price oracle router |
| `creditManagers` | `CreditSuiteData[]` | All connected credit managers |
| `tokens` | `TokenData[]` | Supported collateral tokens |
| `configurator` | `address` | Market configurator |

### Accessing Nested Data

```typescript
const marketData = await marketCompressor.read.getMarketData([poolAddress]);

// Pool info
const underlying = marketData.pool.underlying;
const totalAssets = marketData.pool.totalAssets;
const availableLiquidity = marketData.pool.availableLiquidity;

// Credit managers
for (const cm of marketData.creditManagers) {
  console.log(`Credit Manager: ${cm.creditManager}`);
  console.log(`Facade: ${cm.creditFacade}`);
  console.log(`Max Debt: ${cm.maxDebt}`);
}

// Supported tokens
for (const token of marketData.tokens) {
  console.log(`Token: ${token.symbol} (${token.addr})`);
}
```

---

## Finding MarketCompressor Address

MarketCompressor is not in AddressProvider. Query it from the SDK or use known deployment addresses.

```typescript
import { MarketCompressor } from '@gearbox-protocol/sdk';

// SDK provides typed wrapper
const compressor = new MarketCompressor(publicClient, chainId);
const markets = await compressor.getMarkets({ underlying: USDC });
```

Or use direct address from [deployments repository](https://github.com/Gearbox-protocol/deployments).

---

## Next Steps

- [Contract Discovery](contract-discovery.md) - Find other protocol contracts
- [Credit Suite Overview](../core/credit-suite.md) - Deep dive into credit infrastructure
- [Pool V3](../core/poolv3-the-liquidity-hub.md) - Lending pool mechanics

## Conceptual Background

For the architectural design behind markets, see:

- [Credit Suite Architecture](../../new-docs-about/core-architecture/credit-suite.md)
