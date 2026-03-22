# Price Oracle

The Price Oracle determines the value of every collateral asset in the protocol. All solvency checks, liquidation triggers, and collateral valuations depend on it. The system normalizes all price data to a uniform format, enforces freshness constraints, and supports multiple feed types — enabling curators to list complex DeFi assets as collateral without waiting for centralized oracle support.

## Data Normalization

DeFi assets vary in decimal precision (USDC: 6 decimals, WETH: 18 decimals). The Price Oracle eliminates this complexity by enforcing a strict **8-decimal standard** for all price outputs:

- **$1.00** is represented as `100,000,000`
- All feeds — Chainlink, Pyth, Uniswap, fundamental — are scaled to this format

This uniformity allows the Credit Manager to perform solvency checks (HF = TWV / Total Debt) using a single consistent formula across all collateral types. No decimal-mismatch errors are possible.

## Staleness Protection

Every price feed is configured with a `stalenessPeriod` (measured in seconds), typically derived from the feed provider's heartbeat or update frequency.

On every transaction requiring a price (borrowing, liquidation, withdrawal), the oracle checks:

```
block.timestamp - updatedAt > stalenessPeriod → revert
```

If the data is older than the staleness threshold, the transaction reverts immediately. The protocol does not fall back to stale data — it halts rather than operate on outdated prices.

When a primary feed becomes stale, the system falls back to the reserve feed for that asset. If both feeds are stale, the transaction reverts.

**Implication for partners:** The protocol is conservative by design. Oracle downtime causes transaction failures, not incorrect valuations.

## Feed Types

The protocol supports three categories of price feeds, selected based on the asset's liquidity profile and available on-chain data.

### Spot Feeds

Current market price based on off-chain aggregation or high-frequency on-chain updates. Used for liquid assets with deep centralized and decentralized markets.

- **Push models** (Chainlink, Redstone Push): Oracle nodes push updates on-chain at defined intervals or deviation thresholds
- **Pull models** (Pyth, Redstone Pull): Price updates are cryptographically signed off-chain and pushed on-chain only when needed by a transaction, reducing gas costs

**Typical assets:** WETH, WBTC, USDC, major liquid tokens.

### TWAP Feeds (Time-Weighted Average Price)

Average price over a defined period (e.g., 30 minutes), calculated from AMM price accumulators. TWAP dampens short-term volatility and increases the cost of price manipulation for assets with thinner liquidity.

**Typical assets:** Curve LP tokens, Pendle PTs, long-tail assets with limited spot oracle coverage.

### Fundamental Feeds (Derived Value)

Value derived from on-chain backing or exchange rates rather than secondary market trading. The feed reads `convertToAssets()`, `getRate()`, or equivalent functions from the token contract and multiplies by the underlying asset's price.

**Typical assets:** ERC-4626 vault shares, Liquid Staking Tokens (stETH, rETH), stablecoin peg modules.

## Modular Pricing for Complex Assets

Beyond standard integrations, the protocol maintains purpose-specific pricing contracts for complex DeFi positions:

- **Curve & Balancer LP tokens** — Priced via the pool's virtual price (derived from the invariant and constituent token prices)
- **Pendle PTs** — Market price derived from a TWAP of the PT/SY exchange rate
- **Bounded Feeds** — Wrappers that enforce upper and lower price bounds (e.g., cap a stablecoin at $1.00, cap an LST at its backing ratio). Prices below the lower bound cause a revert; prices above the upper bound are capped.

**Implication for partners:** Curators can list productive assets (vaults, LP positions, derivatives) as collateral using on-chain pricing, without dependency on centralized oracle providers adding support.

---

**Related pages:**

- [Dual-Oracle System](dual-oracle-system.md) — How two independent feeds per asset create circuit breakers against manipulation
- [Smart Oracles Overview](smart-oracles.md) — Architecture overview of the oracle safety system
- [Loss Policy](loss-policy.md) — How fundamental pricing prevents unnecessary bad debt during flash crashes
