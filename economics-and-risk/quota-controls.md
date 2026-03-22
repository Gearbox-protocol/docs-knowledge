# Collateral Limits & Specific Rates

Concentration risk in Gearbox is managed through the Quota system: hard caps prevent over-exposure to any single collateral type, and asset-specific rate premiums ensure borrowers using riskier collateral pay commensurately higher rates. Pool exposure to any individual asset is structurally bounded — LP loss from a single collateral crash cannot exceed the quota limit for that token.

## Hard Caps on Collateral Exposure

Each collateral token has a **Quota Limit** — the maximum total debt that can be backed by that asset across all Credit Managers attached to a pool. `PoolQuotaKeeperV3` manages these per-token limits. Whether a given token is quota-limited can be checked via `isQuotedToken(address token)`.

### Who Sets Limits

The market configurator (the curator's configuration contract) calls `setTokenLimit(address token, uint96 limit)` on `PoolQuotaKeeperV3` to set or update the cap. Only the configurator has this access — individual borrowers cannot modify limits.

### Enforcement Mechanics

Quota is tracked per Credit Account per token inside `PoolQuotaKeeperV3`. `getQuota(address creditAccount, address token)` returns the current quota amount and cumulative interest index. The global limit is enforced as the sum of all individual account quotas for that token.

When `CreditManagerV3` calls `updateQuota(address creditAccount, address token, int96 quotaChange, uint96 minQuota, uint96 maxQuota)`, the contract reverts if `totalQuoted + change > limit` — no partial fills. The state change emits `UpdateQuota(address indexed creditAccount, address indexed token, int96 quotaChange)`.

When the limit is reached:

- No new positions using that collateral can open
- Existing positions cannot increase their exposure to the capped asset
- Repayments and closures always succeed — deleveraging is never blocked

If a curator reduces a token limit below the current `totalQuoted`, no existing positions are forcibly unwound. New quota increases for that token are blocked until closures and repayments bring utilization back under the new limit.

## Asset-Specific Risk Pricing

The total cost of borrowing before fees is the sum of two independent rate components:

$$
\text{Total APR} = \text{Base Rate} + \text{Quota Rate}
$$

- **Base Rate** — Cost of pool liquidity, determined by utilization via `LinearInterestRateModelV3`. The same for all borrowers in a given pool.
- **Quota Rate** — Risk premium specific to the collateral asset. Set per token by the gauge mechanism described below.

### Who Sets Rates

`GaugeV3` determines quota rates via GEAR token holder voting. Each epoch (~1 week), GEAR holders vote on rate parameters for each quoted token. Governance sets a **Minimum Risk Premium** (floor) per token; the voted rate cannot fall below this floor regardless of voting outcome. At the start of each epoch, `PoolQuotaKeeperV3` reads the updated rates from `GaugeV3` and applies them to all borrower interest calculations going forward.

Borrowers using safe collateral are not subsidizing risky positions — the additive structure ensures each asset's risk cost is priced independently:

| Collateral Type | Base Rate | Quota Rate | Total APR |
|-----------------|-----------|------------|-----------|
| Low-risk (e.g., WETH) | 3% | 0% | 3% |
| Mid-risk (e.g., mid-cap token) | 3% | 2% | 5% |
| High-risk (e.g., governance token) | 3% | 5% | 8% |

*Rates shown are illustrative. Actual values are configurable per pool deployment.*

---

**Next questions:**

- How pool utilization determines the base rate component → [Interest Rate Model](interest-rate-model.md)
- How interest and quota revenue is split between curators and DAO → [Business Model](business-model.md)
- How liquidation thresholds interact with collateral valuation → [Liquidation Dynamics](liquidation-dynamics.md)
