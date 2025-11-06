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
- APY/APR: Annualized yield metrics; APR excludes compounding; APY includes compounding over time.

VERIFY: confirm exact formula display or location for HF, and fee/limit previews in the current UI

---

## Roles

- Lender: Supplies assets to a pool to earn yield from borrowers; can withdraw subject to available liquidity and gas.
- Borrower: Opens a Credit Account, uses leverage to swap/stake across supported integrations, and manages HF to stay safe.
- Trader: A borrower focused primarily on swaps/price exposure, potentially with higher turnover and tighter slippage.

---

## UI terms (labels & indicators)

- Network indicator: Shows which network the app and wallet are using; they must match for actions to work.
- Wallet status: Shows your connected address and connection state; use it to verify you’re on the intended account.
- APY / Utilization (Pools): Pool‑level yield and usage metrics to help gauge expected returns and liquidity conditions.
- HF display (Account): Health Factor readout on your Credit Account dashboard with warnings if you approach risk.
- Min received / Price impact (Swap): Preview values indicating execution safety and expected outcome for swaps.
- Confirm / Approve buttons: Approve grants token allowance to a contract; Confirm submits the action itself.

TODO: add exact UI locations for these labels (header, Pools list, Credit Account dashboard, Swap form)
VERIFY: confirm the current phrasing and capitalization of labels in the live app
SCREENSHOT: Top bar with wallet and network; Account dashboard with HF; Swap form with min received/price impact

---

### See also
- Getting Started — Interface tour and key indicators
- Fees & Limits — where fees/limits appear in the app
- In‑App Actions — Swap; Partial repay
TODO: add links to the corresponding pages once finalized
