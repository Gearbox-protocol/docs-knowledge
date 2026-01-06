# Gearbox Markets

## One pool - multiple collaterals

* **For lenders**\
  Deposit a single asset and earn yield backed by loans against a curated basket of collaterals.
* **For borrowers**\
  Access liquidity using a diversified portfolio of tokens as collateral.
* **For curators**\
  Maximize LP yields through collateral-specific interest rates, without actively managing funds.

<figure><img src="../../.gitbook/assets/image (12).png" alt=""><figcaption></figcaption></figure>

## Anatomy of the market

Gearbox operates on a tiered constraint model. This hierarchy ensures that capital is protected by global safety rails, while enabling Curators to design distinct lending products with specific risk profiles.

Risk parameters flow downstream: global constraints set the absolute boundaries, while downstream layers refine these rules for specific strategies.

1. **Pool (Global Constraint Layer):** Defines market-wide parameters: eligible collateral types, price sources, utilization curve, and global limits. All downstream components inherit these constraints.
2. **Credit Managers (Strategy Constraint Layer):** The business logic modules attached to the Pool. Defines the specific "Lending Product" offered to borrowers. One manager might offer high leverage on correlated assets, while another offers lower leverage on volatile assets.
3. **Credit Accounts (Execution Layer):** Individual accounts execute under both the global Market constraints and the strategy-level constraints of their Credit Manager.\
   If an action violates the specific rules of its Credit Manager (e.g., leverage too high) or the global limits of the Pool (e.g., asset not allowed), the transaction reverts.

<figure><img src="../../.gitbook/assets/image (10).png" alt=""><figcaption></figcaption></figure>

### How Market Rules Shape Outcomes

Understanding the rules at each level guides decision-making process for every participant:

* **For lending users (LPs and borrowers)**
  * Constraints set the credit risk and expected yield for LPs. Tighter settings reduce risk and also reduce return.
  * Borrowers must operate within market parameters, so they should review the rules before taking leverage.
* **For curators**
  * Constraints determine the target investors by fixing the risk and return profile on both supply and borrow sides.
* **For asset issuers and applications**
  * Market configuration includes parameters that shape UX: external integrations, capital capacity, and liquidation discounts influence how end users experience the product.
