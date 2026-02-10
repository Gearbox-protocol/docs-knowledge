# Health Factor Monitoring

Track credit account health factors over time and alert on liquidation risk.

## Overview

Health factor monitoring needs to:
1. Query current health factor for accounts
2. Track changes over time
3. Alert when accounts approach liquidation
4. Provide actionable data for position management

This guide covers each step with SDK patterns.

---

## Understanding Health Factor

**WHY:** Know what you're measuring before building monitoring.

### The Formula

```
Health Factor = Total Weighted Value / Total Debt

Where:
- Weighted Value = Sum of (Token Balance * Price * Liquidation Threshold)
- Total Debt = Principal + Accrued Interest + Quota Fees
```

Health factor is scaled by 10000 in the protocol. `healthFactor = 10000` means HF = 1.0.

### Risk Thresholds

| Health Factor | Status | Action |
|---------------|--------|--------|
| > 1.5 (15000) | Healthy | No action needed |
| 1.1 - 1.5 (11000-15000) | Moderate | Monitor more frequently |
| 1.0 - 1.1 (10000-11000) | Critical | Alert user, suggest adding collateral |
| < 1.0 (< 10000) | Liquidatable | Account can be liquidated |

### What Moves Health Factor

Health factor changes when:
- **Token prices change** (most common) - market moves affect collateral values
- **Interest accrues** - debt grows over time, reducing HF
- **Quota fees accumulate** - adds to total debt
- **User actions** - adding/removing collateral, borrowing/repaying

---

## Querying Current Health Factor

**WHY:** Get a snapshot of account health for display or alerting.

### Single Account

```typescript
import {
  creditAccountCompressorAbi,
  AP_CREDIT_ACCOUNT_COMPRESSOR,
  VERSION_RANGE_310,
} from '@gearbox-protocol/sdk';

const [accountCompressor] = sdk.addressProvider.mustGetLatest(
  AP_CREDIT_ACCOUNT_COMPRESSOR,
  VERSION_RANGE_310
);

// Get specific account data
const [accounts] = await client.readContract({
  address: accountCompressor,
  abi: creditAccountCompressorAbi,
  functionName: 'getCreditAccounts',
  args: [
    creditManagerAddress,
    {
      owner: userAddress,
      minHealthFactor: 0n,
      maxHealthFactor: 65535n, // All HF values
      includeZeroDebt: false,
      reverting: false,
    },
    0n,
  ],
});

for (const account of accounts) {
  const hf = Number(account.healthFactor) / 10000;
  console.log(`Account ${account.addr}: HF = ${hf.toFixed(4)}`);
}
```

### All Accounts at Risk

Filter for accounts approaching liquidation:

```typescript
// Accounts with HF between 1.0 and 1.1 (at risk but not yet liquidatable)
const [atRiskAccounts] = await client.readContract({
  address: accountCompressor,
  abi: creditAccountCompressorAbi,
  functionName: 'getCreditAccounts',
  args: [
    creditManagerAddress,
    {
      owner: '0x0000000000000000000000000000000000000000',
      minHealthFactor: 10000n, // HF >= 1.0
      maxHealthFactor: 11000n, // HF < 1.1
      includeZeroDebt: false,
      reverting: false,
    },
    0n,
  ],
});

console.log(`${atRiskAccounts.length} accounts in critical range`);
```

---

## Continuous Monitoring

**WHY:** Health factors change with every block as prices move and interest accrues.

### Polling Pattern

```typescript
interface HealthSnapshot {
  account: string;
  healthFactor: number;
  debt: bigint;
  totalValue: bigint;
  timestamp: number;
}

async function monitorAccounts(
  creditManager: `0x${string}`,
  owner: `0x${string}`,
  onAlert: (snapshot: HealthSnapshot) => void
) {
  const POLL_INTERVAL = 5000; // 5 seconds
  const ALERT_THRESHOLD = 1.1; // Alert when HF < 1.1

  while (true) {
    try {
      const [accounts] = await client.readContract({
        address: accountCompressor,
        abi: creditAccountCompressorAbi,
        functionName: 'getCreditAccounts',
        args: [
          creditManager,
          {
            owner,
            minHealthFactor: 0n,
            maxHealthFactor: 65535n,
            includeZeroDebt: false,
            reverting: false,
          },
          0n,
        ],
      });

      for (const account of accounts) {
        const hf = Number(account.healthFactor) / 10000;
        const totalValue = account.tokens.reduce(
          (sum, t) => sum + t.balanceInUnderlying,
          0n
        );

        const snapshot: HealthSnapshot = {
          account: account.addr,
          healthFactor: hf,
          debt: account.debt,
          totalValue,
          timestamp: Date.now(),
        };

        if (hf < ALERT_THRESHOLD) {
          onAlert(snapshot);
        }
      }
    } catch (error) {
      console.error('Monitor error:', error);
    }

    await new Promise(resolve => setTimeout(resolve, POLL_INTERVAL));
  }
}
```

### Event-Driven Updates

For more efficient monitoring, watch for events that affect health factor:

```typescript
// Watch for multicall completions (position changes)
const unwatchMulticall = client.watchContractEvent({
  address: creditFacadeAddress,
  abi: creditFacadeAbi,
  eventName: 'FinishMultiCall',
  onLogs: async (logs) => {
    for (const log of logs) {
      // Refresh HF for affected account
      await refreshHealthFactor(log.args.creditAccount);
    }
  },
});

// Watch for liquidations
const unwatchLiquidation = client.watchContractEvent({
  address: creditFacadeAddress,
  abi: creditFacadeAbi,
  eventName: 'LiquidateCreditAccount',
  onLogs: async (logs) => {
    for (const log of logs) {
      console.log(`Account ${log.args.creditAccount} was liquidated`);
    }
  },
});
```

---

## Health Factor Breakdown

**WHY:** Understanding why HF is low helps users take the right corrective action.

### Decomposing Health Factor

```typescript
interface HealthBreakdown {
  healthFactor: number;
  totalWeightedValue: bigint;
  totalDebt: bigint;
  principal: bigint;
  accruedInterest: bigint;
  quotaFees: bigint;
  topCollaterals: Array<{
    symbol: string;
    balance: bigint;
    valueInUnderlying: bigint;
    liquidationThreshold: number;
    weightedContribution: bigint;
  }>;
}

function analyzeHealthFactor(account: CreditAccountData): HealthBreakdown {
  const tokens = account.tokens
    .filter(t => t.balance > 0n)
    .map(t => ({
      symbol: t.symbol,
      balance: t.balance,
      valueInUnderlying: t.balanceInUnderlying,
      liquidationThreshold: Number(t.lt) / 10000,
      weightedContribution: t.balanceInUnderlying * BigInt(t.lt) / 10000n,
    }))
    .sort((a, b) => Number(b.weightedContribution - a.weightedContribution));

  const totalWeightedValue = tokens.reduce(
    (sum, t) => sum + t.weightedContribution,
    0n
  );

  const quotaInterest = account.cumulativeQuotaInterest;
  const quotaFees = account.quotaFees;
  const baseInterest = account.debt - account.borrowedAmount - quotaInterest - quotaFees;

  return {
    healthFactor: Number(account.healthFactor) / 10000,
    totalWeightedValue,
    totalDebt: account.debt,
    principal: account.borrowedAmount,
    accruedInterest: baseInterest,
    quotaFees,
    topCollaterals: tokens,
  };
}

// Usage
const breakdown = analyzeHealthFactor(account);
console.log(`Health Factor: ${breakdown.healthFactor.toFixed(4)}`);
console.log(`Debt: ${breakdown.totalDebt} (principal: ${breakdown.principal})`);
console.log(`Interest: ${breakdown.accruedInterest}, Quota fees: ${breakdown.quotaFees}`);
console.log('Collateral contributions:');
for (const col of breakdown.topCollaterals) {
  console.log(`  ${col.symbol}: ${col.weightedContribution} (LT: ${(col.liquidationThreshold * 100).toFixed(1)}%)`);
}
```

---

## Alerting Strategies

**WHY:** Different users need different alert thresholds and delivery methods.

### Tiered Alerts

```typescript
type AlertLevel = 'info' | 'warning' | 'critical' | 'liquidatable';

function classifyRisk(healthFactor: number): AlertLevel {
  if (healthFactor < 1.0) return 'liquidatable';
  if (healthFactor < 1.05) return 'critical';
  if (healthFactor < 1.1) return 'warning';
  return 'info';
}

interface AlertConfig {
  account: `0x${string}`;
  creditManager: `0x${string}`;
  thresholds: {
    warning: number;   // e.g. 1.2
    critical: number;  // e.g. 1.1
  };
  cooldown: number; // milliseconds between repeat alerts
}

const lastAlertTime = new Map<string, number>();

function shouldAlert(
  account: string,
  level: AlertLevel,
  config: AlertConfig
): boolean {
  if (level === 'info') return false;

  const key = `${account}-${level}`;
  const lastTime = lastAlertTime.get(key) ?? 0;
  const now = Date.now();

  if (now - lastTime < config.cooldown) return false;

  lastAlertTime.set(key, now);
  return true;
}
```

### Suggested Actions per Level

```typescript
function suggestAction(breakdown: HealthBreakdown, level: AlertLevel): string {
  switch (level) {
    case 'warning':
      return 'Consider adding collateral or reducing debt';
    case 'critical':
      return `Add at least ${formatValue(breakdown.totalDebt / 10n)} collateral immediately`;
    case 'liquidatable':
      return 'Account is liquidatable. Add collateral or repay debt NOW';
    default:
      return 'Position is healthy';
  }
}
```

---

## Complete Example: Health Monitor Service

```typescript
import { createPublicClient, http } from 'viem';
import { mainnet } from 'viem/chains';
import {
  GearboxSDK,
  creditAccountCompressorAbi,
  AP_CREDIT_ACCOUNT_COMPRESSOR,
  VERSION_RANGE_310,
} from '@gearbox-protocol/sdk';

const WARNING_HF = 1.15;
const CRITICAL_HF = 1.05;
const POLL_INTERVAL = 10_000; // 10 seconds

async function runHealthMonitor(
  creditManagerAddress: `0x${string}`,
  ownerAddress: `0x${string}`
) {
  const client = createPublicClient({
    chain: mainnet,
    transport: http(),
  });

  const sdk = await GearboxSDK.attach({
    client,
    marketConfigurators: [],
  });

  const [accountCompressor] = sdk.addressProvider.mustGetLatest(
    AP_CREDIT_ACCOUNT_COMPRESSOR,
    VERSION_RANGE_310
  );

  let previousHFs = new Map<string, number>();

  while (true) {
    try {
      const [accounts] = await client.readContract({
        address: accountCompressor,
        abi: creditAccountCompressorAbi,
        functionName: 'getCreditAccounts',
        args: [
          creditManagerAddress,
          {
            owner: ownerAddress,
            minHealthFactor: 0n,
            maxHealthFactor: 65535n,
            includeZeroDebt: false,
            reverting: false,
          },
          0n,
        ],
      });

      for (const account of accounts) {
        const hf = Number(account.healthFactor) / 10000;
        const prevHF = previousHFs.get(account.addr);
        previousHFs.set(account.addr, hf);

        // Determine direction
        const direction = prevHF !== undefined
          ? (hf > prevHF ? 'improving' : hf < prevHF ? 'declining' : 'stable')
          : 'initial';

        // Classify and alert
        if (hf < 1.0) {
          console.log(`LIQUIDATABLE: ${account.addr} HF=${hf.toFixed(4)} [${direction}]`);
        } else if (hf < CRITICAL_HF) {
          console.log(`CRITICAL: ${account.addr} HF=${hf.toFixed(4)} [${direction}]`);
        } else if (hf < WARNING_HF) {
          console.log(`WARNING: ${account.addr} HF=${hf.toFixed(4)} [${direction}]`);
        } else if (direction !== 'stable') {
          console.log(`OK: ${account.addr} HF=${hf.toFixed(4)} [${direction}]`);
        }
      }
    } catch (error) {
      console.error('Monitor error:', error);
    }

    await new Promise(resolve => setTimeout(resolve, POLL_INTERVAL));
  }
}

runHealthMonitor('0x...', '0x...').catch(console.error);
```

---

## Gotchas

### Stale Price Feeds

If on-demand price feeds (Pyth, Redstone) haven't been updated recently, the health factor from compressors may not reflect current market prices. For accurate monitoring:

```typescript
// Check if any feeds need updating
const feeds = await client.readContract({
  address: priceFeedCompressor,
  abi: priceFeedCompressorAbi,
  functionName: 'getUpdatablePriceFeeds',
  args: [priceOracleAddress],
});

const staleFeeds = feeds.filter(f => f.needsUpdate);
if (staleFeeds.length > 0) {
  console.log(`Warning: ${staleFeeds.length} price feeds are stale`);
}
```

### Health Factor Precision

Health factor is an integer scaled by 10000. Small changes (e.g., 10001 to 10000) can cross the liquidation boundary. Always use precise comparison:

```typescript
// WRONG: floating point comparison
if (hf < 1.0) { ... }

// CORRECT: compare raw values
if (account.healthFactor < 10000n) { ... }
```

### Interest Accumulation

Health factor decreases over time even without price changes, because interest accrues continuously. Factor this into alert timing - an account at HF 1.05 today may be liquidatable tomorrow purely from interest.

---

## Next Steps

- [Frontend Applications](./frontend-applications.md) - Display health data in a UI
- [Liquidation Bots](./liquidation-bots.md) - Act on liquidatable accounts
- [Compressors Reference](../../reference/compressors.md) - Full compressor API
- [Debt Management](../multicalls/debt-management.md) - Repay debt to improve health
- [Adding Collateral](../multicalls/adding-collateral.md) - Add collateral to improve health
