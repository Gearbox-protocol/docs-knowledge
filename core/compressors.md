# Compressors

Compressor contracts aggregate on-chain data efficiently. Instead of dozens of individual reads, a single compressor call returns complete protocol state.

```solidity
// Discover compressor addresses via AddressProvider
[address compressor] = addressProvider.getLatestAddressByContractType(
    AP_MARKET_COMPRESSOR,
    VERSION_RANGE_310
);
```

## MarketCompressor

The primary data aggregation contract. Returns complete market state including pools, credit managers, and price oracles.

```solidity
interface IMarketCompressor {
    function getMarkets(MarketFilter memory filter)
        external view returns (MarketData[] memory);

    function getMarketData(address pool)
        external view returns (MarketData memory);

    function getPoolState(address pool)
        external view returns (PoolState memory);
}
```

### MarketFilter

```solidity
struct MarketFilter {
    address[] configurators;  // Filter by Risk Curator addresses
    address[] pools;          // Filter by specific pool addresses
    address underlying;       // Filter by underlying token (e.g., USDC)
}
```

Pass empty arrays and `address(0)` for no filtering:

```typescript
import { marketCompressorAbi } from '@gearbox-protocol/sdk';

// Get all markets
const markets = await client.readContract({
  address: compressorAddress,
  abi: marketCompressorAbi,
  functionName: 'getMarkets',
  args: [{
    configurators: [],
    pools: [],
    underlying: '0x0000000000000000000000000000000000000000'
  }],
});

// Get specific pool data
const marketData = await client.readContract({
  address: compressorAddress,
  abi: marketCompressorAbi,
  functionName: 'getMarketData',
  args: [poolAddress],
});
```

### MarketData Structure

```solidity
struct MarketData {
    PoolState pool;                    // Pool state and rates
    QuotaKeeperState quotaKeeper;      // Quota limits and rates
    CreditSuiteData[] creditManagers;  // All CMs for this market
    PriceOracleState priceOracle;      // Oracle configuration
    TokenData[] tokens;                // Allowed collateral tokens
}
```

**Key fields in PoolState:**

| Field | Type | Description |
|-------|------|-------------|
| `baseParams.addr` | `address` | Pool contract address |
| `availableLiquidity` | `uint256` | Borrowable liquidity |
| `dieselRate` | `uint256` | Share price (RAY) |
| `supplyRate` | `uint256` | Lender APY (RAY) |
| `baseInterestRate` | `uint256` | Borrower APR (RAY) |
| `totalAssets` | `uint256` | Total pool value |

**Key fields in CreditSuiteData:**

| Field | Type | Description |
|-------|------|-------------|
| `creditManager` | `address` | Credit Manager address |
| `creditFacade` | `address` | Credit Facade address |
| `creditConfigurator` | `address` | Configurator address |
| `debtLimits` | `DebtLimits` | min/max debt per account |
| `collateralTokens` | `CollateralToken[]` | Allowed tokens + LTs |

## CreditAccountCompressor

Fetches credit account data with filtering and pagination.

```solidity
interface ICreditAccountCompressor {
    function getCreditAccounts(
        address creditManager,
        CreditAccountFilter memory filter,
        uint256 offset
    ) external view returns (CreditAccountData[] memory accounts, uint256 total);

    function countCreditAccounts(
        address creditManager,
        CreditAccountFilter memory filter
    ) external view returns (uint256);

    function getCreditAccountData(
        address creditManager,
        address creditAccount
    ) external view returns (CreditAccountData memory);
}
```

### CreditAccountFilter

```solidity
struct CreditAccountFilter {
    address owner;           // Filter by owner (address(0) = any)
    uint256 minHealthFactor; // Minimum HF (0 = no min)
    uint256 maxHealthFactor; // Maximum HF (type(uint256).max = no max)
    bool includeZeroDebt;    // Include accounts with no debt
    bool reverting;          // Include reverting accounts
}
```

```typescript
import { creditAccountCompressorAbi } from '@gearbox-protocol/sdk';

// Get all accounts with debt
const [accounts, total] = await client.readContract({
  address: compressorAddress,
  abi: creditAccountCompressorAbi,
  functionName: 'getCreditAccounts',
  args: [
    creditManagerAddress,
    {
      owner: '0x0000000000000000000000000000000000000000', // Any owner
      minHealthFactor: 0n,
      maxHealthFactor: BigInt('0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff'),
      includeZeroDebt: false,
      reverting: false,
    },
    0n, // offset
  ],
});

console.log(`Found ${total} accounts, fetched ${accounts.length}`);
```

### CreditAccountData Structure

```solidity
struct CreditAccountData {
    address addr;                    // Credit Account address
    address owner;                   // Account owner
    address creditManager;           // Parent Credit Manager
    uint256 debt;                    // Total debt (principal + interest)
    uint256 cumulativeIndexLastUpdate;
    uint256 cumulativeQuotaInterest;
    uint128 quotaFees;
    uint256 enabledTokensMask;       // Bitmask of enabled tokens
    uint256 healthFactor;            // Current HF (10000 = 1.0)
    TokenInfo[] tokens;              // Token balances and values
    bool isLiquidatable;
}
```

**Key fields in TokenInfo:**

| Field | Type | Description |
|-------|------|-------------|
| `token` | `address` | Token address |
| `balance` | `uint256` | Balance in account |
| `balanceInUnderlying` | `uint256` | Value in underlying |
| `lt` | `uint16` | Liquidation threshold |

### Pagination

Large result sets are paginated. Use `offset` to fetch subsequent pages:

```typescript
const PAGE_SIZE = 100n;
let offset = 0n;
let allAccounts: CreditAccountData[] = [];

while (true) {
  const [accounts, total] = await compressor.read.getCreditAccounts([
    creditManager,
    filter,
    offset,
  ]);

  allAccounts.push(...accounts);
  offset += BigInt(accounts.length);

  if (offset >= total) break;
}
```

## PriceFeedCompressor

Aggregates price feed state for oracle updates.

```solidity
interface IPriceFeedCompressor {
    function getUpdatablePriceFeeds(address priceOracle)
        external view returns (PriceFeedData[] memory);

    function loadPriceFeedTree(address priceOracle, address token)
        external view returns (PriceFeedTreeNode memory);
}
```

```typescript
// Get all feeds that need updating
const feeds = await client.readContract({
  address: priceFeedCompressor,
  abi: priceFeedCompressorAbi,
  functionName: 'getUpdatablePriceFeeds',
  args: [priceOracleAddress],
});

// Filter for stale feeds
const staleFeeds = feeds.filter(f => f.needsUpdate);
```

## When to Use Compressors vs SDK

| Scenario | Approach |
|----------|----------|
| General market data | SDK `marketRegister` |
| Credit account queries | SDK services |
| Custom filtering logic | Direct compressor calls |
| Liquidation bots | Direct compressor (gas-optimized) |
| On-chain integration | Direct compressor (no SDK in contracts) |
| Real-time monitoring | Direct compressor with specific filters |

The SDK uses compressors internally. Use direct compressor calls when you need:
- Custom filter combinations not exposed by SDK
- Pagination control
- Gas-optimized queries for bots
- On-chain access (Solidity contracts)

## Complete Example

```typescript
import { createPublicClient, http } from 'viem';
import { mainnet } from 'viem/chains';
import {
  marketCompressorAbi,
  creditAccountCompressorAbi,
  AP_MARKET_COMPRESSOR,
  AP_CREDIT_ACCOUNT_COMPRESSOR,
} from '@gearbox-protocol/sdk';

const client = createPublicClient({
  chain: mainnet,
  transport: http(),
});

async function getMarketOverview() {
  // Get market compressor from AddressProvider
  const marketCompressor = '0x...'; // From AddressProvider

  // Fetch all markets
  const markets = await client.readContract({
    address: marketCompressor,
    abi: marketCompressorAbi,
    functionName: 'getMarkets',
    args: [{ configurators: [], pools: [], underlying: '0x0000000000000000000000000000000000000000' }],
  });

  for (const market of markets) {
    console.log(`Pool: ${market.pool.baseParams.addr}`);
    console.log(`  Available: ${market.pool.availableLiquidity}`);
    console.log(`  Supply Rate: ${market.pool.supplyRate}`);
    console.log(`  Credit Managers: ${market.creditManagers.length}`);
  }
}

async function findLiquidatableAccounts(creditManager: `0x${string}`) {
  const accountCompressor = '0x...'; // From AddressProvider

  // Query accounts with low health factor
  const [accounts] = await client.readContract({
    address: accountCompressor,
    abi: creditAccountCompressorAbi,
    functionName: 'getCreditAccounts',
    args: [
      creditManager,
      {
        owner: '0x0000000000000000000000000000000000000000',
        minHealthFactor: 0n,
        maxHealthFactor: 10000n, // HF < 1.0
        includeZeroDebt: false,
        reverting: false,
      },
      0n,
    ],
  });

  return accounts.filter(a => a.isLiquidatable);
}
```

<details>

<summary>Sources</summary>

* [contracts/compressors/MarketCompressor.sol](https://github.com/Gearbox-protocol/periphery-v3/blob/main/contracts/compressors/MarketCompressor.sol)
* [contracts/compressors/CreditAccountCompressor.sol](https://github.com/Gearbox-protocol/periphery-v3/blob/main/contracts/compressors/CreditAccountCompressor.sol)
* [contracts/compressors/PriceFeedCompressor.sol](https://github.com/Gearbox-protocol/periphery-v3/blob/main/contracts/compressors/PriceFeedCompressor.sol)
* [contracts/interfaces/IMarketCompressor.sol](https://github.com/Gearbox-protocol/periphery-v3/blob/main/contracts/interfaces/IMarketCompressor.sol)

</details>
