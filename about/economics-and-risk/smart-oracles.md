# Smart Oracles

Leveraged lending protocols face a fundamental oracle dilemma: market-price feeds reflect real-time conditions but are manipulable, while fundamental-value feeds (exchange rates, backing ratios) resist manipulation but ignore genuine insolvency. A single feed of either type creates an attack surface — borrow at inflated prices to drain the pool, or liquidate solvent positions during flash crashes. Gearbox resolves this with a layered architecture: a dual-feed system that applies `min()` logic per asset per transaction (FACT-071), combined with an aliased loss policy that blocks bad-debt liquidations unless fundamental insolvency is confirmed (FACT-059).

## Architecture: Three Defense Layers

### Layer 1 — PriceOracleV3: Normalized Feed Registry

`PriceOracleV3` maps every collateral token to one or two price feeds (FACT-070). All outputs are standardized to 8 decimals (FACT-073), eliminating decimal-mismatch errors across assets with different token precision (e.g., USDC at 6 decimals, WETH at 18).

Supported feed types (FACT-074):

| Category | Providers | Validation |
|----------|-----------|------------|
| Push-based spot | Chainlink, Redstone Push | Staleness check against `stalenessPeriod` |
| Pull-based spot | Pyth, Redstone Pull | Staleness + confidence interval / signature checks |
| On-chain derived | LP feeds, Composite, Bounded | Rate bounds + underlying price checks |
| Fixed | Constant, Zero | No external dependency |

Each feed implements `IPriceFeed`, which is compatible with Chainlink's `AggregatorV3Interface` (FACT-072). This uniformity allows the Credit Manager to value any collateral — from WBTC to Pendle PTs — through a single interface.

### Layer 2 — Dual-Feed Circuit Breakers

Every collateral token can be configured with a primary feed and a reserve (fallback) feed (FACT-071). During user operations that reduce collateralization (withdrawals, new borrows), the protocol uses the **Safe Price**: `min(Primary, Reserve)`. This creates automatic per-asset circuit breaking without global pauses.

**Concrete scenario — stETH/ETH depeg to 0.96:**

1. Primary feed (fundamental): stETH exchange rate = 1.0 ETH (reads `getPooledEthByShares()`)
2. Reserve feed (market): Chainlink stETH/ETH = 0.96 ETH
3. Safe Price = `min(1.0, 0.96)` = 0.96 — new borrows and withdrawals value stETH at the depressed market price
4. Existing positions are checked for liquidation against the primary feed (1.0 ETH), so no mass liquidation cascade occurs
5. If both feeds agree the asset is impaired, liquidation proceeds normally

**Net effect:** Borrowers cannot exploit the fundamental feed to extract capital at inflated values. Existing positions are not force-liquidated by transient market dips.

### Layer 3 — Loss Policy: Bad Debt Gate

When a liquidation would create bad debt (collateral value < total debt), `AliasedLossPolicyV3` re-checks solvency against TWAP-based alias price feeds (FACT-059). If the aliased check shows the position is fundamentally solvent, the liquidation is blocked — the protocol waits for price recovery rather than realizing losses at distressed valuations.

Only a permissioned **Loss Liquidator** role can execute bad-debt liquidations (FACT-058). This prevents opportunistic liquidators from forcing losses during temporary dislocations.

## Key Safety Parameters

| Parameter | Mechanism | Effect |
|-----------|-----------|--------|
| `stalenessPeriod` | `block.timestamp < updatedAt + stalenessPeriod` (FACT-075) | Stale primary feed → automatic fallback to reserve. Both stale → transaction reverts. |
| `lowerBound` / `upperBound` | Bounded feed wrapper (FACT-076) | Rate below `lowerBound` → revert (hard floor). Rate above `upperBound` → capped. `upperBound = lowerBound + 200 bps`. |
| `maxConfToPriceRatio` | Pyth confidence check (FACT-077) | Revert if the confidence interval is too wide relative to price — prevents trading on uncertain data. |
| Redstone signature threshold | Multi-signer validation (FACT-078) | Requires unique authorized signatures above a threshold. Max delay: 10 minutes. Max ahead: 1 minute. |

**Bounded feed example:** An LST like wstETH uses a bounded feed with `lowerBound` set near the expected exchange rate. If the on-chain rate drops below `lowerBound` (indicating a possible exploit or genuine depeg), the feed reverts — halting all operations for that asset. If the rate rises above `lowerBound + 200 bps`, it is capped, preventing inflated collateral valuations.

## Protection Guarantees and Residual Risks

**What the architecture prevents:**

- Single-feed manipulation draining the pool (dual-feed `min()` logic blocks extraction at inflated prices)
- Cascading liquidations during flash crashes (loss policy blocks bad-debt liquidations when fundamental value is intact)
- Stale or uncertain price data reaching solvency calculations (staleness + confidence checks revert rather than proceed)
- LP token price inflation attacks (bounded feeds cap rates within 200 bps of the governance-set floor)

**What can still go wrong:**

⚠️ **Simultaneous feed failure:** If both primary and reserve feeds become stale or unreachable, all operations for the affected asset revert. Positions cannot be opened, closed, or liquidated until a feed recovers. Existing positions remain in place but cannot be managed.

⚠️ **Fundamental value compromise:** The loss policy trusts the aliased (fundamental) feed. If the underlying protocol is exploited — e.g., a liquid staking derivative loses its backing — the fundamental feed will eventually reflect the true loss, and bad-debt liquidations will proceed. The loss policy delays recognition, not prevention, of genuine insolvency.

⚠️ **Bounded feed misconfiguration:** The `lowerBound` is set by governance. If set too low, it fails to catch real depegs. If set too high, it causes unnecessary reverts during normal volatility. Periodic governance review of bounds is a manual dependency.

⚠️ **Oracle-dependent positions:** All collateral valuations, liquidation triggers, and borrowing limits depend entirely on oracle accuracy. No on-chain mechanism can compensate for systematically incorrect price data across all configured feeds.

---

- How do the primary and reserve feeds interact during divergence? → [Dual-Oracle System](dual-oracle-system.md)
- What is the exact decision flow when a liquidation would create bad debt? → [Loss Policy](loss-policy.md)
- How are individual feed types configured, normalized, and validated? → [Price Oracle](price-oracle.md)
- How do liquidation thresholds and health factors depend on oracle prices? → [Liquidation Dynamics](liquidation-dynamics.md)
