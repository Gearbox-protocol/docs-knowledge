# Earn (Lend) — Earning in Pools

Earning passive yields with Gearbox is refreshingly straightforward. You deposit assets into lending pools, and they earn APY for you. There's no impermanent loss to worry about, no hidden fees eating into your returns, and no lockup periods trapping your funds. Your assets are lent to borrowers who use them for leverage, and you earn interest on what you supply—simple and transparent.

This passive approach is perfect if you want to put your assets to work without actively managing positions. The yields come from utilization-based rates (higher borrower demand means higher rates) and may include additional rewards, giving you exposure to the protocol's growth while keeping risk relatively low compared to active trading.

## Deposit to a pool

Depositing to a pool takes just a few minutes, and once you're set up, your assets start earning immediately. Here's how it works.

### Step 1 — Choose a pool

Navigate to the Pools section in the Gearbox interface, and you'll see all available lending pools for your network. Different networks support different assets, so what you see depends on where you're connected. Common options include USDC, WETH, WBTC, and others, each with their own APY rates and utilization levels.

Take a moment to review the options. You'll see current APY rates, how much of each pool is being utilized by borrowers, and how much total liquidity is available. This information helps you make an informed choice about where to deploy your capital.

TODO: Add exact navigation path to Pools section and current list of available pools

SCREENSHOT: Pools page showing available pools with APY rates and deposit options

### Step 2 — Enter deposit amount

Once you've chosen a pool, specify how much you want to deposit. You can enter a specific amount or click MAX to deposit your full available balance. Before confirming, make sure you have enough of the asset in your wallet and sufficient gas for the transaction.

The interface shows you everything you need to know upfront: your available balance, the current APY for the pool, and often an estimated earnings preview so you can see what kind of returns to expect. This transparency helps you plan ahead and make confident decisions.

TODO: Add exact location of deposit form and fields shown (balance, APY, estimated earnings)

VERIFY: Balance displayed matches your wallet balance for the selected asset

### Step 3 — Approve and deposit

For your first deposit of any asset, you'll need to approve the protocol to use your tokens. This is a standard DeFi security measure—approval is a one-time requirement per asset that grants the protocol permission to move those tokens. After that, you can deposit as many times as you want without re-approving.

The process is straightforward: click Approve and wait for the transaction to be confirmed in your wallet. Once approved, click Supply (or Deposit) and confirm the transaction. After confirmation, you'll receive Diesel Tokens (dTokens) or staked Diesel Tokens (sdTokens) representing your share of the pool. These tokens automatically accrue interest—you don't need to do anything else.

TODO: Add exact button labels and transaction flow details

SCREENSHOT: Deposit form showing Approve and Supply buttons with transaction status

### What you receive: Diesel Tokens

When you deposit to a pool, you receive Diesel Tokens (also called dTokens), which work like LP tokens on other protocols but with a key advantage: they automatically accrue interest and fees. Your Diesel Tokens grow in value over time as borrowers pay interest, and they represent your proportional share of the pool.

You can hold these tokens in your wallet—there's no need to claim interest separately because it's already baked into the token value. The longer you hold, the more value they accrue, making them a simple way to track your position without managing separate interest claims.

In V3, your dTokens are typically staked automatically (becoming sdTokens), which makes you eligible for additional rewards like GEAR tokens. This staking is handled automatically, so you benefit from extra rewards without extra steps.
VERIFY: confirm auto-staking of dTokens to sdTokens in current version

**Important:** While Gearbox has been operational for over 3 years without incidents, if a pool were to suffer losses from bad liquidations or security issues, your Diesel Tokens value could decrease. This risk exists in all DeFi lending, but Gearbox's track record and security measures help mitigate it.

## Withdraw & expected yield

Withdrawal is just as straightforward as deposit. There are no lockups or withdrawal fees from Gearbox, so you can exit whenever you're ready.
VERIFY: confirm fee policy (no protocol withdrawal fees) in the current version

### Partial or full withdrawal

To withdraw, navigate back to the pool you deposited to and use the withdrawal option. Select the pool with your deposit, click Withdraw, enter the amount you want to withdraw (or click MAX for full withdrawal), and confirm the transaction.

After confirmation, your assets are returned to your wallet, and your Diesel Tokens are burned accordingly—reducing your share of the pool by the amount you withdrew. You'll see the transaction in your history, and your funds should appear in your wallet shortly after confirmation.

TODO: Add exact navigation and button labels for withdrawal

VERIFY: After withdrawal, funds appear in your wallet and your dTokens balance decreases

### Where to see accrued yield

The beautiful thing about Diesel Tokens is that your yield is automatically compounded—you don't need to claim anything. The tokens grow in value over time as interest accrues, so simply holding them means you're earning. There's no separate claim step, no manual compounding, just automatic growth.

To see your earnings, view your Diesel Tokens balance and watch it increase over time. You can also check pool information for current APY and utilization metrics, or review your transaction history to see when you deposited and compare your token value then versus now.

For additional rewards like GEAR tokens from staking, you may need to claim those separately from a rewards section in the interface. But the core interest from lending is already in your token value.

TODO: Add exact locations in UI where yield and rewards are displayed

### APY/APR explained

**APY (Annual Percentage Yield)** is the actual rate of return you earn on your deposit, accounting for compounding. This is what you'll typically see displayed, and it's the number that reflects what you'll actually earn if you hold for a full year.

**APR (Annual Percentage Rate)** is the simple interest rate without compounding. APY is usually higher because it accounts for the fact that interest compounds over time.

Your yield comes from a few sources. Utilization-based rates mean borrowers pay interest based on how much of the pool is being used—higher utilization generally translates to higher rates, which benefits lenders. Gauge rates add another layer determined by GEAR token stakers, which can vary over time based on governance decisions. And there may be extra rewards like GEAR tokens distributed to lenders as additional incentives.
SOURCE-CONFLICT: Gauge-based lender rewards vs Permissionless curator-set fixed risk premiums and bootstrapping rewards; keep both until confirmed

**Variable yield:** It's important to understand that APY is variable and can change based on pool utilization, borrow rates (which follow a utilization curve), gauge rates (set by governance), and overall market conditions. Your actual earnings depend on how long you keep your deposit in the pool and how APY changes over that time period.

### Withdrawal timing

If pool utilization is very high (close to 100%), you might not be able to withdraw all your liquidity immediately. This doesn't mean your funds are stuck permanently or that the protocol has lost money—it simply means the liquidity is currently being used by borrowers.

In such cases, APY typically increases to attract more lenders, which helps restore balance. You can usually still withdraw partially even when utilization is high, and full withdrawal becomes available as borrowers repay or more liquidity enters the pool. This is standard behavior for lending protocols (similar to how Compound and Aave operate) and helps maintain protocol stability.

## Lender risks (light)

While lending on Gearbox is designed to be safer than active trading, it's important to understand the risks involved so you can make informed decisions.

### Smart contract risk

Gearbox Protocol consists of smart contracts on blockchain networks, and like all smart contracts, they carry inherent risks. While Gearbox has been live for over 3 years without exploits or bad debt and has undergone multiple security audits from top firms, smart contract risk always exists. The protocol team has invested over $3M in security, which provides significant confidence, but no system is completely risk-free.
VERIFY: confirm years live, audits count, and security spend in current official materials

### Variable yield

APY is not fixed and will change over time based on utilization, borrower demand, and governance decisions. Your actual earnings may differ from initial estimates depending on how market conditions evolve. This variability is normal for lending protocols, but it means your returns aren't guaranteed.

### Withdrawal timing

If pool utilization is very high, you may temporarily not be able to withdraw all your funds at once. While this is rare, you should be aware that withdrawals depend on available liquidity. In most cases, partial withdrawals remain possible even during high utilization, and full withdrawal becomes available as the situation normalizes.

### Potential losses from liquidations

In extreme cases where borrowers cannot be liquidated in time or liquidation results in bad debt, pool lenders could face losses. Gearbox has multiple safeguards to prevent this: a reserve fund to cover bad debt, an active liquidator network incentivized to keep the system healthy, and risk parameters set by experienced curators who understand the markets.

However, this risk cannot be completely eliminated in DeFi lending. Gearbox's strong track record and security infrastructure minimize the likelihood, but understanding the risk helps you make appropriate decisions about how much to lend and where.

For more detailed information about risks and security, see the [Risks & Security section](../risks-and-security).
TODO: add link to official Risks & Security page

---

**Next steps:** Once you're comfortable with lending, you might want to explore [borrowing and leverage](../borrow-credit-accounts) to see the other side of the protocol, or learn about [in-app actions](../in-app-actions) available to borrowers for deploying their leverage.
