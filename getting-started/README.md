# Getting Started

Gearbox V3.1 provides composable leverage infrastructure. This section covers the essential patterns for integrating with the protocol.

## Prerequisites

- Solidity proficiency (0.8.x)
- TypeScript/viem or ethers.js experience
- Basic understanding of EVM and DeFi primitives

## What V3.1 Offers

| Capability | Description |
|------------|-------------|
| Credit Accounts | Isolated smart contract wallets with borrowed funds |
| Atomic Multicalls | Batch operations in a single transaction |
| Composable Adapters | Pre-audited integrations with Uniswap, Curve, Convex, etc. |
| On-chain State Compression | Single-call market state queries |

## Quick Links

- [SDK Setup](sdk-setup.md) - **Recommended:** Initialize SDK and access markets
- [Contract Discovery](contract-discovery.md) - Find any protocol contract programmatically
- [Market Data](market-data.md) - Query complete market state with MarketCompressor

> **Note:** The Gearbox SDK is the recommended approach for most integrations. It provides typed access to markets, credit accounts, and protocol state. Raw viem/ethers.js examples are provided for reference and on-chain integrations.

## Conceptual Background

For architecture and design rationale, see the About documentation:

- [Credit Suite Architecture](../../new-docs-about/core-architecture/credit-suite.md)
- [How Gearbox Works](../../new-docs-about/doc-gitbook/overview/how-it-works.md)
