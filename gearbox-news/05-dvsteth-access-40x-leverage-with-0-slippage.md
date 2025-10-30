# DVstETH: Access 40X Leverage With 0 Slippage

gh-author-image-list
[](/author/mugglesect/)
gh-author-name-list
#### [Mugglesect](/author/mugglesect/)
gh-article-meta
gh-article-meta-inner
Jul 21, 2025 [] [10 min]
Decentralized exchanges (DEXes) have long been a vital backbone for lending protocols, enabling borrowers to swap assets and create leveraged positions, either through recursive loops or swapping of leveraged spot assets. However, this reliance on DEXes comes with a hidden cost, in the form of ***Slippage and DEX trading fees.***

Today, that changes. Gearbox Permissionless introduces a new way to access leverage in DeFi, without losing value to DEX inefficiencies\...

------------------------------------------------------------------------

## I. Leveraged Minting and Withdrawals: DVstETH

Instead of offering leverage via swapping of debt assets through DEXes, Gearbox introduces leverage directly at the contract of the asset. Enabling **borrowers to mint and withdraw leveraged positions straight from the source**; *completely by-passing DEXes.*

By doing so, Gearbox can offer users up to **40X leverage without any slippage or DEX fees.** In a first for DeFi lending, users can now access leveraged minting and withdrawals for **Lido Finance\'s DVstETH.**

DVstETH is a Liquid Staking Token (LST) enabling users to stake their ETH through Lido\'s infrastructure while participating in decentralized validator technology (DVT) initiatives. The minting and withdrawals for DVstETH are processed via Mellow Protocol\'s vault infrastructure with no DEXes involved.

> **Important Note:** While the leveraged deposits and withdrawals from DVstETH contract are slippage and DEX fee free, redemption of DVstETH withdraws stETH or wstETH by default.

> Users can pay back their WETH debt manually and withdraw wstETH or swap the wstETH to pay back their debt. The latter option could attract dex fee but stETH/ETH is one of the most liquid pools and slippage for it is usually negligible.

Since this strategy is the first of its kind, we had to make it special..

------------------------------------------------------------------------

### 0% Protocol Fee for Early Birds

The first 1,000 WETH borrowed to leverage up DVstETH won\'t pay any protocol fee for the duration of their farm.

That means:

• 0 Slippage\
• 0 DEX trading fee\
• 0% Protocol fee

You keep 100% of the yields you earn: [https://app.gearbox.fi/pools](https://app.gearbox.fi/pools?ref=blog.gearbox.fi)

------------------------------------------------------------------------

### How Gearbox makes 0 Slippage Leverage Possible

Gearbox's infrastructure runs on smart contract wallets called Credit Accounts. These accounts let borrowers access up to 40x leverage from Gearbox's passive lending pools, creating capital-efficient, leveraged positions.

This leveraged position can then be utilised across permitted assets and protocols to turn DeFi leveraged. For DVstETH, Gearbox Credit Accounts are programmed to interact directly with the DVstETH vault on Mellow. This allows borrowers to mint and redeem leveraged positions natively, *eliminating slippage, DEX fees, and the need for swaps entirely*.

Credit Accounts programmatically ensure that fund utilisation aligns with risk parameters set by the Risk Curator, cp0x, in the case of DVstETH. This prevents withdrawals to or interactions with malicious contracts, creating a secure, walled garden that remains highly composable.

*While the elimination of DEXes helps users save slippage and trading fee costs, this isn\'t the only benefit..*

------------------------------------------------------------------------

## II. Benefits of Bypassing DEXes

Minting natively at the contracts does a lot more than saving up to 2 months of your rewards. It makes strategies safer, enables easier scaling, saves costs for projects AND let\'s the users earn more. How? Read Below!

------------------------------------------------------------------------

### Unlocking Highest Leverage in DeFi: 40X

Leveraged yields are driven by the spread between borrow rates and the asset's underlying yield. This yield arbitrage, amplified by leverage, allows borrowers to multiply returns. Thus, higher the leverage, higher the maximum yield a borrower can earn.

0:00

/0:02

1×

But leverage is determined by Loan-to-Value (LTV) ratios, which usually depend on the asset's DEX liquidity. But since liquidity is often deeper and more stable directly on the asset's contract than a DEX, LTVs can be set much higher on Gearbox, unlocking greater leverage.

------------------------------------------------------------------------

### Multifold Scale: Higher Borrow Limits

Since assets like DVstETH are minted directly into the strategy contract, the protocol isn\'t limited by how much can be swapped on a DEX . It can support much higher borrow volumes without impacting price or yield.

This direct minting unlocks massive borrow cap potential, making it possible to serve larger borrowers and institutional flows with confidence. **The max borrow limit for every account leveraging DVstETH is 6.6K WETH.** A leverage position of that size will still be executed without slippage or DEX fees.

------------------------------------------------------------------------

### Safer Positions: Lower Liquidation Points

When **maximum LTV is higher**, the **liquidation point is deeper**. A Higher LTV allows borrowers to withstand a **larger drawdown** before liquidation, for the same leverage. This might seem counterintuitive, but it's because the **same borrow amount** is being measured against a more lenient liquidation threshold.

For example, if a user were to leverage up 5X the same asset at an LTV of 90 vs 97.5, the drawdown required to reach their liquidation point would be lower by almost 60% with the higher LTV.

**Max LTV**   **Liquidation Price**   **Drawdown Required**
------------- ----------------------- -----------------------
**90%**           0.89 ETH                 -11.2%
**97.5%**          0.82 ETH                 −18.0%

As you can see, a higher LTV leads to a lower liquidation point. So, **higher max LTV doesn\'t increase risk by itself,** it\'s only riskier if you borrow closer to that limit (i.e., use higher leverage).

------------------------------------------------------------------------

### Cost Savings for Issuers

By eliminating the need to bootstrap DEX liquidity, Gearbox can save projects millions in liquidity costs. Launching a lending market often demands \$5--\$10M in paired liquidity to maintain low slippage and safe LTVs. But this liquidity is capital-inefficient.

On average, realized IL led to a 3.8% loss per position compared to a simple buy-and-hold strategy, [as per a recent study](https://arxiv.org/html/2501.07828v1?ref=blog.gearbox.fi#abstract). Gearbox sidesteps this waste by enabling leverage directly through asset contracts.

------------------------------------------------------------------------

## III. Key Details For Users

To make the best use of the unique advantages unlocked by leveraged minting and withdrawals, users can utilise Gearbox in 2 ways.

### The Opportunity for Borrowers

Borrowers on Gearbox can now borrow up to 40X WETH to lever up DVstETH. This enables them to

• Maximise staking rewards\
• Multiply their OBOL and SSV rewards

> Obol and SSV (Secret Shared Validators) are two distinct but complementary technologies that enable decentralized Ethereum staking infrastructure, specifically via Distributed Validator Technology (DVT).

To ensure 40X leverage doesn\'t lead to borrowers facing easy liquidation, Gearbox takes multiple measures to *make your leverage farming experience peaceful and non-volatile*. These include

• **No DEX price volatility: **The ***fundamental price feed*** for DVstETH utilises the exchange rate of DVstETH deposited into the Mellow vault, eliminating DEX price volatility.\
**• No Slippage or DEX Fee:** Enables you to keep 100% of your collateral and yields.\
**• Correlated Debt: **The correlation between the borrowed WETH and leveraged DVstETH further reduces volatility as ETH\'s directional risk is avoided.\
**• Highest LRT LTV in DeFi, 97.5:** Reduces liquidation points at the same leverage when compared to lower LTVs.

------------------------------------------------------------------------

### Borrowers: Position Management and Risks

While higher LTVs can enhance capital efficiency, it's important to manage leveraged positions with a clear view of associated risks. With Gearbox, these risks are minimal and well-defined:

-   **Contract-Level Depeg**: A highly unlikely event, only possible in extreme cases such as validator slashing or smart contract exploits.
-   **Negative Leveraged Spread**: This occurs when the borrow rate on your strategy exceeds the effective APY being earned. However, it's important to note that **Gearbox has recorded zero liquidations from negative spread scenarios in over 3.5 years** of operation.

To continue maintaining this standard of safety, one key mechanism is **Quota Management**.

**What is Quota Management?**

For DVstETH rewards, part of your yield will be distributed in tokens like **SSV** or **OBOL**. Since these rewards do not automatically reflected in your Health Factor, Gearbox allows users to **manually assign quotas,** essentially deciding how much of your assets in your Credit Account should count towards health factor calculations.

Without quota adjustments, your account may appear to have a lower health factor given a significant portion of rewards are in claimable, rather than auto-compounded, tokens.

To keep your position in optimal health, users are encouraged to periodically:

-   **Claim and, if necessary, swap rewards into WETH** or another base asset.
-   **Update quotas** within your Credit Account so the protocol can properly recognize your rewards as part of your position's value.

As Gearbox Permissionless continues to roll out, this mechanism is expected to become fully automated or phased out altogether.

In the meantime, our team is always available to help. If you have questions or need assistance, reach out via Discord or Telegram**,** we\'re here to support you.

------------------------------------------------------------------------

### The Opportunity For Lenders

If you are a user who is looking for safer yields without leverage, Gearbox has got that too. The instance brings lenders the opportunity to earn completely passive lending yields on wETH with Gearbox\'s battle-tested infrastructure that has had 0 security incidents or bad-debt since 2021.

And for the first month, WETH lending comes with 1M GEAR rewards above your passive rewards.

Gearbox\'s lending pools have no impermanent loss, fees or lock ups. Lenders can deposit and withdraw whenever they decide, making lending truly passive.

> Users can deposit wstETH to earn passive yields and additional rewards here: [https://app.gearbox.fi/pools](https://app.gearbox.fi/pools?ref=blog.gearbox.fi)

------------------------------------------------------------------------

## IV. Unlocking Gearbox permissionless

This institutional-grade scale and cost efficiency is made possible by Gearbox Permissionless. Gearbox Permissionless is an institutional-grade lending stack which brings real-world risk and lending frameworks onchain. Combining capital efficiency, composability, and compliance in a way no traditional DeFi lending system has before.

Purpose-built for institutions, the stack enables seamless integration of existing risk, underwriting, and credit systems while eliminating the inefficiencies of pool-based lending. Here's how:

1.  **Support for non-tokenised and unique collateral:** Gearbox Credit Accounts are composable by design, enabling native credit across protocols including for non-tokenized assets like Convex LPs. Unlike pool-based architectures, Gearbox allows institutions to lend against a wider set of assets without relying on DEX liquidity, unlocking capital efficiency where it wasn't previously possible.
2.  **Risk-Adjusted Borrow Rates:** Institutional underwriters take into consideration innumerable factors when deciding on borrow rates for an asset. Traditional DeFi lending uses utilization-based interest rates, ignoring borrower-specific risk and collateral quality. Gearbox replaces this with built-in, risk-adjusted rate modeling, letting institutions mirror their off-chain underwriting models onchain.\
3.  **No Active Liquidity Management:** Gearbox lending pools enable institutions to set up multiple markets with unique risk parameters utilising a single, unified lending pool for every debt asset. This removes operational overhead caused by liquidity management required on other lending stacks. It also enables institutions to remain more compliant as managing liquidity and moving it requires licensing in multiple jurisdictions across the world.
4.  **In-built leverage tooling:** Leverage is one of the primary drivers of institutional lending. Unlike protocols that rely on external integrations like Paraswap, Gearbox Credit Accounts come with native leverage tooling from Day 0. No third-party DEX needed, no waiting time for leverage.
5.  **Omni-EVM architecture:** The permissionless lending stack comes with a modular architecture that can be deployed on any EVM. Enabling institutions to access lending on any EVM, even their own, from Day-0 without having to write any code.
6.  **Compliance Tooling:** KYC and private market compatibility are also a key part of the Permissionless Stack, allowing institutions to move onchain in a compliant manner.

Gearbox Permissionless is already partially live, with select markets and features handling over \$5M in TVL. The full stack is scheduled for release in Q3, but early access is available for institutions, protocols, and networks ready to move today. Create institutional-grade lending markets onchain with Gearbox, [Get in touch!](https://t.me/GearboxProtocol?ref=blog.gearbox.fi)

> Backing these features is the focus on security Gearbox has always had.

------------------------------------------------------------------------

### Battle-Tested Gearbox

Security is paramount in DeFi, and Gearbox has demonstrated a strong commitment to maintaining a secure environment, **spending over \$3M on security.** Gearbox has been live for 3+ years and has never faced any exploits. It is further backed by

• 10+ Audits\
• Whitehack bug bounties\
• AI-based monitoring tools

These factors provide a safe environment for protocols and institutions to expand their on-chain operations and services.

------------------------------------------------------------------------

## V. UI Walkthrough

The deployment of the DVstETH strategy is now live! Getting started with Gearbox is as easy as heading to [the Gearbox dApp](https://app.gearbox.fi/pools?ref=blog.gearbox.fi)

### To Lend

1.  Head over to [https://app.gearbox.fi/pools](https://app.gearbox.fi/pools?ref=blog.gearbox.fi) and choose the wETH pool by cp0x.

2\. Enter the amount you would like to lend and click on \"Supply\"

3\. You should now receive diesel tokens which reflect the ownership of supplied assets to the pool.

### To Leverage

1.  Head over to [https://app.gearbox.fi/strategies/list](https://app.gearbox.fi/strategies/list?ref=blog.gearbox.fi) and choose the DVstETH strategy

2\. Fill in the amount you want to put as collateral and the leverage you want to access. Click on \"Open Position\" to deploy your leveraged position in 1 click.

Easy as that! Approve the transaction and you can access passive lending, leverage, and loans with Gearbox.

------------------------------------------------------------------------

*If you are an institution and are looking to expand your operations onchain, Gearbox can offer you the credit infrastructure you require. Contact us on *[*Telegram*](https://t.me/GearboxProtocol?ref=blog.gearbox.fi)* or *[*Discord*](https://discord.gg/gearbox?ref=blog.gearbox.fi)*, and we will guide you. Let's build the onchain economy together!*

-   Website: [[https://gearbox.fi/]](https://gearbox.fi/?ref=blog.gearbox.fi)
-   Main App: [[https://app.gearbox.fi/]](https://app.gearbox.fi/?ref=blog.gearbox.fi)
-   Telegram: [[https://t.me/GearboxProtocol]](https://t.me/GearboxProtocol?ref=blog.gearbox.fi)
-   Discord: [[https://discord.gg/gearbox]](https://discord.gg/gearbox?ref=blog.gearbox.fi)
-   Twitter: [[https://twitter.com/GearboxProtocol]](https://twitter.com/GearboxProtocol?ref=blog.gearbox.fi)
-   User Docs: [[https://docs.gearbox.finance/]](https://docs.gearbox.finance/?ref=blog.gearbox.fi)
-   Developer Docs: [[https://dev.gearbox.fi/]](https://dev.gearbox.fi/?ref=blog.gearbox.fi)
-   Github: [[https://github.com/Gearbox-protocol]](https://github.com/Gearbox-protocol/?ref=blog.gearbox.fi)
-   Snapshot page: [[https://snapshot.org/#/gearbox.eth]](https://snapshot.org/?ref=blog.gearbox.fi#/gearbox.eth)
-   Notion DAO monthly reports:

Notion – The all-in-one workspace for your notes, tasks, wikis, and databases.

A new tool that blends your everyday work apps into one. It’s the all-in-one workspace for you and your team

Notion

JOIN NOW