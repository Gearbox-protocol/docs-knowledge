# SDK Guide (TypeScript)

The Gearbox SDK provides typed access to protocol state and operations. It wraps contract calls, handles encoding, and provides cached market data through a clean TypeScript interface.

## Prerequisites

- Node.js 18+
- Basic familiarity with [viem](https://viem.sh/)
- Understanding of async/await patterns

## What the SDK Provides

| Component | Purpose |
|-----------|---------|
| `GearboxSDK` | Main entry point with `attach()` initialization |
| `marketRegister` | Cached market data access |
| `addressProvider` | Contract discovery wrapper |
| Plugins | Extended functionality (AccountsPlugin, AdaptersPlugin) |
| Services | Credit account operations and multicall helpers |

## Guide Structure

1. **[Setup](setup.md)** - Installation, SDK initialization, basic configuration
2. **[Reading Data](reading-data.md)** - Market queries, account state, pool data
3. **[Credit Accounts](credit-accounts.md)** - Account operations via services
4. **[Multicalls](multicalls.md)** - Building and executing multicalls

## When to Use the SDK

| Use Case | Recommended |
|----------|-------------|
| Frontend applications | Yes |
| Analytics dashboards | Yes |
| Liquidation bots | Yes (or direct compressor calls) |
| Backend services | Yes |
| On-chain contracts | No (use Solidity Guide) |

The SDK handles ABI management, type conversions, and caching internally. For on-chain integrations or gas-optimized bot implementations, consider the [Solidity Guide](../solidity-guide/README.md).

## Architecture Understanding

For conceptual background on how Gearbox works:

- [Credit Suite Architecture](../concepts/credit-suite.md) - How Credit Managers, Facades, and Configurators work together
- [Pool Architecture](../concepts/pools.md) - Lending pools and ERC-4626 compliance
- [Multicall System](../concepts/multicall-system.md) - How multicalls execute and validate
