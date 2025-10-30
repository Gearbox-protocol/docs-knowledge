# Gearbox User Docs — Two-Level Structure (User-Focused)

> Scope: end-user documentation only (no adapters, curation, or advanced configuration).  
> Each page uses the page template at the end of this file.

## 1. Introduction — What is Gearbox?
**Purpose.** Explain what Gearbox is, who it is for, the value proposition (Credit Accounts, leverage on top of DeFi), and high-level risks.

### Subpages
- **What Gearbox lets you do** — 4–6 short value scenarios (earn in pools; open leveraged exposure; partially unwind; etc.).
- **Key concepts (light)** — Credit Account, Health Factor, liquidation, limits, fees (brief, non-technical).
- **Safety note & disclaimers** — smart-contract and market risk, liquidation risk; links to Risks & Security and FAQ.

**Required UI actions.** None (overview; include annotated screenshots of main screens).  
**Checks.** Where to see app version, connected network, wallet status; how to switch networks.

---

## 2. Getting Started
**Purpose.** Get the user up and running: networks, wallets, basic UI navigation.

### Subpages
- **Wallets & Networks** — supported networks, connect a wallet, switch network in app, gas requirements, where to see balances.
- **Interface tour** — “Pools”, “Credit Account”, “History”, “Settings”; explain key indicators on top screens.
- **Safety first** — hardware wallet, site verification, network checks, basic key hygiene; where to ask for help.

**Required UI actions.** Connect wallet; switch network; open “Pools” and “Account”.  
**Checks.** Address and network visible after connect; relevant UI sections accessible; balance displayed.

---

## 3. Earn (Lend) — Earning in Pools
**Purpose.** Show how to deposit/withdraw and understand displayed yield.

### Subpages
- **Deposit to a pool** — choose a pool, enter amount, confirm, track transaction status.
- **Withdraw & expected yield** — partial/full withdraw, where to see accrued yield; APY/APR explained at user level.
- **Lender risks (light)** — contract risk, variable yield, withdrawal order (if applicable); link to Risks & Security.

**Required UI actions.** Deposit; withdraw; view yield and status in “Pools” / “History”.  
**Checks.** Deposit state and accrued yield visible; after withdraw, funds return to wallet.

---

## 4. Borrow with Credit Accounts — Leverage & Position Management
**Purpose.** Step-by-step: open/manage/close a Credit Account; understand Health Factor.

### Subpages
- **Open a Credit Account** — pick base asset, enter amount, confirm; where to see the account and available limit.
- **Manage leverage & HF** — what Health Factor means for users; how swaps/market moves affect it; keeping safe buffer.
- **Close / Partial unwind** — reduce exposure, partially repay, fully close; what happens to funds.

**Required UI actions.** Open account; monitor HF; reduce leverage/unwind; close account.  
**Checks.** Account appears in “Credit Account”; HF updates after actions; closing returns funds to wallet.

---

## 5. In-App Actions (User Flows)
**Purpose.** Click-by-click common actions inside the account — no integration jargon.

### Subpages
- **Swap inside a Credit Account** — pick pair, enter amount, slippage, confirm; verify received asset.
- **Stake / Unstake via integrated protocols** — stake/unstake supported assets via UI; verify result inside the account.
- **Partial repay / Reduce exposure** — repay with account asset; lower leverage.

**Required UI actions.** Swap; stake/unstake; partial repay.  
**Checks.** Balances update as expected; HF changes accordingly; transactions visible in “History”.

---

## 6. Fees & Limits
**Purpose.** Clearly show which fees and limits users will see in the app.

### Subpages
- **What fees you’ll see** — operation-level fees displayed in forms/receipts; gas shown separately by wallet.
- **Operation limits** — minimum amounts for deposit/withdraw/swap/opening; how often limits update; where to check them.
- **Where fees/limits appear in the app** — exact form sections that preview calculations before confirmation.

**Required UI actions.** Open deposit/swap forms to see calculated fees/limits before confirming.  
**Checks.** Fees match final transaction; UI shows clear warnings when outside limits.

---

## 7. Risks & Security (light)
**Purpose.** Practical, user-level risk guidance.

### Subpages
- **User-level risks** — liquidation from price moves, volatility, swap price impact, variable pool yield.
- **Audits & bug bounty (links)** — brief note that audits/bug bounty exist; deep details live elsewhere.
- **Best practices** — keep HF buffer, avoid over-exposure, monitor gas/network, verify addresses.

**Required UI actions.** None (guidelines).  
**Checks.** Links to full materials open; include “What to do when HF drops” quick checklist.

---

## 8. Contracts & Addresses (read-only hub)
**Purpose.** Show **where** to verify official contract and deployment addresses to avoid phishing/outdated copies.

### Subpages
- **Where to verify addresses** — always check the official deployments/Dev Docs list (do not mirror tables here).
- **How to self-check** — copy address from UI → open in block explorer → match with official deployments list and network.

**Required UI actions.** Copy address from UI; open explorer; compare with official list.  
**Checks.** UI address equals official deployment; network matches.

---

## 9. FAQ & Troubleshooting
**Purpose.** Remove frequent questions and solve common errors fast.

### Subpages
- **Wallet & network issues** — wallet won’t connect, wrong network, no gas.
- **Transactions & approvals** — pending tx, approval error, how to “unlock” a token if needed.
- **Health Factor & liquidation** — why HF drops, immediate actions to de-risk.
- **Withdraw / redeem issues** — cannot withdraw, “insufficient liquidity” (if relevant), what to try.

**Required UI actions.** Retry confirmation, switch network, speed up/cancel with higher gas where appropriate.  
**Checks.** Operation succeeds after steps; HF returns to safer zone; tx status updates in “History”.

---

## 10. Glossary
**Purpose.** Single source of truth for wording across the docs.

### Subpages
- **Core terms** — Credit Account, Health Factor, liquidation, margin, leverage, unwind, swap, staking, slippage, fee, limit, APY/APR.
- **Roles** — Lender, Borrower, Trader.
- **UI terms** — meanings of labels/indicators in the interface.

**Required UI actions.** None.  
**Checks.** Terms reused consistently in all other sections.

---

## 11. Changelog & What’s New
**Purpose.** Short notes on visible user-facing changes with links to detailed releases.

### Subpages
- **What’s new for users** — new screens/buttons/labels or changed display formulas (UI-level only).
- **Release notes (links)** — link out to full blog/release announcements for deeper reading.

**Required UI actions.** None.  
**Checks.** Each change has a date, a concise description, and a link to details.