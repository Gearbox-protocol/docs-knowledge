# Use Cases

The SDK guide shows you how to use individual methods. This section shows you how to combine them to build real applications.

## Choose Your Path

| If you're building... | Start here | You'll learn |
|----------------------|------------|--------------|
| Web dashboard, portfolio UI | [Frontend Applications](./frontend-applications.md) | Data fetching patterns, display mapping, real-time updates |
| Indexer, analytics, data pipeline | [Backend Services](./backend-services.md) | Historical snapshots, event indexing, state tracking |
| Liquidation bot | [Liquidation Bots](./liquidation-bots.md) | Account monitoring, health factor filtering, execution patterns |
| Health monitoring | [Health Factor Monitoring](./health-factor-monitoring.md) | Track HF over time, alerts, risk analysis |

## Quick Decision Guide

**Need to display data to users in real-time?**
Start with [Frontend Applications](./frontend-applications.md). You'll use `marketRegister` for cached data and compressors for fresh queries.

**Need to collect and analyze historical data?**
Start with [Backend Services](./backend-services.md). You'll index events and snapshot state at specific blocks.

**Need to monitor accounts and execute on-chain actions?**
Start with [Liquidation Bots](./liquidation-bots.md). You'll filter accounts by health factor and use the Router for execution.

**Need to track account health and alert on risk?**
Start with [Health Factor Monitoring](./health-factor-monitoring.md). You'll poll compressors, classify risk levels, and build alerting.

## Prerequisites

Before diving into use-case guides, complete:

1. **[Setup](../setup.md)** - Install the SDK and initialize `GearboxSDK`
2. **[Reading Data](../reading-data.md)** - Understand `marketRegister` and basic queries

## Common Foundation: Compressors

All use cases rely on compressors for efficient data fetching. Compressors aggregate on-chain data into single calls, reducing RPC overhead.

| Compressor | Use Case |
|------------|----------|
| `MarketCompressor` | Pool state, credit manager config, token data |
| `CreditAccountCompressor` | Account queries with filtering and pagination |
| `PriceFeedCompressor` | Oracle status and update requirements |

See [Compressors Reference](../../reference/compressors.md) for the complete API.

## Relationship to Other Guides

```
SDK Guide
├── setup.md              # Installation and initialization
├── reading-data.md       # Basic queries
├── credit-accounts.md    # Account operations
├── multicalls.md         # Operation overview
├── multicalls/           # Individual operation docs
│   └── [10 operation pages]
└── use-cases/            # <-- You are here
    ├── frontend-applications.md
    ├── backend-services.md
    ├── liquidation-bots.md
    └── health-factor-monitoring.md
```

The **multicalls/** directory documents individual operations (add collateral, manage debt, etc.). The **use-cases/** directory shows how to combine those operations with data fetching to build complete applications.
