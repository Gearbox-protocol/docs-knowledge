# In‑App Actions — Working Inside a Credit Account

This chapter walks you through the most common user flows inside your Credit Account. The actions below are written in a smooth, step‑by‑step format so you always know what to do, why it matters, and what result to expect.

SCREENSHOT: Credit Account screen showing tabs for Swap / Stake (or Strategies) / Manage

---

## Swap inside a Credit Account

Swapping assets lets you rebalance your position, enter strategies, or move to safer collateral without leaving your Credit Account.

### Step 1 — Open Swap
Open your Credit Account and go to the Swap section.
TODO: add exact navigation path and tab/section label in the current UI

### Step 2 — Pick tokens, amount, and slippage
Select the token you want to swap from and to, then enter the amount. Set a slippage tolerance that matches your risk preference — lower slippage protects against price moves but may cause the transaction to revert.
VERIFY: confirm default slippage and min/max slippage bounds in the current UI
SCREENSHOT: Swap form with token selectors, amount field, slippage control, and price impact info

### Step 3 — Review and confirm
Review the preview (minimum received / price impact / fees if shown). Confirm and approve in your wallet if needed. After confirmation, your Credit Account balances update to reflect the new asset.
VERIFY: balances in the Credit Account update as expected and Health Factor changes accordingly
VERIFY: transaction appears in History with status and a link to the block explorer

Notes:
Swapping into assets with different liquidation thresholds can change your Health Factor. If your account includes a multi‑step route (for example, intermediate hops), the UI may present it as one flow.
TODO: add exact labels for preview rows (min received, price impact) if present in the current UI

---

## Stake / Unstake via integrated protocols

Staking and unstaking through supported integrations lets you deploy leverage into yield strategies without leaving the Gearbox app.

### Step 1 — Open Stake (or Strategies)
Open your Credit Account and navigate to Stake (or Strategies), then choose the supported protocol/asset.
TODO: add exact navigation path and section label in the current UI

### Step 2 — Enter amount and review
Enter the amount you want to stake or unstake. Review any preview values shown (est. APR/APY, lockup notes, position value, or fees if applicable).
VERIFY: confirm where APR/APY and any integration‑specific fees are displayed in the current UI
SCREENSHOT: Stake form with asset selector, amount field, and Confirm button

### Step 3 — Confirm and verify position
Confirm the action and approve in your wallet if required. Your Credit Account position updates accordingly (staked asset or receipt token appears; available balance decreases).
VERIFY: new position (or receipt token) appears in the Credit Account view; balances reflect the change
VERIFY: transaction appears in History with status and explorer link

Notes:
Some integrations may issue receipt tokens that track your staked position. If rewards accrue separately, you may need to claim them in a dedicated UI section.
TODO: add exact labels for the resulting position (receipt token name) if displayed

---

## Partial repay / Reduce exposure

Partial repayment lowers your leverage and increases your Health Factor, giving you a safer buffer against market moves.

### Step 1 — Open Manage (Repay)
Open your Credit Account and navigate to Manage (Repay) or an equivalent section that lets you reduce debt.
TODO: add exact navigation path and section/button label in the current UI

### Step 2 — Choose repay source and amount
Choose to repay using assets in your Credit Account (or from wallet, if supported). Enter the amount you want to repay and review the preview of your new Health Factor and remaining debt.
VERIFY: confirm where the post‑repay Health Factor preview is displayed in the current UI
SCREENSHOT: Repay form showing amount, post‑action HF preview, and Confirm button

### Step 3 — Confirm and verify
Confirm the repayment and approve in your wallet if required. After confirmation, your debt decreases and Health Factor increases.
VERIFY: debt decreases, Health Factor increases, and the transaction appears in History with status

Notes:
If your current Health Factor is low, the UI may temporarily limit withdrawals until you reduce risk. Repaying from the wallet may avoid swaps and reduce price impact.
TODO: add exact labels for repay‑from‑wallet vs repay‑from‑account options if both are present

---

### See also
Open / Manage / Close a Credit Account — related flows
TODO: add links to the corresponding pages once finalized
