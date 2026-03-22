# Faster RWA Settlement with Leverage

RWA tokens — tokenized securities, private credit, treasuries — do not settle atomically. Deposits (e.g., USDC → ACRED mint) can require hours or days. Redemptions can take materially longer: ACRED redemption windows can extend to approximately 90 days. This settlement profile breaks standard leverage strategies and discourages liquidator participation.

Gearbox acts as a prime brokerage layer during transition phases, holding positions when assets are pending deposits or redemption receipts rather than mature ERC20 tokens. The result: near-immediate entry into RWA-backed debt positions and single-period exit, without requiring changes to the partner lending platform's core architecture.

---

## The Problem: Non-Atomic Settlement Constrains RWA-Backed Debt

Three specific constraints emerge from delayed settlement:

- **Limited market opportunity capture.** By the time a deposit matures into the target RWA token, market conditions may have shifted. Multi-day deposit windows prevent timely entry.
- **Positions trapped during volatility.** During price movements, positions can remain locked in redemption queues. The borrower cannot deleverage quickly.
- **Reduced liquidator participation.** Institutional liquidators are reluctant to warehouse long-dated redemption receipts (~90 days for ACRED). Lower liquidation participation increases bad-debt risk for the entire lending system.

---

## What Gearbox Provides

| Metric | Without Gearbox | With Gearbox |
|---|---|---|
| **Time to open RWA-backed debt position** | Wait for deposit settlement (hours to days) | Near-immediate (Hour 0) |
| **Time to unwind leveraged position** | Iterative deleverage across multiple redemption periods (>240 days) | 1 redemption period (~90 days) |
| **Time to de-risk position exposure** | Tied to full redemption window (~90 days) | Near-immediate if receipt is sold or financed |

Gearbox improves liquidity and risk transfer during the waiting period. It does not shorten issuer redemption cycles — final settlement timing remains issuer-dependent.

---

## Who Benefits

| Participant | Problem | Outcome with Gearbox |
|---|---|---|
| **Traders** | Miss entry points during multi-day settlement | Immediate RWA-backed debt position, exit when appropriate |
| **Liquidators** | Reluctant to hold ~90-day redemption receipts during volatility | Fast de-risking path: sell or finance the receipt at a discount |
| **Risk Curators** | Cannot offer fast credit products on RWAs with delayed settlement | Integration-ready infrastructure with no core protocol changes |

---

## Architecture

The user interacts through the existing Partner UI. Gearbox operates as a transition venue — holding positions only during deposit and redemption windows, then migrating them to the partner lending market.

- **Partner Market** holds positions when collateral is mature ERC20.
- **Gearbox** holds positions during transition (pending deposits, redemption receipts).
- **Curator** manages liquidity allocation between Partner Market and Gearbox as positions mature.

Migration is capital-neutral: supply-side allocation and user debt move together. The financial position — same collateral, same debt, same health factor — is unchanged. Only the infrastructure changes.

---

## Entry Flow: 5x Leverage on ACRED

A borrower seeks $500 ACRED exposure with $100 own capital.

**Phase 1 — Capital Allocation:**
The Curator allocates USDC from the Partner Vault to the Gearbox Pool, making capital available for borrowing.

**Phase 2 — Transition Setup:**
A Credit Account is opened. It borrows $400 USDC from the Gearbox Pool, combines with the borrower's $100 USDC, and deposits $500 USDC into the Securitize mint contract. The Credit Account receives a pending-deposit token as collateral. Position: pending-deposit token (collateral), $400 USDC (debt) — overcollateralized.

**Phase 3 — Waiting:**
The deposit window passes (hours to days, depending on ACRED terms). The pending-deposit token becomes ACRED. The position remains on the Gearbox Credit Account.

**Phase 4 — Migration to Partner Market:**
The Curator reallocates liquidity from the Gearbox Pool to the Partner Market. The Credit Account borrows $400 USDC from the Partner Market, repays the Gearbox Pool debt, supplies ACRED as collateral to the Partner Market, and closes the Credit Account. Result: $500 ACRED collateral, $400 USDC debt on the Partner Market. No additional capital required.

---

## Exit Flow: Redeeming ACRED Position

A borrower holds a $500 ACRED position ($100 equity, $400 debt) and seeks to exit to USDC.

**Phase 1 — Capital Reallocation:**
The Curator reallocates USDC from the Partner Vault to the Gearbox Pool.

**Phase 2 — Transition Setup:**
A Credit Account borrows $400 USDC from the Gearbox Pool, repays the Partner Market debt, releases ACRED, and initiates Securitize redemption. The Credit Account receives a redemption receipt token as collateral. Position: redemption receipt (collateral), $400 USDC (debt) — overcollateralized.

**Phase 3 — Waiting:**
The redemption window passes (~90 days, issuer-dependent). The redemption receipt matures into USDC.

**Phase 4 — Finalization:**
The Credit Account repays $400 debt to the Gearbox Pool and closes. The borrower receives net USDC: redemption proceeds minus debt, accrued interest, and fees (plus or minus PnL). The Curator rebalances liquidity back to the Partner Market.

---

## Liquidator Value Proposition

The same mechanism that enables faster trader entry also enables faster liquidator de-risking:

| Metric | Traditional | With Gearbox |
|---|---|---|
| **Time to de-risk** | Tied to full redemption window (~90 days) | Near-immediate if receipt is sold or financed at a discount |
| **Issuer cash settlement** | ~90 days (issuer-dependent) | ~90 days (unchanged — Gearbox does not shorten issuer timelines) |
| **Liquidator risk** | High: duration exposure + market risk during hold | Lower: faster de-risking path available |
| **Protocol health** | Lower liquidation participation, higher bad-debt risk | More active liquidation participation |

More willing liquidators under stress conditions produce healthier protocol outcomes for all participants.

---

## Related Pages

- [Direct Redemptions](direct-redemptions.md) — How Gearbox handles semi-liquid assets without DEX liquidity
- [Prime Brokerage](prime-brokerage.md) — Multi-protocol integration architecture for RWA credit positions
- [Market Curators](../governance/market-curators.md) — Curator role in configuring transition-state collateral
- [Risk Configuration Dictionary](risk-configuration-dictionary.md) — Collateral parameters and permissions
