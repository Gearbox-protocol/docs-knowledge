# Audits & Bug Bounty

Gearbox Protocol has undergone multiple independent security audits across each major version. The Bytecode Repository enforces on-chain audit verification as a deployment prerequisite. An active Immunefi bug bounty program provides continuous economic incentive for responsible vulnerability disclosure.

⚠️ **Smart contract risk:** Audits reduce but do not eliminate smart contract risk. DeFi protocols are composable and interdependent. An undiscovered vulnerability in audited code — whether in Gearbox contracts, integrated adapters, or upstream dependencies — could result in partial or total loss of deposited funds. Audit completion is not a guarantee of correctness.

---

## Audit History by Version

All audit reports are published in the [Gearbox security repository](https://github.com/Gearbox-protocol/security/tree/main/audits).

| Version | Audit Firms | Scope | Report Links |
|---------|------------|-------|--------------|
| V1 | ChainSecurity, MixBytes | Core lending, Credit Accounts, pool logic | [Security repo — V1 audits](https://github.com/Gearbox-protocol/security/tree/main/audits) |
| V2 | ChainSecurity, Sigma Prime | Credit Manager upgrades, multicall, adapters | [Security repo — V2 audits](https://github.com/Gearbox-protocol/security/tree/main/audits) |
| V3 (core) | ChainSecurity, ABDK | CreditManagerV3, CreditFacadeV3, PoolV3, quota system, liquidation logic | [Security repo — V3 audits](https://github.com/Gearbox-protocol/security/tree/main/audits) |
| V3 (permissionless) | ChainSecurity | MarketConfigurator, BytecodeRepository, factory contracts | [Security repo — permissionless audits](https://github.com/Gearbox-protocol/security/tree/main/audits) |

*Last verified: 2026-03-21. Confirm current report availability at the security repository linked above.*

---

## On-Chain Audit Enforcement

Unlike most protocols where audit status is a social claim, Gearbox enforces audit verification at the smart contract level:

1. **Approved auditor whitelist.** The Gearbox DAO maintains a list of authorized auditor addresses in the `BytecodeRepository` contract.
2. **Cryptographic attestation.** Auditors sign the specific `bytecodeHash` of reviewed contracts via EIP-712 and submit signatures through `submitAuditReport`.
3. **Deployment gate.** The `deploy()` function checks `isBytecodeAudited` before execution. If a bytecode hash lacks a valid auditor signature, deployment is rejected. There is no override mechanism.

This means every contract in the Gearbox ecosystem has passed on-chain audit verification — a property that is independently confirmable, not trust-dependent.

**Implication for partners:** Query `isBytecodeAudited` with any deployed contract's bytecode hash to confirm audit status and the signing auditor's address. See [Protocol Audits](../governance/protocol-audits.md) for full Bytecode Repository architecture.

---

## Deterministic Deployment (Create2)

Factory-based deployment uses `CREATE2` for deterministic contract addresses across Ethereum Mainnet and supported L2s (Optimism, Arbitrum). This provides:

- **Cross-chain address consistency.** A contract deployed on Mainnet produces the same address on L2s — same code, same address, every chain.
- **Front-running protection.** The deployer's address is mixed into the salt, preventing address-sniping by malicious actors.
- **Integrity verification.** Upon deployment, the repository verifies that the resulting contract's `contractType` and `version` match registry records.

**Implication for partners:** A contract address verified on Mainnet can be confirmed on any supported L2 without additional verification steps.

---

## Additional Security Measures

Beyond external audits, the Gearbox security posture includes:

- **On-chain bytecode verification.** The [Bytecode Repository](https://permissionless.gearbox.foundation/bytecode) serves as the on-chain source of truth for every deployed contract. Each contract on mainnet is traceable to audited bytecode.
- **Blacklisting mechanism.** The DAO can permanently forbid specific `initCode` hashes via `forbidInitCode`. If a vulnerability is found in a contract version, that version is bricked — no further deployments on any chain.
- **Market-wide pause capability.** Emergency pause mechanisms exist for CreditFacade operations. Emergency Liquidator roles can liquidate even when the facade is paused.
- **Adapter isolation.** Credit Accounts interact with external protocols only through whitelisted adapter contracts, limiting the attack surface for composability exploits.

---

## Bug Bounty Program (Immunefi)

Gearbox maintains an active bug bounty program through [Immunefi](https://immunefi.com/bounty/gearbox/).

*Reward tiers last verified: 2026-03-21. Confirm current amounts at the Immunefi listing linked above.*

### Reward Tiers

| Severity | Payment (USDC or equivalent stablecoin) |
|----------|----------------------------------------|
| Low | $100 – $1,000 |
| Medium | $1,000 – $5,000 |
| High | $5,000 – $20,000 |
| Critical | $20,000 – $200,000 (+ GEAR tokens) |

Final payout amounts are determined by DAO developers at their discretion, based on the impact of the vulnerability.

### Scope

- **V3 contracts:** All severity tiers in scope
- **V1/V2 contracts:** Only Critical and High impacts are in scope
- **Out-of-scope findings:** Ad-hoc payouts have been made for findings outside the formal scope when they serve the protocol's security interests

The in-scope contract list is maintained at the [Gearbox security repository](https://github.com/Gearbox-protocol/security/tree/main/bug-bounty).

### Reporting Requirements

All bug reports must include:

1. Description of the suspected vulnerability
2. Steps to reproduce the issue
3. Reporter name and/or collaborators (for attribution)
4. (Optional) A patch or suggested resolution

### Prohibited Activities

- Testing on mainnet or public testnets — all testing must use private testnets
- Testing with pricing oracles or third-party smart contracts
- Social engineering attacks against team members or users
- Testing with third-party systems, browser extensions, or external websites
- Denial of service attacks or automated traffic generation
- Public disclosure of unpatched vulnerabilities under embargo

**Implication for partners:** An active, funded bounty program with tiered payouts up to $200,000 creates continuous economic incentive for security researchers to report vulnerabilities through responsible disclosure rather than exploitation. The program's scope, reward history, and in-scope contracts are publicly auditable.

---

**Related pages:**

- [Protocol Audits (Bytecode Repository)](../governance/protocol-audits.md) — On-chain audit enforcement architecture and deployment gates
- [Insurance & Solvency Reserves](insurance-and-solvency.md) — How the protocol absorbs bad debt (distinct from hack coverage)
- [Risks & Disclosures](risks-and-disclosures.md) — Specific risk categories including smart contract, oracle, and bad debt risk
