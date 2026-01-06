# Credit Suite (The Strategy module)

The **Credit Manager** is the "Brain" of a lending market. While the Pool holds the money, the Credit Manager defines **how that money can be used**.

By configuring a Credit Manager, a Curator creates a specific **Financial Product** (e.g., "Stablecoin Farming Strategy" or "Leveraged ETH Staking").

#### 1. The Credit Manager (The Accountant)

This contract is the central ledger. It tracks the debt and collateral of every individual Credit Account.

* **Risk Isolation:** A single Liquidity Pool (e.g., USDC) can fund multiple Credit Managers.
  * _Manager A_ might allow only Blue-Chip assets (Low Risk).
  * _Manager B_ might allow Volatile assets (High Risk).

#### 2. The Credit Facade (The Gatekeeper)

This is the contract borrowers interact with. It acts as a firewall for the Credit Account.

**The "Check-on-Exit" Rule:**\
Users can perform complex actions (swap, trade, farm) within a single transaction. The Facade allows _any_ action as long as the account remains solvent at the end of the transaction.

The check is simple: **Is the Health Factor (HF) greater than 1?**

* _If HF > 1:_ Transaction succeeds.
* _If HF < 1:_ Transaction reverts.

{% hint style="info" %}
**HF** calculation is based on **Total Weighted Value (TWV)** of collateral. This is not just the market value; it is the market value _discounted_ by the Liquidation Threshold (LT).

If Account holds $100 of ETH with an LT of 90%, the system values it at $90 for solvency purposes.

* [**Deep Dive: Full Liquidation Math & Formulas**](https://www.google.com/url?sa=E\&q=..%2Fgearbox-markets%2Fliquidation-dynamics.md)
{% endhint %}

#### 3. The Credit Configurator (The Control Panel)

Credit Configurator stores the key risk parameters of the Strategy, like liquidation Threshold, Liquidation premium, which are referenced by Facade and Manager on logic execution.

* **Safety:** The Configurator validates every change (e.g., "Is this Liquidation Threshold valid?") before applying it to the live system.

### Deep Dive

Now that you understand the container, explore the mechanics that govern it.

#### 1. What are the core risk parameters?

Curators control the market by tuning specific variables (LTV, Supply Caps, Fees). Understanding these inputs is critical for both managing a market and using one.

* [**See: Roles & Contract Specification**](https://www.google.com/url?sa=E\&q=roles-and-contract-level-specification.md)

#### 2. How do liquidations work?

The system relies on third-party liquidators to maintain solvency. Learn the rules, incentives, and math that determine when an account is liquidated.

* [**See: Liquidation Dynamics**](https://www.google.com/url?sa=E\&q=liquidation-dynamics.md)

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
