# Omni-EVM Architecture

## Omni-EVM Architecture

Gearbox Protocol is designed as a **Deployable Primitive** rather than a monolithic cross-chain application. It does not rely on bridges for message passing or state synchronization between chains. Instead, every deployment on a new chain is a standalone, self-contained **Instance**.

This architecture ensures that risk is isolated to the specific chain and that the protocol can scale permissionlessly to any EVM-compatible network without waiting for centralized bridge infrastructure.

### Modular Instances

An **Instance** is a complete, functional replica of the Gearbox Protocol deployed on a specific blockchain network.

* **Independence:** Each Instance operates autonomously. A failure or pause on one chain does not propagate to others.
* **No Bridge Dependency:** Core protocol functions (borrowing, lending, liquidations) do not require cross-chain messaging.
* **Local Configuration:** Parameters are tuned specifically for the local ecosystem (e.g., block times, gas costs, and available liquidity) rather than inheriting global defaults that may not fit.

This modularity allows the protocol to exist natively on high-speed L2s or sidechains while maintaining the security standards established on Mainnet.

### Bytecode Repository (Verifiable Deployment)

To ensure security across many independent instances, Gearbox utilizes a **Bytecode Repository**. This acts as an onchain "Source of Truth" for protocol logic.

1. **Global Verification:** The Gearbox DAO votes to approve specific contract versions (e.g., `CreditFacade V3.1`) after audits are completed.
2. **Onchain Storage:** The compiled bytecode of these approved contracts is stored in the Bytecode Repository on the canonical chain.
3. **Trustless Deployment:** When a new Instance is deployed or updated, the factory contracts verify that the code being deployed matches the authorized bytecode in the repository.

This mechanism guarantees that every Instance, regardless of who deployed it, runs the exact, audited code approved by the DAO.

### Governance Architecture

Because Instances are independent, governance is split into **Global** (Code & IP) and **Local** (Configuration & Risk) layers. This separation of concerns allows for efficient scaling without creating a bottleneck at the DAO level.

| Entity              | Scope                    | Responsibility                                                                                              |
| ------------------- | ------------------------ | ----------------------------------------------------------------------------------------------------------- |
| **Protocol DAO**    | Global (All Chains)      | Manages the codebase, approves new versions, and governs the Bytecode Repository.                           |
| **Instance Owner**  | Local (One Chain)        | A technical multisig responsible for chain-specific infrastructure, such as whitelisting local price feeds. |
| **Market Curators** | Local (Specific Markets) | Independent operators who deploy lending markets and manage economic risk parameters (LTVs, Rates).         |

#### Further Reading

* **How are the token holders' financial interests and the delivery of the core codebase managed?**\
  [See: Protocol DAO](https://www.google.com/url?sa=E\&q=..%2Fgovernance-and-operations%2Fprotocol-dao.md)
* **Who oversees local chain parameters specifically?**\
  [See: Instance Owner](https://www.google.com/url?sa=E\&q=..%2Fgovernance-and-operations%2Finstance-owner.md)
* **Who manages business building and specific risk parameters?**\
  [See: Market Curators](https://www.google.com/url?sa=E\&q=..%2Fgovernance-and-operations%2Fmarket-curators.md)
