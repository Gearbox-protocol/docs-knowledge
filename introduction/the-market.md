# The Market

## Market Structure

### Market Structure

Gearbox uses a hierarchical, tree-structured constraint model: Pools define global rules, Credit Managers inherit and specialize them, and Credit Accounts inherit both. Every node operates strictly within the envelopes defined by its ancestors, ensuring consistent risk and parameter discipline across all strategies.

1. **Pool (Global Constraint Layer):** Defines system-wide parameters: eligible collateral types, price sources, utilization curve, and global limits. All downstream components inherit these constraints.
2. **Credit Managers (Strategy Constraint Layer):** Each Credit Manager refines the global constraints into strategy-specific ones: position-level rules, leverage parameters, liquidation settings and more. Credit Manager configuration + Pool-level boundaries are applied to all the credit accounts.
3. **Credit Accounts (Execution Layer):** Individual accounts execute under both the global Pool constraints and the strategy-level constraints of their Credit Manager.

<figure><img src="../.gitbook/assets/image (1).png" alt=""><figcaption></figcaption></figure>

### How Market Rules Shape Outcomes

Understanding the rules at each level guides decision-making process for every participant:

* **For lending users (LPs and borrowers)**
  * Constraints set the credit risk and expected yield for LPs. Tighter settings reduce risk and also reduce return.
  * Borrowers must operate within market parameters, so they should review the rules before taking leverage.
* **For curators**
  * Constraints determine the target investors by fixing the risk and return profile on both supply and borrow sides.
* **For asset issuers and applications**
  * Market configuration includes parameters that shape UX: external integrations, capital capacity, and liquidation discounts influence how end users experience the product.

### Market-specific rules

#### Pool-level rules

If a user disagrees with these terms, they need to select another pool.

* **Total debt limit:** maximum that can be borrowed across the entire pool
* **Collateral limit:** maximum that can be borrowed against each token
* **Main Price Feed:** price source for calculating account value and triggering liquidations
* **Reserve Price Feed:** runs safety checks on operations and can block Credit Account actions to protect LPs
* **Increase Rate:** one-time fee whenever exposure to a collateral increases
* **Collateral-specific rate:** extra interest for borrowing against a given collateral
* **IRM:** utilization-based interest rate model
* **Loss Policy:** additional liquidation logic for cases that create bad debt

**Credit Manager-level rules**

If a user disagrees with these terms, they can choose another Credit Manager within the same pool.

* **Total debt limit:** maximum aggregate debt of all Credit Accounts created from this Credit Manager
* **MinDebt:** minimum required debt for a Credit Account
* **MaxDebt:** maximum permitted debt for a Credit Account
* **Liquidation Premium:** portion of collateral value paid to the liquidator during liquidation
* **Liquidation Fee:** portion of collateral value paid to the curator and Gearbox DAO during liquidation
* **Max Enabled Tokens:** number of different collateral tokens that can count toward account value
* **Interest Fee:** extra rate on top of the IRM and collateral-specific rate, split between the curator and DAO
* **List of allowed collaterals and their LT** (loan to value)
* **List of allowed adapters:** restricts which external contracts a Credit Account can use
* **Expiration Policy:** curator may set an expiration; after the cutoff date, all Credit Accounts become liquidatable regardless of Health Factor with penalties set by the expired liquidation fee and premium parameters.
