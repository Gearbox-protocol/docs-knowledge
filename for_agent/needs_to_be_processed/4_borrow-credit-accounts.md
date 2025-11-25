# Borrow with Credit Accounts — Leverage & Position Management

Credit Accounts are the gateway to leverage on Gearbox. They're isolated smart contract wallets that let you borrow funds from Gearbox pools to create leveraged positions. Once you have a Credit Account open, you can use that leverage to trade, farm, stake, or execute complex strategies across DeFi protocols—all with more capital than you initially deposited.

What makes Credit Accounts powerful is their flexibility. You're not locked into a single strategy or protocol. You can deploy your leverage wherever it makes sense: margin trade on Uniswap, farm on Curve, stake on Lido, or combine multiple strategies in the same account. The leverage comes from Gearbox, but where you use it is entirely up to you.

## Open a Credit Account

Opening a Credit Account is your first step toward using leverage. The process is straightforward, and once you understand the basics, you'll be able to open accounts for different strategies as needed.

### Step 1 — Pick base asset

Start by selecting the asset you want to borrow—this is your "underlying" or "debt asset." Common options include USDC, WETH, or other assets available in Gearbox pools on your network. The asset you choose determines which pool you're borrowing from, what interest rate you'll pay, and what assets you can use as collateral.

This choice matters because different assets have different characteristics. USDC is stable, which can be useful for predictable debt amounts. WETH gives you exposure to ETH price movements. The interface will show you what's available and help you understand the implications of each choice.

TODO: Add exact location where you select the base asset and list of available options

### Step 2 — Enter amount and leverage

Once you've chosen your base asset, you'll specify how much you want to leverage. This involves entering the amount of collateral you're depositing and selecting your leverage factor—how much you want to borrow relative to your collateral. Common leverage levels are 3x, 5x, or 10x, though the maximum depends on your collateral type and the protocol's current parameters.
VERIFY: confirm maximum leverage values and available leverage steps in the current app

The interface shows you everything upfront: your total position size (collateral plus borrowed amount), what your Health Factor will be after opening, the estimated interest rate you'll pay, and the maximum leverage available for your chosen collateral. This transparency helps you make informed decisions about risk and potential returns.

Higher leverage means larger positions and more potential returns, but it also means lower Health Factor and higher liquidation risk. Finding the right balance depends on your risk tolerance and strategy goals. If you're just starting out, consider starting with lower leverage until you're comfortable with how Credit Accounts work.

You'll also set a slippage tolerance if your account setup involves swaps. This protects you from unexpected price movements during transaction execution.

TODO: Add exact form fields and preview calculations shown

SCREENSHOT: Open Credit Account form showing amount, leverage selector, Health Factor preview, and Confirm button

### Step 3 — Confirm and open

After entering your parameters, review everything carefully. Check that your leverage, Health Factor, and interest rate match what you want. If it's your first time using a particular collateral asset, you'll need to approve the protocol to use those tokens—this is a one-time requirement per asset.

Then click Confirm (or Open Account) and approve the transaction in your wallet. The transaction will open your Credit Account, borrow the specified amount from the pool, deposit your collateral, and execute any initial strategy setup if you're using a strategy template.

Once opened, your Credit Account will appear in the Credit Account section of the interface, ready for you to use. You'll be able to see all your account details, manage your position, and start deploying your leverage.

VERIFY: After opening, the Credit Account appears in your account list with the correct collateral and debt

### Where to see the account and available limit

After opening a Credit Account, you can view it in the Credit Account section of the interface. You'll see your account address, current Health Factor, collateral assets and their values, debt amount and interest accruing, available borrowing capacity (how much more you can borrow), and your position value and leverage.

This dashboard gives you everything you need to monitor and manage your account. Your Health Factor is prominently displayed so you always know where you stand relative to liquidation risk. You can see how your position is performing and what actions are available.

TODO: Add exact location of Credit Account dashboard and what information is displayed

SCREENSHOT: Credit Account dashboard showing account overview, Health Factor, collateral, debt, and available actions

**Borrowing limits:** Each Credit Account has minimum and maximum debt limits set by the protocol. These limits ensure that liquidations remain profitable (minimum) while keeping individual positions within reasonable bounds (maximum). You can check your current usage and remaining capacity in the account interface.

## Manage leverage & Health Factor

Managing your Credit Account effectively means staying on top of your leverage and Health Factor. These two metrics determine both your potential returns and your risk level, so understanding how they interact helps you make better decisions.

### What Health Factor means

Your Health Factor is a simple number that tells you how safe your position is. It's calculated as the total weighted value of your collateral divided by your total debt. If your Health Factor is above 1, your account is healthy and safe. If it drops to 1, you're at the liquidation threshold. If it falls below 1, your account can be liquidated.

The higher your Health Factor, the more buffer you have if prices move against you or interest accrues on your debt. This buffer is important because leverage amplifies both gains and losses—what might be a small price movement for an unleveraged position can have a significant impact when leverage is involved.

**Formula:** Health Factor = Total Weighted Value of Collateral / Total Debt

### How swaps and market moves affect Health Factor

Your Health Factor isn't static—it changes constantly based on several factors. Understanding what moves it helps you manage risk proactively.

**Collateral price changes:** If your collateral assets drop in value, your Health Factor decreases. If they increase, your Health Factor goes up. This is the most common reason Health Factor fluctuates—market movements directly impact your collateral value.

**Debt asset price changes:** If you borrowed ETH and ETH price changes, this affects your Health Factor depending on how it correlates with your collateral. If you borrowed stablecoins like USDC, debt value stays relatively stable, which can provide more predictability.

**Interest accrual:** Your debt grows over time as interest accrues, slowly decreasing your Health Factor even if prices stay the same. This gradual decrease is something to keep in mind for longer-term positions.

**Swapping assets:** When you swap assets within your Credit Account, you might move to assets with different liquidation thresholds, which can change your Health Factor. Sometimes this is intentional—swapping to more stable assets can improve your position's safety.

**Adjusting leverage:** Adding more debt decreases your Health Factor, while repaying debt increases it. This direct relationship means you can actively manage your Health Factor by adjusting your leverage.

**Example:** If you have WETH as collateral and borrow USDC, a drop in ETH price will lower your Health Factor. If ETH drops significantly, you could approach liquidation. On the flip side, if ETH rises, your Health Factor improves, giving you more room to maneuver.

### Keeping a safe buffer

To avoid liquidation, maintain a Health Factor well above 1. The exact buffer you need depends on your risk tolerance and strategy, but here are some guidelines:

- **Conservative:** Keep Health Factor above 1.5 or higher. This gives you significant room for market movements and peace of mind.
- **Moderate:** Maintain Health Factor above 1.2–1.3. This provides a reasonable buffer while allowing for more leverage.
- **Risky:** Operating near 1.1 leaves little room for price movements and requires close monitoring.

**To increase Health Factor:**
- Add more collateral to your Credit Account
- Repay some of your debt (reduce leverage)
- Swap to assets with higher liquidation thresholds if appropriate for your strategy

**When Health Factor gets low:**
- Monitor your position more frequently
- Consider adding collateral or reducing debt proactively
- Be ready to take action if markets become volatile
- Have a plan for what you'll do if things get tight

TODO: Add exact location where Health Factor warnings are displayed in the interface

## Close / Partial unwind

One of the advantages of Credit Accounts is flexibility—you're not locked in. You can close your account entirely when you're ready, or you can partially reduce your exposure if you want to maintain a smaller position. Both options give you control over when and how to exit.

### Reduce exposure (partial unwind)

Sometimes you want to reduce your leverage without fully closing your account. Maybe market conditions have changed, or you've hit your profit target and want to lock in some gains. Partial unwinding lets you adjust your position size while keeping the account open for future use.

**Repay debt partially:** Navigate to your Credit Account, select the option to reduce debt, enter the amount to repay, and confirm the transaction. After repaying, your leverage decreases and your Health Factor increases, giving you more safety buffer.

**Remove collateral:** If your Health Factor allows, you may be able to withdraw some collateral. This might require repaying some debt first depending on your current Health Factor, but it's a way to reduce your exposure while keeping some leverage active.

**Swap to safer assets:** You can swap volatile collateral to more stable assets (like stablecoins) to improve your position's safety. This doesn't reduce your leverage, but it can improve your Health Factor by moving to assets with better liquidation thresholds.

TODO: Add exact steps and button labels for partial debt repayment and collateral withdrawal

### Fully close account

When you're ready to fully exit, you have a few options for closing your Credit Account. The best method depends on your situation and what assets you have available.

**Option 1: Swap assets and repay**
The protocol can automatically swap all your collateral assets to the underlying (borrowed) asset, repay your full debt (principal + interest + fees), and send any remaining funds to your wallet. You'll need to set a slippage tolerance for the swaps. If prices move unfavorably during execution, the transaction may revert to protect you from unexpected losses.

**Option 2: Repay with your own funds**
If you have enough of the underlying asset in your wallet, you can repay the debt directly. Navigate to your Credit Account, choose the option to repay debt, and the protocol uses your wallet balance to repay the loan. All collateral from the Credit Account is then sent to your wallet. This method avoids swaps and gives you more control over the process.

**Option 3: Keep a zero-debt account**
You can repay all debt but keep the Credit Account open with zero debt. This stops interest accrual, gives you back your capital, but keeps the account available for potential future use. This might help you retain eligibility for airdrops or rewards tied to the account, while freeing up your capital for other uses.

TODO: Add exact steps and labels for closing account options

SCREENSHOT: Close account options showing swap-and-repay, repay-from-wallet, and zero-debt options

### What happens to funds

When you close or partially unwind, here's what happens to your funds:

- **Repaid debt** goes back to the lending pool, making liquidity available for other borrowers
- **Remaining collateral** returns to your wallet (or stays in the account if you're keeping it open)
- **Interest and fees** are deducted from your position as part of the repayment
- **Any profits or losses** are realized based on how your position performed

After closing, verify that all expected funds appear in your wallet, the Credit Account shows zero debt or is removed from your account list, and the transaction appears in your History. This double-check ensures everything executed as expected.

VERIFY: After closing, funds appear in wallet and Credit Account shows zero debt or is removed from account list

---

**Next steps:** Learn about [in-app actions](../in-app-actions) you can perform within your Credit Account, such as swapping assets, farming, or staking to deploy your leverage effectively.
