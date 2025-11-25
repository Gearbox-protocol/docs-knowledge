# FAQ & Troubleshooting

Quick answers and fast fixes for common issues. Use this page as a checklist when something doesn’t work as expected.

---

## Wallet & network issues

### Issue: Wallet won’t connect or shows the wrong account/network

**Step 1 — Verify the site and connection**
Make sure you are on the official Gearbox interface. Check that the URL is served over HTTPS (a padlock icon is visible in the browser) and confirm that your wallet is unlocked.  
The connected wallet address appears in the top‑right header (e.g., `0xf39F…2266`).
SCREENSHOT: /images/faq/wallet-and-network.png — Top bar showing the connected wallet address; the network selector is available from the **Borrow** page via the “Network” dropdown next to “Multicollateral Loans”.

**Step 2 — Check and switch network**
Open the network selector in the app or switch networks in your wallet so that both match.  
On the **Borrow** page, click the **Network** dropdown next to “Multicollateral Loans” to choose the desired network (e.g., Ethereum, Arbitrum One, OP Mainnet).  
VERIFY (failed): cannot verify network matching in current UI build.

**Step 3 — Disconnect and reconnect**
Disconnect the wallet from the app (and from the wallet’s connected sites list), then reconnect.
VERIFY (failed): disconnect/reconnect cannot be tested in current UI build.

Notes:
- Browser extensions or privacy settings can block wallet popups — try enabling the site or using a different browser profile.
- Hardware wallets require the correct app/network open on the device.

---

## Transactions & approvals

### Issue: Transaction stuck as pending

**Step 1 — Check mempool and gas**
Open your wallet’s activity to see the pending transaction and current gas conditions. Consider speeding up with a higher fee or cancelling if supported by your wallet.
VERIFY (failed): not available in current UI build.

**Step 2 — Avoid nonce conflicts**
If you broadcasted multiple txs, ensure the nonce order is correct. Cancelling or replacing the oldest pending tx often helps the rest proceed.

**Step 3 — Re‑submit**
If the action failed due to price movement or slippage limits, adjust parameters (e.g., slippage) and try again.
SCREENSHOT: SKIP — History screen not present in current UI build.

### Issue: Approval error or allowance mismatch

**Step 1 — Identify the token and spender**
Find which token and spender (contract) needs approval. Use the in‑app prompt and confirm the spender address via the official deployments list.
TODO: link to official deployments list (not in UI, requires docs maintainers)
VERIFY (failed): cannot confirm spender address in current UI build

**Step 2 — Revoke stale approvals if needed**
If approval persists in an error loop, consider revoking the old allowance via your wallet or a trusted allowances tool, then re‑approve in the app.
TODO: link to the recommended allowances management page if available (not in UI)

**Step 3 — Re‑approve and retry**
Approve again, then re‑run the original action.

---

## Health Factor & liquidation

### Issue: Health Factor dropped too low

**Step 1 — Pause and assess**
Check your current HF and the major collateral/debt prices on the dashboard.
HF and liquidation price are displayed in the account summary panel on the right side of the Borrow flow.

**Step 2 — Add collateral or partially repay**
Adding collateral or repaying debt immediately improves HF. Use the Manage (Repay) flow.
TODO: add exact navigation path and labels for Manage (Repay) (requires UI update)

**Step 3 — Swap to safer assets**
If appropriate for your strategy, swap to assets with higher liquidation thresholds.

**Step 4 — Recheck HF and keep a buffer**
After actions settle, confirm your HF is back in a comfortable zone (e.g., ≥ 1.3–1.5 in volatile markets).

### Issue: Liquidation happened

- A liquidator repaid your debt and took a premium; any remaining funds return to your account.
- Review the History entry and explorer link to see details.
VERIFY (failed): History screen not available in current UI build.

---

## Withdraw / redeem issues

### Issue: Cannot withdraw fully from a pool

**Reason — high utilization**
When utilization is very high, full withdrawal may be temporarily unavailable.

**What to do**
- Withdraw partially; try again later as liquidity frees up.
- Monitor APY/utilization — higher APY often draws in new liquidity.
VERIFY (partial): the “Supply APY” column appears in the Pools list; there is no explicit utilization indicator.

### Issue: Strategy or staked position won’t unwind

- Some strategies require an intermediate step (e.g., unstake or redeem receipt tokens) before withdrawing the base asset.
- Check the in‑app instructions for the specific integration and follow the unwind path.
VERIFY (failed): specific integration‑specific instructions not present in current UI build.

---

## General diagnostics checklist

- Confirm the network and the connected address in the header.
- Open the official deployments list to verify any contract address involved.
- Review History for errors and open the explorer link for details.
- Try a smaller test amount to reduce slippage/price impact and isolate issues.
- Reconnect your wallet or try a clean browser profile if UI elements don’t load.
TODO: link to official deployments list (not in UI)
SCREENSHOT: SKIP — History screen not present in current UI build.

---

### See also
- Getting Started — Wallets & Networks
- In‑App Actions — Swap; Partial repay / Reduce exposure
- Risks & Security — What to do when HF drops
TODO: add links to the corresponding pages once finalized
