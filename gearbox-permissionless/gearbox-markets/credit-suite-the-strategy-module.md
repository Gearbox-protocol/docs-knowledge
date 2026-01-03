# Credit Suite (The Strategy module)

The Credit Suite is the Strategy Execution Module attached to the Pool. While the Pool manages the passive liquidity providers, the Credit Suite **serves** the active borrowers.

It acts as a strict operating environment that defines **what a borrower can do** with the funds. By configuring a Credit Suite, a Curator defines a specific **Strategy** — a user-facing credit product with defined collateral assets, maximum leverage, and liquidation rules.

### 1. Credit Manager (Collateral & Debt Accountant)

The Credit Manager acts as the central accounting unit for the strategy. Unlike standard lending protocols where collateral is often pooled, the Credit Manager tracks the specific balances of **each** Credit Account individually.

**Risk Isolation:** Each Credit Manager enforces rules specific to its strategy. For example, the same collateral token can hold different risk weights (Liquidation Thresholds) in two different Credit Managers, ensuring risk in one strategy does not contaminate another.

### 2. Credit Facade (Unified Execution Engine)

The Credit Facade acts as the gateway for users. It allows them to execute complex operations via **Multicall,** bundling actions like borrowing, swapping, and farming into a single atomic transaction.

**Check-on-Exit:** The module enforces an atomic **Solvency Check** after every Multicall. It verifies that `Total Weighted Value >= Total Debt`. This model allows for immense flexibility within the transaction as long as the Account ends up solvent.

### 3. Credit Configurator (The Control Panel)

The Credit Configurator serves as the parameter repository and the Curator's interface. While the Credit Manager holds the logic (formulas), the Configurator holds the **inputs** (risk variables).

**Safety & Validation:** Curators interact exclusively with the Configurator. It validates every parameter change, such as adding tokens or updating fees, before pushing them to the Credit Manager.

***

## Curator Controls (Via Credit Configurator)

Curators use the Credit Configurator to define the boundaries of the strategy.

#### 1. Risk & Solvency Logic

* **Liquidation Thresholds:** Sets the "Max Leverage" for each asset. It determines how much an asset counts towards solvency (e.g., LT 90% ≈ 10x max leverage).
* **Ramping:** Allows for **gradual updates** of risk parameters. Ramping lowers the LT slowly rather than instantly, giving borrowers time to adjust positions and avoiding unfair liquidations.
* **Loss Policy:** Defines the logic executed when a liquidation results in **Bad Debt** (loss). It acts as a safety hook to validate the event or handle the accounting.
* **Token Status:** Controls the asset list. Curators can add new tokens or strictly forbid existing ones if they become too risky.

#### 2. Strategy Constraints

* **Position Sizing:** Sets the **Min and Max Debt** per single account. This prevents "dust" accounts (unprofitable to liquidate) and limits the protocol's exposure to any single whale.
* **Velocity Limits:** Limits the **Total New Debt** that can be opened in a single block. This prevents "Flash Loan Attacks" where an attacker tries to max out the pool in one transaction to manipulate rates.
* **Lifecycle Management:** Sets a "shutdown date" for the strategy. Useful for fixed-term lending products. After this date, users can no longer borrow, only repay or close positions. Accounts may become liquidatable regardless of health factor to ensure the pool winds down.

#### 3. Financial Model

* **Liquidation Premium:** The bonus paid to liquidators to ensure they prioritize cleaning up bad debt.
* **Liquidation Fee:** The revenue cut taken by the Curator and the DAO from liquidation proceeds.
* **Interest Fee:** A percentage of the interest paid by borrowers is captured as revenue instead of passing to lenders. This fee is typically shared between the **Curator** and the **DAO**, incentivizing Curators to build active, healthy markets.

#### 4. Protocol Integration

* **Allowed Actions:** Defines the "Allowlist" of external protocols. Curators specify exactly which contracts are accessible. If an adapter isn't whitelisted, the borrower cannot interact with it.

#### 5. Emergency Controls

* **Pause Borrowing:** A "Soft Pause" mechanism for safety. It stops new loans from being taken while **always allowing** existing users to repay debt, add collateral, or close positions. Curators use this during market turbulence to cap exposure without trapping users.
