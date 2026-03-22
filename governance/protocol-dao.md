# Protocol DAO

The Gearbox DAO governs the protocol's core infrastructure: contract upgrades, chain deployments, and global economic parameters. It does not manage individual lending markets. Market-level risk parameters — LTVs, interest rates, collateral lists — are delegated entirely to Market Curators.

This page establishes the DAO's hard constraints before describing its governance scope, so that partners can confirm that DAO votes will not destabilize or override individual market configurations.

---

## What the DAO CANNOT Do

The following limitations are enforced at the smart contract level, not by social agreement:

- **Cannot change risk parameters of any live Curator-managed market.** LTVs, Liquidation Thresholds, interest rates, collateral lists, and adapter permissions are controlled exclusively by the Curator who operates that market. No DAO vote can override these settings.
- **Cannot seize or reallocate funds deposited into Curator-managed pools.** Capital deposited by lenders is governed by the pool's smart contracts, not by DAO governance.
- **Cannot interfere with individual market operations.** The DAO has no mechanism to pause, reconfigure, or shut down a specific Curator's market.

**Implication for partners:** The risk profile of a given market is determined by the Curator operating it, not by DAO governance outcomes. DAO votes affect protocol-level infrastructure only.

---

## What the DAO Governs

### System Upgrades and Versioning

The DAO is the only entity that can authorize new versions of core smart contracts.

- **Contract updates:** The DAO votes to deploy and authorize new implementations of system components (e.g., `PoolV3`, `CreditManagerV3`).
- **Bytecode Repository:** The DAO manages the on-chain registry of verified contract bytecode. When Curators deploy new markets, the contracts are drawn from this audited, DAO-approved registry.

### Chain Activation

The DAO controls expansion to new blockchain networks.

- **Instance deployment:** Before Gearbox can operate on a new chain (e.g., Arbitrum, Optimism), the DAO must authorize deployment of the Instance Owner and Treasury contracts on that network.
- **Canonical addressing:** The DAO ensures a single canonical instance of protocol infrastructure on each supported chain, preventing fragmentation.

### Fee Split Configuration

While Curators set the total fees for their markets, the DAO defines the protocol-level fee split between Curator revenue and DAO revenue.

- **Default split:** 50% Curator / 50% DAO — enforced at the `TreasurySplitter` contract level.
- Changing this global parameter requires a DAO vote.

### Economic Alignment (GEAR Token)

The DAO allocates GEAR tokens to align incentives across the ecosystem:

- **Incentive programs:** Liquidity mining, grants to bootstrap specific markets or integrations.
- **Governance:** GEAR token holders vote on all DAO-level decisions described above.

---

## Separation of Powers Summary

| Role | Domain | Constraint |
|---|---|---|
| **DAO** | Builds the rails — code, chains, global economics | Cannot touch individual market parameters or funds |
| **Curators** | Operate the trains — markets, parameters, collateral | Cannot modify core protocol code or deploy to new chains |
| **Instance Owner** | Maintains the tracks — price feeds, technical infrastructure | Cannot make financial risk decisions or initiate upgrades |

Three independent roles, each with hard constraints on what they can and cannot do. No single role has authority over another role's domain.

---

## Related Pages

- [Market Curators](market-curators.md) — Who manages risk parameters and day-to-day market operations
- [Instance Owner](instance-owner.md) — Technical infrastructure management per chain
- [Protocol Audits](protocol-audits.md) — On-chain bytecode verification and audit enforcement
- [Supply Information](../reference/supply-information.md) — GEAR token distribution and circulation details
