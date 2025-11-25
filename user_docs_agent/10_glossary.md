# Glossary

Short, user‑level definitions for terms you’ll see across the docs and in the app.

---

## Core terms

- Credit Account: An isolated smart‑contract wallet that holds your collateral and borrowed funds, and executes actions (swap, stake, repay) under risk constraints.
- Health Factor (HF): Safety ratio = discounted collateral value / total debt. If HF > 1, you’re safe; at HF = 1, your account is liquidatable.
- Liquidation: Process when HF < 1. A liquidator repays your debt, takes a premium, and any remaining funds return to you.
- Margin: Using borrowed funds in addition to your own capital to increase position size.
- Leverage: Position size divided by your own capital. Higher leverage means higher potential PnL and higher risk.
- Unwind (Partial unwind): Reducing exposure by repaying part of the debt, withdrawing some collateral, or both.
- Swap: Exchanging one token for another inside your Credit Account under slippage limits.
- Staking: Depositing tokens into a supported protocol to earn yield (often via an integration that issues a receipt token).
- Slippage: Difference between expected and actual execution price; controlled by your slippage tolerance.
 - Fee: Any protocol, integration, or liquidation charge shown in forms or receipts; wallet gas is separate.
 - Limit: A boundary such as minimum amount, maximum debt, LTV/liquidation thresholds, or per‑transaction constraints.
 - APY/APR: Annualized yield metrics; APR excludes compounding while APY includes compounding over time.

VERIFY (partial): HF is displayed on the Credit Account dashboard as a ratio (no explicit formula). Fee and limit previews appear in deposit/borrow forms and vary by network.

---

## Roles

- Lender: Supplies assets to a pool to earn yield from borrowers; can withdraw subject to available liquidity and gas.
- Borrower: Opens a Credit Account, uses leverage to swap/stake across supported integrations, and manages HF to stay safe.
- Trader: A borrower focused primarily on swaps/price exposure, potentially with higher turnover and tighter slippage.

---

## UI terms (labels & indicators)

- Network indicator (top bar): Displays the network that the app is connected to alongside your wallet address in the header. Your wallet and app network must match for actions to work.
- Wallet status (top bar): Shows your connected address and connection state in the header; use it to verify you’re on the intended account.
- Supply APY / Utilization Rate (Pools): Pool‑level yield ("Supply APY") and usage ("Utilization Rate") metrics displayed in the pools list to help gauge expected returns and liquidity conditions.
- HF display (Credit Account dashboard): Health Factor readout on your Credit Account dashboard; an on‑screen indicator warns you if you approach a risky HF.
- Min received / Price impact (Swap form): Preview values at the bottom of the swap form indicating execution safety and expected outcome for swaps.
- Confirm / Approve buttons (forms): “Approve” grants token allowance to a contract; “Confirm” submits the action itself. These buttons appear on deposit, borrow and swap forms.

SCREENSHOT: /images/glossary/top-bar-wallet-network.png — top bar showing wallet address and network indicator.
SCREENSHOT: /images/glossary/account-dashboard-hf.png — Credit Account dashboard showing the Health Factor (HF) readout.
SCREENSHOT: /images/glossary/swap-form-min-received.png — swap form inside a Credit Account showing “Min received” and “Price impact” preview values.

---

### See also
- Getting Started — Interface tour and key indicators
- Fees & Limits — where fees/limits appear in the app
- In‑App Actions — Swap; Partial repay
TODO: add links to the corresponding pages once finalized (not in UI, requires docs maintainers)
