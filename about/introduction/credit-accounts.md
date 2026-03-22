# Credit Accounts

The Credit Account is Gearbox's core lending primitive — an isolated smart contract wallet deployed per borrower that holds both collateral and borrowed funds. This design makes Gearbox composable with the rest of DeFi and prevents bad debt without restricting what borrowers can do.

This page covers the architectural rationale, the solvency enforcement mechanism, and the composability model.

---

## Why "One Contract Per Borrower" Changes Everything

Traditional lending protocols pool user collateral into shared vaults. Gearbox takes a different approach: each borrower receives a unique smart contract — a Credit Account — that serves as the container for that borrower's entire position.

This has three consequences:

**Asset segregation.** Assets within a Credit Account are technically and logically distinct from the protocol's liquidity pools. One borrower's position does not comingle with another's.

**Operational control.** The borrower retains control over the account's operations — which assets to hold, which protocols to interact with, when to add or withdraw collateral — subject to solvency enforcement by the Credit Manager.

**Native DeFi identity.** Because the Credit Account is a standard smart contract with its own address, external protocols see it as a normal wallet. When a Credit Account executes a swap on Uniswap or deposits into a Curve pool, the external protocol processes a standard transaction from a standard address. No wrappers. No proxy abstractions. This is why Gearbox integrations feel native rather than intermediated.

---

## How Solvency Is Enforced Without Restricting Actions

Gearbox uses a **check-on-exit** architecture. The protocol does not restrict individual operations within a transaction bundle. A borrower can swap, deposit, withdraw, and rebalance across multiple protocols in a single multicall. The protocol evaluates only the final state.

At the end of every interaction, the Credit Manager computes the account's **Health Factor**:

> **Health Factor = Total Weighted Value / Total Debt**

- **Total Weighted Value (TWV):** The sum of all collateral asset balances, each multiplied by its oracle price and discounted by its Liquidation Threshold.
- **Total Debt:** Principal plus accrued interest (base rate + quota rate) plus fees.

The enforcement rule is binary:

| Outcome | Result |
|---|---|
| HF > 1 | Transaction commits. State changes are finalized on-chain. |
| HF < 1 | Entire transaction reverts atomically. No state change occurs. |

This design has two critical implications:

1. **Complex strategies are first-class operations.** A borrower can execute a multi-step strategy — borrow, swap through three protocols, deposit into a vault — in a single transaction. The protocol does not need to understand intermediate states; it enforces only the terminal solvency condition.

2. **Bad debt cannot be created atomically.** If a sequence of operations would leave the account undercollateralized, the transaction reverts before any state change is written. This is a hard guarantee enforced at the EVM level, not a soft constraint managed by off-chain monitoring.

---

## How Credit Accounts Connect to DeFi

Credit Accounts interact with external protocols through **Adapters** — lightweight translation contracts that map user intents to protocol-specific function calls.

From an external protocol's perspective, the Credit Account appears as a standard wallet executing a standard call. From Gearbox's perspective, the interaction is constrained to an audited set of functions.

This architecture enables **programmable credit**: developers can compose leverage into arbitrary workflows — yield farming, basis trading, structured products — without building protocol-specific integration layers. The Credit Account is the leverage module; the Adapter is the connection point; the external protocol executes as if interacting with any other wallet.

---

## Learn More

- **How is the Health Factor calculated, and who triggers liquidation?** → [Core Architecture: Credit Suite](../core-architecture/credit-suite.md)
- **How do Adapters work and what security guarantees do they provide?** → [Core Architecture: Adapters & Integrations](../core-architecture/adapters-integrations.md)
- **Where does the borrowed capital come from?** → [Core Architecture: Pool](../core-architecture/pool.md)
