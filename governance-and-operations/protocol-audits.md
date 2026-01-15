# Protocol audits

The **Bytecode Repository** is a core infrastructure component of Gearbox V3 designed to enable permissionless, multi-chain protocol expansion while maintaining strict security guarantees. It serves as a decentralized, on-chain registry for verified smart contract implementations.

#### An On-Chain "GitHub" for Smart Contracts

The Bytecode Repository acts as a decentralized version of a code hosting platform like GitHub, but for compiled EVM bytecode rather than source code.

* **Versioned Catalog:** Like a GitHub repository with tags, it organizes contracts into **Domains** (e.g., `IRM` for interest rate models) and **Postfixes** (e.g., `_LINEAR`), allowing for semantic versioning (Major/Minor/Patch).
* **Public vs. System Domains:**
  * **System Domains** (Core contracts like Credit Managers) are DAO-governed; updates require an on-chain vote.
  * **Public Domains** allow any developer to submit "plugins" (e.g., a new yield farming adapter). Once a developer's submission is verified, they "own" that identifier in the repository.
* **Immutable Storage:** Instead of a centralized server, the contract uses **SSTORE2** to store the initialization code (init code) directly in the Ethereum state, ensuring it can never be deleted or modified.

#### Protecting the Protocol Lifecycle

The repository protects the protocol by decoupling the **upload** of code from its **deployment**, introducing a mandatory verification layer.

**1. On-Chain Audit Verification**

Before a contract can be deployed via the repository, it must be "audited" on-chain. This is not just a social claim; it is a cryptographic requirement:

* **Approved Auditors:** The Gearbox DAO maintains a whitelist of approved auditor addresses in the `BytecodeRepository`.
* **EIP-712 Attestations:** Auditors sign a specific `bytecodeHash`. This signature is submitted to the repository via `submitAuditReport`.
* **Enforced Solvency:** The `deploy` function checks `isBytecodeAudited`. If a bytecode hash does not have a valid signature from an authorized auditor, the protocol will refuse to deploy it, preventing unverified or malicious code from entering the ecosystem.

**2. Deterministic and Secure Deployment**

The repository uses `CREATE2` to ensure that a contract deployed on Ethereum Mainnet will have the exact same address and code when deployed on L2s like Optimism or Arbitrum.

* **Front-running Protection:** It mixes the deployer's address into the salt, preventing malicious actors from "sniping" a contract address before the legitimate user.
* **Integrity Checks:** Upon deployment, the repository verifies that the resulting contract's `contractType` and `version` (via the `IVersion` interface) match the registry records.

#### Key Security Features

* **Init Code Blacklisting:** The DAO can permanently forbid specific `initCode` hashes (via `forbidInitCode`) if a vulnerability is found, effectively "bricking" that version and preventing any further deployments of it.
* **Author Signatures:** Only the original author of the bytecode can upload it on Mainnet, preventing others from claiming ownership of a developer's work.
* **Token-Specific Logic:** It handles edge cases (like USDT's non-standard transfer behavior) through `tokenSpecificPostfixes`, ensuring the correct specialized implementation is used for specific assets.

<details>

<summary>Sources</summary>

* [contracts/global/BytecodeRepository.sol](https://github.com/Gearbox-protocol/permissionless/blob/master/contracts/global/BytecodeRepository.sol)
* [specification.md](https://github.com/Gearbox-protocol/permissionless/blob/master/specification.md)
* [contracts/interfaces/IBytecodeRepository.sol](https://github.com/Gearbox-protocol/permissionless/blob/master/contracts/interfaces/IBytecodeRepository.sol)
* [contracts/traits/DeployerTrait.sol](https://github.com/Gearbox-protocol/permissionless/blob/master/contracts/traits/DeployerTrait.sol)
* [script/UploadBytecode.s.sol](https://github.com/Gearbox-protocol/periphery-v3/blob/main/script/UploadBytecode.s.sol)

</details>
