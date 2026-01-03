# Price Oracle (The Valuation Engine)

The Price Oracle is the "source of truth" for the entire market. It aggregates real-time price data from external providers (like Chainlink or Redstone) and normalizes it so the protocol can accurately calculate account health, collateral values, and liquidation thresholds.

#### Core Functions

* Data Aggregation & Normalization: It acts as a router that standardizes disparate data sources. Regardless of whether a feed comes from Chainlink, Redstone, or a custom adapter, the Oracle converts it into a uniform format (typically 8 decimals) that the Credit Managers can consume.
* Staleness Enforcement: It actively polices data quality. If a price feed hasn't updated within its defined heartbeat (e.g., 1 hour), the Oracle rejects the data and transactions relying on it will revert, preventing the system from acting on old market information.
* Dual-Feed Architecture: Uniquely, it supports a Main Feed and a Reserve Feed for every asset. This allows the system to compare price sources against each other (e.g., Chainlink vs. Uniswap TWAP) to detect de-pegs or oracle manipulation attacks.

#### Curator Controls

* Main Feed: Curators map tokens to specific on-chain feed contracts, which must return the dollar price of assets to be used for Health checks and liquidations.
* Staleness Period: Defines the maximum age (in seconds) of a valid price update. Curators tune this based on the asset's volatility and the feed's update frequency. If the feed weren't updated for more than Staleness Period, all the operations depending on it will revert.
* Reserve Feed: Assigns a secondary backup feed. While often optional, Curators use this for high-risk assets to provide a "second opinion" on the price, ensuring that a single oracle failure doesn't result in false liquidations.
