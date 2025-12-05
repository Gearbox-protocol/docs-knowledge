[MODE=PRODUCT]


Gearbox Permissionless for Curators
Gearbox Permissionless is the new foundation for building on-chain credit markets. As Gearbox shifts into a fully permissionless architecture, we invite fintech companies, asset managers, structured product desks, and sophisticated DeFi operators to build their own lending verticals on top of an infrastructure that has already proven itself across four years of mainnet performance.

For fintech and TradFi teams, the appeal is straightforward: Gearbox gives you the ability to run a capital-efficient lending business without building a lending protocol from scratch, without managing liquidity, and without the operational or regulatory burden of directly handling user funds. You define the market, its risk parameters, collateral mix, and pricing logic — and Gearbox executes everything automatically and securely under the hood.

A Curator on Gearbox effectively becomes the owner of a lending instance: a standalone vertical that attracts deposits from passive liquidity providers and offers leverage or borrowing opportunities to users. Instead of thinking of risk curation as just adjusting LTVs and measuring volatility, it becomes a way to grow an entire business vertical. As a Curator, you control how borrowers interact with your market, how rates are structured, and how your vertical differentiates itself. Fees are shared between the protocol, LPs, and you — the Curator — allowing you to build recurring revenue from a product that would otherwise require a large engineering and risk team to maintain.

No Active Liquidity Management Needed
A curator on Gearbox is not required to directly manage user liquidity, neither on the passive side nor on the borrower side, unlike with other curator-based DeFi lendings. On Gearbox Permissionless, a curator manages risks (LTVs, collateral assets, limits per asset) and is also able to manage unique ±collateral borrow rates (see below) - but not the money itself. That means less transaction overhead and a more efficient unified experience for users.
For example, suppose a curator wants to enable several collateral assets that utilize USDC as a borrowing asset. In that case, they don’t need to create separate USDC pools for each; one unified pool suffices. Reducing compliance overhead: By eliminating the need for manual liquidity management, Curators can avoid activities that in many jurisdictions could be classified as financial intermediation (managing liquidity directly).

Unique Borrow Rates Per Collateral
Curators on Gearbox have the autonomy to set borrowing rates as per the risk associated with the market. All of the enabled collaterals inside a pool can have unique borrow rates per collateral. A proposition unique to Gearbox.
Unlike traditional DeFi lending protocols, Gearbox uses a dynamic two-part rate model:

Base rates: driven by pool utilization, the curve you are all familiar with (3-tick, in fact). It can be set up steep or flat, to enable less unnecessary rate fluctuations.
An adaptive risk premium set by Curators: every collateral has a unique extra borrow rate, meaning if you borrow USDC to put it into USDe, you might be paying 6%, while if you put the borrowed USDC into USDS, you would be paying 4%.
This allows Curators to apply targeted risk premiums based on the actual collateral and strategies used. Making capital allocation safer and risk-aligned for lenders, and most importantly, making the rates more efficient to set yourself apart from others.

The Easiest Deployment On New Chains & Day-0 Oracles
Gearbox Permissionless supports deployments on any new chain faster than anyone else, because it does not require any existing supporting infrastructure to be pre-deployed:

No need to wait for oracles to be deployed on that chain: pull-oracles like Redstone can be reused from another chain to support price feeds on a new chain.
No need to wait for Safe to be live on the new chain.
Gearbox has its own router/aggregator so that you don’t have to wait for CowSwap or 1inch to deploy on a new chain.
No AMM Depth Requirement: There is also no need to wait for AMMs or DEXes liquidity to be deep if the integrations are based on withdraw-deposit operations (where the secondary market is not essential). Unlike other lending protocols that rely only on DEX liquidity to add collaterals, Gearbox can support such integrations.
Gearbox Permissionless is already technically live on 27 different networks, enabling Curators to launch markets across various Layer 2 and Layer 1 EVMs.
Our modular oracle stack, including Chainlink, RedStone, Pyth and smart-contract-based price feeds tailored for ERC4626, Curve, Convex, Balancer LP positions, etc., provides reliable and flexible data feeds essential for accurate pricing from Day 0.

No-Slippage & No-Price-Impact UX for Borrowers (!)
Lending markets are majorly used for farming strategies, whereas price impact and slippage on entry/exit usually eat a solid chunk of a position. With Gearbox, integrations like LRTs or LSTs or any farming which has direct asset withdrawals-redemptions - can be integrated directly into Credit Accounts. What this means is no slippage or price impact on entry and exit. You can do high-leverage strategies without worrying about these things! You can go 10x farming stables or ETH and lose nothing on entry or exit. Unique to Gearbox.

Unique Collateral Support
Gearbox Credit Accounts come with 45+ integrations, offering collateral support for most major DeFi protocols like Pendle, Ethena, Sky, Morpho, Curve and other BTCfi, LST and LRT collaterals. Any new collateral support is usually a breeze with Gearbox.
Non-Tokenised Collateral support: as mentioned before, Gearbox’s Credit Accounts are capable of providing leverage natively on other protocols. This enables Curators to set up markets for non-tokenised assets such as staking vaults for LSTs and LRTs, Convex LP positions, Infrared positions and more. These strategies remain exclusive to Gearbox.

1-Click Integrated Leverage Functionality
Markets on Gearbox feature native 1-click leverage capabilities. Borrowers can access leverage instantly, facilitating streamlined execution of complex strategies without additional engineering overhead or the need for integration by third-party tools. The same works for rebalancing or exiting positions, natively. No requirement to ask for other UIs to integrate.
Multichain UI support for leverage & borrows: some other prtocools require Curators to source integrations with other UI when deploying on new chains. Gearbox, on the other hand, supports UX for both lending and borrowing side out of the box. Easier path to users!

Security and Compliance Resilience
Security is foundational at Gearbox. Over 4 years of continuous mainnet operation, the protocol has not incurred a single cent of bad debt or suffered any security exploit, placing Gearbox among the most battle-tested lending protocols in DeFi. With more than $3 million invested in audits, formal verification, and real-time monitoring systems, Gearbox sets a high bar for resilience. Additionally, Gearbox has multiple inbuilt compliance measures.
KYC and Whitelist Optionality: Gearbox provides built-in flexibility for Curators to deploy KYC-gated markets as needed, supporting use cases that require regulatory compliance. You can also restrict a list of borrowers or lenders, building a more permissioned vertical. For example, if you want to be the sole borrower of your pool (instance).

“Is there anything extra I can get as a Curator, perhaps technical support with price feeds and integrations?” - Sure thing, reach out to us and we’d love to walk you through!