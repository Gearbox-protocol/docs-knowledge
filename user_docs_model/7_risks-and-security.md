# Risks & Security (Light)

This chapter gives you practical guidance on user‑level risks and how to stay safe while using Gearbox. It also points you to audits and bug bounty materials for deeper reading.

---

## User‑level risks

Using leverage amplifies both gains and losses. Understanding where risk comes from helps you prepare and react calmly.

### Market moves and Health Factor
Price changes can lower the value of your collateral or raise the value of your debt, which reduces your Health Factor. If HF reaches 1, your Credit Account becomes liquidatable. The simplest protection is a safety buffer.

- Conservative: keep HF ≥ 1.5 for a wide safety margin.
- Moderate: HF around 1.2–1.3, but monitor more often.
- Risky: near 1.1 requires close attention and quick reactions.

TODO: add link to the Manage leverage & HF page

### Swap price impact and execution
When swapping, price impact and slippage can move the execution price. Tight slippage settings protect you but may cause the transaction to revert if the market moves.

- For large swaps, consider splitting into smaller parts or widening slippage slightly if execution risk is high.
- Watch the preview: minimum received, price impact, and estimated fees.

VERIFY: confirm exact preview labels and where they appear in the current UI

### Variable pool yield (for lenders)
APY moves with utilization and borrowing demand. It can go up or down; your realized return depends on how APY evolves over time.

- High utilization may temporarily limit full withdrawals; partial withdrawals are usually possible until liquidity returns.
- Rewards — if present — may require a separate claim.

VERIFY: confirm where APY and utilization are displayed for pools in the current UI

### Liquidation event
If HF < 1, your account may be liquidated. A liquidator repays debt and takes a premium; your remaining funds (if any) go back to you.

- Avoid getting near HF = 1 by adding collateral, partially repaying, or swapping to safer assets ahead of time.
- During volatility, consider de‑risking earlier than usual.

TODO: add link to Close / Partial unwind page

---

## Audits & bug bounty (links)

Gearbox has undergone multiple audits from recognized firms and operates a bug bounty program. Use these materials to assess security posture in depth.

- Audits: summary and links to reports.
- Bug bounty: scope and reporting process.

TODO: add links to official audits and bug bounty pages
VERIFY: confirm years live, audits count, and security spend in current official materials

---

## Best practices (quick wins)

Small habits go a long way. Treat the list below as a quick checklist before you act.

- Keep a buffer: maintain HF above your comfort threshold (e.g., ≥ 1.3 if markets are choppy).
- Verify the site: always check the official domain and SSL; bookmark it to avoid phishing.
- Confirm the network: make sure wallet and app network match; keep enough native gas token for your actions.
- Double‑check addresses: copy from the UI, open in a block explorer, and compare with the official deployments list.
- Watch slippage: use tight slippage for volatile markets; review minimum received and price impact.
- Plan exits: know how you will partially repay, swap to safer collateral, or fully close.

TODO: add link to official deployments list
VERIFY: confirm where the HF value and warnings are shown in the current UI

---

### What to do when HF drops (fast checklist)

- Step 1 — Pause and assess: check your current HF and the main collateral/debt prices.
- Step 2 — Add collateral or repay: increasing equity or reducing debt raises HF quickly.
- Step 3 — Swap to safer assets: if appropriate, move to assets with higher liquidation thresholds.
- Step 4 — Recheck HF and keep a buffer: confirm that HF is back in a comfortable zone.

SCREENSHOT: Credit Account dashboard with HF value visible and Manage actions

---

### See also
- Borrow with Credit Accounts — Manage leverage & Health Factor
- Fees & Limits — where fees/limits appear in the app
- In‑App Actions — Partial repay / Reduce exposure
TODO: add links to the corresponding pages once finalized
