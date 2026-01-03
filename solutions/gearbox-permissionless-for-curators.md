# Gearbox Permissionless for Curators

Gearbox Permissionless provides the operational rails for institutions, asset managers, and fintechs to deploy onchain credit markets.

As a **Curator**, you act as the operator of a standalone lending vertical. This role is designed for entities seeking to retain full ownership of their market's risk parameters and economic model, while leveraging Gearbox’s battle-tested settlement engine to handle execution, solvency, and compliance.

This page outlines the operational model and strategic advantages of the Gearbox curation stack.

## Risk Management, Not Fund Management

In many onchain lending models, curation requires active capital reallocation—manually moving funds between vaults to chase yield. This creates significant operational burden and can inadvertently classify operators as financial intermediaries or asset managers.

**The Gearbox Approach:**\
Curators manage **Parameters**, not **Funds**.

* **Non-Custodial:** You define the rules (LTVs, Interest Rate Models), but you never possess or control user funds.
* **Automated Execution:** The protocol automatically routes liquidity and enforces solvency based on your pre-defined logic.
* **Compliance Benefit:** This passive model allows you to operate a lending business without engaging in active fund management activities.vv

## Structured Credit Products

Standard lending markets are commoditized, offering simple borrowing against collateral. Gearbox enables Curators to structure complex **Credit Products**.

* **Strategy Integration:** Deploy markets that offer native access to specific yield strategies (e.g., Leveraged Staking, Basis Trading, or RWA accumulation).
* **Capital Efficiency:** By integrating execution directly into the credit account, Curators can offer higher leverage ratios with tighter risk controls than standard over-collateralized lending.

## Institutional-Grade Risk Framework

For asset issuers and fund managers, security is the primary constraint. Gearbox provides a multi-layered safety stack designed for high-value deployments.

* **Dual-Oracle Architecture:** Markets utilize a primary and secondary oracle source to prevent price manipulation and ensure accurate mark-to-market valuations.
* **Automated Insolvency Resolution:** The "Loss Policy" mechanism provides pre-defined logic for handling bad debt events, protecting Liquidity Providers from black swan scenarios.
* **Granular Access Control:** Curators can deploy permissioned instances, utilizing allowlists for borrowers or lenders to meet KYC/AML requirements.
