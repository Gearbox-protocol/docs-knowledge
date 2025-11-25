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

In the current UI, the borrow form displays a base borrow rate (labelled **“Borrow rate from X%”**) plus per‑asset quota rates under the expanded **Borrow rate** section.  When you expand **More details**, you also see the **Liquidation Premium** and **Liquidation Fee** listed separately.  These elements replace legacy gauge‑based rates; the preview shows the exact rate numbers before you confirm.
SCREENSHOT: /images/fees-limits/borrow-form-details.png — Amount step of the USDC Credit Account with pt.wstUSR collateral; shows the “Borrow rate from 0%” label, the per‑asset quota rate in the **Borrow rate** section, and the **Liquidation Premium 3.00%** and **Liquidation Fee 0.02%** listed under **More details**.

### Lenders (pool deposits/withdrawals)

Gearbox doesn’t charge a protocol fee for deposit or withdrawal; gas is handled by your wallet. As a lender, your yield comes from interest paid by borrowers, and any rewards — if present — are shown where applicable.
Verified (agent): the supply/withdraw liquidity form shows no protocol fees for deposit or withdrawal; gas fees are paid separately by your wallet.  The form preview displays the current APY and the amount of LP tokens you’ll receive without any additional protocol fee.
SCREENSHOT: /images/fees-limits/pool-deposit-preview.png — Supply liquidity form for a kpk pool on mainnet showing the deposit amount, resulting LP tokens, current APY and no protocol fee.

---

## Operation limits

Limits protect users and keep markets healthy. You’ll see relevant limits in the same form where you set the amount.

### Common limits you may encounter

- Minimum transaction amounts: the smallest deposit/withdraw/swap/open allowed.
- Per‑account constraints: minimum/maximum debt, and available borrowing capacity.
- Collateral‑specific parameters: liquidation thresholds, LTVs, and any additional rate/policy that affects the position.
- Slippage and safety checks: swaps and multicalls use slippage limits; if beyond safe bounds, the transaction reverts.
The borrow form shows the minimum and maximum debt limits directly: expanding **More details** reveals **Debt Limit**, **Min Debt** and **Max Debt**.  When you enter a borrow amount below the minimum, a warning appears below the input (for example, *“Min borrow amount is 30.00K USDC”*).  Loan‑to‑value (current and max LTV) values appear in the left‑hand panel of the **Amount** step.
SCREENSHOT: /images/fees-limits/min-borrow-warning.png — Amount step after entering a small borrow amount; shows the “Min borrow amount is 30.00K USDC” warning and lists **Debt Limit**, **Min Debt** and **Max Debt** under **More details**.

Notes:
If your Health Factor is at risk, the UI may restrict withdrawals or collateral removal until HF improves. Slippage guards help you avoid unexpected execution prices on swaps or multi‑step routes.

---

## Where fees/limits appear in the app

You don’t need to guess — the app previews fees and limits before you confirm.

### Step 1 — Open the relevant form
Open the Deposit, Swap, Open Credit Account, or Close/Manage form, depending on your goal.  From the **Earn** page, click a pool row to open its **Manage** screen; the form tabs there are **Supply liquidity** and **Withdraw liquidity**.  From the **Borrow** page, select the asset you want to borrow and one or more collateral tokens, then click **Next Step** to open the **Amount** form.

### Step 2 — Enter amount and review preview
Enter your amount and review the preview values: estimated interest/fees (if any), slippage, and any limits that apply.  Fee and limit previews appear inside the form: in the borrow **Amount** step, the right‑hand panel labeled *USDC Credit Account* shows the borrow rate and per‑asset quota rates; expanding **More details** reveals liquidation premium/fee and debt limits.  In deposit/withdraw forms, the current APY and expected LP token amount appear under the input fields.  When a value is outside allowed limits, a warning message (such as a minimum amount message) appears below the input.
SCREENSHOT: /images/fees-limits/fee-limit-preview.png — Borrow *Amount* step showing the borrow rate panel, Debt Limit section, and a warning below the input when the amount is outside allowed limits.

### Step 3 — Confirm and verify
Confirm and approve in your wallet when ready. After confirmation, verify the receipt and History entry.
VERIFY (failed): not tested in this environment; real transaction confirmation and history entry require submitting a live transaction, which was not done.

---

### Practical tips

Always check your Health Factor after changes — swaps or leverage adjustments can move it quickly. For large swaps, consider a slightly higher slippage if execution risk is high; otherwise, keep slippage tight to minimize price impact. If you hit a limit, adjust the amount or change the sequence (for example, repay a bit of debt, then withdraw collateral).

---

### See also
In‑App Actions — step‑by‑step flows for Swap and Partial Repay
Borrow with Credit Accounts — managing leverage and Health Factor
TODO: add links to the corresponding pages once finalized
