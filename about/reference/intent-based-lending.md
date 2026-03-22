# On-Demand Pools

Institutional lenders face a structural conflict with pooled DeFi lending: capital is comingled, rates are unpredictable, losses are socialized, and counterparties are unknown. Most regulatory frameworks require counterparty identification and fund segregation — pooled DeFi offers neither.

On-demand pools on Gearbox create fixed-rate, KYC-gated credit markets with defined terms, isolated capital, and verified counterparties.

---

## Structure

Each on-demand pool consists of one lender and multiple borrowers. The pool has a fixed interest rate and a defined term (expiration date). All participants pass KYC via Securitize before any capital moves.

The lender does not deposit capital into a vault. Instead, the lender grants an ERC-20 approval from an existing wallet. Capital is pulled just-in-time when a borrower opens a position — until that moment, the lender's capital remains productive in its current allocation.

---

## Lender Capital States

Lender capital exists in exactly three states at any time:

| State | Location | Earning |
|---|---|---|
| **Approved** | In the lender's wallet, held via ERC-20 approval | No pool yield — capital is available for other uses |
| **Active** | Lent out to borrowers | Fixed rate accruing |
| **Ready to Claim** | Repaid by borrower, awaiting withdrawal | No — claim promptly |

The lender controls total exposure by adjusting the approval amount. Partial withdrawals are possible by reducing the approval.

---

## Rate Mechanics

The interest rate is fixed for the duration of the pool term. The curator commits not to change the rate during the active period. This is a social and contractual commitment, not a protocol-enforced constraint — the curator retains the technical ability to modify the rate but is bound by off-chain agreement not to do so.

**Borrower rate ≠ lender rate.** The difference is the curator's spread fee. The lender earns the pool rate; the borrower pays a higher rate that includes the curator's margin.

---

## KYC and Compliance Architecture

All participants interact through `SecuritizeWallet`, an intermediary contract that enforces compliance at the transaction level. Securitize Admin retains the ability to freeze wallets, seize assets, or block specific operations.

| Requirement | Implementation |
|---|---|
| **Know-the-Counterparty** | KYC/AML verification via Securitize required before pool access |
| **No comingling** | One lender per pool — capital never mixes with other lenders' funds |
| **Audit trail** | On-chain record of all transactions: counterparty, amount, timestamp |
| **Bot restrictions** | Automated bot permissions are blocked for compliant accounts — no third-party automated control of KYC-verified wallets |
| **Risk segregation** | Each pool is isolated. One borrower default does not cascade to other pools |

---

## Term Expiration and Liquidation

Each on-demand pool has a defined expiration date. After expiration:

1. Remaining open positions are force-closed via liquidation.
2. Post-expiry liquidation fees are set lower than bad-debt liquidation fees, reducing the cost to borrowers who fail to close before term end.
3. The lender's capital transitions to Ready to Claim status as positions are unwound.

The borrower is responsible for closing positions before expiration to avoid liquidation fees. The curator commits not to shorten the term (social/contractual commitment) but may extend it.

---

## Risk Disclosures

⚠️ **Securitize dependency (existential):** All borrower and lender operations flow through `SecuritizeWallet`. If Securitize experiences downtime, regulatory action, or service discontinuation, pool operations may be blocked entirely. This is an existential dependency — the product cannot function without it.

⚠️ **Rate commitment is not protocol-enforced:** The fixed rate is maintained by curator commitment, not by smart contract immutability. The curator retains the on-chain ability to modify the rate. Lenders rely on the curator's contractual obligation, not protocol mechanics, for rate stability.

⚠️ **Smart contract risk:** On-demand pools use audited Gearbox V3 contracts, but no audit eliminates all risk. Undiscovered vulnerabilities may affect capital.

⚠️ **Oracle risk:** Collateral valuation depends on configured price feeds. Price feed failure, staleness, or manipulation could result in delayed liquidations or incorrect collateral valuations.

---

## Comparison: Pooled Lending vs. On-Demand Pools

| Dimension | Traditional Pool | On-Demand Pool |
|---|---|---|
| **Capital** | Locked on deposit | In wallet until borrowed (ERC-20 approval) |
| **Rates** | Utilization-driven volatility | Fixed for term (curator commitment) |
| **Counterparty** | Unknown, comingled | KYC-verified, one lender per pool |
| **Risk isolation** | Socialized losses across all depositors | Isolated per pool |
| **Compliance** | No KYC, no fund segregation | Securitize KYC, full segregation |
| **Term** | Open-ended | Defined expiration with force-close |

---

## Related Questions

- [How curators configure collateral types and risk parameters](risk-configuration-dictionary.md)
- [How liquidation thresholds and health factors are calculated](../economics/liquidation-dynamics.md)
- [How price feeds are selected and validated](../economics/price-oracle.md)
- [How the curator role operates in standard pooled markets](../governance/market-curators.md)
