# Adapters & Integrations

## Adapters & Integrations

A Credit Account is a secure "Container." By default, it cannot interact with the outside world because the protocol cannot guarantee the safety of external smart contracts.

**Adapters** are the solution. They are specialized "Translation Contracts" that allow Credit Accounts to interact with specific DeFi protocols (like Uniswap, Curve, or Lido) while maintaining the strict solvency checks required by Gearbox.

### Modular Execution: Purpose-Optimized UX

Gearbox’s modular architecture unifies credit and execution.

* **The Core Layer:** Provides the capital and enforces solvency (Health Factor).
* **The Adapter Layer:** Extends this base with purpose-specific execution rules.

This allows Curators to design Financial Products tailored for specific use cases. One product might be optimized for **Prediction Markets** (interacting with order books), while another is optimized for **Yield Farming** (interacting with vaults).

<figure><img src="../.gitbook/assets/image (1).png" alt=""><figcaption></figcaption></figure>

### The Security Problem: Unrestricted Execution

A Credit Account holds leveraged funds. If users could interact directly with any smart contract, they could exploit complex DeFi mechanics to bypass solvency checks.

**How Adapters Fix This:**\
Adapters act as a **Sanitized Interface**. They restrict interactions to a specific, pre-defined set of functions that have been audited for safety.

1. **Function Whitelisting:** Users cannot call `any` function on Uniswap; they can only call the specific `swap` functions defined in the Adapter.
2. **Result Verification:** The Adapter ensures that the outcome of the trade (the tokens received) matches the protocol's expectations, preventing complex state manipulation attacks.

By forcing all interactions through these "Safe Tunnels," Gearbox ensures that the Credit Account's state remains predictable at all times.

### The Router: Intelligent Execution

While Adapters provide the _connection_, the **Router** provides the _path_.

DeFi strategies are rarely simple. A user might want to "Zap" from USDC directly into a Convex Curve-stETH position. This requires multiple steps:

1. Swap USDC -> WETH (Uniswap)
2. Deposit WETH -> stETH (Lido)
3. Deposit stETH + WETH -> steCRV (Curve)
4. Stake steCRV -> Convex

The Gearbox Router calculates the optimal path across all enabled Adapters and bundles these steps into a single **Multicall**.

<figure><img src="../.gitbook/assets/image.png" alt=""><figcaption></figcaption></figure>

### Curator Responsibilities

As a Curator, the choice of Adapters defines the **Utility** of the market.

1. **Enable Liquidity:** If a market accepts `wstETH` as collateral, the Curator should enable DEX Adapters (e.g., Uniswap or Curve) that support `wstETH` trading. Without it, users cannot swap into the Debt token. Limited allowed adapters will result in high slippage losses.
2. **Enable Yield:** To offer a "Farming Strategy," the Curator must enable the specific Adapter for that farm (e.g., the Convex Adapter or Midas vault adapter).
3. **Risk Management:** If a specific external protocol is hacked or becomes risky, the Curator can **Disable** that specific Adapter instantly via the Emergency Admin, protecting the pool from further exposure.

### Learn More

* **Solvency checks:**  How accounts are kept overcollateralized after each operation?
  * [credit-suite.md](credit-suite.md "mention")
* **Unique usecases:** How Credit Accounts and adapters unlock new credit interactions.
  * [direct-redemptions.md](../reference/direct-redemptions.md "mention")
