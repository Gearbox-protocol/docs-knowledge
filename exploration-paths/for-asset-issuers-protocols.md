# For Asset Issuers/Protocols

#### Phase 1: The Value Proposition (Distribution & Efficiency)

**User Intent:** Understand how Gearbox drives growth for the underlying protocol.

| Key Question                         | System Answer                                                                                                                                                                                                                                                                                | Sitemap Component                              |
| ------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| **"How does this grow our TVL?"**    | **Leverage as a Feature.** Gearbox acts as a multiplier on existing demand. By enabling users to mint/stake assets with leverage, issuers increase capital efficiency, attracting sticky, yield-focused capital that might otherwise go to competitors.                                      | `2-core-architecture/credit-manager.md`        |
| **"Does it require DEX liquidity?"** | **Zero-Slippage Execution.** Unlike standard lending markets, Gearbox does not strictly require deep DEX liquidity to enable leverage entry. Through **Direct Integration**, Credit Accounts can mint/redeem directly with protocol contracts, bypassing secondary market slippage entirely. | `2-core-architecture/adapters-integrations.md` |
| **"Can it handle complex flows?"**   | **Purpose-Specific Execution.** Gearbox adapts to the asset's mechanics. Whether it's staking, locking, or vesting, the Credit Account executes the logic natively. This allows issuers to offer "Leveraged Staking" or "Leveraged RWA Vaults" as a seamless user experience.                | `2-core-architecture/credit-manager.md`        |

#### Phase 2: Solving the Liquidity Problem (RWAs & Vaults)

**User Intent:** Address the specific friction points of illiquid or semi-liquid assets (RWAs, Private Credit).

| Key Question                                    | System Answer                                                                                                                                                                                                                                                                             | Sitemap Component                              |
| ----------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| **"We have delayed settlement. Does it work?"** | **Async Redemption Support.** Yes. Standard lending protocols fail here, but Gearbox excels. Credit Accounts can initiate a redemption, hold the receipt token through the settlement period, and claim the underlying funds upon finalization—all while maintaining the credit position. | `2-core-architecture/adapters-integrations.md` |
| **"Do we need to pay for incentives?"**         | **Capital Efficiency > Incentives.** By allowing users to mint assets at NAV (Net Asset Value) via leverage, issuers reduce the need to spend millions on incentives to deepen Curve/Uniswap pools just to support lending liquidations.                                                  | `3-risk-and-economics/liquidation-dynamics.md` |
| **"Can we enforce KYC/Whitelists?"**            | **Compliance Compatibility.** Yes. Because the Credit Account is a smart contract wallet, it can be compatible with protocol allowlists or transfer restrictions, ensuring that leveraged users meet compliance requirements.                                                             | `2-core-architecture/credit-manager.md`        |

#### Phase 3: Technical Integration (Adapters)

**User Intent:** Assess the engineering effort required to connect.

| Key Question                  | System Answer                                                                                                                                                                                                                        | Sitemap Component                              |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------- |
| **"How do we connect?"**      | **The Adapter Model.** Integration requires building an **Adapter**—a lightweight wrapper contract that translates Gearbox's safety checks into the protocol's function calls (e.g., `deposit()`, `stake()`, `requestRedemption()`). | `2-core-architecture/adapters-integrations.md` |
| **"Who builds the adapter?"** | **Collaborative Development.** Gearbox DAO maintains a library of standard adapters (ERC-4626, Curve, Uniswap). For custom logic, teams can fork a template or collaborate with Gearbox contributors for guidance.                   | `2-core-architecture/adapters-integrations.md` |

#### Phase 4: Risk Underwriting (Getting Approved)

**User Intent:** Understand how to satisfy the risk requirements of potential Curators.

| Key Question                     | System Answer                                                                                                                                                                                                                                                                                                        | Sitemap Component                              |
| -------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| **"How is risk assessed?"**      | **Curator Due Diligence.** There is no universal formula. Each Curator has a unique risk framework—some prioritize backing transparency, others prioritize secondary liquidity. Issuers should be prepared to provide data on volatility, redemption mechanics, and backing to facilitate this underwriting process. | `3-risk-and-economics/liquidation-dynamics.md` |
| **"How is the asset priced?"**   | **Flexible Oracle Architecture.** Gearbox supports diverse pricing models (Spot, TWAP, Fundamental/NAV). The choice depends on what the Curator is comfortable with. Issuers should propose a pricing source that is robust against manipulation to increase the likelihood of listing.                              | `3-risk-and-economics/price-oracle.md`         |
| **"How do we ensure solvency?"** | **Shared Assurance.** Curators need to know that liquidations will execute in bad market conditions. Issuers can significantly improve their listing chances by committing to run their own liquidator bots or providing a backstop for collateral liquidation.                                                      | `3-risk-and-economics/liquidation-dynamics.md` |

#### Phase 5: Go-to-Market (Decentralized Listing)

**User Intent:** Navigate the listing process in a permissionless environment.

| Key Question                         | System Answer                                                                                                                                                                                                                                                                               | Sitemap Component                       |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------- |
| **"Who approves the listing?"**      | **Marketplace of Risk.** Gearbox is a neutral infrastructure; there is no central "Listing Committee." Issuers must pitch **Market Curators**—independent operators who manage the liquidity. Curators decide what to list based on their own risk models and incentive requirements.       | `4-governance-roles/market-curators.md` |
| **"What drives Curator decisions?"** | **Incentive Alignment.** Different Curators have different mandates. Some prioritize high-yield assets and may require incentives (bribes/points) to list new tokens. Others prioritize safety and require strict audits. Success requires finding the right Curator for the asset profile. | `4-governance-roles/market-curators.md` |
| **"How fast can we launch?"**        | **Permissionless Agility.** Once a Curator agrees to underwrite the asset, the listing is permissionless. There is no DAO governance vote required to add a new collateral type to an existing Credit Manager.                                                                              | `4-governance-roles/market-curators.md` |
