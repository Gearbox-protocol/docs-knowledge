# SDK Setup

Install and initialize the Gearbox SDK for TypeScript development.

> For Solidity contract discovery, see [Contract Discovery](../solidity-guide/discovery.md).

## Installation

```typescript
npm install @gearbox-protocol/sdk viem
```

## SDK Initialization

```typescript
import { GearboxSDK } from '@gearbox-protocol/sdk';
import { createPublicClient, http } from 'viem';
import { mainnet } from 'viem/chains';

const client = createPublicClient({
  chain: mainnet,
  transport: http(),
});

const sdk = await GearboxSDK.attach({
  client,
  marketConfigurators: [], // Empty array = auto-discover all markets
});
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `client` | `PublicClient` | viem client instance |
| `marketConfigurators` | `Address[]` | Filter to specific configurators, or `[]` for all |

## Accessing Markets

The SDK exposes markets through `marketRegister`:

```typescript
// All markets
const markets = sdk.marketRegister.markets;

// Find by pool address
const market = sdk.marketRegister.findByPool(poolAddress);

// Find by credit manager
const market = sdk.marketRegister.findByCreditManager(cmAddress);

// Market provides typed access
const pool = market.pool;           // Pool state
const creditManagers = market.creditManagers;  // Array of CMs
const priceOracle = market.priceOracle;
```

## Using Plugins

Plugins extend SDK functionality for specific use cases:

```typescript
import { AccountsPlugin, AdaptersPlugin } from '@gearbox-protocol/sdk';

// Attach plugins
sdk.use(new AccountsPlugin());
sdk.use(new AdaptersPlugin());

// After loading, access plugin data
const accounts = sdk.accounts.byCreditManager(cmAddress);
const adapters = sdk.adapters.byProtocol('uniswap-v3');
```

**Available Plugins:**

| Plugin | Purpose |
|--------|---------|
| `AccountsPlugin` | Credit account indexing and filtering |
| `AdaptersPlugin` | Protocol adapter discovery and metadata |

## Address Provider via SDK

The SDK wraps AddressProvider for contract discovery:

```typescript
import { AP_MARKET_COMPRESSOR, VERSION_RANGE_310 } from '@gearbox-protocol/sdk';

// Get latest compressor address
const [compressor] = sdk.addressProvider.mustGetLatest(
  AP_MARKET_COMPRESSOR,
  VERSION_RANGE_310
);

// List all registered contracts
const contracts = sdk.addressProvider.list();
```

## Complete Example

```typescript
import { GearboxSDK, createCreditAccountService } from '@gearbox-protocol/sdk';
import { createPublicClient, http } from 'viem';
import { mainnet } from 'viem/chains';

async function main() {
  const client = createPublicClient({
    chain: mainnet,
    transport: http(),
  });

  // Initialize SDK
  const sdk = await GearboxSDK.attach({
    client,
    marketConfigurators: [],
  });

  // Find USDC market
  const usdcMarket = sdk.marketRegister.markets.find(
    m => m.pool.underlying.symbol === 'USDC'
  );

  if (!usdcMarket) throw new Error('USDC market not found');

  // Get credit managers for this market
  const creditManagers = usdcMarket.creditManagers;
  console.log(`Found ${creditManagers.length} credit managers`);

  // Create service for account operations
  const service = createCreditAccountService(sdk, 310);

  // Query accounts
  const accounts = await service.getCreditAccounts(
    { creditManager: creditManagers[0].address },
    sdk.currentBlock
  );
  console.log(`Found ${accounts.length} credit accounts`);
}

main().catch(console.error);
```

## Next Steps

- [Reading Data](reading-data.md) - Query market state and pool data
- [Credit Accounts](credit-accounts.md) - Account operations via services

For architectural background, see [Credit Suite Architecture](../concepts/credit-suite.md).
