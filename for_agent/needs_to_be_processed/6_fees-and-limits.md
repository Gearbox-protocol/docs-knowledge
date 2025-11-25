# Fees & Limits — What You’ll See in the App

Understanding fees and limits helps you plan actions confidently and avoid surprises. This chapter shows what appears in forms and receipts, how limits work in practice, and where to check them before you confirm.

---

## What fees you’ll see

Fees appear contextually in the form you’re using (Deposit, Swap, Open/Manage Credit Account, Close). Gas is always shown by your wallet separately.

### Operation-level fees (for borrowers)

- Borrow interest: depends on pool utilization and collateral‑specific settings. You’ll see the current/estimated rate in the form preview before confirming.
- Collateral‑specific premiums: some collaterals can include an additional risk premium set by curators in Permissionless markets.
- Liquidation fee: applies only if your Health Factor falls below 1 and the account is liquidated.
- Integration fees (if any): some integrations may display protocol‑specific fees in the preview.

SOURCE-CONFLICT: Legacy quota/gauge-based rates vs Permissionless curator-set fixed premiums and bootstrapping rewards; keep both until confirmed

VERIFY: confirm exact fee labels and where they appear in the current UI
SCREENSHOT: Borrow action form showing interest rate, any additional premium, and Confirm button

### Lenders (pool deposits/withdrawals)

Gearbox doesn’t charge a protocol fee for deposit or withdrawal; gas is handled by your wallet. As a lender, your yield comes from interest paid by borrowers, and any rewards — if present — are shown where applicable.

VERIFY: confirm fee policy (no protocol withdrawal fee) in the current version
SCREENSHOT: Pool form preview showing APY and estimated earnings (if present)

---

## Operation limits

Limits protect users and keep markets healthy. You’ll see relevant limits in the same form where you set the amount.

### Common limits you may encounter

- Minimum transaction amounts: the smallest deposit/withdraw/swap/open allowed.
- Per‑account constraints: minimum/maximum debt, and available borrowing capacity.
- Collateral‑specific parameters: liquidation thresholds, LTVs, and any additional rate/policy that affects the position.
- Slippage and safety checks: swaps and multicalls use slippage limits; if beyond safe bounds, the transaction reverts.

VERIFY: confirm where min/max amounts, LTV/liquidation threshold, and per‑account debt bounds are displayed in the current UI
SCREENSHOT: Form showing entered amount and a warning when outside allowed limits

Notes:
If your Health Factor is at risk, the UI may restrict withdrawals or collateral removal until HF improves. Slippage guards help you avoid unexpected execution prices on swaps or multi‑step routes.

---

## Where fees/limits appear in the app

You don’t need to guess — the app previews fees and limits before you confirm.

### Step 1 — Open the relevant form
Open the Deposit, Swap, Open Credit Account, or Close/Manage form, depending on your goal.
TODO: add exact navigation path and section labels in the current UI

### Step 2 — Enter amount and review preview
Enter your amount and review the preview values: estimated interest/fees (if any), slippage, and any limits that apply. If something is outside the allowed range, the UI shows a warning.
VERIFY: confirm locations and labels for fees/limits preview in the current UI
SCREENSHOT: Example form with fee/limit preview and a visible warning state

### Step 3 — Confirm and verify
Confirm and approve in your wallet when ready. After confirmation, verify the receipt and History entry.
VERIFY: fees match the final transaction; entry appears in History with explorer link

---

### Practical tips

Always check your Health Factor after changes — swaps or leverage adjustments can move it quickly. For large swaps, consider a slightly higher slippage if execution risk is high; otherwise, keep slippage tight to minimize price impact. If you hit a limit, adjust the amount or change the sequence (for example, repay a bit of debt, then withdraw collateral).

---

### See also
In‑App Actions — step‑by‑step flows for Swap and Partial Repay
Borrow with Credit Accounts — managing leverage and Health Factor
TODO: add links to the corresponding pages once finalized
