# Omni-EVM Architecture

Gearbox deploys as independent, self-contained instances per chain — no bridges, no cross-chain messaging, no shared state. Each deployment is a complete protocol with its own pools, markets, and governance parameters.

This page explains the rationale for independent instances, the mechanism that keeps deployments trustworthy without central control, and the governance split between global and local authority.

---

## Why Independent Instances, Not a Cross-Chain Application

Gearbox is a deployable primitive, not a monolithic cross-chain application. Every deployment on a new EVM chain is a standalone **Instance** — a full, functional protocol stack operating autonomously.

This design has four properties relevant to integration and deployment planning:

**Fault isolation.** A failure, exploit, or governance pause on one chain does not propagate to any other chain. Each Instance's risk boundary is the chain it runs on.

**No bridge dependency.** Core protocol functions — borrowing, lending, liquidation — require zero cross-chain messaging. There is no bridge to trust, no relay to monitor, no cross-chain latency to account for.

**Local parameter tuning.** Each Instance is configured for its local ecosystem: block times, gas costs, available liquidity, oracle infrastructure. Parameters are optimized for the chain, not inherited from global defaults that may not fit.

**Deployment flexibility.** Gearbox can deploy on any EVM-compatible chain — L1, L2, sidechain — without waiting for bridge infrastructure, cross-chain governance tooling, or messaging protocol support.

---

## How Deployments Stay Trustworthy Without Central Control

Independent instances raise a trust question: how can a lender or integrator verify that a Gearbox deployment on an unfamiliar chain runs the correct code?

The answer is the **Bytecode Repository** — an on-chain source of truth for protocol logic.

The verification process works in three stages:

1. **DAO approval.** The Gearbox DAO votes to approve specific contract versions (e.g., CreditFacade V3.1) after audits are completed.
2. **On-chain storage.** The compiled bytecode of approved contracts is stored in the Bytecode Repository on the canonical chain.
3. **Deployment verification.** When a new Instance is deployed or updated, factory contracts verify that the code being deployed matches the authorized bytecode in the repository. Deployment uses deterministic addressing (Create2) for independent verification.

This mechanism eliminates trust in the deployer. An integrator evaluating a Gearbox market on a new chain does not need to audit the operator's deployment. The integrator verifies that the deployed bytecode matches the DAO-approved version — a check that is programmatic, not social.

---

## Who Controls What: Global vs. Local Governance

Because Instances are independent, governance is split into layers. This separation prevents the DAO from becoming a bottleneck while ensuring local operators have autonomy within a defined framework.

| Entity | Scope | Responsibility |
|---|---|---|
| **Protocol DAO** | Global (all chains) | Manages the codebase. Approves new contract versions. Governs the Bytecode Repository. Sets the rules of the game. |
| **Instance Owner** | Local (one chain) | Technical multisig for chain-specific infrastructure — whitelisting local price feeds, managing chain-level operational parameters. |
| **Market Curators** | Local (specific markets) | Independent operators who deploy lending markets and manage economic risk parameters: Liquidation Thresholds, interest rates, debt limits. |

### What This Means for Deployment Planning

- **A new chain deployment does not require DAO approval for every parameter change.** The DAO approves the codebase; local operators configure the markets.
- **Market Curators operate independently.** Two Curators on the same chain can run entirely different strategies, risk profiles, and collateral sets — no coordination required.
- **The Instance Owner is a technical role, not a business role.** The Instance Owner manages infrastructure (price feeds, emergency pauses), not market strategy.

---

## Learn More

- **How does the Protocol DAO govern the codebase?** → Governance & Operations: Protocol DAO
- **What does the Instance Owner do on a specific chain?** → Governance & Operations: Instance Owner
- **How do Market Curators create and manage lending markets?** → Governance & Operations: Market Curators
