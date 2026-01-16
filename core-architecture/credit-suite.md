# Credit Suite (The Strategy Module)

The Credit Suite is the architectural assembly responsible for managing the asset side of the protocol's balance sheet. While the Liquidity Pool manages passive capital (liabilities), the Credit Suite defines the logic, risk parameters, and execution boundaries for active borrowers (assets).

A single Liquidity Pool can be connected to multiple Credit Suites, each representing a distinct **Credit Manager** with unique risk configurations, allowed collateral assets, and borrowing limits. This isolation allows the protocol to compartmentalize risk strategies without fragmenting underlying liquidity.

### Architectural Components

The Credit Suite consists of three primary smart contracts, each with distinct responsibilities regarding accounting, execution, and configuration.

#### 1. Credit Manager (The Accountant)

The Credit Manager is the central logic container and state manager for a specific lending strategy. It acts as the "Accountant" of the system.

* **State Management:** It maintains the ledger of all Credit Accounts associated with the strategy, tracking debt amounts and collateral values.
* **Adapter Registry:** It stores the list of approved Adapters (integrations) and enforces the "Allowlist" of tokens that can be held as collateral.
* **Solvency Logic:** It contains the mathematical logic for calculating the Health Factor (HF).

#### 2. Credit Facade (The Entry Point)

The Credit Facade serves as the primary entry point for borrower interactions. It abstracts the complexity of the Credit Manager and enforces execution safety.

* **Multicall Execution:** The Facade allows users to bundle multiple operations (e.g., `borrow`, `swap`, `deposit_into_vault`) into a single atomic transaction.
* **Check-on-Exit Solvency:** The Facade implements the protocol's optimistic execution model. It permits any sequence of whitelisted operations during a transaction but enforces a strict solvency check at the end.
  * If HF > 1 at the end of the transaction, the state changes are committed.
  * If HF < 1, the entire transaction reverts.
* **Permissions:** It handles user permissions, ensuring that only the owner of a Credit Account can initiate transactions affecting that account.

{% hint style="info" %}
**HF** calculation is based on **Total Weighted Value (TWV)** of collateral. This is not just the market value; it is the market value _discounted_ by the Liquidation Threshold (LT).

If Account holds $100 of ETH with an LT of 90%, the system values it at $90 for solvency purposes.

* [**Deep Dive: Full Liquidation Math & Formulas**](https://www.google.com/url?sa=E\&q=..%2Fgearbox-markets%2Fliquidation-dynamics.md)
{% endhint %}

#### 3. Credit Configurator (The Management Layer)

The Credit Configurator provides the administrative interface for Market Curators to manage the Credit Suite. It decouples governance logic from the core accounting logic.

* **Parameter Updates:** Curators interact with the Configurator to adjust risk parameters (e.g., Liquidation Thresholds, Fees, Limits) rather than interacting with the Credit Manager directly.
* **Validation & Safety:** The Configurator validates inputs to prevent invalid states (e.g., setting a Liquidation Threshold > 100%) before applying changes to the Credit Manager.
* **Timelock Enforcement:** It enforces mandatory delays for critical parameter changes, ensuring users have time to react to risk adjustments before they become active.

### Interaction Flow

1. **Configuration:** The Curator sets risk parameters via the **Credit Configurator**.
2. **Execution:** The Borrower submits a multicall transaction to the **Credit Facade**.
3. **Accounting:** The Facade routes instructions to the **Credit Manager**, which updates the Credit Account's state and interacts with the **Pool** or **Adapters**.
4. **Verification:** The Facade requests a final solvency check from the Credit Manager before finalizing the transaction.

### Learn More

* **Solvency enforcement:** How liquidations work?
  * [liquidation-dynamics](../economics-and-risk/liquidation-dynamics/ "mention")
* **Risk controls:** What is the complete list of parameters that define the strategy?
  * [risk-configuration-dictionary.md](../reference/risk-configuration-dictionary.md "mention")
