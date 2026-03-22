# Loss Policy

The Loss Policy prevents the protocol from realizing bad debt at temporarily distressed prices. During flash crashes, liquidations can sell collateral far below recoverable value, creating unnecessary losses for lenders. `AliasedLossPolicyV3` gates every loss-creating liquidation behind a TWAP-based solvency re-check, blocking execution until fundamental insolvency is confirmed.

## The Problem: Cascading Liquidations

Rapid price drops trigger mass liquidations. Those liquidations further depress prices. Positions that are fundamentally solvent get liquidated at distressed valuations, creating bad debt that would not exist if prices recovered.

**Example:** In April 2024, ezETH experienced a temporary de-peg that triggered over $60M in DeFi liquidations across protocols. Positions backed by fundamentally sound collateral were liquidated at panic prices.

Without a Loss Policy, flash crashes create avoidable losses for lenders — collateral is sold below its recoverable value.

## How the Loss Policy Works

The Loss Policy acts as a conditional gate during the liquidation process. It applies only when a liquidation would create bad debt:

**Step 1 — Solvency check:** Is HF < 1 using the Main Feed?
The Main Feed is typically a fundamental feed (exchange rate, backing value) — consistent with the dual-oracle configuration described in the [Dual-Oracle System](dual-oracle-system.md).
- **No** → Account is healthy. No action.
- **Yes** → Proceed to Step 2.

**Step 2 — Bad debt check:** Would this liquidation create bad debt (Collateral Value < Debt)?
- **No** → Normal liquidation proceeds. The liquidator repays debt and claims collateral at a discount. No Loss Policy involvement.
- **Yes** → Flagged as a loss liquidation. Proceed to Step 3.

**Step 3 — TWAP alias solvency re-check:** Is the account insolvent using TWAP-based alias price feeds?
`AliasedLossPolicyV3` re-checks account solvency using TWAP-based alias price feeds. The TWAP (time-weighted average price) smooths out short-term volatility spikes, ensuring that transient market dislocations do not register as genuine insolvency.
- **No** → The TWAP-smoothed price indicates the account is fundamentally solvent. **Liquidation is blocked.** The protocol holds the position open rather than realizing the loss at a distressed price.
- **Yes** → The TWAP feed confirms fundamental insolvency. **Liquidation proceeds.** Only a permissioned Loss Liquidator can execute. Bad debt is recognized and handled through the insurance mechanism.

## Protection Window Behavior

When Step 3 blocks a liquidation, there is no fixed timeout. The position remains open indefinitely until one of two conditions is met:

1. **Price recovery:** The Main Feed health factor returns above 1, and the account exits the liquidation zone entirely.
2. **TWAP confirmation of insolvency:** The TWAP-based alias feed reflects sustained price decline, passing the Step 3 check. The Loss Liquidator can then execute.

The duration of the protection window depends on the TWAP averaging period configured for the alias feed. A longer TWAP window provides greater resistance to flash crashes but delays recognition of genuine insolvency. The curator configures this trade-off per market.

## What This Means in Practice

| Condition | Loss Policy Outcome |
|-----------|-------------------|
| HF < 1, collateral > debt | Normal liquidation — no loss, no policy intervention |
| HF < 1, collateral < debt, TWAP shows solvent | **Liquidation blocked** — position held open pending recovery or TWAP convergence |
| HF < 1, collateral < debt, TWAP shows insolvent | Loss Liquidator executes — genuine insolvency confirmed |

The Loss Liquidator role is permissioned. Standard liquidators cannot execute bad-debt liquidations. This prevents opportunistic actors from forcing losses during temporary dislocations.

## Residual Risks

⚠️ **Delayed loss recognition:** The TWAP smoothing that protects against flash crashes also delays recognition of genuine insolvency. If an asset's fundamental value is irreversibly impaired (e.g., an underlying protocol exploit), the Loss Policy holds the position open until the TWAP catches up to the true price. During this delay, bad debt may grow as interest accrues on the underwater position.

⚠️ **TWAP feed dependency:** The aliased solvency check relies entirely on the accuracy of the TWAP-based alias feed. If the TWAP feed is misconfigured, stale, or manipulated over a sustained period, the Loss Policy may block legitimate liquidations or allow premature ones.

⚠️ **Unbounded hold period:** No protocol-enforced maximum duration exists for a blocked liquidation. In extreme scenarios — prolonged market dislocation where TWAP remains above the solvency threshold — positions can remain in limbo, accruing debt without resolution. Lender capital remains locked in these positions.

⚠️ **Loss Liquidator availability:** Bad-debt liquidations require a permissioned Loss Liquidator. If no Loss Liquidator is active or willing to execute, confirmed bad-debt positions remain unresolved even after the TWAP check passes.

---

**Related pages:**

- [Liquidation Process](liquidation-dynamics.md) — Full liquidation mechanics and bad debt resolution
- [Dual-Oracle System](dual-oracle-system.md) — How Main and Reserve feeds interact
- [Smart Oracles](smart-oracles.md) — Layered oracle defense architecture including the Loss Policy gate
- [Insurance & Solvency Reserves](insurance-and-solvency.md) — How realized bad debt is absorbed
