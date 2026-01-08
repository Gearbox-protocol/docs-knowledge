# For Curators

The Market Curator views Gearbox as a **Risk Parameterization Engine**, not a fund management tool. Unlike other lending primitives where curators actively allocate liquidity (e.g., Morpho), Gearbox Curators define the _boundary conditions_ (LTVs, Limits, Rates) within which users autonomously execute strategies.

#### Phase 1: The Operational Model (Mental Model Alignment)

**User Intent:** Understand the legal and operational distinction between "Managing Funds" and "Managing Parameters."

| Key Question                       | System Answer                                                                                                                                                                                                                                                           | Sitemap Component                              |
| ---------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| **"Do I manage the liquidity?"**   | **Non-Custodial Curation.** Unlike Morpho, Curators do not actively rebalance funds between vaults. Curators set the _rules_ and users/borrowers autonomously utilize the liquidity. This distinction is critical for entities avoiding custodial classification.       | [one-pool-many-markets](https://gearbox.gitbook.io/gearbox-docs/about-gearbox/one-pool-many-markets "mention")   |
| **"What is the deliverable?"**     | **The Lending Product.** The Curator's product is a set of smart contracts with specific risk parameters. The "Product" is the _access_ to leverage and earning under these specific terms, not the yield itself.                                                       | [credit-suite](https://gearbox.gitbook.io/gearbox-docs/about-gearbox/core-architecture/credit-suite "mention")        |
| **"Who bears the economic risk?"** | **Risk Liability.** The Curator bears the reputational and economic risk of their configuration. Gearbox Protocol provides the _mechanism_ for liquidation, but the _guarantee_ of solvency depends entirely on the Curator's parameter selection (LTV vs. Volatility). | [liquidation-dynamics](https://gearbox.gitbook.io/gearbox-docs/about-gearbox/economics-and-risk/liquidation-dynamics "mention") |

#### Phase 2: Infrastructure Dependencies (The "Full Stack" Reality)

**User Intent:** Assess the reliance on Gearbox DAO for critical infrastructure vs. autonomous capabilities.

| Key Question                          | System Answer                                                                                                                                                                                                                                                           | Sitemap Component                      |
| ------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------- |
| **"Is it fully permissionless?"**     | **Hybrid Governance.** While market creation is permissionless, critical infrastructure is gated. 1) **Chain Activation** requires DAO approval. 2) **Price Feed Whitelisting** is controlled by the Instance Owner multisig (though open to Curator participation).    | [instance-owner](https://gearbox.gitbook.io/gearbox-docs/about-gearbox/governance-and-operations/instance-owner "mention") |
| **"Who runs the interface?"**         | **UI & Tooling Dependency.** The official Gearbox App and Curation Interface are maintained by the DAO. While the protocol is onchain, practical operation relies on these offchain services unless the Curator builds their own frontend.                              | [protocol-dao](https://gearbox.gitbook.io/gearbox-docs/about-gearbox/governance-and-operations/protocol-dao "mention")   |
| **"How are transactions generated?"** | **Operational Complexity.** Configuring a market involves complex transaction batches. Curators rely on the DAO-maintained **Curation Interface** to generate these payloads. Autonomous operation requires significant technical capability to replicate this tooling. | [risk-configuration-dictionary](https://gearbox.gitbook.io/gearbox-docs/about-gearbox/reference/risk-configuration-dictionary "mention")    |

#### Phase 3: Product Structuring & Incentives

**User Intent:** Define the commercial structure and align incentives with the DAO.

| Key Question                      | System Answer                                                                                                                                                                                                                         | Sitemap Component                       |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------- |
| **"How do I monetize?"**          | **Fee Sharing.** Curators capture a configurable percentage of interest and liquidation fees. This revenue stream is programmatic and shared with the Protocol DAO.                                                                   | [market-curators](https://gearbox.gitbook.io/gearbox-docs/about-gearbox/governance-and-operations/market-curators "mention") |
| **"Can I get token incentives?"** | **DAO Alignment.** GEAR token incentives are discretionary and voted on by the DAO. There is no programmatic guarantee of incentives; Curators must align their product with the DAO's strategic goals to receive support.            | [protocol-dao](https://gearbox.gitbook.io/gearbox-docs/about-gearbox/governance-and-operations/protocol-dao "mention")    |
| **"Can the DAO interfere?"**      | **Sovereignty vs. Support.** The DAO cannot alter a Curator's parameters onchain. However, the DAO _can_ delist a market from the official UI or cut incentives if the Curator's risk management endangers the protocol's reputation. | [protocol-dao](https://gearbox.gitbook.io/gearbox-docs/about-gearbox/governance-and-operations/protocol-dao "mention")    |

#### Phase 4: Risk Parameterization (The Core Job)

**User Intent:** Calibrate the system to balance capital efficiency with solvency protection.

| Key Question                             | System Answer                                                                                                                                                                                                                        | Sitemap Component                              |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------- |
| **"How is leverage capped?"**            | **Liquidation Thresholds.** Curators set the $LT$ for each asset. This is the primary lever for risk management. Setting this too high relative to asset volatility _will_ result in bad debt, for which the protocol is not liable. | [liquidation-dynamics](https://gearbox.gitbook.io/gearbox-docs/about-gearbox/economics-and-risk/liquidation-dynamics "mention") |
| **"How is concentration risk managed?"** | **Quota Limits.** Curators must set global caps on specific collateral assets via the Quota Keeper. This prevents the pool from becoming over-exposed to illiquid tokens.                                                            | [quota-controls](https://gearbox.gitbook.io/gearbox-docs/about-gearbox/economics-and-risk/quota-controls "mention")         |
| **"How are liquidators incentivized?"**  | **Liquidation Premium.** Curators configure the premium paid to liquidators. If this is set too low, liquidators will not execute, and the system _will_ fail. The protocol does not guarantee liquidation execution.                | [liquidation-dynamics](https://gearbox.gitbook.io/gearbox-docs/about-gearbox/economics-and-risk/liquidation-dynamics "mention") |

#### Phase 5: Operational Governance

**User Intent:** Understand the ongoing management and emergency procedures.

| Key Question                         | System Answer                                                                                                                                                                                | Sitemap Component                       |
| ------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------- |
| **"How are updates executed?"**      | **Timelock Constraints.** All critical parameter changes are subject to a 24-hour timelock. Curators must plan updates in advance.                                                           | [risk-configuration-dictionary](https://gearbox.gitbook.io/gearbox-docs/about-gearbox/reference/risk-configuration-dictionary "mention")     |
| **"What are the emergency powers?"** | **Pause & Loss Policy.** In the event of an exploit or market failure, Curators (or their Emergency Admins) can pause borrowing or trigger the Loss Policy to prevent bad debt accumulation. | [smart-oracles](https://gearbox.gitbook.io/gearbox-docs/about-gearbox/economics-and-risk/smart-oracles "mention") |
