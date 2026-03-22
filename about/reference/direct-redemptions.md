# Direct Redemptions for Semi-Liquid Assets

Assets with timelocked redemptions — vault tokens, LRTs, RWA receipt tokens — face a structural barrier on lending protocols that require DEX liquidity for leverage. Building and maintaining deep liquidity pools for semi-liquid assets is capital-intensive, and thin pools force conservative collateral limits. Gearbox eliminates this dependency: adapters integrate directly with issuer deposit and redemption contracts, enabling leverage without any DEX liquidity requirement.

---

## The Problem

Standard lending protocols treat timelocked assets as regular tokens. Leverage requires a liquid DEX market for the collateral asset. Three constraints follow:

- **Issuers must fund DEX liquidity.** Seeding and maintaining deep order books for a semi-liquid asset is an ongoing capital cost — often exceeding the yield the asset generates.
- **Conservative collateral limits.** Thin DEX liquidity forces lending protocols to cap collateral exposure well below the asset's actual backing value, limiting leverage availability.
- **Slow or expensive exit.** Borrowers either wait for the native redemption period (days to months) or pay significant slippage to exit through a shallow DEX pool.

The result: semi-liquid assets remain underutilized as collateral despite being fully backed by underlying value.

---

## How Direct Redemption Works

Gearbox adapters integrate directly with issuer deposit and redemption contracts at the smart-contract level. Each interaction between a Credit Account (an isolated smart contract per borrower — FACT-003) and an external protocol passes through an audited adapter that constrains calls to whitelisted functions and verifies results. All operations execute as batched MultiCall arrays through `CreditFacadeV3` (FACT-004).

**Concrete example — Leveraged LRT position using EtherFi's eETH:**

### Entry Flow

1. A Credit Account receives ETH collateral and borrows additional ETH from the pool.
2. The Credit Account deposits the total (own capital + borrowed) into EtherFi's staking contract via the EtherFi adapter, receiving weETH (wrapped eETH) tokens.
3. weETH serves as collateral within the Credit Account. The Curator has configured a Liquidation Threshold for weETH and registered a price feed — typically a bounded feed with `lowerBound` near the expected exchange rate (FACT-076). If the on-chain rate drops below `lowerBound`, the feed reverts, halting operations for that asset.
4. The Credit Account remains overcollateralized. Health Factor = TWV / Total Debt, where TWV includes the weETH balance valued by the configured oracle (FACT-050, FACT-051).

No DEX pool for weETH is required at any point in this flow. The adapter calls EtherFi's contracts directly.

### Unwind Flow

1. The Credit Account calls EtherFi's withdrawal function via the adapter, submitting weETH for redemption.
2. EtherFi issues a withdrawal NFT (or receipt token) representing a claim on the underlying ETH, subject to a redemption delay.
3. The Curator has pre-configured this receipt token as valid collateral with its own Liquidation Threshold and price feed. The receipt token is added to the Credit Account's enabled collateral mask.
4. During the redemption window, the Credit Account holds the receipt token and outstanding debt. It remains overcollateralized — the receipt token's value is tracked by the oracle, and the Health Factor is checked on every operation.
5. After the redemption window completes: the adapter calls the claim function, the receipt is burned, underlying ETH is received by the Credit Account, and debt is repaid.

**Collateral transformation:** weETH → withdrawal receipt → ETH. The Credit Account is overcollateralized at every step of this transformation.

---

## Capital Efficiency: Worked Comparison

The efficiency gain comes from eliminating iterative deleverage cycles. Without direct redemption, a leveraged position must be unwound through repeated partial exits — each requiring a full redemption period.

**Scenario:** A borrower holds a 5x leveraged position (own capital: $100, borrowed: $400, total exposure: $500) in an asset with a 30-day redemption period. The position must be fully closed.

| Method | Steps | Total Time | Capital Locked |
|---|---|---|---|
| **DEX exit** | Swap collateral to debt asset on DEX | Instant | Slippage cost proportional to position size and pool depth |
| **Iterative deleverage (no Gearbox)** | Each cycle: redeem a portion, wait 30 days, repay partial debt, repeat. At 5x leverage, ~4 cycles needed to fully deleverage. | ~120 days | Full position locked during each cycle |
| **Direct redemption (Gearbox)** | Single redemption of full collateral. Receipt token serves as collateral during wait. | 1 redemption period (30 days) | Credit Account holds receipt; no additional capital required |

The difference scales with leverage and redemption period length. Higher leverage requires more iterative cycles in the non-Gearbox case; direct redemption always requires exactly one cycle.

---

## Key Properties

| Property | Mechanism |
|---|---|
| DEX liquidity dependency | None. Adapters call issuer contracts directly. |
| Time-to-leverage | Available as soon as the Curator configures the adapter and oracle feed. No liquidity bootstrap phase. |
| Collateral during redemption | Receipt token is valid collateral with its own Liquidation Threshold (Curator-configured). |
| Overcollateralization | Health Factor checked on every operation throughout the position lifecycle (FACT-050). |
| Oracle coverage | Bounded, Composite, or external feeds depending on asset type (FACT-074). Curator selects feed appropriate to the asset's pricing characteristics. |
| Applicable asset types | Any token with a smart-contract issuance/redemption path: LRTs (eETH, rETH), ERC-4626 vaults, RWA receipt tokens |

---

## Risks and Failure Modes

⚠️ **Issuer redemption delay or failure.** The position depends on the issuer's redemption contract functioning correctly. If the issuer extends the redemption period, pauses withdrawals, or the redemption contract has a bug, the Credit Account remains holding the receipt token with accruing debt. The position is not automatically unwound — debt continues to grow. If the Health Factor drops below 1.0 during an extended delay, the position becomes liquidatable (FACT-056).

⚠️ **Receipt token oracle risk.** The receipt token's collateral value depends on the configured price feed. If the feed cannot accurately track the receipt's redemption value — for example, if the issuer devalues pending claims — the Health Factor calculation may not reflect actual risk. Bounded feeds (FACT-076) mitigate but do not eliminate this: they cap and floor the rate, but the bounds are governance-set parameters that require periodic review.

⚠️ **Adapter scope limitation.** The adapter exposes only audited functions on the issuer's contract. If the issuer upgrades their contract or changes the redemption interface, the adapter must be updated and re-audited before the new interface is usable. During this gap, redemptions through the old interface may fail if the issuer has deprecated it.

⚠️ **Liquidation of receipt-holding positions.** If a position holding a receipt token is liquidated, the liquidator receives the receipt token — which itself has a redemption delay. Liquidator willingness to participate depends on the receipt token's remaining time-to-maturity and secondary market liquidity (if any). Low liquidator participation during long redemption windows increases bad-debt risk.

---

## Related Pages

- How do Curators configure collateral types including receipt tokens? → [Market Curators](../governance/market-curators.md)
- What parameters control Liquidation Thresholds and collateral limits? → [Risk Configuration Dictionary](risk-configuration-dictionary.md)
- How does Gearbox handle RWA settlement with longer redemption cycles (e.g., ACRED ~90 days)? → [RWA Settlement](rwa-settlement.md)
- How do adapters constrain Credit Account interactions with external protocols? → [Adapters & Integrations](../core-architecture/adapters-integrations.md)
- How do bounded and composite oracle feeds value illiquid collateral? → [Smart Oracles](../economics-and-risk/smart-oracles.md)
