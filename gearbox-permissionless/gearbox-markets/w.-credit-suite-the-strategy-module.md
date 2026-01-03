# w. Credit Suite (The Strategy Module)

The Credit Suite is the Strategy Execution Module attached to the Pool. While the Pool manages the passive liquidity providers, the Credit Suite **serves** the active borrowers.

It acts as a strict operating environment that defines **what a borrower can do** with the funds. By configuring a Credit Suite, a Curator defines a specific **Strategy**—a user-facing credit product with defined collateral assets, maximum leverage, and liquidation rules.

### Core Architecture

#### 1. Credit Manager (The Accountant)

Acts as the central ledger. Unlike standard lending protocols where collateral is often pooled, the Credit Manager tracks the specific balances of **each** Credit Account individually.

* **Risk Isolation:** Each Credit Manager enforces rules specific to its strategy. A token can have a 90% Liquidation Threshold in a "Stable" strategy but 0% in a "Volatile" strategy, ensuring risks don't cross-contaminate.

#### 2. Credit Facade (The Execution Engine)

Acts as the gateway for users. It allows them to execute complex operations via **Multicall**—bundling actions like borrowing, swapping, and farming into a single atomic transaction.

* **Check-on-Exit:** The module enforces an atomic **Solvency Check** after every Multicall. It verifies that `Total Weighted Value >= Total Debt`. This model allows for immense flexibility within the transaction as long as the Account ends up solvent.

#### 3. Credit Configurator (The Control Panel)

Serves as the Curator's interface. While the Credit Manager holds the logic (formulas), the Configurator holds the **inputs** (risk variables).

* **Safety & Validation:** Curators interact exclusively with the Configurator. It validates every parameter change (e.g., adding tokens, updating fees) before pushing them to the Credit Manager.

***

### Curator Controls

Curators use the **Credit Configurator** to define the boundaries of the strategy.

#### Risk & Solvency

* **Liquidation Thresholds:** Sets the "Max Leverage" for each asset (e.g., LT 90% ≈ 10x leverage).
* **Ramping:** Allows for gradual updates of risk parameters to avoid unfair immediate liquidations.
* **Loss Policy:** Defines the logic executed when a liquidation results in Bad Debt (e.g., triggering a secondary oracle check).
* **Token Status:** Controls the asset allowlist (Add/Forbid tokens).

#### Strategy Constraints

* **Position Sizing:** Sets Min/Max Debt per account to prevent dust and limit whale exposure.
* **Velocity Limits:** Limits total new debt per block to prevent Flash Loan attacks.
* **Lifecycle Management:** Sets a "shutdown date" for fixed-term strategies.

#### Financial Model

* **Liquidation Premium:** Bonus paid to liquidators to ensure fast response.
* **Liquidation Fee:** Protocol revenue from liquidations.
* **Interest Fee:** A % of borrowing interest captured as revenue for the Curator and DAO.

#### Protocol Integration

* **Allowed Actions:** The "Allowlist" of external protocols (Uniswap, Curve, etc.). If an adapter isn't listed, users cannot touch it.

#### Emergency Controls

* **Pause Borrowing:** A "Soft Pause" that stops new loans but allows repayments and closures.

***

### Operational Mechanics

_Critical behaviors for Curators and Integrators._

* **Liquidations during Pause:** If the Credit Facade is paused, liquidations become whitelisted to Emergency Liquidators who can still execute liquidations to prevent bad debt accumulation.
* **Expiration Behavior:** If a strategy has an expiration date, **all** accounts become liquidatable/closable after that timestamp, regardless of their Health Factor. Borrowing is disabled; only repayment is allowed.
* **Token Enablement:** Simply sending a token to a Credit Account does not count it as collateral. The user must explicitly `enableToken` for it to be included in the Health Factor calculation.

***

#### Developer Resources

* ICreditManagerV3 Interface
* ICreditFacadeV3 Interface
* ICreditConfiguratorV3 Interface
