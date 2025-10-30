# Migrating to Permissionless: Guide for Lenders

gh-author-image-list
[](/author/mugglesect/)
gh-author-name-list
#### [Mugglesect](/author/mugglesect/)
gh-article-meta
gh-article-meta-inner
Oct 15, 2025 [] [8 min]
Driven by shifting industry trends, clearer regulations, and growing institutional demand for onchain credit rails, the DAO launched **Gearbox Permissionless**. Just six months later, Permissionless now accounts for **over 70% of total TVL**, has **4×**ed **our speed to market**, and future-proofed Gearbox's growth trajectory.

The Permissionless model was initially launched alongside the DAO-governed pools. However, given its clear outperformance and the operational complexity of maintaining both models in parallel, the DAO decided to transition entirely to the Permissionless framework.

With [GIP-264](https://snapshot.box/?ref=blog.gearbox.fi#/s:gearbox.eth/proposal/0x8f0b13b93c7cc40981b4156a16b1aca26cd556ed125722ce3eb13b59c487515a), the DAO now leads the development and management of Gearbox Protocol while Curators lead permissionless lending market set up. To ensure lenders can seamlessly migrate, Permissionless markets by kpk, the largest managers in the industry are now live! Details below.

> The migration begins with the ETH and wstETH pool. Migration of stablecoin pools will begin in the coming weeks.

------------------------------------------------------------------------

### About kpk

For the past five years, kpk has helped leading organizations secure, manage, and grow their onchain assets. From advising the Ethereum Foundation, Aave, and Lido to building one of the largest onchain liquidity networks, kpk brings deep expertise in risk and liquidity management.

With **Permissionless**, kpk expands into the curation layer of DeFi. kpk pools will initially support all collateral types available in Gearbox's legacy pools, ensuring a seamless transition for existing lenders and borrowers. Over time, kpk will actively introduce and manage new collateral assets across its ETH and wstETH markets, this will ensure maximum capital efficiency and optimized yield for all lenders.

Users can find details regarding their risk framework, approach to curation

Introduction | kpk

This handbook is the canonical reference for kpk-curated products across supported protocols. It explains the strategy design, asset selection, incentives, fees and risk controls that govern each product.

kpk Logo

------------------------------------------------------------------------

### About Permissionless

Permissionless empowers institutions, curators and projects to create no-code lending markets onchain using Gearbox\'s institutional-grade lending stack. The stack combines capital efficiency, composability, and innovation in a way no traditional DeFi lending system has before.

Curators on Gearbox can deploy multiple lending markets with distinct risk parameters and risk-adjusted borrow rates, all drawing liquidity from a single, unified pool. Since curators cannot move user-deposited capital, lenders operate within a more secure framework while curators access a more compliant and efficient infrastructure.

Purpose-built for institutions, Permissionless enables market setup across 20+ leading DeFi protocols including Curve, Pendle, Convex, and Uniswap. It doesn't just allow curators to create lending markets, it allows them to instantiate their own version of Gearbox, operated end to end under their control.

> While market creation becomes permissionless, the DAO will still be leading the development of the protocol. Permission brings to the table never seen before innovations in DeFi, learn about them below.

Gearbox Permissionless: Adaptation, Evolution, Evaluation

Ever since being set up in 2021, Gearbox DAO has operated and governed every aspect of the protocol and the product. From deciding which assets could be onboarded to determining what collateral could be lent and under what risk parameters, the DAO ran both the protocol and the product, embodying

Gearbox Protocol BlogMugglesect

------------------------------------------------------------------------

## Seamless Migration for ETH Lenders

Users can now seamlessly migrate from DAO-governed pools to Permissionless pools through an automated process. Migration is currently available for ETH pools, with support for stablecoin pools launching next. Users can now migrate from

• DAO-Governed **ETH Pool** to kpk curated Permissionless ETH Pool\
• Chaos Labs\' **wstETH Pool** to cp0x or kpk curated Permissionless wstETH pool

The key difference between the Permissionless pools and legacy pools is who curates the risks. The Permissionless pools and legacy pools remain identical in terms of operations. Lending on Permissionless will continue to be without impermanent loss, lock ups or any additional complexities.

While Permissionless pools don\'t add any complexity, they do come improve lender experience.

------------------------------------------------------------------------

### Improved Yields and Curation

With cp0x and kpk, lenders access curation from industry experts that don\'t just understand risk, but also understand how to generate borrow demand for the deposited capital in a safe manner.

Curators aren\'t DAO-appointed risk managers, they are onchain businesses with incentives tied directly to how well the lending pool performs. Curators\' revenue relies directly on the yield the pool generates and the amount of capital the pool attracts. This incentivises the curators to proactively list assets and generate demand to ensure the pool grows with healthy lending yields.

Coupling this with their background and expertise in risk management, the curators are likely to outperform DAO pools in terms of yields and speed to market, as we have seen with Permissionless over the last 6 months.

------------------------------------------------------------------------

### Curator bootstrapping rewards

The pools go live with initial bootstrapping rewards, replacing the earlier liquidity mining rewards Gearbox pools had. The rewards approved by the are about 3x of the LM numbers but the dilution is closely aligned with the revenue these pools generate. This revenue then triggers GEAR LP buybacks and creates a sustainable incentives mechanism.

Initially, kpk pools go live with ***over \$150K in rewards***.

• Month 1: 8.5 M GEAR for the WETH market and 12 M GEAR for wstETH.\
• Month 2: 15 M GEAR distributed across all pools according to TVL weight.

Additionally, Reserve protocol is allocating 12ETH in rewards to kpk\'s WETH pool. 60% of this will flow to lenders while the remaining 40% will incentivise borrowing for ETH+. These rewards will be distributed over 2 months as well.

> The existing legacy pools will remain active, allowing users to choose when to migrate. However, migrating early ensures users can maximize rewards and yields as Gearbox phases out DAO-governed pools.

------------------------------------------------------------------------

### Same Gearbox Security

Live for nearly 4 years, Gearbox has never faced any security exploits, placing it among the most secure protocols in DeFi. The codebase powering Permissionless pools continues to be developed and governed by Gearbox DAO, even as market creation itself becomes fully permissionless.

The DAO has invested more than \$3M in the protocol\'s security. Our defences are further reinforced through:

• 10+ Audits from top security firms like Consensys, Chainsecurity, ABDK, MixBytes, Spearbit, Watchpugs and more\
• Whitehack bug bounty of \$200K+\
• Real time monitoring systems

Gearbox DAO remains dedicated to maintaining a secure and resilient lending environment.

------------------------------------------------------------------------

## Lender Migration: UI Guide

To simplify the process, Gearbox has introduced a **Migration Bot,** an immutable contract that automates fund transfers to the pool you choose. This eliminates the need for users to manually monitor and migrate their positions. The migration for lenders follows the steps outlined below.

1.  **Lenders register their intent to migrate with the bot**\
You approve the bot to move your lending pool tokens from the legacy pool to the Permissionless one. This doesn't move your funds yet, it just sets things up.
2.  **The bot waits for the right time**\
If the liquidity available to migrate isn\'t available or utilisation on legacy pools is too high, the system keeps checking until conditions improve.
3.  **Migration happens automatically**\
As liquidity becomes available, the bot safely moves your liquidity to the new pool. You automatically receive the receipt tokens (dTokens) that denote your share of the lending pool when your capital is migrated! No additional action is required from users.

To execute this on the UI, lenders can either watch the walkthrough video or follow the steps outlined below.

0:00

/0:27

1×

1.  Go to \"Dashboard\" on app.gearbox.fi. Click on the position you wish to migrate.
2.  Click on \"Start Upgrading\". Choose the destination Permissionless pool you want to migrate to.
3.  Approve the upgrade and let the bot take care of the rest.
4.  Check the status of your migration on the Dashboard.

> For lenders migrating to the kpk pool, we recommend joining Gearbox\'s discord and keeping up with the #kpk channel for updates or to address any queries you might have, link below.

Discord - Group Chat That’s All Fun &amp; Games

Discord is great for playing games and chilling with friends, or even building a worldwide community. Customize your own space to talk, play, and hang out.

Discord

------------------------------------------------------------------------

### Why are we implementing a bot?

Without the Migration Bot, lenders would need to manually withdraw funds from legacy pools and redeposit them into the new ones. Since this process can't be perfectly synchronized with borrower migrations, it may cause two key issues:

1.  Liquidity gaps: legacy pools may not always have enough liquidity for lenders to withdraw.
2.  High utilization spikes: utilization could temporarily reach near 100%, creating a poor experience and losses for borrowers.

With the automated Migration Bot, users simply submit their intent to migrate, and the bot coordinates the fund movement as per liquidity constraints. Ensuring smooth transitions without constant monitoring or disruptions to user experience.

------------------------------------------------------------------------

### What The Bot Can and Can Not Do

Here\'s what it can do:

-   Migrate your capital from the legacy pool to the specific permissionless pool you approved.
-   Time the migration for you as liquidity becomes available
-   Perform all the actions on audited, immutable smart contracts.

And here\'s what it can\'t do

-   Not move any of your other funds.
-   Not move your capital to any other contract, the bot is immutable.
-   Can\'t let the curators withdraw your capital
-   Can\'t cause loss of funds.

Transactions on the mainnet have already been executed using the bot to ensure it functions as required, users can find the transaction [here](https://etherscan.io/tx/0xd1c7c7e523168e1274369bd1900dc261c167f7e6c0e265fd6e983ca41d7c99d8?ref=blog.gearbox.fi).

------------------------------------------------------------------------

### **What you can expect from the bots execution**

The bot will follow certain execution principles to ensure a smooth transition.

-   **Migration of positions up to \$1,000,000.**\
Migrated in full within the nearest suitable batch.
-   **Positions above \$1,000,000.**\
Migrated in required chunks. This is normal and will help keep utilization healthy while your position transitions.
-   **Target batch size.**\
The bot will group requests into roughly \$1,000,000 batches to execute efficiently when liquidity allows.
-   **First In, First Out queueing.**\
Lender migration requests are processed in chronological order. This keeps the process transparent and predictable.
-   **Timing.**\
Your migration may wait while a batch fills. The maximum wait time will not exceed 14 days.

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