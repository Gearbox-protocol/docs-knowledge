# Earn (Lend) — Earning in Pools

Earning passive yields with Gearbox is refreshingly straightforward. You deposit assets into lending pools, and they earn APY for you. There's no impermanent loss to worry about, no hidden fees eating into your returns, and no lockup periods trapping your funds. Your assets are lent to borrowers who use them for leverage, and you earn interest on what you supply—simple and transparent.

This passive approach is perfect if you want to put your assets to work without actively managing positions. The yields come from utilization-based rates (higher borrower demand means higher rates) and may include additional rewards, giving you exposure to the protocol's growth while keeping risk relatively low compared to active trading.

## Deposit to a pool

Depositing to a pool takes just a few minutes, and once you're set up, your assets start earning immediately. Here's how it works.

### Step 1 — Choose a pool

Navigate to the **Earn → Pools** section in the Gearbox interface, and you'll see all available lending pools for your current network. Different networks support different assets, so what you see depends on where you're connected. Common options include USDC, WETH, WBTC, wstETH and others, each with their own APY rates and utilization levels.

Take a moment to review the options. You'll see current APY rates, how much of each pool is being utilized by borrowers, and how much total liquidity is available. This information helps you make an informed choice about where to deploy your capital.

### Step 2 — Enter deposit amount

Once you've chosen a pool, specify how much you want to deposit. You can enter a specific amount or click **MAX** to deposit your full available balance. Before confirming, make sure you have enough of the asset in your wallet and sufficient gas for the transaction.

The interface shows you everything you need to know upfront: your available balance, the current APY for the pool, and an earnings preview so you can see what kind of returns to expect. This transparency helps you plan ahead and make confident decisions.

### Step 3 — Approve and deposit

For your first deposit of any asset, you'll need to approve the protocol to use your tokens. This is a standard DeFi security measure—approval is a one-time requirement per asset that grants the protocol permission to move those tokens. After that, you can deposit as many times as you want without re-approving.

The process is straightforward: click **Approve** and wait for the transaction to be confirmed in your wallet. Once approved, click **Deposit** (or **Supply**, depending on the pool card) and confirm the transaction. After confirmation, you'll receive Diesel Tokens (dTokens) or staked Diesel Tokens (sdTokens) representing your share of the pool. These tokens automatically accrue interest—you don't need to do anything else.

## What you receive: Diesel Tokens

When you deposit to a pool, you receive Diesel Tokens (also called dTokens), which work like LP tokens on other protocols but with a key advantage: they automatically accrue interest and fees. Your Diesel Tokens grow in value over time as borrowers pay interest, and they represent your proportional share of the pool.

You can hold these tokens in your wallet—there's no need to claim interest separately because it's already baked into the token value. The longer you hold, the more value they accrue, making them a simple way to track your position without managing separate interest claims.

In many V3 pools, dTokens may also be staked into reward mechanisms that can earn you additional incentives such as GEAR or partner tokens. Details depend on the specific pool and curator settings and are shown in the pool card or rewards section.

**Important:** If a pool were to suffer losses from bad liquidations or security issues, your Diesel Tokens value could decrease. This risk exists in all DeFi lending, but Gearbox's security measures and risk curation help mitigate it.

## Withdraw & expected yield

Withdrawal is just as straightforward as deposit. There are no protocol-imposed lockups from Gearbox, so you can exit whenever you're ready.

### Partial or full withdrawal

To withdraw, navigate back to the pool you deposited to and use the withdrawal option. Select the pool with your deposit, click **Withdraw**, enter the amount you want to withdraw (or click **MAX** for full withdrawal), and confirm the transaction.

After confirmation, your assets are returned to your wallet, and your Diesel Tokens are burned accordingly—reducing your share of the pool by the amount you withdrew. You'll see the transaction in your wallet and, if you use a block explorer, under your address shortly after confirmation.

### Where to see accrued yield

The beautiful thing about Diesel Tokens is that your yield is automatically compounded—you don't need to claim anything. The tokens grow in value over time as interest accrues, so simply holding them means you're earning. There's no separate claim step, no manual compounding, just automatic growth.

To see your earnings, view your Diesel Tokens balance and watch it increase over time. You can also check pool information for current APY and utilization metrics, or review your transaction history to see when you deposited and compare your token value then versus now.

For additional rewards like GEAR tokens from staking, you may need to claim those separately from a rewards or **Rewards** section in the interface. But the core interest from lending is already in your token value.

### APY/APR explained

**APY (Annual Percentage Yield)** is the actual rate of return you earn on your deposit, accounting for compounding. This is what you'll typically see displayed, and it's the number that reflects what you'll actually earn if you hold for a full year.

**APR (Annual Percentage Rate)** is the simple interest rate without compounding. APY is usually higher because it accounts for the fact that interest compounds over time.

Your yield comes from a few sources. Utilization-based rates mean borrowers pay interest based on how much of the pool is being used—higher utilization generally translates to higher rates, which benefits lenders. In the permissionless design, curators configure risk parameters and borrow rates for their markets, and there may be extra bootstrapping rewards such as GEAR or partner tokens distributed to lenders as additional incentives.

**Variable yield:** It's important to understand that APY is variable and can change based on pool utilization, borrow rates (which follow a utilization curve), curator settings, and overall market conditions. Your actual earnings depend on how long you keep your deposit in the pool and how APY changes over that time period.

### Withdrawal timing

If pool utilization is very high (close to 100%), you might not be able to withdraw all your liquidity immediately. This doesn't mean your funds are stuck permanently or that the protocol has lost money—it simply means the liquidity is currently being used by borrowers.

In such cases, APY typically increases to attract more lenders, which helps restore balance. You can usually still withdraw partially even when utilization is high, and full withdrawal becomes available as borrowers repay or more liquidity enters the pool. This is standard behavior for lending protocols (similar to how Compound and Aave operate) and helps maintain protocol stability.

## Lender risks (light)

While lending on Gearbox is designed to be safer than active trading, it's important to understand the risks involved so you can make informed decisions.

### Smart contract risk

Gearbox Protocol consists of smart contracts on blockchain networks, and like all smart contracts, they carry inherent risks. Gearbox has been live since 2021 and, according to official materials, has not experienced security exploits or protocol-level bad debt so far and has undergone multiple security audits. Smart contract risk, however, always exists—no system is completely risk-free.

### Variable yield

APY is not fixed and will change over time based on utilization, borrower demand, curator parameters and governance decisions. Your actual earnings may differ from initial estimates depending on how market conditions evolve. This variability is normal for lending protocols, but it means your returns aren't guaranteed.

### Withdrawal timing

If pool utilization is very high, you may temporarily not be able to withdraw all your funds at once. While this is rare, you should be aware that withdrawals depend on available liquidity. In most cases, partial withdrawals remain possible even during high utilization, and full withdrawal becomes available as the situation normalizes.

### Potential losses from liquidations

In extreme cases where borrowers cannot be liquidated in time or liquidation results in bad debt, pool lenders could face losses. Gearbox has multiple safeguards to prevent this: a reserve fund to cover bad debt, an active liquidator network incentivized to keep the system healthy, and risk parameters set by experienced curators who understand the markets.

However, this risk cannot be completely eliminated in DeFi lending. Gearbox's strong track record and security infrastructure minimize the likelihood, but understanding the risk helps you make appropriate decisions about how much to lend and where.

For more detailed information about risks and security, see the [Risks & Security section](../risks-and-security).

---

**Next steps:** Once you're comfortable with lending, you might want to explore [borrowing and leverage](../borrow-credit-accounts) to see the other side of the protocol, or learn about [in-app actions](../in-app-actions) available to borrowers for deploying their leverage.