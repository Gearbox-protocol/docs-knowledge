# Price Oracle

`PriceOracleV3` is the central price registry mapping each token to its price feed, governing all solvency checks, liquidation triggers, and collateral valuations across the protocol.

## Data Normalization

All price feeds — Chainlink, Pyth, Uniswap, fundamental — are scaled to a strict **8-decimal standard** (e.g., $1.00 = `100,000,000`), regardless of the underlying asset's native decimal precision. This uniformity allows the Credit Manager to perform solvency checks (`HF = TWV / Total Debt`) using a single consistent formula across all collateral types.

## Staleness Protection

Every price feed is configured with a `stalenessPeriod`, typically matching the feed provider's heartbeat.

On each price read, the oracle checks:

```
block.timestamp < updatedAt + stalenessPeriod
```

If the primary feed is stale, `PriceOracleV3` falls back to the reserve feed for that asset. If the reserve feed is also stale, the transaction reverts.

**Implication for partners:** Oracle downtime causes transaction failures, not incorrect valuations.

## Oracle Failure and Open Positions

When all feeds for an asset are stale, the oracle reverts on any price read. Liquidators cannot liquidate positions (protecting borrowers from execution against bad prices), but borrowers also cannot modify or close positions. Capital is temporarily frozen until feeds resume or governance intervenes by updating the feed configuration.

## Feed Types

### Spot Feeds

- **Push models** (Chainlink, Redstone Push): Oracle nodes push updates on-chain at defined intervals or deviation thresholds
- **Pull models** (Pyth, Redstone Pull): Price updates are cryptographically signed off-chain and pushed on-chain only when needed by a transaction, reducing gas costs. Pyth feeds enforce a `maxConfToPriceRatio` parameter — the transaction reverts if the confidence interval relative to price exceeds this threshold.

**Typical assets:** WETH, WBTC, USDC, major liquid tokens.

### TWAP Feeds (Time-Weighted Average Price)

Average price over a defined period (e.g., 30 minutes), calculated from AMM price accumulators.

**Typical assets:** Curve LP tokens, Pendle PTs, long-tail assets with limited spot oracle coverage.

### Fundamental Feeds (Derived Value)

The feed reads `convertToAssets()`, `getRate()`, or equivalent functions from the token contract and multiplies by the underlying asset's price.

**Typical assets:** ERC-4626 vault shares, Liquid Staking Tokens (stETH, rETH), stablecoin peg modules.

## Modular Pricing for Complex Assets

- **Curve & Balancer LP tokens** — Priced via the pool's virtual price (derived from the invariant and constituent token prices)
- **Pendle PTs** — Market price derived from a TWAP of the PT/SY exchange rate
- **Bounded Feeds** — Wrappers that enforce `lowerBound` (hard floor) and `upperBound` (set to `lowerBound + 200 bps`). Prices below `lowerBound` cause a revert; prices above `upperBound` are capped. Used to constrain stablecoin and LST price feeds to expected ranges.

**Implication for partners:** Curators can list productive assets (vaults, LP positions, derivatives) as collateral using on-chain pricing, without dependency on centralized oracle providers adding support.

---

**Related pages:**

- [Dual-Oracle System](dual-oracle-system.md) — How two independent feeds per asset create circuit breakers against manipulation
- [Smart Oracles Overview](smart-oracles.md) — Architecture overview of the oracle safety system
- [Loss Policy](loss-policy.md) — How fundamental pricing prevents unnecessary bad debt during flash crashes
ENDOFREVISION; __hermes_rc=$?; printf '__HERMES_FENCE_a9f7b3__'; exit $__hermes_rc
