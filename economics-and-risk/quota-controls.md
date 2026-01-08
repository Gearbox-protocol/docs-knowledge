# Quota Limits & Concentration

The Quota Control system is the protocol's mechanism for managing concentration risk and pricing asset-specific exposure. While the Liquidity Pool provides a shared source of capital, the Quota system enforces strict limits on how that capital can be allocated toward specific collateral assets and applies additional risk premiums where necessary.

### Asset-Side Caps (Concentration Limits)

To protect Liquidity Providers (LPs) from over-exposure to specific assets, the protocol enforces **Quota Limits**. These are hard caps on the total amount of debt that can be collateralized by a specific token across all Credit Managers attached to a pool.

#### Mechanism

Unlike a global debt ceiling which limits the total size of the pool or Credit Manager limits which define maximum exposure to particular strategies, Quota Limits operate on the **collateral side**.

* **Exposure Calculation:** The system tracks the total value of borrowing power currently backed by a specific asset (e.g., $WBTC).
* **Enforcement:** If the total exposure reaches the defined Quota Limit, the system blocks any transaction that would further increase exposure to that asset.
  * New Credit Accounts cannot be opened with that collateral.
  * Existing accounts cannot increase the amount of debt that is backed by particular token.
  * Repayments and closures remain enabled to allow deleveraging.

This architecture ensures that even if a pool has abundant idle liquidity, it cannot be drained into a single illiquid or high-risk strategy beyond the safety parameters defined by the Curator.

### Quota Rates (Risk Premium)

The Quota system decouples the cost of liquidity from the cost of risk. It allows the protocol to charge an additional interest rate—the **Quota Rate**—based specifically on the collateral held by the borrower.

#### The Additive Rate Model

The total cost of borrowing before fees is the sum of the base cost of capital and the specific risk premium of the collateral.

$$
\text{Total APR} = \text{Base Rate} + \text{Quota Rate}
$$

* **Base Rate:** Determined by the utilization of the Liquidity Pool. This represents the opportunity cost of the underlying asset (e.g., USDC).
* **Quota Rate:** Determined by the specific collateral asset (e.g., a volatile governance token). This represents the risk premium for holding that specific asset.

#### Pricing Granularity

This separation allows for granular risk pricing within a single pool:

* **Low-Risk Collateral:** Borrowers using blue-chip assets (e.g., WETH) may pay only the Base Rate (Quota Rate = 0%).
* **High-Risk Collateral:** Borrowers using volatile or less liquid assets must pay the Base Rate plus a significant Quota Rate (e.g., +5%).

This ensures that borrowers using safe collateral do not subsidize the risk of those using volatile collateral, improving capital efficiency for low-risk strategies while properly pricing tail risk.

### Further Reading

* **Base Interest Calculation:** For details on how the underlying pool utilization determines the base cost of capital, see Interest Rate Model.
* **Parameter Configuration:** To understand who configures these limits and the specific parameter ranges, see the Risk Configuration Dictionary.
*   **Protocol Fees**

    A portion of the interest paid is captured as revenue for the Protocol DAO and the Market Curator.

    * **See:** [Fee Sharing](https://www.google.com/url?sa=E\&q=..%2Fintroduction%2Ffee-sharing.md)
