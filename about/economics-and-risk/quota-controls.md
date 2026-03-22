# Collateral Limits & Specific Rates

Concentration risk in Gearbox is managed through the Quota system: hard caps prevent over-exposure to any single collateral type, and asset-specific rate premiums ensure borrowers using riskier collateral pay commensurately higher rates. Partners can communicate to LPs that pool exposure to any individual asset is structurally bounded.

## Hard Caps on Collateral Exposure

Each collateral token has a **Quota Limit** — the maximum total debt that can be backed by that asset across all Credit Managers attached to a pool.

When the limit is reached:

- No new positions using that collateral can open
- Existing positions cannot increase their exposure to the capped asset
- Repayments and closures always work — deleveraging is never blocked

Unlike a global debt ceiling (which caps total pool size) or per-Credit Manager limits (which cap strategy exposure), Quota Limits operate on the collateral side. Even if a pool has abundant idle liquidity, it cannot be allocated toward a single asset beyond the defined cap.

**Implication for partners:** If a collateral asset crashes, the pool's maximum exposure to it was capped from the start. LP loss is bounded by the quota limit, not by total pool size.

## Asset-Specific Risk Pricing

The total cost of borrowing before fees is the sum of two independent rate components:

$$
\text{Total APR} = \text{Base Rate} + \text{Quota Rate}
$$

- **Base Rate** — Cost of pool liquidity, determined by utilization. The same for all borrowers in a given pool.
- **Quota Rate** — Risk premium specific to the collateral asset. Set per token (e.g., 0% for WETH, 5% for volatile governance tokens).

This additive model separates the cost of liquidity from the cost of risk:

| Collateral Type | Base Rate | Quota Rate | Total APR |
|-----------------|-----------|------------|-----------|
| Low-risk (e.g., WETH) | 3% | 0% | 3% |
| Mid-risk (e.g., mid-cap token) | 3% | 2% | 5% |
| High-risk (e.g., volatile governance token) | 3% | 5% | 8% |

**Implication for partners:** Borrowers using safe collateral are not subsidizing risky positions. Rates are fair per asset. Partners can present this to LPs as evidence that risk pricing is granular, not pooled.

---

**Related pages:**

- [Interest Rate Model](interest-rate-model.md) — How pool utilization determines the base rate
- [Business Model](business-model.md) — How interest and quota revenue is split between curators and DAO
