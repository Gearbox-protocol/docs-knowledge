# For Market Curators

Market curation on Gearbox is a risk parameterization business: curators define boundary conditions — liquidation thresholds, exposure limits, interest rate models — within which borrowers autonomously execute leveraged strategies. Curators never custody or allocate liquidity. The product a curator delivers is a set of smart contracts with a specific risk configuration; revenue comes from a programmatic share of interest and liquidation fees.

---

## Operational Model: Parameters, Not Funds

The curator role in Gearbox differs structurally from curator models in other lending protocols. There is no active rebalancing of funds between vaults or strategies. The distinction:

- **Curators set rules.** Borrowers and lenders act within those rules autonomously.
- **No custody.** Capital flows through smart contracts (PoolV3, CreditAccountV3). The curator never holds, moves, or directs funds. This distinction matters for entities evaluating custodial classification risk.
- **The deliverable is a market.** A curator deploys a Credit Suite — a PoolV3 (the liquidity hub) connected to one or more CreditManagers (the risk spokes) — each with independent parameters. The "product" is access to leverage and earning under those terms.

Risk liability sits with the curator. Gearbox Protocol provides the liquidation mechanism, but solvency depends entirely on the curator's parameter selection relative to asset volatility and liquidity conditions.

---

## Infrastructure: What the DAO Provides

Market creation is permissionless: curators call `MarketConfigurator.createMarket()` to deploy a full market suite (PoolV3, PoolQuotaKeeperV3, PriceOracleV3, InterestRateModel, RateKeeper, LossPolicy) via factory-based Create2 deployment. Several infrastructure components remain DAO-dependent:

| Component | Status | Implication |
|-----------|--------|-------------|
| Chain activation | DAO-gated | Protocol must be deployed on a chain before curators can create markets there |
| Price feed whitelisting | Instance Owner multisig | New oracle feeds require multisig approval; curators can participate in this process |
| Curation interface | DAO-maintained | Configuring a market involves complex transaction batches; the DAO provides tooling to generate these payloads |
| Official UI | DAO-maintained | The primary Gearbox App is maintained by the DAO; curators relying on it depend on DAO frontend support |

Autonomous operation — building a proprietary frontend and transaction generation tooling — is possible but requires significant engineering investment.

---

## Revenue Mechanics

Curators capture revenue from two sources:

1. **Interest fee share.** A configurable percentage of borrower interest payments flows to the curator. The remainder goes to the Protocol DAO treasury.
2. **Liquidation fee share.** When a position is liquidated, the curator receives a share of the liquidation fee taken by the protocol.

Both streams are programmatic and onchain. Revenue scales with total borrowed volume and liquidation activity in the curator's markets.

**GEAR token incentives** are discretionary. The DAO votes on incentive allocations; there is no programmatic entitlement. Curators whose markets align with DAO strategic priorities are more likely to receive support.

---

## Risk Parameterization: The Core Job

The curator's primary responsibility is calibrating risk parameters to balance capital efficiency against solvency protection. The key levers:

### Liquidation Thresholds (LT)

Each collateral asset receives a liquidation threshold. The health factor formula — `HF = TWV / Total Debt`, where `TWV = Σ(Balance_i × Price_i × LT_i)` — determines when an account becomes liquidatable (HF < 1).

Setting LT too high relative to asset volatility produces bad debt. The protocol bears no liability for miscalibration; the curator absorbs the reputational and economic consequences.

### Exposure Limits (Quotas)

The PoolQuotaKeeperV3 manages per-token borrowing limits. Curators set these caps via `setTokenLimit(address token, uint96 limit)` to prevent concentration risk — overexposure to illiquid tokens that cannot be liquidated at scale.

Additional controls:
- `setTotalDebtLimit(uint256 limit)` — aggregate borrowing cap across the pool
- `setCreditManagerDebtLimit(address creditManager, uint256 limit)` — per-CreditManager cap

### Liquidation Premium

Curators configure the premium paid to liquidators (defined as `1 - liquidation discount`). If this premium is too low, liquidators will not execute, and the system fails. The protocol does not guarantee liquidation execution — adequate incentives are the curator's responsibility.

### Interest Rate Model

The LinearInterestRateModelV3 prices borrowing based on utilization. Curators select or configure the IRM for each market and can update it via the configurator (old model deauthorized, new model authorized).

Borrower cost = base interest rate (from IRM) + quota rate premium (from RateKeeper/Gauge) for quoted assets.

---

## Operational Governance

### Parameter Updates

All critical parameter changes are subject to a **24-hour timelock**. Curators must plan updates in advance; emergency parameter changes are not instantaneous.

### Emergency Powers

In the event of an exploit or market failure, the curator (or designated Emergency Admin) can:

- **Pause borrowing** to halt new exposure
- **Trigger the Loss Policy** — the AliasedLossPolicyV3 re-checks account solvency using TWAP-based alias price feeds before allowing bad debt liquidation, preventing panic liquidations on transient price spikes
- Authorize the **Emergency Liquidator** role, which can liquidate accounts even when the CreditFacade is paused

### DAO Relationship

The DAO cannot alter a curator's onchain parameters. However, the DAO can:
- Delist a market from the official UI
- Withdraw incentive support
- Remove the market from co-marketing efforts

These actions serve as a reputational check without overriding onchain sovereignty.

---

## Decision Paths

| Curator Profile | Starting Point |
|----------------|---------------|
| Risk management firm evaluating the business model | Review the revenue share structure and DAO incentive framework → [Market Curators governance](../governance-and-operations/market-curators.md) |
| Technical team ready to deploy a market | Review the risk configuration dictionary and parameter constraints → [Risk Configuration Dictionary](../reference/risk-configuration-dictionary.md) |
| Existing DeFi curator comparing to other protocols | Review the non-custodial model and Credit Suite architecture → [Credit Suite](../core-architecture/credit-suite.md) |
| Curator assessing asset-specific risks | Review liquidation dynamics and oracle architecture → [Liquidation Dynamics](../economics-and-risk/liquidation-dynamics.md) |
