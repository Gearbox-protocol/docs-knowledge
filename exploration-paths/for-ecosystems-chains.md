# For Ecosystems/Chains

#### Phase 1: The Value Proposition (Composability Engine)

**User Intent:** Understand how Gearbox enriches the existing DeFi ecosystem beyond simple lending.

| Key Question                            | System Answer                                                                                                                                                                                                                                                                     | Sitemap Component                              |
| --------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| **"How does this benefit local apps?"** | **Unified Execution Layer.** Gearbox is not a silo. Through **Adapters**, Credit Accounts inject leverage directly into local protocols (e.g., Uniswap, Curve, Pendle). This turns a passive lending market into an active volume generator for the chain's DEXs and yield farms. | [adapters-integrations](https://gearbox.gitbook.io/gearbox-docs/about-gearbox/core-architecture/adapters-integrations) |
| **"Is it compatible with our assets?"** | **Versatile Collateral.** Gearbox supports complex assets like LP tokens, Vault shares, and PTs. This allows the chain to offer leverage on its unique "Productive Assets," not just plain vanilla tokens.                                                                        | [credit-suite](https://gearbox.gitbook.io/gearbox-docs/about-gearbox/core-architecture/credit-suite)        |

#### Phase 2: The Operating Model (Roles & Responsibilities)

**User Intent:** Clarify the division of labor between the Chain, the Gearbox DAO, and the Market Operators.

| Key Question                  | System Answer                                                                                                                                                                                                                                                                                  | Sitemap Component                       |
| ----------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------- |
| **"Who runs the markets?"**   | **Service Provider vs. Operator.** Gearbox DAO provides the _technology stack_ (Service Provider). **Curators** (Operators) run the actual business (Risk/Parameters). The Chain can bring its own trusted curators, or Gearbox can help facilitate introductions to existing active curators. | [market-curators](https://gearbox.gitbook.io/gearbox-docs/about-gearbox/governance-and-operations/market-curators) |
| **"Who guarantees success?"** | **Shared Responsibility.** Gearbox DAO ensures the code functions correctly and provides operational support. However, the economic success of a market is a function of the Curator's strategy and the Chain's underlying liquidity depth.                                                    | [protocol-dao](https://gearbox.gitbook.io/gearbox-docs/about-gearbox/governance-and-operations/protocol-dao)    |
| **"Is deployment gated?"**    | **Permissionless Architecture.** No. Once the protocol is deployed on the chain, market creation is permissionless. Curators do not need Gearbox DAO approval to launch new markets or list new assets, ensuring rapid integration with the chain's roadmap.                                   | [market-curators](https://gearbox.gitbook.io/gearbox-docs/about-gearbox/governance-and-operations/market-curators) |

#### Phase 3: Ecosystem Prerequisites (Economic Viability)

**User Intent:** Determine the maturity level required to support leveraged markets.

| Key Question                             | System Answer                                                                                                                                                                                                                                     | Sitemap Component                              |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| **"What is required for liquidations?"** | **Liquidity Enables Capacity.** Gearbox relies on swapping collateral on local DEXs. Deeper DEX liquidity allows for higher borrowing limits. We work with chains to identify the most liquid assets suitable for initial markets.                | [liquidation-dynamics](https://gearbox.gitbook.io/gearbox-docs/about-gearbox/economics-and-risk/liquidation-dynamics) |
| **"How are liquidators onboarded?"**     | **Collaborative Keeper Network.** Gearbox provides open-source liquidator bot infrastructure. We actively collaborate with the Chain to onboard local MEV searchers and keepers, ensuring a robust liquidation network is established pre-launch. | [liquidation-dynamics](https://gearbox.gitbook.io/gearbox-docs/about-gearbox/economics-and-risk/liquidation-dynamics) |
| **"What assets work best?"**             | **Productive Collateral.** Gearbox shines when there are yield-bearing assets (LSTs, LRTs, Yield Vaults). Leverage on zero-yield assets is less attractive to borrowers in high-rate environments.                                                | [credit-suite](https://gearbox.gitbook.io/gearbox-docs/about-gearbox/core-architecture/credit-suite)        |

#### Phase 4: Technical Requirements (Deployment Feasibility)

**User Intent:** Verify technical compatibility to ensure a smooth launch.

| Key Question                         | System Answer                                                                                                                                                                                                                       | Sitemap Component                            |
| ------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------- |
| **"What are the hard constraints?"** | **Block Gas Limit.** Gearbox contracts are sophisticated. To deploy the core infrastructure, the chain should ideally support a Block Gas Limit of **>30 Million**. We can assist in evaluating chain parameters for compatibility. | [omni-evm-architecture](https://gearbox.gitbook.io/gearbox-docs/about-gearbox/system-overview/omni-evm-architecture) |
| **"What infrastructure is needed?"** | **RPC Reliability.** Robust offchain operations (Interface, Liquidator Bots) require stable RPC providers. Gearbox contributors can assist in testing and verifying infrastructure readiness.                                       | [omni-evm-architecture](https://gearbox.gitbook.io/gearbox-docs/about-gearbox/system-overview/omni-evm-architecture) |
| **"Are oracles ready?"**             | **Oracle Infrastructure.** Reliable oracle providers (Chainlink, Redstone, Pyth, or API3) are required for collateral assets. We can help coordinate with oracle partners to ensure coverage.                                       | [price-oracle](https://gearbox.gitbook.io/gearbox-docs/about-gearbox/economics-and-risk/price-oracle)       |

#### Phase 5: Growth & Incentives (Go-to-Market)

**User Intent:** Plan the launch strategy and incentive allocation.

| Key Question                       | System Answer                                                                                                                                                                                      | Sitemap Component                       |
| ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------- |
| **"How do we attract liquidity?"** | **Co-Marketing & Grants.** The Chain can offer incentives to Curators to encourage market creation. Gearbox DAO frequently partners with chains to co-market these launches to existing user base. | [market-curators](https://gearbox.gitbook.io/gearbox-docs/about-gearbox/governance-and-operations/market-curators) |
