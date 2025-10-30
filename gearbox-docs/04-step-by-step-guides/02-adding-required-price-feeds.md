[Copy]

:

:
##

The Price Feed Store is a chain-specific registry that lists which tokens and price feeds can be used within Gearbox on that chain.

For a token to be used as collateral, it must first be added to the Price Feed Store, along with a list of available price feeds.
Only the **Instance Owner**---a chain-specific multisig---can add or update entries in the Price Feed Store. This role acts as a neutral technical gatekeeper, ensuring safe and verified configurations while staying out of risk or business decisions.

The Instance Owner multisig is open to participation from active curators and chain contributors, making the process transparent and inclusive without compromising protocol safety.
##

Interface for accessing each chain\'s PFS is located at [https://permissionless.gearbox.foundation/instances](https://permissionless.gearbox.foundation/instances/1).

**Demo of PFS setup workflow:**

:

iframe
:

:

##

Price source

Feed type

Supported collaterals & features

[***Chainlink, Redstone push, EO*** AggregatorV3Interface - compatible external price providers](https://docs.gearbox.fi/gearbox-permissionless-doc/step-by-step-guides/adding-required-price-feeds#external-feeds)
:

External
:

Blue-chip tokens
:

[***ERC4626 exchange rate***](https://docs.gearbox.fi/gearbox-permissionless-doc/step-by-step-guides/adding-required-price-feeds#erc4626-exchange-rate)
:

ERC4626
:

Most of the yield-bearing vaults
:

[***Pyth***](https://docs.gearbox.fi/gearbox-permissionless-doc/step-by-step-guides/adding-required-price-feeds#pyth)
:

Pyth
:

Blue chip & emerging tokens
:

[***Redstone pull***](https://docs.gearbox.fi/gearbox-permissionless-doc/step-by-step-guides/adding-required-price-feeds#redstone-pull)
:

Redstone
:

Deployed on any EVM on day 0
:

***Upper bound***
:

Bounded
:

-
:

-
:

:

***Multiply 2 feeds price***
:

Composite
:

Optimal way to price correlated token pairs
:

***Constant price***
:

Constant
:

-
:

-
:

:

[***Curve LP*** ](https://docs.gearbox.fi/gearbox-permissionless-doc/step-by-step-guides/adding-required-price-feeds#curve-stable)
:

Curve_crypto Curve_stable
:

Collateralize Curve LP tokens
:

***Token price from Curve Pool***
:

Curve TWAP
:

Collateralize experimental tokens with pricing based on DEX trades
:

[***Pendle PT***](https://docs.gearbox.fi/gearbox-permissionless-doc/step-by-step-guides/adding-required-price-feeds#pendle-pt)
:

Pendle PT TWAP
:

Get TWAP market price of PTs
:

[***Kodiak Island***](https://docs.gearbox.fi/gearbox-permissionless-doc/step-by-step-guides/adding-required-price-feeds#kodiak-island)
:

Kodiak_island
:

Get island share price
:

##

Pyth[](#pyth)

:
:

Name:

-
:

-
:

:

Name: RLP (Redemption rate) Feed: [https://insights.pyth.network/price-feeds/Crypto.RLP%2FUSD.RR](https://insights.pyth.network/price-feeds/Crypto.RLP%2FUSD.RR)
:

Name: RLP (Market) Feed: [https://insights.pyth.network/price-feeds/Crypto.RLP%2FUSD](https://insights.pyth.network/price-feeds/Crypto.RLP%2FUSD)

:

Token:

-
:

:

descriptionTicker

-
:

:

:
:

Pyth

-
:

:

Ethereum - 0x4305FB66699C3B2702D4d05CF36551390A4c69C6
:

Berachain - 0x2880aB155794e7179c9eE2e38200202908C17B43
:

Etherlink - 0x2880aB155794e7179c9eE2e38200202908C17B43

:

maxConfToPriceRatio (takes value in bps: 300 = 3%)

-
:

-
:

:

Example (consider maxConfToPriceRatio = 3%)

-
:

:

Price: 3000
:

Confidence interval: 15
:

confToPriceRatio = 15/3000 = 0.5%

-
:

:

Price: 3000
:

Confidence interval: 120
:

confToPriceRatio = 120/3000 = 4%

:

Staleness Period

-
:

-
:

External feeds[](#external-feeds)

**Click New Feed and select External type**

:

***Dashboards of external providers:***

-
:

-
:

-
:

-
:

:

[*Resolv*](https://docs.resolv.xyz/litepaper/for-developers/smart-contracts/price-oracles)
:

[*Midas*](https://docs.midas.app/defi-integration/price-oracle)

###

-
:

:

Specify token Symbol and Provider name
:

Examples:

-
:

-
:

-
:

-
:

-
:

:

Address of deployed feed

-
:

:

Gearbox contracts track the timestamp of last Feed\'s update If the update happened more than Staleness Period seconds ago contracts will revert ***Motivation**: If the feed with heartbeat of 24 hours wasn\'t updated in the last 30 hours, smth bad happened with the oracle providers and protocol operations are blocked waiting for Curator to interfere*
:

Recommended value:

-
:

:

87 300s = 24h + 15min

-
:

:

86 520s = 24h + 2min

ERC4626 exchange rate[](#erc4626-exchange-rate)

:

[](#config-parameters-1)

*Config parameters:*
:

Name:

-
:

-
:

:

Name: sDAI (Chainlink) Will mean that this feed takes ERC4626 sDAI/DAI exchange rate directly from sDAI contract + DAI/USD price from Chainlink

:

Vault:

-
:

:

underlyingPriceFeed:

-
:

-
:

:

If the specified vault it sUSDe, then underlying price feed should return USDe/USD price.

Redstone pull[](#redstone-pull)

**Click New Feed and select Redstone type**

:

###

-
:

:

Specify token Symbol and Price methodology

Examples:

-
:

-
:

-
:

:

Token address Needed for Gearbox contracts to understand what pull feed needs to be updated

-
:

:

The same as name This parameter is to be removed later

-
:

:

Most likely should be kept untouched Internal variable for non-standard sources of redstone data

-
:

:

:

-
:

:

Minimum amount of signatures from Redstone nodes to have for the feed\'s result to be deemed valid.
:

Redstone currently have maximum of 5 nodes.
:

The safest option is to set this value to 5 (this was historically used in Gearbox), but sometimes couple of Redstone nodes may stop working for a short periods of time.

-
:

:

Most likely should be kept untouched Redstone have fixed list of signers\' addresses that rarely (if ever) changes

Kodiak island[](#kodiak-island)

**Click New Feed and select Kodiak_island type**

:

###

-
:

:

Specify token Symbol and sources of Underlying Prices Example:

-
:

:

[Island](https://app.kodiak.finance/#/liquidity/pools/0x24afceb372b755f4953e738d6b38e9e4646d9f57?farm=0x199f156bba61496401dc2a009b5f69eb9a7e6f21&chain=berachain_mainnet)
:

Feed0: [Pyth iBERA](https://insights.pyth.network/price-feeds/Crypto.IBERA%2FUSD)
:

Feed1: [Redstone push iBGT](https://app.redstone.finance/app/feeds/berachain/ibgt/)

-
:

:

Island Address

-
:

:

Select the feed from already added to price token with 0\'th index in terms of USD

-
:

:

Select the feed from already added to price token with 1\'st index in terms of USD

-
:

:

The same as name This parameter is to be removed later

Pendle PT[](#pendle-pt)

[](#before-any-deployment-ensure-that-pendle-market-has-correct-cardinality.-it-should-be-no-less-than-t)

Before any deployment, ensure that pendle market has correct cardinality. It should be no less than twapWindow / blockTime + 1 for a given chain.

To check cardinality, go to LP contract and get \_storage()\[4\]. To update cardinality, call increaseObservationsCardinalityNext of an LP contract.

[](#pendle-chainlink-compatible-factory)

Pendle chainlink-compatible factory
:

Factory Addresses:

-
:

-
:

:

:
:

Add deployed pendle feed as external (staleness period = 1)
:

Deploy Composite Gearbox Oracle Set Feed 1 to previously deployed PT-to-SY feed Set Feed 2 to feed which prices SY to USD

:
:

:

[](#gearbox-pt-feed)

Gearbox PT feed

:

[](#config-parameters-4)

*Config parameters:*
:

Name:

-
:

:

Name: PT-sUSDE-25SEP2025 (Chainlink)

-
:

:

market

-
:

Pendle Market address

:

:

UnderlyingPriceFeed

-
:

:

priceToSy

-
:

-
:

:

twapWindow

-
:

-
:

[](#deploy-bounded-gearbox-oracle)

Deploy Bounded Gearbox Oracle
:

Curve Stable[](#curve-stable)

**Click New Feed and select Curve_stable type**

:

###

-
:

:

Specify pool Symbol and sources of Underlying Prices Example:

-
:

:

[Pool](https://www.curve.finance/dex/ethereum/pools/factory-crvusd-0/deposit/)
:

Feed0: Chainlink crvUSD
:

Feed1: Chainlink USDC

-
:

:

:

-
:

:

:

-
:

:

Select a feed from allowed list to price pool\'s tokens at given indexes
:

If pool has only 2 tokens in it, specify only underlyingPriceFeed0 & 1

Pendle LP[](#pendle-lp)

[](#before-any-deployment-ensure-that-pendle-market-has-correct-cardinality.-it-should-be-no-less-than-t-1)

Before any deployment, ensure that pendle market has correct cardinality. It should be no less than twapWindow / blockTime + 1 for a given chain.

To check cardinality, go to LP contract and get \_storage()\[4\]. To update cardinality, call increaseObservationsCardinalityNext of an LP contract.

[](#pendle-chainlink-compatible-factory-1)

Pendle chainlink-compatible factory
:

Factory Addresses:

-
:

-
:

:

:
:

Add deployed pendle feed as external (staleness period = 1)
:

Deploy Composite Gearbox Oracle Set Feed 1 to previously deployed LP-to-SY feed Set Feed 2 to feed which prices SY to USD

:
:

:

[](#gearbox-pt-feed-1)

Gearbox PT feed

:

[](#config-parameters-6)

*Config parameters:*
:

Name:

-
:

:

Name: PT-sUSDE-25SEP2025 (Chainlink)

-
:

:

market

-
:

Pendle Market address

:

:

UnderlyingPriceFeed

-
:

:

priceToSy

-
:

-
:

:

twapWindow

-
:

-
:

[](#deploy-bounded-gearbox-oracle-1)

Deploy Bounded Gearbox Oracle
:
: