# Market Curators

A Market Curator operates a specific lending market instance on Gearbox. The Curator defines boundary conditions — Loan-to-Value ratios, interest rate curves, allowed collateral, debt limits — under which the market operates. The Curator is a risk parameter manager, not an asset manager.

This page establishes what a Curator is constrained from doing before covering what a Curator controls, so that any party building on or lending through a Gearbox market can evaluate the trust assumptions involved.

---

## What a Curator CANNOT Do

A compromised or adversarial Curator cannot drain a market. The protocol enforces the following hard constraints at the smart contract level:

- **Cannot withdraw LP funds or seize borrower collateral.** The Curator has no custody over deposited capital. Funds move only through protocol-defined operations (borrowing, repayment, liquidation).
- **Cannot actively allocate capital between strategies.** The Curator sets eligibility rules (e.g., "Strategy A is allowed up to $10M debt"). The protocol manages capital flow based on borrower demand. There is no manual fund movement.
- **Cannot bypass the 24-hour timelock.** Every parameter change that increases risk — raising LTVs, expanding debt limits, adding collateral types — must wait a mandatory 24-hour delay before execution.
- **Cannot increase risk instantly.** The Emergency Admin role can act without delay, but only to restrict operations: pause contracts, reduce limits to zero, forbid tokens or adapters. It cannot raise LTVs, increase debt limits, or add new exposure.

**Implication for partners and lenders:** A rogue or compromised Curator can only shut down or restrict market operations. It cannot open new risk vectors or extract funds.

---

## What a Curator CAN Do (Subject to Timelock)

All parameter changes below require the Administrator to queue them in the Timelock contract. Execution occurs no earlier than 24 hours after queuing. Lenders and borrowers can audit pending changes and exit the market during this window.

- Modify all risk parameters: Liquidation Thresholds (LTs), supply caps, interest rate models, fee splits
- Add or remove collateral types and allowed protocol integrations (adapters)
- Configure per-collateral quota limits and collateral-specific interest rates
- Set the Interest Rate Model (IRM) contract for the pool
- Define loss policies and liquidator whitelists

**Implication for partners and lenders:** Every risk-increasing change is observable on-chain at least 24 hours before it takes effect. Any party that disagrees with a pending change has time to withdraw.

---

## Role Architecture: Separation of Powers

Curator powers are segregated into distinct roles, typically assigned to different multisigs or governance controllers. No single key can both increase risk and act instantly.

### Administrator (Governance)

The ultimate authority for the market. This address controls the `MarketConfigurator` contract.

- **Capabilities:** Can modify all risk parameters — LTVs, supply caps, interest rate models, fee splits, collateral lists, adapter lists.
- **Constraint:** All actions are subject to the mandatory 24-hour timelock.

### Emergency Admin (Security)

A crisis-response role with a limited subset of powers that bypass the timelock.

- **Capabilities:**
  - Pause contracts (freeze borrowing and withdrawals)
  - Set debt limits to zero (halt new borrowing)
  - Forbid specific adapters or tokens (block exposure to a risky asset)
- **Constraint:** Cannot increase risk. Can only restrict operations. Cannot raise LTVs, expand debt limits, or whitelist new assets.

### Operational Roles

Granular roles for day-to-day maintenance without full administrative access:

- **Pausable / Unpausable Admin:** Can freeze or unfreeze specific market contracts.
- **Fee Multisig:** Designated recipient for accrued protocol fees.
- **Emergency Liquidator:** Whitelisted address permitted to liquidate positions when the market is paused, ensuring bad debt does not accumulate during an emergency freeze.

---

## Economic Model

Curators monetize markets through programmatic fees deducted automatically by the smart contracts. Revenue is a function of market activity, not discretionary allocation.

### Revenue Sources

1. **Interest Fee:** A percentage of the interest paid by borrowers, added on top of the base rate paid to lenders.
2. **Liquidation Fee:** A percentage of the collateral value seized during a liquidation event.

### Fee Sharing

The protocol enforces a revenue split between the Curator and the Protocol DAO at the `TreasurySplitter` contract level.

- **Default split:** 50% to the Curator / 50% to the Protocol DAO.
- Changing this global split requires a DAO governance vote.

---

## Permissionless Entry

Any entity can deploy a `MarketConfigurator` and launch a lending business on Gearbox. No DAO approval is required to become a Curator. The protocol imposes no gatekeeping on who can operate a market — only on how that market operates (via the constraints above).

**Implication for the ecosystem:** A competitive market for curation. Lenders and borrowers choose which Curator's market to participate in based on that Curator's risk configuration, track record, and fee structure.

---

## Related Pages

- [Risk Configuration Dictionary](../reference/risk-configuration-dictionary.md) — Full parameter reference with permissions matrices
- [Instance Owner](instance-owner.md) — Technical infrastructure role (price feed verification)
- [Protocol DAO](protocol-dao.md) — Protocol-level governance scope and constraints
- [Operational Multisigs](operational-multisigs.md) — Multisig roles, thresholds, and signer composition
