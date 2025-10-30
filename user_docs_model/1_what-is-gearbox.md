# What is Gearbox?

Gearbox is a leverage protocol built for DeFi. Think of it as having more capital to work with, and you decide where to deploy it—whether that's trading on Uniswap, farming on Curve or Yearn, staking on Lido, or building complex strategies that span multiple protocols.

What makes Gearbox different? Unlike traditional lending protocols that lock your leverage into isolated pools, Gearbox gives you real assets that interact with the entire DeFi ecosystem. Your trades happen on Uniswap using their liquidity. Your farms run on Curve using their pools. The leverage comes from Gearbox, but execution happens wherever you choose, using the global liquidity of established protocols you already know.

The protocol serves two types of users. If you're looking for passive income, you can deposit assets into lending pools and earn APY without impermanent loss, fees, or lockups. Your assets are lent to active users who need leverage, and you earn interest on what you supply. On the other side, traders, farmers, and even other protocols borrow those assets to create leveraged positions—often up to 10x leverage, depending on your collateral and strategy.

SCREENSHOT: Main dashboard showing Pools and Credit Account sections

## What Gearbox lets you do

Gearbox opens up possibilities that go beyond simple borrowing or lending. The leverage you get isn't isolated in Gearbox's own pools. Instead, your trades and farms execute across the broader DeFi ecosystem using global DEX liquidity.

If you're starting out with passive income, the path is straightforward: deposit assets into lending pools and let them earn yield. Your assets are lent to borrowers, and you collect interest. There's no impermanent loss to worry about, no fees eating into your returns, and no lockup periods trapping your funds. It's as simple as earning interest on a savings account, but with the transparency and control that comes with DeFi.

For those ready to be more active with their capital, Gearbox unlocks leverage you can deploy anywhere. Want to margin trade? You can leverage trade on Uniswap, Curve, or other real spot DEXes using borrowed funds. Interested in yield farming? Take leverage and farm stablecoins, staked ETH, or other yield-bearing assets to multiply your returns. Have more sophisticated goals? Build delta-neutral positions, arbitrage correlated assets, or combine trading and farming strategies all within the same Credit Account.

The flexibility extends to how you manage your position, too. You're not locked in. You can partially unwind by repaying some debt, adjust your leverage up or down as market conditions change, or close your position entirely when you're ready—all without friction.

## How Gearbox differs from other protocols

If you've used other lending protocols like Aave or Compound, you might wonder what makes Gearbox different. The core difference is flexibility and composability.

Traditional lending protocols give you leverage, but it often comes with limitations. You might be stuck trading on their platform, or your leverage only works within specific isolated pools. Gearbox takes a different approach: it gives you real assets you can deploy anywhere in DeFi. The leverage you borrow is actual USDC, WETH, or other tokens—not synthetic positions or internal credits. This means you can use it on Uniswap, Curve, Yearn, or any other protocol that Gearbox integrates with.

Another key difference is composability. On many platforms, you can either lend or borrow, but your collateral sits locked in their system. With Gearbox, your Credit Account acts like a smart wallet. You can borrow funds, use them to farm on Curve, then swap the farm tokens, stake on Lido, and run complex strategies—all from the same account, all using the leverage you borrowed.

There's also no funding rates to worry about. Since Gearbox doesn't create its own trading pairs or maintain short-long ratios, you don't pay the funding fees common in perpetual trading. Your leverage is based on real spot assets, executed through real DEX liquidity.

For lenders, the experience is similar to other protocols—deposit assets and earn yield. But Gearbox's unique architecture means your funds are used more efficiently. Because borrowers can deploy leverage across multiple protocols and strategies, there tends to be higher demand, which often translates to better yields for lenders.

The bottom line? Gearbox isn't trying to replace the protocols you already use. It's enhancing them by giving you more capital to work with, while you keep using the DEXes, farms, and strategies you're already comfortable with.

## Key concepts

Understanding a few core concepts will help you get the most out of Gearbox and make informed decisions about your positions.

### Credit Account

At the heart of Gearbox is the Credit Account—an isolated smart contract that holds both your funds and the funds you borrow. Think of it as a specialized DeFi wallet that's designed for leverage and strategic positioning.

After you open a Credit Account, all your operations flow through it. Whether you're swapping assets, farming yield, or building complex strategies, everything happens within this account. The assets stay on it, and you manage them by sending instructions—like telling a smart wallet what to do, but with built-in leverage capabilities.

What makes Credit Accounts powerful is their composability. The funds you deposit serve as collateral for your debt, but you're not limited to passive holding. You can actively operate those funds by sending financial orders to your Credit Account. That might mean margin trading on Uniswap or Sushiswap, leverage farming on Yearn, arbitraging pegged assets on Curve, or any combination that fits your strategy.

### Health Factor

Your Health Factor is a simple number that tells you how safe your position is. It's the ratio between the discounted value of your collateral and your total debt. If your Health Factor is above 1, you're in good shape. If it drops below 1, your account becomes eligible for liquidation.

The higher your Health Factor, the more cushion you have against market movements. If your collateral prices drop or your debt increases, your Health Factor decreases. Since leverage amplifies both gains and losses, monitoring your Health Factor is crucial for managing risk.

Keep in mind that your Health Factor isn't static—it changes as market prices fluctuate, interest accrues on your debt, and you perform actions like swapping assets or adjusting leverage. The key is maintaining a comfortable buffer well above 1 to give yourself room for normal market volatility.

TODO: Add exact location where Health Factor is displayed in the current UI

### Liquidation

If your Health Factor drops below 1, anyone can liquidate your Credit Account. This protects lenders by ensuring that the pool's capital is always fully backed. During liquidation, a liquidator repays your debt and takes a premium as compensation for the service, while you receive any remaining funds after the debt and fees are settled.

Liquidations incur fees paid to both the liquidator and the protocol, so avoiding them is in your best interest. The good news is that maintaining a healthy buffer above the liquidation threshold is straightforward: keep your Health Factor well above 1, monitor your position regularly (especially during volatile periods), and be ready to add collateral or reduce debt if things get tight.

### Limits

Gearbox sets various limits to ensure security and proper risk management across the protocol. Each Credit Account has maximum leverage limits that typically range up to 10x, though the exact amount varies based on your collateral type. There are also minimum and maximum debt limits per account to ensure liquidations remain profitable while keeping individual positions within reasonable bounds.

Some assets have quota limits—global exposure caps that prevent the protocol from taking on too much risk from a single collateral type. If a particular asset reaches its quota limit, you might not be able to use it as collateral until capacity becomes available. These limits help protect both lenders and the broader system.

TODO: Add specific limit values from current protocol parameters

### Fees

What you pay depends on what you're doing. If you're lending, there are no fees from Gearbox—what you see in terms of APY is what you earn. Your earnings come from the interest borrowers pay.

If you're borrowing, you'll pay borrow interest that fluctuates based on pool utilization. The more of the pool that's being used, the higher the rates tend to be. Some collateral assets also have quota fees—additional dynamic fees that reflect the risk profile of the asset. These fees go to the protocol and help balance risk across different types of positions.

The only other fee borrowers might encounter is liquidation fees, which only apply if your position gets liquidated. All fees are displayed in the interface before you confirm any transaction, so you always know what to expect.

TODO: Add exact locations where fees are displayed in deposit and borrowing forms

## Safety note & disclaimers

Using Gearbox, like any DeFi protocol, comes with risks. Understanding these risks helps you make informed decisions and manage your positions effectively.

### Smart contract risk

Gearbox Protocol consists of smart contracts deployed on blockchain networks. Like all smart contracts, they carry inherent risks. While Gearbox has undergone multiple security audits from top firms and has been live for over 3 years without exploits or bad debt, smart contract risk always exists. The protocol team has invested over $3M in security, but no system is completely risk-free.

### Market risk

When you use leverage, you amplify both potential gains and losses. Price movements can reduce your collateral value, causing your Health Factor to drop. If your Health Factor falls below 1, your position can be liquidated. This is a fundamental aspect of leveraged positions—they offer more upside but require careful risk management.

### Liquidation risk

The best way to avoid liquidation is to maintain a buffer above Health Factor of 1. Monitor your position regularly, especially during volatile periods when prices can move quickly. If your Health Factor approaches 1, you have options: add more collateral, reduce your debt, or close or adjust your position entirely. The key is staying ahead of potential problems rather than waiting until you're at risk.

### Variable yield

If you're lending, understand that APY is variable and depends on pool utilization and borrower demand. It can go up or down based on market conditions. This is normal for lending protocols—your yield reflects the real-time supply and demand dynamics in the pools.

### Withdrawal timing

If pool utilization is high, you may not be able to withdraw all your liquidity immediately. This doesn't mean the protocol lost money or that your funds are at risk. It simply means that liquidity is currently being used by borrowers. In such cases, APY typically increases to attract more lenders, which helps restore balance. You can usually still withdraw partially even when utilization is high.

For more details on risks, security audits, and safety practices, see the [Risks & Security section](../risks-and-security) and [FAQ](../faq-troubleshooting).

---

**Ready to get started?** The next step is learning how to [connect your wallet and navigate the interface](../getting-started), or you can jump straight to [earning passive yields](../earn-lend) or [opening your first Credit Account](../borrow-credit-accounts).
