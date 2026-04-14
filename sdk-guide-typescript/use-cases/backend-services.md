# Backend Services

Build indexers, analytics pipelines, and data warehouses that track Gearbox protocol state over time.

## Overview

Backend services typically need to:

1. Capture historical snapshots at specific blocks
2. Index events for efficient state reconstruction
3. Track rates, values, and utilization over time
4. Store and query historical data

This guide shows patterns for each requirement.

***

## Historical Snapshots

**WHY:** Track how protocol state changes over time for analytics, reporting, and historical queries.

### What to Snapshot

| Data                 | Source              | Change Frequency          |
| -------------------- | ------------------- | ------------------------- |
| Pool rates           | `PoolState`         | Every block with activity |
| Pool liquidity       | `PoolState`         | Every deposit/borrow      |
| Quota utilization    | `QuotaKeeperState`  | Every position change     |
| Credit account state | `CreditAccountData` | Every account operation   |
| Token prices         | `PriceOracle`       | External feed updates     |

### How to Query at Specific Blocks

Compressors support querying at historical blocks using viem's `blockTag` or `blockNumber`:

```typescript
import {
  marketCompressorAbi,
  AP_MARKET_COMPRESSOR,
  VERSION_RANGE_310,
} from '@gearbox-protocol/sdk';

const [compressor] = sdk.addressProvider.mustGetLatest(
  AP_MARKET_COMPRESSOR,
  VERSION_RANGE_310
);

// Query at specific block
const historicalData = await client.readContract({
  address: compressor,
  abi: marketCompressorAbi,
  functionName: 'getMarketData',
  args: [poolAddress],
  blockNumber: 19000000n, // Specific block
});

console.log(`Pool state at block 19000000:`);
console.log(`  Available liquidity: ${historicalData.pool.availableLiquidity}`);
console.log(`  Supply rate: ${historicalData.pool.supplyRate}`);
```

### Archive Node Requirements

Historical queries require an archive node. Standard nodes only keep recent state (\~128 blocks).

**RPC providers with archive access:**

* Alchemy (archive add-on)
* Infura (archive add-on)
* QuickNode (archive plans)
* Self-hosted Erigon/Reth

### Snapshot Pattern

```typescript
interface PoolSnapshot {
  blockNumber: bigint;
  timestamp: number;
  availableLiquidity: bigint;
  totalAssets: bigint;
  supplyRate: bigint;
  borrowRate: bigint;
}

async function capturePoolSnapshot(
  blockNumber: bigint
): Promise<PoolSnapshot> {
  const block = await client.getBlock({ blockNumber });

  const marketData = await client.readContract({
    address: compressor,
    abi: marketCompressorAbi,
    functionName: 'getMarketData',
    args: [poolAddress],
    blockNumber,
  });

  return {
    blockNumber,
    timestamp: Number(block.timestamp),
    availableLiquidity: marketData.pool.availableLiquidity,
    totalAssets: marketData.pool.totalAssets,
    supplyRate: marketData.pool.supplyRate,
    borrowRate: marketData.pool.baseInterestRate,
  };
}

// Capture hourly snapshots
const BLOCKS_PER_HOUR = 300n; // ~12 second blocks
let currentBlock = startBlock;

while (currentBlock <= endBlock) {
  const snapshot = await capturePoolSnapshot(currentBlock);
  await saveToDatabase(snapshot);
  currentBlock += BLOCKS_PER_HOUR;
}
```

***

## Event Indexing

**WHY:** Events provide efficient tracking of specific state changes without polling.

### Key Events

Credit Facade emits events for all account operations:

| Event                    | When Emitted       | Key Data                                  |
| ------------------------ | ------------------ | ----------------------------------------- |
| `OpenCreditAccount`      | Account opened     | owner, creditAccount, borrowAmount        |
| `CloseCreditAccount`     | Account closed     | creditAccount                             |
| `LiquidateCreditAccount` | Account liquidated | creditAccount, liquidator, remainingFunds |
| `StartMultiCall`         | Multicall begins   | creditAccount                             |
| `FinishMultiCall`        | Multicall ends     | creditAccount                             |

Pool emits events for liquidity changes:

| Event      | When Emitted           | Key Data                            |
| ---------- | ---------------------- | ----------------------------------- |
| `Deposit`  | LP deposits            | sender, owner, assets, shares       |
| `Withdraw` | LP withdraws           | sender, receiver, assets, shares    |
| `Borrow`   | Credit Manager borrows | creditAccount, amount               |
| `Repay`    | Debt repaid            | creditAccount, amount, profit, loss |

### Watching Events with viem

```typescript
import { parseAbiItem } from 'viem';

// Watch for new credit accounts
const unwatchOpen = client.watchContractEvent({
  address: creditFacadeAddress,
  abi: creditFacadeAbi,
  eventName: 'OpenCreditAccount',
  onLogs: async (logs) => {
    for (const log of logs) {
      console.log(`New account: ${log.args.creditAccount}`);
      console.log(`  Owner: ${log.args.owner}`);
      console.log(`  Initial debt: ${log.args.borrowAmount}`);

      await indexCreditAccount(log);
    }
  },
});

// Watch for liquidations
const unwatchLiquidate = client.watchContractEvent({
  address: creditFacadeAddress,
  abi: creditFacadeAbi,
  eventName: 'LiquidateCreditAccount',
  onLogs: async (logs) => {
    for (const log of logs) {
      console.log(`Liquidated: ${log.args.creditAccount}`);
      console.log(`  Liquidator: ${log.args.liquidator}`);

      await recordLiquidation(log);
    }
  },
});
```

### Fetching Historical Events

For backfilling, fetch events in block ranges:

```typescript
async function fetchHistoricalEvents(
  fromBlock: bigint,
  toBlock: bigint
) {
  // Fetch in chunks to avoid RPC limits
  const CHUNK_SIZE = 10000n;
  let current = fromBlock;

  while (current <= toBlock) {
    const chunkEnd = current + CHUNK_SIZE > toBlock
      ? toBlock
      : current + CHUNK_SIZE;

    const logs = await client.getContractEvents({
      address: creditFacadeAddress,
      abi: creditFacadeAbi,
      eventName: 'OpenCreditAccount',
      fromBlock: current,
      toBlock: chunkEnd,
    });

    for (const log of logs) {
      await processEvent(log);
    }

    current = chunkEnd + 1n;
  }
}
```

***

## State Tracking

**WHY:** Build complete account or pool history over time by combining events and snapshots.

### Credit Account Lifecycle

Track an account from open to close:

```typescript
interface AccountHistory {
  creditAccount: string;
  owner: string;
  openBlock: bigint;
  closeBlock: bigint | null;
  operations: AccountOperation[];
}

interface AccountOperation {
  blockNumber: bigint;
  txHash: string;
  type: 'open' | 'multicall' | 'liquidate' | 'close';
  healthFactorAfter?: bigint;
}

async function trackAccountLifecycle(creditAccount: string): Promise<AccountHistory> {
  // Find open event
  const openEvents = await client.getContractEvents({
    address: creditFacadeAddress,
    abi: creditFacadeAbi,
    eventName: 'OpenCreditAccount',
    args: { creditAccount },
    fromBlock: 0n,
    toBlock: 'latest',
  });

  const openEvent = openEvents[0];

  // Find all multicall events
  const multicallEvents = await client.getContractEvents({
    address: creditFacadeAddress,
    abi: creditFacadeAbi,
    eventName: 'FinishMultiCall',
    args: { creditAccount },
    fromBlock: openEvent.blockNumber,
    toBlock: 'latest',
  });

  // Find close event (if any)
  const closeEvents = await client.getContractEvents({
    address: creditFacadeAddress,
    abi: creditFacadeAbi,
    eventName: 'CloseCreditAccount',
    args: { creditAccount },
    fromBlock: openEvent.blockNumber,
    toBlock: 'latest',
  });

  return {
    creditAccount,
    owner: openEvent.args.owner,
    openBlock: openEvent.blockNumber,
    closeBlock: closeEvents[0]?.blockNumber ?? null,
    operations: [
      { blockNumber: openEvent.blockNumber, txHash: openEvent.transactionHash, type: 'open' },
      ...multicallEvents.map(e => ({
        blockNumber: e.blockNumber,
        txHash: e.transactionHash,
        type: 'multicall' as const,
      })),
      ...(closeEvents[0] ? [{
        blockNumber: closeEvents[0].blockNumber,
        txHash: closeEvents[0].transactionHash,
        type: 'close' as const,
      }] : []),
    ].sort((a, b) => Number(a.blockNumber - b.blockNumber)),
  };
}
```

### Combining Events and Snapshots

For complete state reconstruction:

```typescript
async function reconstructAccountStateAtBlock(
  creditAccount: string,
  targetBlock: bigint
): Promise<CreditAccountData | null> {
  // Check if account existed at this block
  const history = await trackAccountLifecycle(creditAccount);

  if (history.openBlock > targetBlock) {
    return null; // Account didn't exist yet
  }

  if (history.closeBlock && history.closeBlock <= targetBlock) {
    return null; // Account was closed
  }

  // Query compressor at target block
  const [accountData] = await client.readContract({
    address: accountCompressor,
    abi: creditAccountCompressorAbi,
    functionName: 'getCreditAccountData',
    args: [creditManagerAddress, creditAccount],
    blockNumber: targetBlock,
  });

  return accountData;
}
```

***

## Rate History

**WHY:** Analytics on yield, utilization trends, and rate changes over time.

### Rates to Track

| Rate            | Source                      | Notes                                              |
| --------------- | --------------------------- | -------------------------------------------------- |
| Supply APY      | `pool.supplyRate`           | RAY scaled (10^27)                                 |
| Base borrow APR | `pool.baseInterestRate`     | RAY scaled                                         |
| Quota rates     | `quotaKeeper.tokens[].rate` | Per-token, RAY scaled                              |
| Utilization     | Calculated                  | `(totalAssets - availableLiquidity) / totalAssets` |

### Polling Pattern

```typescript
interface RateSnapshot {
  blockNumber: bigint;
  timestamp: number;
  supplyRate: bigint;
  borrowRate: bigint;
  utilization: number;
  quotaRates: Map<string, bigint>;
}

async function pollRates(): Promise<RateSnapshot> {
  const block = await client.getBlock({ blockTag: 'latest' });

  const marketData = await client.readContract({
    address: compressor,
    abi: marketCompressorAbi,
    functionName: 'getMarketData',
    args: [poolAddress],
  });

  const pool = marketData.pool;
  const borrowed = pool.totalAssets - pool.availableLiquidity;
  const utilization = pool.totalAssets > 0n
    ? Number(borrowed * 10000n / pool.totalAssets) / 100
    : 0;

  const quotaRates = new Map<string, bigint>();
  for (const token of marketData.quotaKeeper.tokens) {
    quotaRates.set(token.token, token.rate);
  }

  return {
    blockNumber: block.number,
    timestamp: Number(block.timestamp),
    supplyRate: pool.supplyRate,
    borrowRate: pool.baseInterestRate,
    utilization,
    quotaRates,
  };
}

// Poll every minute
setInterval(async () => {
  const snapshot = await pollRates();
  await saveRateSnapshot(snapshot);
}, 60_000);
```

### Rate Conversion

Convert RAY-scaled rates to annual percentages:

```typescript
const RAY = 10n ** 27n;

function rayToAnnualPercent(rayRate: bigint): number {
  // rate is per-second, annualize it
  const SECONDS_PER_YEAR = 365n * 24n * 60n * 60n;
  const annualRate = rayRate * SECONDS_PER_YEAR;
  return Number(annualRate * 10000n / RAY) / 100;
}

const supplyAPY = rayToAnnualPercent(pool.supplyRate);
console.log(`Supply APY: ${supplyAPY.toFixed(2)}%`);
```

***

## Complete Example: Simple Indexer

```typescript
import { createPublicClient, http } from 'viem';
import { mainnet } from 'viem/chains';
import {
  GearboxSDK,
  marketCompressorAbi,
  creditAccountCompressorAbi,
  AP_MARKET_COMPRESSOR,
  VERSION_RANGE_310,
} from '@gearbox-protocol/sdk';

interface IndexerState {
  lastIndexedBlock: bigint;
  pools: Map<string, PoolData>;
  accounts: Map<string, AccountData>;
}

async function runIndexer(
  startBlock: bigint,
  poolAddress: `0x${string}`,
  creditManagerAddress: `0x${string}`
) {
  const client = createPublicClient({
    chain: mainnet,
    transport: http(process.env.ARCHIVE_RPC_URL),
  });

  const sdk = await GearboxSDK.attach({
    client,
    marketConfigurators: [],
  });

  const [marketCompressor] = sdk.addressProvider.mustGetLatest(
    AP_MARKET_COMPRESSOR,
    VERSION_RANGE_310
  );

  let currentBlock = startBlock;

  while (true) {
    const latestBlock = await client.getBlockNumber();

    while (currentBlock <= latestBlock) {
      // Snapshot pool state
      const marketData = await client.readContract({
        address: marketCompressor,
        abi: marketCompressorAbi,
        functionName: 'getMarketData',
        args: [poolAddress],
        blockNumber: currentBlock,
      });

      await savePoolSnapshot(currentBlock, marketData.pool);

      // Index events in this block range
      const events = await client.getContractEvents({
        address: creditManagerAddress,
        abi: creditFacadeAbi,
        fromBlock: currentBlock,
        toBlock: currentBlock + 100n,
      });

      for (const event of events) {
        await processEvent(event);
      }

      currentBlock += 100n;
    }

    // Wait for new blocks
    await sleep(12_000);
  }
}

function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}
```

***

## Next Steps

* [Liquidation Bots](liquidation-bots.md) - If you need to act on indexed data
* [Compressors Reference](../../utilities/compressors.md) - Complete compressor API
* [Frontend Applications](frontend-applications.md) - If you also need real-time display
