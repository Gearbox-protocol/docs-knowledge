# Renzo: ezpz loans

gh-author-image-list
[](/author/mugglesect/)
gh-author-name-list
#### [Mugglesect](/author/mugglesect/)
gh-article-meta
gh-article-meta-inner
Sep 26, 2024 [] [7 min]
Imagine you have a valuable watch collection, but there\'s a yacht you want to buy. Instead of selling your watches for the yacht, you convince a watch dealer to loan you money against your collection. You then leave your watches with the lender until you return the money.

But what if you have a watch in your collection you want to sell? What if you are no longer into watches and want to swap them for vintage cars? What if you want to rent the watches and earn passively from them while they are with the lender?

In usual circumstances, this won\'t be possible as your collateral gets locked when you take a loan against it. This problem stands true even for onchain borrowing against ezETH and pzETH. *And this is precisely what Gearbox\'s Multicollateral loans are here to change.*

------------------------------------------------------------------------

## Multicollateral loans against ezETH/pzETH

Multicollateral loans enable users to borrow against multiple assets AND use their collateral to farm, trade, stake, or do what they want across DeFi. Think of it as owing a lender money against your watch collection but still being able to trade, rent, or sell your watches so long as the collateral value is higher than debt. Unlike Gearbox\'s spot leverage, Multicollateral loans can be withdrawn to a user\'s wallet and are non-levered.

Don't worry about the number of steps, multicall uses account abstraction to execute the entire process in 1 click.

### ezETH

What you can borrow: **USDC, WETH**\
LTV: 90\
Points boost: **2X ezPoints** and 1X EigenLayer points\
Oracle: **Reserve/Fundamental oracle**, no exposure to market price

------------------------------------------------------------------------

### pzETH

What you can borrow: **WETH**\
LTV: 90\
Points boost: **2X ezPoints, 2X Mellow Points** and 1X Symbiotic points (Subject to symbiotic restaking caps)\
Oracle: **Reserve/Fundamental oracle**, no exposure to market price

To simplify, borrowing against your assets on Gearbox enables you to

⏫ Earn More Points\
🧘‍♀️ Removes exposure to market price\
🌊 Keep your collateral liquid

*How and where? Just follow the quick UI walkthrough below.*

> NOTE: To enter a leveraged ezETH or pzETH position, you don\'t need to loop. Gearbox enables this in 1 click through leveraged strategies here: [https://app.gearbox.fi/restaking/list](https://app.gearbox.fi/restaking/list?ref=blog.gearbox.fi)

------------------------------------------------------------------------

### UI Walkthrough

Despite the backend mechanics of a Multicollateral loan being slightly complex, ***opening a position only takes 1 click***.

1.  Head over to [https://app.gearbox.fi/lending](https://app.gearbox.fi/lending?ref=blog.gearbox.fi), and make sure you are on the \"Borrow\" tab.
2.  Select whether you want to borrow against ezETH or pzETH and the amount of debt you want to take. Note the liquidation price (on the right), and avoid withdrawing near the maximum LTV to reduce the risk of being liquidated.

3.  Want to borrow against ezETH and pzETH both? Click on the \"Add asset\" option and borrow against both in 1 go.

4.  Click on \"Borrow Asset\", approve your transaction and voila! You are all set.

You can see your borrowed asset in your wallet. Make sure you monitor your position and borrow rate periodically. A healthy LTV is the ideal way to borrow!

**Quick Note:** The UI shows borrow rates in two ways. The default setting is to calculate the borrow rate relative to your collateral instead of your debt. You can switch this by clicking on \"Borrow rate\" on the right and then clicking on \"Account Value.\" This will display borrow rates similar to other lending apps.

Multicollateral Loans use an isolated smart contract wallet called the **Credit Account (CA)** for borrowers to deposit collateral, instead of using a lending pool.. The Credit Account can borrow assets from Gearbox\'s lending pools till the LTV on the supplied assets is reached. The debt is then transferred to a user\'s wallet (EOA). Effectively:

> Open a Credit Account -\> Add Collateral -\> Borrow from lending pool -\> Withdraw debt

------------------------------------------------------------------------

## Benefits of Multicollateral Loans

### **Flexible Collateral Management**

Let\'s divide collateral assets into 3 broader categories: Majors, Stables, and Alts. With crypto\'s volatility, users often swap between the 3 to manage their portfolio. In a peer-to-pool borrowing model, the collateral you provide has no flexibility. This means you can\'t switch your collateral from majors to stables without first repaying your debt and then withdrawing your collateral from the lending pools.. For that, you need to use portfolio management tools like DeFiSaver. Then it's solvable, but not as flexible or native as a user would want it to be.

Multicollateral loans, though, completely solve this problem. Since you supply your collateral to a smart contract wallet (Credit Account) instead of a pool, ***your collateral is isolated and remains liquid***. The credit account lets you swap your collateral for any other allowed asset. Once a CA is opened, users can access all the usual operations of reducing debt, increasing it, and whatever else older-generation lending protocols allow you to do. But because of Multicollateral you can also swap from stables to alts or majors even when you have borrowed and withdrawn assets. You can move your collateral between different yield sources. Fully liquid!

------------------------------------------------------------------------

### **Collateral-Based Borrow Rates**

With older-generation lending protocols, the borrow rate for an asset remains the same regardless of what collateral is deposited. Consider two users: The first supplies CRV and LINK, while the other deposits ETH and WBTC. If they both borrowed USDC against their collateral on OG lending protocols, they would both pay the same borrow rate.

Borrow rate for USDC on existing lending protocols

On Gearbox, this changes. Your borrow rates depend on the risk associated with your collateral. If you supply majors or stables, you are likely to pay a lower rate than the users who borrow against alts.

Borrow rate for USDC on Gearbox (Indicative; actuals might differ)

This is made possible through Gearbox\'s \"Quota\" rates, which align borrow rates with risk. More on that later in the article.

------------------------------------------------------------------------

### Rates on Gearbox - Quotas

Lending protocols usually determine rates based on utilisation. While this addresses an asset\'s supply-demand dynamics, it doesn\'t address the risk that different positions represent to the lenders and the protocol. To achieve this, borrow rates on Gearbox have two components.

1.  **Base Borrow Rate:** Determined by utilisation of a debt pool and remains relatively low till utilisation is greater than 90%
2.  **Quota rates: **This component addresses the risk aspect of the collateral. GEAR stakers democratically vote regarding the additional borrow rates for an asset. More volatile assets see higher quota rates, while lower-risk assets see lower quota rates. How do quota rates work, and what are gauges? Read the article below.

Gauges: Democratising Borrow Rates

This week saw the rise of macroeconomic experts across CT. Will Powell cut rates by 25 BPS? Or by 50 BPS? CT waited with bated breath to know how the Fed would affect our internet coins. While the build-up to the event was fascinating, it also outlined the importance of

Gearbox Protocol BlogMugglesect

The above two rates combined help create a risk-adjusted rate for every collateral. This also enables Multicollateral loans to offer lower rates to users with less risky collateral. So go ahead and get borrowing, head over to:

Gearbox Protocol - Composable Leverage

Leverage farm and stake on Curve, Lido, Balancer, and more. Or simply earn passive APY.

Composable Leverage

------------------------------------------------------------------------

> Borrow against your cake and eat it, too. Multicollateral Lending.

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

JOIN DISCORD