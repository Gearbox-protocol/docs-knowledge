# Price Oracle

The Price Oracle serves as the protocol's central valuation engine. Its primary function is to ingest raw price data from diverse external sources and standardize it into a uniform format that the Credit Manager and Pool contracts can consume mathematically.

### Data Normalization

DeFi assets vary significantly in their technical specifications, particularly regarding decimal precision (e.g., USDC uses 6 decimals, WETH uses 18). To prevent calculation errors and complexity within the risk engine, the Price Oracle enforces a strict normalization standard.

**The 8-Decimal Standard**\
Regardless of the underlying token's decimals or the external feed's native precision, the Gearbox Price Oracle always returns prices scaled to **8 decimals**.

* **Input:** Raw data from Chainlink (8 decimals), Uniswap (18 decimals), or USDC (6 decimals).
* **Process:** The Oracle wrapper scales the value up or down mathematically.
* **Output:** A standardized USD price where `1.00` is represented as `100,000,000`.

This uniformity allows the Credit Manager to perform solvency checks ($HealthFactor > 1$) using a single, consistent formula across all collateral types.

### Staleness Enforcement

To ensure solvency calculations reflect current market reality, the Price Oracle enforces strict data freshness constraints.

Every price feed is configured with a specific `stalenessPeriod` (measured in seconds), typically derived from the feed provider's heartbeat or update frequency.

* **The Check:** Upon every transaction requiring a price (e.g., borrowing, liquidating), the Oracle compares the current `block.timestamp` against the feed's `updatedAt` timestamp.
* **The Revert:** If `block.timestamp - updatedAt > stalenessPeriod`, the transaction reverts immediately.

This mechanism prevents the protocol from accepting invalid collateral or allowing under-collateralized borrowing during periods of oracle downtime or network congestion.

### Feed Types

The protocol supports various data methodologies depending on the asset's liquidity profile and available onchain data. These are categorized into three primary mental models.

#### 1. Spot Feeds

Spot feeds provide the current market price based on off-chain aggregation or high-frequency on-chain updates. These are typically used for highly liquid "Blue Chip" assets where the price discovery happens on centralized exchanges or deep DEX pools.

* **Push Models:** Traditional oracles where nodes push updates onchain at defined intervals or deviation thresholds (e.g., Chainlink, Redstone Push).
* **Pull Models:** On-demand oracles where the price update is cryptographically signed off-chain and pushed onchain only when needed by a transaction (e.g., Pyth, Redstone Pull). This model reduces gas costs and allows for higher frequency updates.
* **Use Case:** WETH, WBTC, USDC.

#### 2. TWAP Feeds (Time-Weighted Average Price)

TWAP feeds calculate the average price of an asset over a specific period (e.g., 30 minutes). This methodology dampens volatility and increases the cost of manipulation for assets that rely primarily on decentralized exchange liquidity.

* **Mechanism:** Queries the cumulative price accumulator from an AMM (Automated Market Maker) and divides by the time elapsed.
* **Use Case:** Curve LP Tokens, Pendle PTs, or long-tail assets where spot liquidity is thin.

#### 3. Fundamental Feeds (Derived Value)

Fundamental feeds determine value based on the on-chain backing or exchange rate of the asset, rather than secondary market trading activity. These feeds calculate what the asset is "worth" in terms of its underlying reserves.

* **Mechanism:** Reads the `convertToAssets` or `getRate` function from the token contract and multiplies it by the underlying asset's USD price.
* **Use Case:** ERC-4626 Vault Shares, Liquid Staking Tokens (LSTs), or Stablecoin peg-protection modules.

### Modular Pricing Architecture

Beyond standard oracle integrations, Gearbox maintains a library of purpose-specific pricing contracts designed to collateralize complex DeFi positions.

These modular feeds allow the protocol to support assets that lack direct secondary market feeds by programmatically deriving their value from the underlying protocol state:

* **Curve & Balancer LPs:** Calculates the "Virtual Price" or fair value of the LP token based on the pool's invariant and the prices of the constituent tokens.
* **Pendle PTs:** Derives the market price using a TWAP of the PT/SY exchange rate from the Pendle market contract.
* **Bounded Feeds:** Wrappers that enforce upper or lower bounds on a price (e.g., capping a stablecoin at $1.00 or an LST at its backing ratio) to prevent manipulation during de-peg events.

This architecture enables Curators to list productive assets (Vaults, LPs, Derivatives) as collateral without waiting for centralized oracle providers to support them.

***

#### Learn More

* **Safety & manipulation resistance:** How does the system protect against oracle manipulation and extreme market conditions?
  * [dual-oracle-system.md](smart-oracles/dual-oracle-system.md "mention")
