# Leveraged RWAs: Sky on Gearbox

gh-author-image-list
[](/author/mugglesect/)
gh-author-name-list
#### [Mugglesect](/author/mugglesect/)
gh-article-meta
gh-article-meta-inner
Nov 18, 2024 [] [6 min]
Boasting \$13B in TVL, 600K+ users and 8.5% APYs, Sky assets are now live on Gearbox.

Sky, previously Maker, is one of the most iconic DeFi rebrands. Maker\'s leveraged sDAI has been one of the most consistent strategies on Gearbox, generating double digit stablecoin yields. Like Maker, Sky aims to bring non-custodial yield to its stable assets. With Gearbox, users will now be able to leverage these assets and earn leveraged rewards. But exactly which assets can be leveraged? What do the rewards look like? Find the complete details in the article below.

> **NOTE: **The onboarding of Sky assets and their associated risk parameters have been defined according to the recommendations of Gearbox\'s Risk Curators, Chaos Labs. Complete details can be found in the attached GIP.

Snapshot

------------------------------------------------------------------------

## Sky Assets: Details and Rewards

With Maker\'s rebrand, DAI upgraded to USDS, sDAI upgraded to sUSDS, and MKR upgraded to the Sky token. Like DAI, USDS is designed to maintain a soft peg to the U.S. dollar and serve as a reliable store of value and medium of exchange. While USDS in itself doesn\'t yield any rewards, users now have two options to earn leveraged rewards:

1.  **Staking USDS, sUSDS**: Similar to sDAI, the sUSDS is the staked version of Sky\'s USDS. By staking USDS users become eligible to earn **The Sky Savings Rate (SSR).** SSR is variable and determined by the decentralised Maker/Sky Ecosystem onchain governance. The rate provided here is an estimate of the SSR expressed in expected compounded rate per annum. **Users staking their USDS in SSR earn rewards in the form of sUSDS tokens**
2.  **Sky Rewards Rate:** Sky Rewards are what you access when you supply USDS to the Sky Token Rewards module of the Sky Protocol. **Sky Rewards Rate is paid out in the form of SKY governance tokens.**

Effectively, you decide how you want to earn your rewards. Prefer stables? Lever up SSR. Prefer Sky tokens? Lever up SRR. But what are the rewards like?

That\'s up to **105% in rewards if you opt for Sky rewards or 44% on sUSDS**, creating one of the highest yielding strategies on Gearbox.

> NOTE: Borrow rates on Gearbox tend to remain stable over the course of the week and only see significant changes on Mondays, post Gauges epochs. You can monitor the changes on the [Gauges page](https://app.gearbox.fi/gauge?ref=blog.gearbox.fi). Changes in borrow rates directly affect your effective yields.

### **How does Gearbox reduce liquidation risk?**

Volatility, apart from the asset you hold, also depends on the debt you borrow. If you were to leverage sUSDS using ETH debt, your position would be prone to price volatility. Gearbox, though, enables users to **borrow stables to leverage Sky Assets**. Since USDS and sUSDS are correlated to stables, the volatility gets significantly muted.

------------------------------------------------------------------------

## How do leveraged Sky assets work?

Gearbox creates leverage by letting users borrow real assets up to 9 times the collateral they deposit. The borrowed assets and the user\'s collateral both are deposited to an isolated smart contract called **Credit Account**. Since these assets are real in nature, they can be further deployed across DeFi protocols to turn any *allowed* activity leveraged. For SSR or SRR, users can borrow upto 9X DAI to their CA and swap it to sUSDS or stkUSDS (Token rewards) to create a Leveraged position.

> This, though, isn\'t limited to just **Sky Assets**

**Gearbox is DeFi\'s Leverage Layer. **Think of it as plug and play leverage, whatever protocol Gearbox integrates automatically becomes leveraged. *An evolution of onchain credit with composability. *Users can access leveraged LRTs, Ethena, LSTs, RWAs, Trading on DEXes and more.

> Find the other strategies using the different tabs on the [dApp](https://app.gearbox.fi/pools?ref=blog.gearbox.fi). Here\'s a UI walkthrough to help you navigate it with ease.

------------------------------------------------------------------------

## Opening a position: dApp UI walkthrough

To start it all, first, go to the **Farm tab**: [https://app.gearbox.fi/strategies/list](https://app.gearbox.fi/strategies/list?ref=blog.gearbox.fi)

then:

A.** Choose the network you want to open a position on: **Which should bring you to this page. Choose between SSR (sUSDS) or SSR (stkUSDS).

B.** Choose Your Leverage: **Customise the position as per your risk tolerance. The page also displays the borrow rate, the liquidation price and more to help you take an informed decision. All these details are up to you, you decide all the parameters!

C. Scroll to the bottom of the page and click on **\"Open position\"**.

**And Voila! **You are all set. **Multicall** will now execute **all the required transactions in one go, using** account abstraction.

You retain complete flexibility to exit your position whenever you want, your collateral isn\'t burned or goes to 0. Simply close your CA to exit your position.

------------------------------------------------------------------------

### Price Feeds

The strategies for Sky assets don\'t have fundamental oracles. USDS utilises the DAI oracle which has been significantly stable over the last month, as can be seen below.

The feed for SRR is the same as USDS as you simply deposit the USDS to the Sky Token Rewards module.

The price for SSR is determined basis price of USDS\*Vault exchange rate from Sky.

------------------------------------------------------------------------

### Audit

Security is Gearbox\'s utmost priority with every new integration or asset onboarded. To ensure the safety The contracts for the sky integration have been audited by [Decurity](https://www.decurity.io/?ref=blog.gearbox.fi). Decurity has also performed security audits for DeFi protocols like 1inch, Compound and Yearn Finance.

You can find the results of the audit in our Github Below.

security/audits/2024 Oct - Decurity_Gearbox_SKY_integration.pdf at main · Gearbox-protocol/security

Contribute to Gearbox-protocol/security development by creating an account on GitHub.

GitHubGearbox-protocol

------------------------------------------------------------------------

### Not a fan of leverage? Lend passively instead

Don\'t want to actively leverage an asset despite correlated debt and low volatility? We get it. Lend your stables or ETH on Gearbox and earn up to 19% APYs\
\
• Without IL\
• Without Lock ups\
• Without fee\
\
100% passive lending: [https://app.gearbox.fi/pools](https://app.gearbox.fi/pools?ref=blog.gearbox.fi)

------------------------------------------------------------------------

*Gearbox DAO has no \"team\", what you say in the discord matters the most and is always considered. If you think there\'s something we suck at, come berate us. Join the DAO - get involved on Discord. Discuss, research, lead and share. Call contributors out on their bullshit and collaborate on making things better. Here is how you can follow developments:*

-   Website: [https://gearbox.fi/](https://gearbox.fi/?ref=blog.gearbox.fi)
-   dApp: [https://app.gearbox.fi/](https://app.gearbox.fi/?ref=blog.gearbox.fi)
-   User Docs: [https://docs.gearbox.finance/](https://docs.gearbox.finance/?ref=blog.gearbox.fi)
-   Developer Docs: [https://dev.gearbox.fi/](https://dev.gearbox.fi/?ref=blog.gearbox.fi)
-   Github: [https://github.com/Gearbox-protocol](https://github.com/Gearbox-protocol/?ref=blog.gearbox.fi)
-   Telegram: [https://t.me/GearboxProtocol](https://t.me/GearboxProtocol?ref=blog.gearbox.fi)
-   Twitter: [https://twitter.com/GearboxProtocol](https://twitter.com/GearboxProtocol?ref=blog.gearbox.fi)
-   Snapshot page: [https://snapshot.org/#/gearbox.eth](https://snapshot.org/?ref=blog.gearbox.fi#/gearbox.eth)
-   And of course, Notion monthly reports:

Notion – The all-in-one workspace for your notes, tasks, wikis, and databases.

A new tool that blends your everyday work apps into one. It’s the all-in-one workspace for you and your team

Notion