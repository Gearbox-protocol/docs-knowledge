# Risk Configuration Dictionary

Every configurable risk parameter in Gearbox, organized by scope (pool-level vs. Credit Manager-level), who can change it, how fast, and which parameters are immutable at deployment. This reference is intended for Curators setting up markets and partners evaluating the trust assumptions of a given market configuration.

---

## Curator Roles

The Curator manages market parameters through two roles with fundamentally different authority:

- **Admin:** Can modify all configurable parameters, subject to a minimum 24-hour timelock. Every change is visible on-chain during the delay period.
- **Emergency Admin:** Can update a limited set of parameters instantly (no timelock) to mitigate immediate threats. Can only restrict — never increase risk.

**Key distinction:** Admin changes are observable 24 hours before execution. Emergency Admin actions are instant but uni-directional: they can reduce exposure, pause operations, or forbid assets, but cannot raise limits, add collateral, or increase LTVs.

---

## Pool-Level Parameters

These parameters define global constraints for the liquidity pool. If a lender or borrower disagrees with these terms, the recourse is to select a different pool.

### Definitions

| Parameter | Description |
|---|---|
| **Total debt limit** | Maximum amount of underlying assets that can be borrowed across the entire pool |
| **Collateral limit** | Maximum amount of debt that can be backed by a specific collateral token (Quota Limit) |
| **Main Price Feed** | Primary price source for calculating account value and triggering liquidations |
| **Reserve Price Feed** | Secondary price source for safety checks on operations; can block Credit Account actions to protect LPs |
| **Increase Rate** | One-time fee charged whenever exposure to a collateral increases |
| **Collateral-specific rate** | Additional interest rate (APR) charged for borrowing against a specific collateral |
| **IRM** | The utilization-based Interest Rate Model contract |
| **Loss Policy** | Logic executed when a liquidation results in bad debt |
| **Emergency liquidators whitelist** | Addresses authorized to liquidate accounts when the Credit Manager is paused (default: permissionless) |
| **Loss liquidators whitelist** | Addresses authorized to execute liquidations that result in bad debt (default: permissionless) |

### Permissions Matrix

| Parameter | Admin (24h Delay) | Emergency Admin (Instant) |
|---|:---:|---|
| **Total debt limit** | ✅ | ⚠️ Reduce to zero only |
| **Collateral limit** | ✅ | ⚠️ Reduce to zero only |
| **Main Price Feed** | ✅ | ⚠️ Limited choice |
| **Loss Policy** | ✅ | ⚠️ Can turn off |
| **Loss liquidators whitelist** | ✅ | ⚠️ Can turn off |
| **Emergency liquidators whitelist** | ✅ | ⚠️ Can turn off |
| **Reserve Price Feed** | ✅ | ❌ |
| **Increase Rate** | ✅ | ❌ |
| **Collateral-specific rate** | ✅ | ❌ |
| **IRM** | ✅ | ❌ |

**Implication:** Every parameter a compromised Emergency Admin could modify is restrictive — it can shut down exposure but cannot open new risk. The Reserve Price Feed, Increase Rate, Collateral-specific rate, and IRM are beyond Emergency Admin reach entirely.

---

## Credit Manager-Level Parameters

These parameters define the strategy for a specific Credit Manager. Multiple Credit Managers can connect to a single pool, each with independent risk configurations. If a borrower disagrees with these terms, an alternative Credit Manager within the same pool may be available.

### Definitions

| Parameter | Description |
|---|---|
| **Total debt limit** | Maximum aggregate debt of all Credit Accounts created from this Credit Manager |
| **MinDebt** | Minimum required debt to open a Credit Account |
| **MaxDebt** | Maximum permitted debt per Credit Account |
| **Liquidation Premium** | Percentage of collateral value paid to the liquidator as an incentive |
| **Liquidation Fee** | Percentage of collateral value paid to the protocol (Curator & DAO) |
| **Max Enabled Tokens** | Maximum number of collateral tokens a single account can enable simultaneously |
| **Interest Fee** | Percentage of borrowing interest captured as revenue (split between Curator & DAO) |
| **Collateral's LT** | Liquidation Threshold — the maximum ratio of debt to collateral value before liquidation |
| **Collateral's forbidden status** | Controls whether a specific token is allowed or forbidden as collateral |
| **List of allowed adapters** | Restricts which external contracts (e.g., Uniswap, Curve) a Credit Account can interact with |
| **Expiration Policy** | Date after which the strategy winds down; all Credit Accounts become liquidatable regardless of Health Factor |

### Permissions Matrix

| Parameter | Admin (24h Delay) | Emergency Admin (Instant) |
|---|:---:|---|
| **Total debt limit** | ✅ | ⚠️ Reduce to zero only |
| **List of allowed adapters** | ✅ | ⚠️ Forbid only |
| **Collaterals list** | ✅ | ⚠️ Forbid only |
| **Liquidation Premium** | ✅ | ❌ |
| **Liquidation Fee** | ✅ | ❌ |
| **Collaterals' LT** | ✅ | ❌ |
| **Expiration Policy** | ✅ | ❌ |
| **MinDebt** | ❌ | ❌ |
| **MaxDebt** | ❌ | ❌ |
| **Max Enabled Tokens** | ❌ | ❌ |
| **Interest Fee** | ❌ | ❌ |

### Immutable Parameters

MinDebt, MaxDebt, Max Enabled Tokens, and Interest Fee are set at deployment and cannot be changed by either role. These are permanent trust assumptions — they remain fixed for the lifetime of the Credit Manager contract.

**Implication for partners:** When evaluating a Credit Manager, the immutable parameters define permanent bounds. Any change to these values requires deploying a new Credit Manager entirely.

---

## Related Pages

- [Market Curators](../governance/market-curators.md) — Curator role architecture and operational model
- [Instance Owner](../governance/instance-owner.md) — Price feed verification (technical prerequisites for collateral listing)
- [Protocol Audits](../governance/protocol-audits.md) — Contract verification and the Bytecode Repository
