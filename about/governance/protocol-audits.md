# Protocol Audits (Bytecode Repository)

The Bytecode Repository is the on-chain registry that guarantees every deployed Gearbox contract is verified, audited, and identical across all supported chains. It decouples code upload from deployment, introducing a mandatory cryptographic verification layer between them.

This page covers how the repository enforces audit verification on-chain — not as a social claim but as a deployment prerequisite — for partner technical due diligence.

---

## What CANNOT Be Deployed

The Bytecode Repository enforces hard constraints on what code can enter the protocol:

- **Unverified code:** The `deploy()` function checks `isBytecodeAudited` before execution. If a bytecode hash does not carry a valid signature from an authorized auditor, the protocol refuses deployment. There is no override mechanism.
- **Blacklisted code:** The DAO can permanently forbid specific `initCode` hashes via `forbidInitCode`. If a vulnerability is discovered in a contract version, that version is bricked — no further deployments are possible, on any chain.
- **Impersonated code:** Only the original author of the bytecode can upload it on Mainnet. Other parties cannot claim ownership of another developer's work.

**Implication for partners:** Every contract in the Gearbox ecosystem has passed on-chain audit verification. This is verifiable — not a trust assumption.

---

## On-Chain Audit Verification

Audit verification is cryptographic, not social. The process:

1. **Approved auditors:** The Gearbox DAO maintains a whitelist of approved auditor addresses in the `BytecodeRepository` contract.
2. **EIP-712 attestation:** Auditors sign the specific `bytecodeHash` of the contract they have reviewed. This signature is submitted to the repository via `submitAuditReport`.
3. **Deployment gate:** The `deploy()` function checks `isBytecodeAudited`. Without a valid auditor signature on record, deployment is rejected.

**Implication for partners:** On-chain verification is possible for every deployed contract. Query `isBytecodeAudited` with the contract's bytecode hash to confirm the audit status and the signing auditor's address.

---

## Deterministic Deployment

The repository uses `CREATE2` to ensure identical addresses and code across Ethereum Mainnet and supported L2s (Optimism, Arbitrum).

- **Cross-chain consistency:** A contract deployed on Mainnet produces the same address when deployed on L2s. Same code, same address, every chain.
- **Front-running protection:** The deployer's address is mixed into the salt, preventing malicious actors from sniping a contract address before the legitimate deployer.
- **Integrity checks:** Upon deployment, the repository verifies that the resulting contract's `contractType` and `version` (via the `IVersion` interface) match the registry records.

**Implication for partners:** A contract address verified on Mainnet can be trusted on any supported L2. The deployment mechanism prevents address collision or substitution.

---

## Repository Architecture

### Versioned Catalog

Contracts are organized into **Domains** (e.g., `IRM` for interest rate models) and **Postfixes** (e.g., `_LINEAR`), with semantic versioning (Major.Minor.Patch). This structure functions as a versioned catalog of all protocol components.

### System Domains vs. Public Domains

| Domain Type | Governance | Use Case |
|---|---|---|
| **System Domains** | DAO-governed. Updates require an on-chain vote. | Core contracts: Pool, Credit Manager, Credit Facade |
| **Public Domains** | Developer-owned. Author controls their identifier. | Plugins: new adapters, custom interest rate models |

System Domains ensure that core protocol components change only through DAO governance. Public Domains allow permissionless extension — developers can submit new adapters or models without requiring a DAO vote, provided the code passes audit verification.

### Immutable Storage

The repository uses SSTORE2 to store initialization code (init code) directly in Ethereum state. Once stored, init code cannot be deleted or modified. This guarantees that the audited version of a contract remains permanently available and verifiable.

---

## Related Pages

- [Protocol DAO](protocol-dao.md) — DAO governance scope: who authorizes upgrades and manages the Bytecode Repository
- [Market Curators](market-curators.md) — How Curators deploy markets using repository-verified contracts
- [Operational Multisigs](operational-multisigs.md) — Multisig roles that execute DAO-authorized changes
