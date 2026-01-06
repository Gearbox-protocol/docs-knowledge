# For Lenders/LPs

#### Phase 1: Structural Risk Assessment (Mental Model)

**User Intent:** Evaluate the fundamental architecture to determine if the risk segregation meets investment mandates.

| Key Question                                      | System Answer                                                                                                                                                                                                                      | Sitemap Component                            |
| ------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------- |
| **"How is liability vs. asset risk structured?"** | **Segregated Risk Architecture.** The protocol decouples passive liquidity (Pool) from active risk strategies (Credit Managers). A failure in one strategy is contained by its specific debt ceiling, protecting the broader pool. | `1-system-overview/one-pool-many-markets.md` |
| **"Is the deployment canonical?"**                | **Omni-EVM Architecture.** Gearbox utilizes a modular deployment model. Each chain operates as an independent, verified instance rather than a bridged dependency.                                                                 | `1-system-overview/omni-evm-architecture.md` |

#### Phase 2: Yield Mechanics & Liquidity Risk

**User Intent:** Analyze the mechanism of yield accrual and the constraints on capital withdrawal.

| Key Question                            | System Answer                                                                                                                                                                             | Sitemap Component                             |
| --------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------- |
| **"How does capital accrue interest?"** | **The Liquidity Vault.** Yield accrues via the Diesel Token (ERC-4626), a non-rebasing interest-bearing token. The exchange rate appreciates as interest is paid by borrowers.            | `2-core-architecture/pool-liquidity-vault.md` |
| **"What drives APY volatility?"**       | **Interest Rate Model.** The base rate is dynamic, driven by the utilization curve. The "Kink" ($U\_{optimal}$) defines the target efficiency range before rates scale exponentially.     | `3-risk-and-economics/interest-rate-model.md` |
| **"What is the liquidity risk?"**       | **Utilization Caps.** High utilization can temporarily block withdrawals. The Interest Rate Model is designed to force borrower repayment during these periods to restore exit liquidity. | `3-risk-and-economics/interest-rate-model.md` |

#### Phase 3: Counterparty Risk & Solvency Enforcement

**User Intent:** Assess the creditworthiness of the borrowers and the automated enforcement of debt obligations.

| Key Question                               | System Answer                                                                                                                                                                                      | Sitemap Component                                                                            |
| ------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| **"What prevents fund misappropriation?"** | **Execution Guardrails.** Borrowers cannot access funds directly. They operate through **Credit Accounts** (smart contract wrappers) restricted to whitelisted interactions via Adapters.          | `2-core-architecture/credit-manager.md` \<br> `2-core-architecture/adapters-integrations.md` |
| **"How is solvency enforced?"**            | **Liquidation Dynamics.** Solvency is enforced mathematically via the Health Factor ($H\_f$). If $H\_f < 1$, the protocol incentivizes third-party liquidators to seize collateral and repay debt. | `3-risk-and-economics/liquidation-dynamics.md`                                               |
| **"How are assets valued?"**               | **Price Oracle.** Asset valuation relies on normalized price feeds. Understanding the oracle source (Spot vs. TWAP) is critical for modeling liquidation triggers.                                 | `3-risk-and-economics/price-oracle.md`                                                       |

#### Phase 4: Stress Testing & Failure Modes

**User Intent:** Evaluate system resilience under adverse market conditions (Oracle attacks, Liquidity crunches).

| Key Question                                          | System Answer                                                                                                                                                                           | Sitemap Component                       |
| ----------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------- |
| **"Is the system resilient to oracle manipulation?"** | **Smart Oracles.** The protocol employs a Dual-Feed architecture (Main vs. Reserve). Significant deviation between feeds blocks sensitive operations to prevent arbitrage.              | `3-risk-and-economics/smart-oracles.md` |
| **"How is concentration risk managed?"**              | **Quota Keeper.** The protocol enforces **Asset-Side Limits**. Even if the pool has excess liquidity, exposure to specific volatile assets is capped globally.                          | `3-risk-and-economics/quota-keeper.md`  |
| **"What happens if bad debt occurs?"**                | **Insolvency Resolution.** The **Loss Policy** defines fallback logic (e.g., switching to fundamental pricing) to prevent selling collateral at distressed prices during flash crashes. | `3-risk-and-economics/smart-oracles.md` |

#### Phase 5: Governance & Parameter Security

**User Intent:** Verify that administrative privileges cannot be exploited to expropriate funds.

| Key Question                                           | System Answer                                                                                                                                                      | Sitemap Component                       |
| ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------- |
| **"Who controls risk parameters?"**                    | **Market Curators.** Specific entities manage the risk parameters (LTVs, Limits) for their respective markets.                                                     | `4-governance-roles/market-curators.md` |
| **"Are there protections against malicious updates?"** | **Timelock Constraints.** Critical parameter changes are subject to a mandatory 24-hour timelock, allowing LPs to withdraw capital before changes take effect.     | `5-reference/risk-configuration.md`     |
| **"Who controls the technical infrastructure?"**       | **Instance Owner.** A chain-specific multisig acts as the technical gatekeeper for the Price Feed Store, ensuring oracle integrity independent of Market Curators. | `4-governance-roles/instance-owner.md`  |
