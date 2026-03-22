# Adapters & Integrations

Adapters are the mechanism that allows Credit Accounts to interact with external DeFi protocols — Uniswap, Curve, Lido, Convex — while maintaining solvency guarantees. Each Adapter is a translation contract that restricts Credit Account interactions to an audited set of functions on a specific target protocol.

This page covers the security problem Adapters solve, how they constrain interactions, their role in market design, the Router's multi-step execution, and emergency controls.

---

## Why Credit Accounts Cannot Call Arbitrary Contracts

A Credit Account holds leveraged funds — borrowed capital plus collateral. If a borrower could call any external contract with any function signature, the check-on-exit solvency model would be circumventable. Complex DeFi interactions could be constructed to extract value from the Credit Account in ways that leave the account insolvent between the operation and the health check.

Adapters exist to close this attack surface. Without them, permissionless composability and solvency enforcement are mutually exclusive.

---

## How Adapters Make External Interactions Safe

Adapters are **constrained interfaces** — each one permits Credit Account interactions with a specific external protocol through a defined, audited set of functions.

### Three Layers of Constraint

**Function whitelisting.** The Adapter exposes only the functions that have been audited for safety. A borrower interacting with Uniswap through the Uniswap Adapter can execute the specific `swap` functions defined in that Adapter — nothing else. Arbitrary function calls to the Uniswap router are not possible.

**Result verification.** After execution, the Adapter verifies that trade outcomes (tokens received, balances changed) match expectations. This prevents state manipulation attacks where an external protocol returns unexpected values.

**Transparent identity.** From the external protocol's perspective, the Credit Account appears as a standard wallet executing a standard transaction. No special handling, no wrapper contracts, no protocol-specific integration on the external side. From Gearbox's perspective, the interaction is fully constrained to the Adapter's audited interface.

---

## How Adapters Shape the Product (Curator Perspective)

The choice of enabled Adapters defines what a market can do. Adapter selection is a product decision, not just a technical one.

Gearbox's modular architecture separates credit into two layers:

- **Core Layer:** Provides capital and enforces solvency (Health Factor checks, debt accounting).
- **Adapter Layer:** Extends the Core with purpose-specific execution capabilities.

### Adapter Selection as Product Design

The Adapter set determines the market's utility:

| Market Purpose | Required Adapters | Example Protocols |
|---|---|---|
| Yield farming | Vault and farm adapters | Convex, Lido, Midas |
| Leveraged trading | DEX swap adapters | Uniswap, Curve |
| Prediction markets | Order book adapters | Protocol-specific |
| Collateral liquidation paths | DEX adapters supporting collateral tokens | Uniswap (wstETH pairs), Curve |

**Practical consequence:** A market that accepts wstETH as collateral but does not enable DEX Adapters supporting wstETH trading forces borrowers into high-slippage exits. Limited Adapter coverage directly reduces product utility.

---

## The Router: Multi-Step Strategies in One Transaction

DeFi strategies often require multiple protocol interactions chained together. A position entry like "USDC → leveraged Convex steCRV" involves four separate protocol calls:

1. Swap USDC → WETH (Uniswap)
2. Deposit WETH → stETH (Lido)
3. Deposit stETH + WETH → steCRV (Curve)
4. Stake steCRV → Convex

The **Router** calculates optimal paths across all enabled Adapters and bundles these steps into a single multicall transaction. The borrower does not need to manually sequence Adapter calls, manage intermediate token balances, or optimize gas across multiple transactions.

The Router reduces execution complexity and gas costs — particularly relevant for strategies that span three or more protocols.

---

## Emergency Controls: Disabling Adapters

If an external protocol is exploited, becomes insolvent, or introduces unexpected risk, the Curator can disable that Adapter immediately through the Emergency Admin role.

Disabling an Adapter cuts off all Credit Account interaction with the affected protocol. The effect is immediate:

- No new transactions through that Adapter are possible.
- Existing positions that hold tokens from the disabled protocol are not automatically liquidated, but borrowers can no longer increase exposure.
- Other Adapters continue operating normally — the containment is surgical, not systemic.

This is the Curator's primary risk containment tool for external protocol failures.

---

## Learn More

- **How are Credit Accounts kept solvent after each operation?** → [Credit Suite](credit-suite.md)
- **How do adapters enable novel use cases like direct redemptions?** → Reference: Direct Redemptions
- **What is the fundamental primitive adapters connect to?** → [Introduction: Credit Accounts](../introduction/credit-accounts.md)
- **How does the Pool supply the capital that adapters help deploy?** → [Pool](pool.md)
