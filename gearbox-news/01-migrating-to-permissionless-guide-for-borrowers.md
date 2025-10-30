# Migrating to Permissionless: Guide for Borrowers

gh-author-image-list
[](/author/mugglesect/)
gh-author-name-list
#### [Mugglesect](/author/mugglesect/)
gh-article-meta
gh-article-meta-inner
Oct 20, 2025 [] [8 min]
Driven by shifting industry trends, clearer regulations, and growing institutional demand for onchain credit rails, the DAO launched **Gearbox Permissionless**. Just six months later, Permissionless now accounts for **over 70% of total TVL**, has **4×**ed** our speed to market**, and future-proofed Gearbox's growth trajectory.

The Permissionless model was initially launched alongside the DAO-governed pools. However, given its clear outperformance and the operational complexity of maintaining both models in parallel, the DAO decided to transition entirely to the Permissionless framework.

With [GIP-264](https://snapshot.box/?ref=blog.gearbox.fi#/s:gearbox.eth/proposal/0x8f0b13b93c7cc40981b4156a16b1aca26cd556ed125722ce3eb13b59c487515a), the DAO now leads the development and management of Gearbox Protocol while Curators lead permissionless lending market set up. To ensure borrowers access the best of opportunities, migration of CAs (Credit Accounts) is now live. Borrowers can move their position to Permissionless without incurring any slippage or additional costs.

> The migration begins with users borrowing from the ETH and wstETH pool. Migration of stablecoin pools will begin in the coming weeks.

------------------------------------------------------------------------

### About kpk

For the past five years, kpk has helped leading organizations secure, manage, and grow their onchain assets. From advising the Ethereum Foundation, Aave, and Lido to building one of the largest onchain liquidity networks, kpk brings deep expertise in risk and liquidity management.

With **Permissionless**, kpk expands into the curation layer of DeFi. kpk pools will initially support all collateral types available in Gearbox's legacy pools, ensuring a seamless transition for existing lenders and borrowers. Over time, kpk will actively introduce and manage new collateral assets across its ETH and wstETH markets, this will ensure the borrowers access the best of opportunities and collaterals.

Users can find details regarding their risk framework and kpk\'s approach to curation below.

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

## Borrower Migration: Better UX, Same Position

Credit Account Migration is a mechanism that enables existing users (especially those on V3 or earlier governance-curated pools) to port their positions over to the kpk curated Permissionless Pools without having to manually close or unwind their positions.

In other words:

-   Your exposure (collateral + debt) can be seamlessly transferred to Gearbox Permissionless without incurring slippage or unwinding.
-   You don't have to sell or exit your leveraged farms.
-   The migration tool handles the reconfiguration under the hood when liquidity is available.

This design greatly reduces friction and risk for users wanting to adopt the new system offerings.

------------------------------------------------------------------------

### Who can move

Initially, this migration is available for users with debt in the wstETH or WETH pools curated by Chaos Labs. To make this migration possible, kpk\'s Permissionless pools feature all of the assets available as collateral on the DAO governed pools.

Users can now move

• Any position borrowing from the Chaos Labs **WETH Pool** to kpk curated Permissionless WETH Pool\
• rstETH positions from Chaos Labs\' **wstETH Pool** to cp0x or kpk curated Permissionless wstETH pool

The key difference between the Permissionless pools and legacy pools is who curates the risks. The Permissionless pools and legacy pools remain identical in terms of operations but ***better in execution.***

While Permissionless pools don\'t add any complexity, they do come improved leverage and borrowing experience.

------------------------------------------------------------------------

### Lower slippage, better routing

Gearbox Permissionless introduces advanced swapping capabilities. By integrating multiple DEX routes and liquidity layers across protocols like Uniswap, Curve, Balancer, and others, it ensures borrowers get the best possible execution when opening, adjusting, or closing leveraged positions.

By increasing the number of available pools, the system routes swaps through a significantly most efficient combination of paths, reducing slippage. This improvement directly translates into months of additional yield saved for active borrowers who would otherwise lose value to inefficient swaps.

These routes will remain unavailable to borrowers in legacy pools due to contract constraints. By migrating to Permissionless, borrowers unlock better routing.

------------------------------------------------------------------------

### More leverage opportunities

With the launch of Gearbox Permissionless, the protocol moves from a single-governance model to a multi-curator framework, where independent curators can set up and manage their own lending markets under defined risk parameters. This decentralization has dramatically expanded the system's ability to onboard new assets safely, ***4Xing the speed to market compared to the legacy setup***. As a result, borrowers migrating to permissionless pools gain access to a wider range of yield opportunities, backed by diverse collateral types and curator-driven strategies.

Meanwhile, since the DAO has paused new market launches on legacy pools, most fresh opportunities for leverage, yield, and strategy discovery will now emerge exclusively within the permissionless ecosystem.

------------------------------------------------------------------------

### Favourable Borrow Rates

In Permissionless, the borrow rates have two aspects.

1.  **Utilisation Rate:** These are demand based rates that increase more funds in the pool get utilised
2.  **Fixed Risk Premium:** Based on underwriting principles, curators and institutions can add a fixed premium that borrowers have to pay on top of the demand based rates.

This mechanism enables curators to recreate lending frameworks they have spent decades perfecting. These fixed premiums replace the existing \"Quota\" rates mechanism which relied on users voting on the rates that updated once a week. With curators being able to update rates proactively, borrowers now access a smoother borrowing experience.

------------------------------------------------------------------------

### GEAR rewards

Users migrating Credit Accounts receive a fixed reward based on the value of their account. These rewards have been tiered as:

-   1k--300k: 30k GEAR
-   300k--1.5M: 50k GEAR
-   1.5M: 80k GEAR

------------------------------------------------------------------------

## Migrate without any slippage: UI Guide

To ensure borrowers can seamlessly access the best new opportunities, the migration of Credit Accounts (CAs) is now live. This feature allows users to move their existing positions from legacy pools into the new permissionless markets without closing or unwinding them. The movement of your position goes through a simple 3 step flow.

-   **Authorization & Pre-checks**\
The user authorizes a migration contract. Before executing, the interface shows the revised health factor, borrowing conditions, and differences in pool parameters under the target curated pool.
-   **Liquidity Check**\
Migration is triggered only once sufficient liquidity is available in the target pool to absorb the migrating position.
-   **Atomic Transfer**\
The migration happens in a single, atomic transaction or sequence of sub-transactions: your credit account is migrated into the new pool's framework, maintaining your collateral + debt relationship under the new rules.

At a UI level, this is executed in 2 clicks. You can follow the video below to migrate

0:00

/0:32

1×

Or refer to the text below.

1.  Go to \"Dashboard\" on app.gearbox.fi. Click on the position you wish to migrate.
2.  Click on \"Start Upgrading\". Choose the pool you want to borrow from in Permissionless.
3.  Approve the upgrade and your CA will be migrated if the intended pool has enough liquidity.
4.  Check the status of your migration on the Dashboard.

------------------------------------------------------------------------

### Conditions for 0 Slippage Migration

At its core, the Credit Account Migration process enables borrowers to shift their entire leveraged position from one market to another, repaying old debt and reopening the same exposure under new parameters, all in a single transaction. Here's how it unfolds step by step:

1.  A new Credit Account is opened in the target market, corresponding to the borrower's desired new pool or curator setup.
2.  From this new account, the system borrows just enough tokens to fully repay the debt on the borrower's existing (old) account.
3.  These newly borrowed tokens are then swapped into the underlying tokens that match the collateral composition of the old account.
4.  The old account's debt is repaid in full, and once settled, its collateral is seamlessly transferred to the new account.

Since the process relies on repaying existing debt using liquidity from the new pool, migrations can only occur when the target market has sufficient available liquidity. If the pool is temporarily saturated, the migration transaction won't execute until more liquidity becomes accessible. Borrowers are advised to check back periodically in such cases, as lenders are also migrating simultaneously, continuously adding fresh liquidity to the new permissionless markets.

0 slippage migration remains applicable only as long as the debt asset remains the same. For changing your debt composition or moving from one borrowed asset to another, users can **incur slippage.**

------------------------------------------------------------------------

### Migration for Lenders

If you are a lender to the legacy wstETH or WETH pools, an automated migration tool is already live for you.

Find the details about migrating your capital below.

Migrating to Permissionless: Guide for Lenders

Driven by shifting industry trends, clearer regulations, and growing institutional demand for onchain credit rails, the DAO launched Gearbox Permissionless. Just six months later, Permissionless now accounts for over 70% of total TVL, has 4×ed our speed to market, and future-proofed Gearbox’s growth trajectory. The Permissionless model was

Gearbox Protocol BlogMugglesect

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