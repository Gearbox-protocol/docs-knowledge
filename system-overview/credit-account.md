---
layout:
  width: default
  title:
    visible: true
  description:
    visible: true
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: true
  metadata:
    visible: true
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/yE16Xb3IemPxJWydtPOj/getting-started/publish-your-docs
---

# Credit Accounts (The Primitive)

## Credit Accounts (The Primitive)

The Credit Account is the fundamental primitive of the Gearbox Protocol. It functions as a user-owned, isolated smart contract wallet that holds both collateral and borrowed funds, enabling leveraged execution across DeFi protocols.

### Core Concept: Isolated Smart Contract Wallet

Unlike traditional lending protocols where user collateral is siloed in a global vault, Gearbox deploys a unique smart contract for each borrower.&#x20;

<figure><img src="../.gitbook/assets/legacy-lending.png" alt=""><figcaption></figcaption></figure>

The Credit Account serves as a container for the user's entire position.

* **Segregated State:** Assets within the Credit Account are legally and technically distinct from the protocol's liquidity pools.
* **User Ownership:** The user retains control over the account's operations, subject only to the solvency checks enforced by the Credit Manager.
* **Portability:** Because the Credit Account is a standard smart contract, it can interact with external protocols as a distinct entity, preserving the identity of the position.

### Atomic Solvency Check

The Credit Account operates on a "Check-on-Exit" architecture. The protocol does not restrict specific actions within a transaction bundle, provided the account remains solvent at the conclusion of the execution trace.

Upon the completion of any interaction (e.g., a swap or deposit), the protocol calculates the account's **Health Factor**.

* **If Health Factor > 1:** The transaction is finalized and recorded on-chain.
* **If Health Factor < 1:** The entire transaction reverts, ensuring no bad debt can be created atomically.

This mechanism allows users to perform complex, multi-step operations in a single transaction without requiring the protocol to understand the intermediate states, as long as the final state satisfies the risk parameters.

<figure><img src="../.gitbook/assets/ca-lending.png" alt=""><figcaption></figcaption></figure>

### Composability via Adapters

The Credit Account interacts with the external DeFi ecosystem through **Adapters**. These are lightweight contract interfaces that translate generic user intents into protocol-specific function calls.

From the perspective of an external protocol, the Credit Account appears as a standard user wallet. This enables:

1. **Native Execution:** Users interact directly with external contracts rather than through a protocol-specific abstraction layer.
2. **Programmable Credit:** Developers can compose credit logic into arbitrary workflows, treating the Credit Account as a programmable leverage module.

***

### Learn More

* **Risk Enforcement:** the logic for calculating the Health Factor and enforcing solvency is managed by the Credit Manager and Credit Facade.
  * &#x20;[credit-suite.md](../core-architecture/credit-suite.md "mention")
* **External Interactions:** The mechanism for connecting Credit Accounts to external DeFi protocols is defined by the Adapter system.
  * [adapters-integrations.md](../core-architecture/adapters-integrations.md "mention")
* **Liquidity Source:** The capital borrowed by the Credit Account is sourced from the passive Liquidity Pool.
  * [pool.md](../core-architecture/pool.md "mention")
