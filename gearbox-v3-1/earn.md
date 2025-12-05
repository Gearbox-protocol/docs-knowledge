[MODE=BALANCED]

# Product overview

Gearbox Pools are single-asset vaults which allow deposits to be borrowed against a set of collaterals. Depositors earn passive yield from borrower activity while curators configure which collaterals can tap each pool. Liquidity stays user-controlled with transparent monitoring and the ability to withdraw whenever unborrowed funds are available.

# Core benefits

- **Simplified yield:** deposit once and let the curator handle sourcing and routing borrower demand.  

- **Curated risk:** specialized roles select eligible collateral, review risk, and set safeguards to protect depositors.  

- **Non-custodial earning:** supply and withdraw at will, limited only by available unborrowed funds.  

- **Onchain transparency:** every configuration change is onchain, role-gated, and timelocked for oversight.

- **ERC-4626 compatibility:** standard vault shares make pools easy to integrate as a yield source across the ecosystem.  

# How it works
- **Curation:** curators set eligible collateral, borrowing guardrails, and oracle choices under a timelock so lenders see risk changes before they take effect.  

- **Supply utilization:** supplied liquidity instantly becomes available to be borrowed from credit accounts within curator-set limits. Curator can configure borrowing access to be permissionless or whitelist-only.

- **User deposits and withdrawals:** deposits issue ERC-4626 vault shares to the user, and redemptions burn those shares to return underlying tokens whenever there is unborrowed liquidity.

# Roles and Responsibilities
Gearbox Markets use distinct roles to separate powers and keep governance visible:

- **Curator:** sets market parameters such as collateral eligibility, limits, oracles and more.

- **Emergency admin:** can quickly cap exposure, swap to conservative oracles, or disable adapters without delay when protecting lender funds.  

- **Pausable admin:** can pause pools and credit managers to halt activity during incidents.  

- **Unpausable admin:** can restore normal operations once safeguards are satisfied and conditions stabilize.
