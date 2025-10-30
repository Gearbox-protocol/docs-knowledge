:

1.  [Competitive advantages](/gearbox-permissionless-doc/competitive-advantages)

# Dual-oracle pricing
Gearbox oracle and solvency checks structure allows creating pricing methods with unique features:

-
:

-
:

###

Gearbox operates with 2 feeds for each collateral: ***Main*** feed and ***Reserve*** one. Main feed is used for for Account Value calculation during Liquidation checks.

Reserve oracles provide an additional security layer to protect liquidity providers (LPs) from oracle manipulation risks, ensuring accurate collateral valuations.

Reserve oracle is used during collateral checks in multicalls, which is a mechanism to perform complex defi interactions from credit accounts in single transaction. The multicalls are introduced on the Credit Accounts page, see below:

In particular, **Reserve** price feed is involved when the multicall includes **Collateral Withdrawal** or **External Calls** through adapters. The collateral check after such operations prices each collateral using the Safe Price:

####

Oracles are crucial for determining collateral value in lending protocols. Unlike simple exchanges (e.g., Uniswap), lending protocols rely heavily on external data. Risks include:

-
:

-
:

###

There are two main methodologies of pricing tokens that is used in most of the lending markets:

-
:

-
:

Feed type

Pros

Cons
:

:

:

:

:

:

###

Let\'s compare how properly configured **Main** and **Reserve** feeds can protect lenders while preserving exceptional UX and capital efficiency for borrowers by studying multiple market cases. In the table below, the case when some collateral token is used to borrow blue-chip stablecoin such as USDC.

:
:

:
sUSDe/USD market price drops by \>2.5%
:

[No liquidations of existing positions ]
:

[No liquidations of existing positions]
:

[Risky positions liquidated]
:
(paranoid) USDe/USD market price drops by \>10%
:

[No liquidations of existing positions][ ][Safe price = min(market, hardcoded) = \$0.9 Can borrow \$0.915 per USDe, but can\'t withdraw it from credit account ⇒ liquidity doesn\'t exit the protocol.]
:

[No liquidations of existing positions] [Attack vector: - buy at \$0.9 - borrow \$0.915 at max LTV (e.g. 91.5%) TVL lent is used as exit liquidity]
:

[Major part of positions liquidated]
:
deUSD/USD market price pumps by \>2.5%
:

[No liquidations of existing positions]
:

[No liquidations of existing positions]
:

[No liquidations of existing positions]
:
(illiquid market manipulation) deUSD/USD market price pumps by \>10%
:

[No liquidations of existing positions Can borrow \$1.02 per deUSD, but can\'t withdraw it from credit account ⇒ liquidity doesn\'t exit the protocol.]
:

[No liquidations of existing positions]
:

[No liquidations of existing positions]

[Attack vector: - mint deUSD at \$1 - borrow \$1.02 at max LTV (e.g. 92.5%)]

[ TVL lent drained due to inflated valuation]
:

###

The Gearbox Oracle contract supports major price feed providers, including Chainlink, Redstone (both pull and push models), and Pyth. These providers are referred to as *external* because their data often comes from off-chain sources (e.g., centralized exchanges) or requires off-chain computation applied to on-chain data.

Integrating tokens with these external providers can be costly and slow. To address this, Gearbox developers created modular, reusable Price Feed contracts to efficiently price DeFi collaterals. For example:

-
:

-
:

This modular pricing approach extends to other DeFi collaterals, such as Pendle PT tokens and Curve LP tokens, with dedicated Price Feed contracts already implemented. For a complete list of Price Feed contracts, refer to the the Gearbox Bytecode Repository:

[[[Previous][Deployment addresses]]](/gearbox-permissionless-doc/deployment-addresses)[[[Next][Collateral-specific rates]]](/gearbox-permissionless-doc/competitive-advantages/collateral-specific-rates)

Last updated 2 months ago
: