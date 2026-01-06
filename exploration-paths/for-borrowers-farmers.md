# For Borrowers/Farmers

#### Phase 1: Feasibility & Capacity Analysis

**User Intent:** Determine if the protocol can support the target strategy size and complexity.

| Key Question                             | System Answer                                                                                                                                                                                                                                  | Sitemap Component                                                                       |
| ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| **"What constrains position size?"**     | **Liquidity & Exposure Limits.** Capacity is bounded by two distinct factors: 1) Global liquidity availability in the Pool, and 2) Strategy-specific Debt Ceilings defined by the Curator.                                                     | `2-core-architecture/pool-liquidity-vault.md` \<br> `5-reference/risk-configuration.md` |
| **"What are the primary risk vectors?"** | **Risk Vector Identification.** Borrowers face three primary threats: 1) **Market Risk** (Collateral volatility), 2) **Rate Risk** (Utilization-driven cost spikes), and 3) **Liquidity Risk** (Inability to exit via external DEX liquidity). | `3-risk-and-economics/liquidation-dynamics.md`                                          |
| **"Is the target collateral eligible?"** | **Collateral Allowlist.** Each Credit Manager enforces a strict allowlist of assets. Tokens not explicitly whitelisted cannot be held within the Credit Account.                                                                               | `2-core-architecture/credit-manager.md`                                                 |

#### Phase 2: Cost of Carry Modeling

**User Intent:** Model the dynamic cost of capital to project net yield and volatility exposure.

| Key Question                             | System Answer                                                                                                                                                                          | Sitemap Component                             |
| ---------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------- |
| **"What drives the base rate?"**         | **Interest Rate Model.** Rates are dynamic and determined by **Pool Utilization**. Large withdrawals by LPs can cause immediate utilization spikes, increasing the cost of capital.    | `3-risk-and-economics/interest-rate-model.md` |
| **"Are there asset-specific premiums?"** | **Quota Rates.** Illiquid or high-volatility collateral assets may carry an _additional_ interest premium (Quota Rate) imposed by the Quota Keeper, independent of the base pool rate. | `3-risk-and-economics/quota-keeper.md`        |
| **"What is the protocol take rate?"**    | **Interest Fee.** The Curator and DAO capture a fixed percentage of the interest paid. This markup is additive to the base rate paid to LPs.                                           | `5-reference/risk-configuration.md`           |

#### Phase 3: Solvency & Liquidation Mechanics

**User Intent:** Define the liquidation boundary and the economic consequences of insolvency.

| Key Question                               | System Answer                                                                                                                                                                                          | Sitemap Component                              |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------- |
| **"What triggers liquidation?"**           | **Liquidation Triggers.** Insolvency can result from: 1) Collateral depreciation, 2) Debt asset appreciation, or 3) **Accrued Interest** (Rate spikes eroding the Health Factor).                      | `3-risk-and-economics/liquidation-dynamics.md` |
| **"What is the penalty structure?"**       | **Liquidation Premium.** Upon liquidation, the borrower forfeits a fixed percentage (e.g., 5%) of the liquidated collateral to the third-party liquidator.                                             | `3-risk-and-economics/liquidation-dynamics.md` |
| **"Are automated mitigations available?"** | **Partial Liquidation & Deleverage.** The protocol supports partial liquidations to restore solvency without full closure. Automated deleveraging tools can be utilized to maintain the Health Factor. | `3-risk-and-economics/liquidation-dynamics.md` |

#### Phase 4: Governance & Parameter Risk

**User Intent:** Assess the risk of adverse parameter changes by the market operator.

| Key Question                                     | System Answer                                                                                                                                                                                   | Sitemap Component                       |
| ------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------- |
| **"Can parameters change mid-trade?"**           | **Parameter Risk.** Yes. Curators can modify Liquidation Thresholds (LTVs). However, these changes are subject to a mandatory **Timelock**, providing a window for borrowers to adjust or exit. | `5-reference/risk-configuration.md`     |
| **"What are the operational circuit breakers?"** | **Smart Oracles & Pauses.** 1) Significant deviation between Main and Reserve price feeds will block operations. 2) Admins retain the ability to pause Credit Managers in emergency scenarios.  | `3-risk-and-economics/smart-oracles.md` |
| **"Can access be revoked?"**                     | **Access Control.** Curators can forbid specific tokens or adapters, preventing borrowers from increasing exposure to those assets.                                                             | `4-governance-roles/market-curators.md` |

#### Phase 5: Position Unwind & Liquidity Dependencies

**User Intent:** Evaluate the reliability of exit mechanisms under stress.

| Key Question                               | System Answer                                                                                                                                                                                                        | Sitemap Component                              |
| ------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| **"What are the execution dependencies?"** | **External Liquidity.** The "Atomic Close" relies on external DEX liquidity (e.g., Curve/Uniswap) to swap collateral for the debt asset. Thin liquidity or high slippage can cause repayment transactions to revert. | `2-core-architecture/adapters-integrations.md` |
| **"What is the contingency procedure?"**   | **Manual Unwind.** If atomic execution fails, the borrower must manually withdraw collateral (subject to solvency checks), execute swaps externally, and repay the debt.                                             | `2-core-architecture/credit-manager.md`        |

\</file>
