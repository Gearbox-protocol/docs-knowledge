# Faster RWA Settlement with Leverage

RWA tokens — tokenized securities, private credit, treasuries — do not settle atomically. Deposits (e.g., USDC → ACRED mint) require hours or days. Redemptions take longer: ACRED redemption windows extend to ~90 days (per Securitize issuer terms; verify current terms with issuer). This breaks standard leverage strategies and discourages liquidator participation.

Gearbox acts as a prime brokerage layer during transition phases, holding positions when assets are pending deposits or redemption receipts rather than mature ERC20 tokens.

---

## The Problem: Non-Atomic Settlement Constrains RWA-Backed Debt

- **Limited market opportunity capture.** Multi-day deposit windows prevent timely entry.
- **Positions trapped during volatility.** Positions can remain locked in redemption queues. The borrower cannot deleverage quickly.
- **Reduced liquidator participation.** Liquidators are reluctant to warehouse long-dated redemption receipts. Lower liquidation participation increases bad-debt risk.

---

## What Gearbox Provides

| Metric | Without Gearbox | With Gearbox |
|---|---|---|
| **Time to open RWA-backed debt position** | Wait for deposit settlement (hours to days) | Near-immediate (Hour 0) |
| **Time to unwind leveraged position** | Iterative deleverage across multiple redemption periods (>240 days) | 1 redemption period (~90 days) |
| **Time to de-risk position exposure** | Tied to full redemption window (~90 days) | Near-immediate if receipt is sold or financed* |

*Both de-risking paths (secondary sale, financing against receipt) depend on external market conditions — buyer availability and pricing for sales, lender willingness for financing. Neither is guaranteed by the protocol. In illiquid conditions, the holder remains subject to the full issuer redemption timeline.

Gearbox does not shorten issuer redemption cycles — final settlement timing remains issuer-dependent.

---

## Who Benefits

| Participant | Problem | Outcome with Gearbox |
|---|---|---|
| **Traders** | Miss entry points during multi-day settlement | Immediate RWA-backed debt position, exit when appropriate |
| **Liquidators** | Reluctant to hold ~90-day redemption receipts during volatility | De-risking path via secondary sale or financing (market-dependent) |
| **Risk Curators** | Cannot offer fast credit products on RWAs with delayed settlement | Integration-ready infrastructure with no core protocol changes |

---

## Architecture

Gearbox operates as a transition venue — holding positions only during deposit and redemption windows, then migrating them to the partner lending market.

- **Partner Market** holds positions when collateral is mature ERC20.
- **Gearbox** holds positions during transition (pending deposits, redemption receipts).
- **Curator** manages liquidity allocation between Partner Market and Gearbox as positions mature.

Migration is capital-neutral: supply-side allocation and user debt move together. Same collateral, same debt, same health factor — only the infrastructure changes.

---

## Risk Disclosures

**Securitize dependency.** The RWA settlement flow depends on Securitize infrastructure. The `SecuritizeWallet` intermediary contract grants Securitize Admin authority to freeze, seize, or block operations. If Securitize exercises these powers during a transition phase, Credit Accounts holding pending-deposit tokens or redemption receipts may be unable to complete settlement. This risk is non-hedgeable within the protocol.

**Issuer redemption timing.** All redemption windows (~90 days for ACRED) are issuer-defined and issuer-enforced. Gearbox cannot accelerate redemption. Actual settlement timing may exceed stated estimates.

**Liquidation during transition.** If Health Factor drops below 1.0 (HF = Total Weighted Value / Total Debt) during a transition phase — due to a price feed update on transition-state collateral — the Credit Account becomes liquidatable via `CreditFacadeV3.liquidateCreditAccount(creditAccount, to, calls, lossPolicyData)`. The borrower loses the position, including equity beyond debt repayment and liquidation premium.

---

## Costs

| Fee Component | Source | Type |
|---|---|---|
| Gearbox Pool borrow rate | On-demand pool (fixed rate, KYC-gated via Securitize, defined term) | Fixed for loan term |
| Partner Market borrow rate | Partner protocol | Variable (protocol-dependent) |
| Securitize mint/redeem fees | Securitize issuer terms | Issuer-dependent |

During the transition phase, borrowers carry both Gearbox Pool and Partner Market rates. Transition-phase duration directly affects total cost.

---

## Entry Flow: 5x Leverage on ACRED

A borrower seeks $500 ACRED exposure with $100 own capital.

**Phase 1 — Capital Allocation:**
The Curator allocates USDC from the Partner Vault to the Gearbox Pool.

**Phase 2 — Transition Setup:**
A Credit Account is opened via `CreditFacadeV3.openCreditAccount(onBehalfOf, calls, referralCode)`. The `calls` MultiCall array encodes: borrow $400 USDC from the Gearbox Pool, combine with the borrower's $100 USDC, deposit $500 USDC into the Securitize mint contract. The Credit Account (`CreditAccountV3`, isolated per borrower) receives a pending-deposit token as collateral. Position: pending-deposit token (collateral), $400 USDC (debt) — overcollateralized.

**Phase 3 — Waiting:**
The deposit window passes (hours to days). The pending-deposit token becomes ACRED.

**Phase 4 — Migration to Partner Market:**
The Curator reallocates liquidity from the Gearbox Pool to the Partner Market. The Credit Account borrows $400 USDC from the Partner Market, repays the Gearbox Pool debt, supplies ACRED as collateral, and closes via `CreditFacadeV3.closeCreditAccount(creditAccount, calls)`. Result: $500 ACRED collateral, $400 USDC debt on the Partner Market.

---

## Exit Flow: Redeeming ACRED Position

A borrower holds a $500 ACRED position ($100 equity, $400 debt) and seeks to exit to USDC.

**Phase 1 — Capital Reallocation:**
The Curator reallocates USDC from the Partner Vault to the Gearbox Pool.

**Phase 2 — Transition Setup:**
A Credit Account is opened via `CreditFacadeV3.openCreditAccount(onBehalfOf, calls, referralCode)`. The MultiCall array encodes: borrow $400 USDC from the Gearbox Pool, repay the Partner Market debt, release ACRED, initiate Securitize redemption. The Credit Account receives a redemption receipt token as collateral. Position: redemption receipt (collateral), $400 USDC (debt) — overcollateralized.

**Phase 3 — Waiting:**
The redemption window passes (~90 days, issuer-dependent). The redemption receipt matures into USDC.

**Phase 4 — Finalization:**
The Credit Account repays $400 debt to the Gearbox Pool and closes via `CreditFacadeV3.closeCreditAccount(creditAccount, calls)`. The borrower receives net USDC: redemption proceeds minus debt, accrued interest, and fees. The Curator rebalances liquidity back to the Partner Market.

---

## Liquidator Value Proposition

| Metric | Traditional | With Gearbox |
|---|---|---|
| **Time to de-risk** | Tied to full redemption window (~90 days) | Near-immediate via secondary sale or financing (market-dependent) |
| **Issuer cash settlement** | ~90 days (issuer-dependent) | ~90 days (unchanged — Gearbox does not shorten issuer timelines) |
| **Liquidator risk** | High: duration exposure + market risk during hold | Lower: faster de-risking path available |
| **Protocol health** | Lower liquidation participation, higher bad-debt risk | More active liquidation participation |

---

## Related Pages

- [Direct Redemptions](direct-redemptions.md) — How Gearbox handles semi-liquid assets without DEX liquidity
- [Prime Brokerage](prime-brokerage.md) — Multi-protocol integration architecture for RWA credit positions
- [Market Curators](../governance/market-curators.md) — Curator role in configuring transition-state collateral
- [Risk Configuration Dictionary](risk-configuration-dictionary.md) — Collateral parameters and permissions
