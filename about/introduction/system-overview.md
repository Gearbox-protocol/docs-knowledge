# System Overview

Gearbox is permissionless lending infrastructure for on-chain credit. It provides the contract-level rails on which institutions, asset issuers, and fintechs deploy and operate lending markets — without protocol team involvement.

After the V3.1 release, any qualified operator can create, configure, and manage a lending market end-to-end. No governance proposal required. No deployment queue. The operator deploys contracts, sets risk parameters, and opens the market to borrowers and lenders.

This page covers what Gearbox does, who it serves, and the two design properties that make permissionless market creation safe — not merely possible.

---

## What Gearbox Is (and Isn't)

Gearbox is not a lending application. It is the infrastructure layer that lending applications deploy on.

A single Gearbox deployment provides the full credit stack: passive liquidity pools, isolated borrower accounts, adapter-based protocol integrations, oracle price feeds, and liquidation mechanics. Market operators assemble these components into products — a stablecoin yield market, a leveraged staking product, a prediction-market credit facility — without writing or auditing new smart contracts.

The distinction matters for capital allocators evaluating Gearbox:

- **For lenders:** Capital is deposited into a Pool, not into a specific market. Yield is aggregated across all connected markets. The lender's exposure is diversified by design.
- **For borrowers:** Each borrower receives an isolated smart contract wallet (a Credit Account) that interacts with external DeFi protocols through audited adapters. The borrowing experience is composable, not siloed.
- **For market operators (Risk Curators):** The full lifecycle — market creation, risk parameterization, adapter selection, interest rate tuning — is self-service. The protocol enforces safety invariants; the operator makes business decisions.

---

## Two Design Choices That Make It Work

Permissionless market creation introduces an obvious question: how does the protocol remain safe when anyone can launch a market? Two architectural properties answer it.

### Strict Role Segregation

Access rights and responsibilities are enforced at the contract level. No single actor — not the DAO, not a market operator, not a multisig — can unilaterally compromise the system.

- The **DAO** ships new protocol versions and configures fee splits. It cannot access user funds.
- The **Instance Owner** (per-chain multisig) whitelists price feeds and manages chain-specific infrastructure. It cannot access user funds.
- **Risk Curators** (per-market operators) set risk parameters — Liquidation Thresholds, debt limits, allowed collateral. These changes affect users and are subject to mandatory timelocks.

This separation means the DAO does not bottleneck market operators, and market operators cannot compromise the protocol.

### Verifiable Deployment

A functional Gearbox market consists of dozens of contracts. With V3.1, the deployment process is fully on-chain and verifiable.

The Gearbox DAO approves specific contract versions after audits. The compiled bytecode is stored in an on-chain Bytecode Repository. When a market is deployed — by any operator, on any chain — factory contracts verify that the deployed code matches the authorized bytecode.

This guarantee eliminates trust in the deployer. An integrator or lender evaluating a new Gearbox market does not need to audit the operator's deployment — only confirm the bytecode matches the DAO-approved version.

---

## Who Does What (Governance at a Glance)

Gearbox governance operates on three tiers. Each tier has defined powers and explicit limitations.

| Entity | Scope | Powers | Affects Users? |
|---|---|---|---|
| **DAO** (tokenholders) | All chains | Ships new protocol versions; configures fee splits | No — cannot touch user funds |
| **Instance Owner** | One chain | Whitelists price feeds; manages chain-level infrastructure | No — cannot touch user funds |
| **Risk Curators** | Specific markets | Sets risk parameters (LTVs, rates, debt limits) | Yes — subject to timelock |

The three-tier model ensures that:

- A protocol upgrade does not require individual market operators to act.
- A market operator's parameter change does not require DAO approval.
- A failure or misconfiguration in one market does not propagate to the protocol or other markets.

---

## Learn More

- **How does the liquidity model work?** → [One Pool, Many Markets](one-pool-many-markets.md)
- **What is the core lending primitive?** → [Credit Accounts](credit-accounts.md)
- **Can Gearbox deploy on a specific chain?** → [Omni-EVM Architecture](omni-evm-architecture.md)
- **How is the Pool technically implemented?** → [Core Architecture: Pool](../core-architecture/pool.md)
