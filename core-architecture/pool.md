# Pool (The Liquidity Vault)

## Pool (The Liquidity Vault)

The **Liquidity Pool** serves as the liability side of the Gearbox Protocol balance sheet. It is a passive, ERC-4626 compliant smart contract where lenders deposit assets (e.g., USDC, WETH) to earn yield.

Unlike traditional lending protocols where a pool interacts directly with individual borrowers, the Gearbox Pool operates on a **Wholesale Banking Model**. It does not lend directly to users; instead, it allocates capital to **Credit Suites** (Credit Managers), which act as specialized lending branches with distinct risk configurations.

### Core Mechanics

#### 1. Passive Liquidity & ERC-4626

The Pool is strictly passive. It holds the underlying asset and issues **Diesel Tokens** (dTokens) to depositors as a receipt of liquidity provision.

* **Standard:** Fully compliant with [ERC-4626](https://www.google.com/url?sa=E\&q=https%3A%2F%2Feips.ethereum.org%2FEIPS%2Feip-4626) (Tokenized Vault Standard).
* **Fungibility:** Diesel Tokens are fungible and transferable, allowing them to be used as collateral in other DeFi protocols.

#### 2. Diesel Tokens (Non-Rebasing Yield)

Yield accrual in Gearbox is reflected through the **Exchange Rate**, not through balance updates.

* **Non-Rebasing:** Unlike aTokens (Aave), the wallet balance of Diesel Tokens does not increase over time.
* **Value Accrual:** As borrowers pay interest, the amount of underlying assets in the Pool grows while the supply of Diesel Tokens remains constant. Consequently, the exchange rate increases.

$$
Exchange\ Rate = \frac{Total\ Assets\ (Principal + Interest)}{Total\ Supply\ of\ dTokens}
$$

#### 3. The Branch Model (Wholesale Lending)

The Pool delegates the complexity of risk management and borrower interaction to **Credit Suites**.

* **The Pool (Wholesale Bank):** Aggregates liquidity from lenders. It has no knowledge of individual borrowers, collateral types, or liquidation logic. Its only function is to lend capital to approved Credit Suites up to a defined limit.
* **Credit Suites (Retail Branches):** Borrow liquidity from the Pool to fund Credit Accounts. Each Suite enforces specific risk parameters (LTV, allowed assets, liquidation rules).

This separation of concerns ensures that the Pool remains lightweight and secure, while complexity is pushed to the periphery (the Suites).

### Risk Isolation & Allocation

A single Pool can fund multiple Credit Suites simultaneously. The Market Curator manages the Pool's risk exposure by setting a **Debt Ceiling** for each connected Suite.

* **Allocation Limits:** The Curator defines the maximum capital available to each Suite (e.g., 80% to a Low-Risk Suite, 20% to a High-Risk Suite).
* **Firewalling:** If a specific Strategy (Credit Suite) suffers a failure or bad debt, the loss is contained within that Suite's allocation. The Pool's exposure is limited to the capital lent to that specific branch, protecting the remaining liquidity.

### Learn More

* **Yield source:** How is the utilization-driven interest rate calculated?
  * [interest-rate-model.md](../economics-and-risk/interest-rate-model.md "mention")
* **Yield optimization & risk control:** How are collateral-specific rates and collateral exposure limits handled?
  * [quota-controls.md](../economics-and-risk/quota-controls.md "mention")
* **Deposits utilization:** Where is the liquidity actually used or lent to?
  * [credit-suite.md](credit-suite.md "mention")
