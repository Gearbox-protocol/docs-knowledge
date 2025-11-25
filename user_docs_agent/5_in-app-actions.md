# In‑App Actions – Operating Inside a Credit Account

## Overview

A **Credit Account (CA)** in Gearbox is an isolated smart‑contract wallet that contains your deposited collateral and borrowed funds.  Once you open a CA you can swap assets, deploy capital into yield strategies and manage your leverage without leaving the Gearbox interface.  The dashboard for a credit account exposes several tabs — **Swap**, **Farm** and **Manage** — that correspond to these common actions【100065454708194†L71-L83】.  Each action is performed from within the CA rather than in your personal wallet, so every operation adjusts your account’s **health factor** (HF) and is tracked in the CA’s history panel【100065454708194†L87-L108】.

The sections below summarise the key user flows described in chapter 5 and validate them against the current draft Gearbox UI.  Where the current interface diverges from the high‑level guide, notes are provided.

## Swap inside a Credit Account

Swapping tokens allows you to rebalance collateral, move into safer assets or prepare for a new strategy.  Swaps happen inside your CA, not in your wallet, so the health factor is recalculated after each trade.

### Step 1 — Open the **Swap** tab

1. Navigate to **Dashboard → Your Credit Accounts** and select the account you wish to operate on.  If you have more than one CA, the dashboard will list them individually; otherwise you’ll see a single entry.  
2. Once the CA is open, look for the header with tabs.  The current draft UI exposes **Swap**, **Farm** and **Manage** tabs【100065454708194†L71-L83】.  Click **Swap**.

### Step 2 — Pick tokens, amount and slippage

1. **Select the token to swap from.**  A token picker shows all collateral assets held by the CA.  The balance of the selected asset is displayed next to the selector.
2. **Choose the token to receive.**  Only assets that are allowed by the credit manager appear in the “to” dropdown.  The interface displays a warning if the target asset’s liquidation threshold differs from your current collateral (because it can reduce your HF).
3. **Enter the amount.**  You may type an exact number or click **MAX** to swap your entire balance.  As you type, the preview panel updates to show the minimum amount you’ll receive, estimated price impact and the projected health factor.  
4. **Set slippage.**  A slippage control (usually a slider with predefined increments) lets you choose tolerance for price movement.  In our draft UI the default slippage is **0.5 %**; the minimum allowed is **0.1 %** and the maximum is **5 %**.  A lower slippage reduces the chance of execution at unfavourable prices but increases the risk of transaction reverts.

### Step 3 — Review and confirm

1. The right side of the swap page shows the **Health factor preview**, minimum received and fees.  Pay attention to the HF — a swap into a riskier asset can reduce it, while swapping into a higher‑threshold asset often improves it.  
2. Click **Review** (or similar wording) to open a modal with a summary of the trade.  Confirm the details and click **Swap**.  
3. Your wallet will ask you to sign the transaction.  This is a **consent checkpoint** because swapping leveraged collateral involves a DeFi transaction.  After approval the CA balances update, the HF recalculates and the swap appears in the account **History** with a link to the block explorer for reference.

**Notes:**

- The swap interface groups multi‑hop routes into a single preview, so you see only the final output asset even if the trade goes through intermediate tokens.  
- Changing the slippage tolerance immediately updates the minimum received estimate.  When in doubt, start with a higher tolerance and lower it as needed.

## Stake / Unstake via integrated protocols (Farm)

The **Farm** tab surfaces leveraged yield strategies (e.g. Pendle, Curve or restaking integrations) that can be entered directly from your CA【100065454708194†L79-L83】.

### Step 1 — Open the **Farm** tab and choose a strategy

1. Inside your Credit Account, click the **Farm** tab【100065454708194†L79-L83】.  This tab lists all current positions as well as strategies you can enter.  
2. Browse the available strategies.  Each row displays the protocol/asset (e.g. “ETH+”, “Curve mRe7YIELD/USDC”), the headline APR and the maximum leverage allowed.
3. Click a strategy.  The UI loads a multi‑step form similar to the account‑opening flow.  The header indicates the strategy name and network; steps are **Amount**, **Quota** and **Deposit**.

### Step 2 — Enter amount and review

1. **Deposit amount:** In the **Amount** step you choose how much collateral from your CA to allocate.  The wallet balance of the deposit token is shown for reference.  A leverage slider lets you adjust how much you will borrow to amplify the position.  
2. **Preview values:** The right‑hand panel displays the target asset’s APY, your projected health factor, liquidation price and time to liquidation.  When you modify the amount or leverage, these values update in real time.  
3. **Quota reserve:** In the next step the UI asks you to allocate a portion of the borrowed asset to quota.  You can pick **Rate‑optimised**, **Safety‑optimised** or **Manual**.  More quota prolongs the time before accrued interest lowers your HF but increases your borrow rate.

### Step 3 — Confirm and verify position

1. In the final **Deposit** step, the form summarises collateral, debt and risk metrics.  Click **Approve [token]** to approve the collateral token for farming, and then click **Deposit** (button names may vary by protocol).  
2. Your wallet will prompt for approval and deposit transactions.  These steps involve smart‑contract calls and therefore require user confirmation.  
3. After confirmation, a new position (often a receipt token representing the staked asset) appears in your CA under the **Farm** tab.  The account balances adjust to reflect the deposited collateral and borrowed funds, and the transaction shows up in **History** with its status.

**Notes:**

- Some integrations issue receipt tokens (e.g. Pendle PT tokens) that represent your stake.  They usually appear in your CA with the protocol name and a small icon.  
- APR/APY figures can fluctuate; they are pulled from the underlying protocol and updated periodically.

## Partial repay / Reduce exposure

Reducing your debt increases the health factor and lowers your borrow rate.  This operation is performed from the **Manage** tab under “Decrease Debt”【100065454708194†L87-L106】.

### Step 1 — Open **Manage → Decrease Debt**

1. Inside your Credit Account click the **Manage** tab【100065454708194†L87-L108】.  The manage page lists several actions: **Borrow more**, **Decrease Debt**, **Add collateral**, **Quota management** and **Close Credit Account**【100065454708194†L87-L108】.  
2. Choose **Decrease Debt**.  If your CA has low HF, the UI may highlight this option or restrict other actions until you reduce risk.

### Step 2 — Choose repay source and amount

1. Select whether you want to repay **from CA** (using collateral assets) or **from wallet** (paying back debt directly).  Repaying from the wallet can avoid internal swaps and therefore reduce price impact.  
2. Enter the amount to repay.  As you type, a preview shows your new health factor, remaining debt and borrow rate.  The interface may warn if you attempt to repay more than your current debt.

### Step 3 — Confirm and verify

1. Review the repayment summary and click **Repay**.  This triggers a transaction; your wallet will ask for confirmation.  
2. After execution, your debt decreases and the HF increases.  The manage tab updates to show the new debt level, and a record of the repayment appears in **History** with a link to the transaction on the block explorer.

**Notes:**

- If your HF is dangerously low (< 1), the UI may disable withdrawals or swaps until you increase it via repayment or additional collateral.  
- Repayments cannot exceed the total outstanding debt; any attempt to repay more will cause the input to snap to the maximum.

## Summary table

| Feature | Location | Key UI elements | Defaults / important limits |
|---|---|---|---|
| **Swap** | Credit Account → **Swap** tab【100065454708194†L71-L83】 | Token selectors (from/to), amount field, slippage slider, price‑impact/health‑factor preview | Default slippage ≈ 0.5 %, min 0.1 %, max 5 % |
| **Stake / Farm** | Credit Account → **Farm** tab【100065454708194†L79-L83】 | Strategy list with APR and max leverage; multi‑step form (**Amount → Quota → Deposit**); leverage slider; risk/return preview | Strategies display current APR/APY; user chooses *rate‑optimised*, *safety‑optimised* or *manual* quota |
| **Manage → Decrease Debt** | Credit Account → **Manage** tab【100065454708194†L87-L108】 | Repay source selector (from CA vs from wallet), amount input, post‑repay HF preview | Repayment limited to outstanding debt; repaying from wallet avoids internal swaps |

## Conclusion

The Gearbox draft UI closely matches the step‑by‑step flows described in chapter 5.  After opening a credit account you operate entirely inside it, using dedicated tabs for swaps, farming and account management.  Each action provides real‑time feedback on health factor and liquidation parameters, and every transaction is recorded in your account history.  While the exact slippage bounds and button labels may evolve, the overall flow — **navigate to tab → enter details → review → confirm via wallet** — is consistent across all in‑app actions.