# For Market Curators

Market curation on Gearbox is a risk parameterization business. The Curator defines boundary conditions within which borrowers autonomously execute leveraged strategies. The deliverable is a set of smart contracts with a specific risk configuration — not a managed fund.

---

> ### How Gearbox Curation Differs
>
> | Dimension | Parameter-Only Curation (Gearbox) | Vault-Based Curation |
> |-----------|----------------------------------|---------------------|
> | Custody | None. Capital flows through protocol contracts (PoolV3, CreditAccountV3). The Curator never holds funds. | Curator or vault contract holds deposited assets. |
> | Capital allocation | Borrowers and lenders act autonomously within Curator-defined rules. | Curator actively allocates capital across strategies or vaults. |
> | Deliverable | A deployed Credit Suite with calibrated risk parameters. | A managed portfolio or yield strategy. |
> | Risk surface | Parameter miscalibration, oracle failure, liquidity crunch. | All of the above, plus directional strategy risk and rebalancing errors. |
> | Regulatory exposure | Non-custodial; no fund management activities. | Potential custodial classification depending on jurisdiction. |

---

## Operational Model: Parameters, Not Funds

- **No custody.** Capital flows through smart contracts (PoolV3, CreditAccountV3). This distinction matters for entities evaluating custodial classification risk.
- **The deliverable is a market.** The Curator deploys a Credit Suite — a PoolV3 (the liquidity hub) connected to one or more CreditManagers (the risk spokes) — each with independent parameters.

Risk liability sits with the Curator. Solvency depends on parameter selection relative to asset volatility and liquidity conditions.

---

## Infrastructure: What the DAO Provides

Curators call `MarketConfigurator.createMarket()` to deploy a market suite (PoolV3, PoolQuotaKeeperV3, PriceOracleV3, InterestRateModel, RateKeeper, LossPolicy) via factory-based Create2 deployment. Several components remain DAO-dependent:

| Component | Status | Implication |
|-----------|--------|-------------|
| Chain activation | DAO-gated | The Protocol must be deployed on a chain before Curators can create markets there |
| Price feed whitelisting | Instance Owner multisig | New oracle feeds require multisig approval; Curators can participate in this process |
| Curation interface | DAO-maintained | Market configuration requires multi-call transaction batches; the DAO provides tooling to generate and submit these payloads |
| Official UI | DAO-maintained | The primary Gearbox App is DAO-maintained; Curators relying on it depend on DAO frontend support |

Autonomous operation is possible — Curators can build proprietary frontends and transaction tooling — but requires significant engineering investment.

---

## Revenue Mechanics

Curators capture revenue from two sources:

1. **Interest fee share.** A configurable percentage of borrower interest payments flows to the Curator. The remainder goes to the Protocol DAO treasury.
2. **Liquidation fee share.** When a position is liquidated, the Curator receives a share of the liquidation fee.

**Configuration:** Fee shares (both interest and liquidation) are set per market at creation time. Exact percentages are market-specific and subject to negotiation with the DAO. See [Market Curators governance](../governance-and-operations/market-curators.md) for current defaults and configuration procedures.

**GEAR token incentives** are discretionary. The DAO votes on allocations; there is no programmatic entitlement.

---

## Risk Parameterization: The Core Job

### Liquidation Thresholds (LT)

Each collateral asset receives a liquidation threshold. The health factor formula — `HF = TWV / Total Debt`, where `TWV = Σ(Balance_i × Price_i × LT_i)` — determines when an account becomes liquidatable (HF < 1).

Setting LT too high relative to asset volatility produces bad debt.

### Exposure Limits (Quotas)

The PoolQuotaKeeperV3 manages per-token borrowing limits. Curators set caps via `setTokenLimit(address token, uint96 limit)` to prevent overexposure to illiquid tokens that cannot be liquidated at scale.

Additional controls:
- `setTotalDebtLimit(uint256 limit)` — aggregate borrowing cap across the pool
- `setCreditManagerDebtLimit(address creditManager, uint256 limit)` — per-CreditManager cap

### Liquidation Premium

Curators configure the premium paid to liquidators (defined as `1 - liquidation discount`). If this premium is too low, liquidators will not execute and the system fails. Adequate incentives are the Curator's responsibility.

### Interest Rate Model

The LinearInterestRateModelV3 prices borrowing based on utilization. Curators select or configure the IRM for each market and can update it via the configurator.

Borrower cost = base interest rate (from IRM) + quota rate premium (from RateKeeper/Gauge) for quoted assets.

---

## Known Risk Vectors

| Risk | Description | Mitigation Pointer |
|------|-------------|-------------------|
| Oracle failure | Price feed corruption or staleness triggers incorrect liquidations or prevents necessary ones. | [Price Oracle Architecture](../core-architecture/price-oracle.md) |
| Liquidity crunch | Insufficient market depth to liquidate collateral positions at the configured premium, producing bad debt. | [Liquidation Dynamics](../economics-and-risk/liquidation-dynamics.md) |
| Parameter miscalibration | LTs, exposure limits, or liquidation premiums set incorrectly relative to realized volatility and liquidity. | [Risk Configuration Dictionary](../reference/risk-configuration-dictionary.md) |

The Curator bears full economic and reputational consequences for parameter choices. The Protocol provides the liquidation mechanism but does not guarantee solvency outcomes.

---

## Operational Governance

### Parameter Updates

All critical parameter changes are subject to a **24-hour timelock**; emergency parameter changes are not instantaneous.

### Emergency Powers

The Curator (or designated Emergency Admin) can:

- **Pause borrowing** to halt new exposure
- **Trigger the Loss Policy** — AliasedLossPolicyV3 re-checks solvency using TWAP-based alias price feeds before allowing bad debt liquidation
- Authorize the **Emergency Liquidator** role, which can liquidate accounts even when the CreditFacade is paused

The DAO cannot alter a Curator's onchain parameters. However, the DAO can delist a market from the official UI, withdraw incentive support, or remove a market from co-marketing efforts. These actions serve as a reputational check.

---

## Decision Paths

| Curator Profile | Starting Point |
|----------------|---------------|
| Risk management firm evaluating the business model | Revenue share structure and DAO incentive framework → [Market Curators governance](../governance-and-operations/market-curators.md) |
| Technical team ready to deploy a market | Risk configuration dictionary and parameter constraints → [Risk Configuration Dictionary](../reference/risk-configuration-dictionary.md) |
| Existing DeFi curator comparing to other protocols | Non-custodial model and Credit Suite architecture → [Credit Suite](../core-architecture/credit-suite.md) |
| Curator assessing asset-specific risks | Liquidation dynamics and oracle architecture → [Liquidation Dynamics](../economics-and-risk/liquidation-dynamics.md) |
