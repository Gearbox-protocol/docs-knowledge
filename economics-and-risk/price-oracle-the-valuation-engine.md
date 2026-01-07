# Price Oracle

The Price Oracle is the "source of truth" for the entire market. It aggregates real-time price data from external providers (like Chainlink or Redstone) and normalizes it so the protocol can accurately calculate account health, collateral values, and liquidation thresholds.

#### Core Functions

* Data Aggregation & Normalization: It acts as a router that standardizes disparate data sources. Regardless of whether a feed comes from Chainlink, Redstone, or a custom adapter, the Oracle converts it into a uniform format (typically 8 decimals) that the Credit Managers can consume.
* Staleness Enforcement: It actively polices data quality. If a price feed hasn't updated within its defined heartbeat (e.g., 1 hour), the Oracle rejects the data and transactions relying on it will revert, preventing the system from acting on old market information.
* Dual-Feed Architecture: Uniquely, it supports a Main Feed and a Reserve Feed for every asset. This allows the system to compare price sources against each other (e.g., Chainlink vs. Uniswap TWAP) to detect de-pegs or oracle manipulation attacks.

#### Curator Controls

* Main Feed: Curators map tokens to specific on-chain feed contracts, which must return the dollar price of assets to be used for Health checks and liquidations.
* Staleness Period: Defines the maximum age (in seconds) of a valid price update. Curators tune this based on the asset's volatility and the feed's update frequency. If the feed weren't updated for more than Staleness Period, all the operations depending on it will revert.
* Reserve Feed: Assigns a secondary backup feed. While often optional, Curators use this for high-risk assets to provide a "second opinion" on the price, ensuring that a single oracle failure doesn't result in false liquidations.

## Pricing

> While oracle providers continue to expand asset coverage, meaningful limitations remain:
>
> * Oracles from major providers are expensive for asset issuers, often delaying asset launches
> * Emerging assets or chain-local DeFi tokens may not be supported at all

Gearbox works with a wide range of oracle models, including major push-based providers such as Chainlink, Redstone, and other AggregatorV3Interface oracles and on-demand pull-based pricing via Pyth and Redstone.

More details on the differences between push and pull price feeds can be found in the Redstone blog.

{% embed url="https://blog.redstone.finance/2024/08/21/pull-oracles-vs-push-oracles/" %}

In addition, Gearbox supports a diverse set of modular smart-contract price feeds that are audited and approved for permissionless deployment. These feeds streamline pricing for standardized assets such as Curve LP tokens, ERC-4626 vaults, Pendle PTs, Tokens with bounded or formula-based prices and more.

The current list of allowed smart-contract feeds is available in the curators’ documentation.

{% embed url="https://docs.gearbox.fi/gearbox-permissionless-doc/step-by-step-guides/adding-required-price-feeds#what-price-feed-sources-are-already-integrated-click-on-feed-to-see-details" %}
