# Documentation Content Architecture

## Phase 1 — System Overview

### 1. `system-overview/one-pool-many-markets.md`
- **Objective:** Explain how Gearbox decouples passive liquidity from active risk.
- **Key Concepts:**
  - The “Wholesale Bank” analogy (Pool) vs. “Retail Branches” (Credit Suites)
  - Risk Isolation (Debt Ceilings)
  - The Diesel Token as the unified yield-bearing asset
- **Anti-Scope:**
  - Do not explain how to configure a Credit Suite (see `credit-suite.md`)
  - Do not explain how yield is calculated (see `pool.md`)
- **Outbound Links:**
  - `../core-architecture/pool.md`
  - `../core-architecture/credit-suite.md`

### 2. `system-overview/credit-account.md`
- **Objective:** Explain the concept of Wallet-Native Credit.
- **Key Concepts:**
  - Smart Contract Wallet (user ownership)
  - Solvency Check (Health Factor > 1)
  - Composability (wallet-native interaction with DeFi)
- **Anti-Scope:**
  - Do not list specific adapters
  - Do not explain liquidation math
- **Outbound Links:**
  - `../core-architecture/credit-suite.md` (solvency enforcement)
  - `../core-architecture/adapters-integrations.md` (flexible defi interactions)
  - `../core-architecture/pool.md` (own source of liquidity; do dependence on external sources)

### 3. `system-overview/omni-evm-architecture.md`
- **Objective:** Explain the deployment model.
- **Key Concepts:**
  - Modular Instances (no bridge dependency)
  - Instance Owner role (chain-specific governance)
  - Bytecode Repository (verifiable deployments)
- **Anti-Scope:**
  - Do not list specific chain IDs
- **Outbound Links:**
  - `../governance-and-operations/protocol-dao.md` (token holders' financial interests; delivery of core codebase)
  - `../governance-and-operations/instance-owner.md` (soft role for overseeing local chain parameters)
  - `../governance-and-operations/market-curators.md` (business builders and risk managers)
  

---

## Phase 2 — Exploration Paths (User-Centric Entry Points)

### 4. `exploration-paths/for-lenders-lps.md`
- **Objective:** Route passive capital providers to Pool mechanics and risk parameters.
- **Outbound Links:**
  - `../core-architecture/pool.md`
  - `../economics-and-risk/interest-rate-model.md`

### 5. `exploration-paths/for-borrowers-farmers.md`
- **Objective:** Route active users to Credit Account mechanics and leverage strategies.
- **Outbound Links:**
  - `../system-overview/credit-account.md`
  - `../core-architecture/adapters-integrations.md`

### 6. `exploration-paths/for-curators.md`
- **Objective:** Route risk managers to Credit Suite configuration and parameter control.
- **Outbound Links:**
  - `../governance-and-operations/market-curators.md`
  - `../reference/risk-configuration-dictionary.md`

### 7. `exploration-paths/for-ecosystems-chains.md`
- **Objective:** Route chain BD/Devs to deployment architecture and Instance Owner logic.
- **Outbound Links:**
  - `../system-overview/omni-evm-architecture.md`
  - `../governance-and-operations/instance-owner.md`

### 8. `exploration-paths/for-asset-issuers-protocols.md`
- **Objective:** Route protocol integrators to Adapter logic and Quota limits.
- **Outbound Links:**
  - `../core-architecture/adapters-integrations.md`
  - `../economics-and-risk/quota-controls.md`

---

## Phase 3 — Core Architecture

### 9. `core-architecture/pool.md`
- **Objective:** Explain the liability side of the balance sheet.
- **Key Concepts:**
  - ERC-4626 standard
  - Diesel Token exchange rate (non-rebasing)
  - Branch model (lending to Credit Suites, not users)
- **Anti-Scope:**
  - Do not explain interest rate models (see `interest-rate-model.md`)
- **Outbound Links:**
  - `../economics-and-risk/interest-rate-model.md` (utilization-driven rate discovery)
  - `../economics-and-risk/quota-controls.md` (collateral-specific rates and collateral exposure limits)
  - `../core-architecture/credit-suite.md` (product branches. currators allow credit lines to specific strategies/ credit products)

### 10. `core-architecture/credit-suite.md`
- **Objective:** Explain the asset side of the balance sheet (formerly Credit Manager).
- **Key Concepts:**
  - Credit Manager - credit accountant (logic container, solvency logic)
  - Credit Facade (user interaction)
  - Configurator (curator interaction)
- **Anti-Scope:**
  - Do not list specific risk parameters (see `risk-configuration-dictionary.md`)
- **Outbound Links:**
  - `../economics-and-risk/liquidation-dynamics.md` (solvency is enforced by liquidations. curators and users must be aware of)
  - reference/risk-configuration-dictionary.md (complete list of parameters that affect behavior)

### 11. `core-architecture/adapters-integrations.md`
- **Objective:** Explain the execution layer.
- **Key Concepts:**
  - Sanitized interface model
  - Multicall (atomic composability)
  - Router (pathfinding)
- **Anti-Scope:**
  - Do not list every supported protocol (link to a dynamic list instead)
- **Outbound Links:**
  - reference/direct-redemptions.md (particular usecase of adapters)
  - `core-architecture/credit-suite.md` (solvency checks that happen on every external integration)


---

## Phase 4 — Economics & Risk

### 12. `economics-and-risk/interest-rate-model.md`
- **Objective:** Explain the cost of capital.
- **Key Concepts:**
  - Utilization curve (kink, slopes)
  - Liquidity reservation (forced repayment)
- **Anti-Scope:**
  - Do not explain quota rates (see `quota-controls.md`)
- **Outbound Links:**
  - `economics-and-risk/quota-controls.md` (collateral-specific rates is core part to ensure capital efficiency)
  - economics-and-risk/fees (protocol and curators take fees on top of paid interest which increases effective rates)

### 13. `economics-and-risk/quota-controls.md`
- **Objective:** Explain concentration risk and asset-specific pricing.
- **Key Concepts:**
  - Asset-side caps
  - Quota rates (risk premium)
- **Anti-Scope:**
  - Do not explain the base rate
- **Outbound Links:**
  - `interest-rate-model.md` (base rate is applied to all debt independent of what it's borrowed against)
  - reference/risk-configuration-dictionary.md (quota limits and rates are parameteer configured by curators and is whithin the scope of their controls)

### 14. `economics-and-risk/liquidation-dynamics.md`
- **Objective:** Explain solvency enforcement.
- **Key Concepts:**
  - Health Factor formula ($H_f$)
  - Liquidation Threshold (LT)
  - Liquidation premium
  - Partial liquidation logic
- **Anti-Scope:**
  - Do not explain oracle feeds
- **Outbound Links:**
  - `price-oracle.md`  (collateral prices is ther core part of calculating position solvency. The protocol knows about token value only from the oracle data)
  - reference/risk-configuration-dictionary.md (qrisk parameters are dynamically controlled by curators and therefore will affect the solvency status and possibly liquidation eligibility)
  - 


### 15. `economics-and-risk/price-oracle.md`
- **Objective:** Explain valuation.
- **Key Concepts:**
  - Normalization (8 decimals)
  - Feed types (Spot, TWAP, Fundamental)
- **Anti-Scope:**
  - Do not explain dual-feed logic (see `smart-oracles/dual-oracle-system.md`)
- **Outbound Links:**
  - `smart-oracles/dual-oracle-system.md` (gearbox is protected against manipulation and extreme conditions on a protocol level of how it works with oracles)

### 16. `economics-and-risk/smart-oracles/dual-oracle-system.md`
- **Objective:** Explain the price safety architecture.
- **Key Concepts:**
  - Dual-feed architecture (Main vs. Reserve)
  - Staleness checks
  - Circuit breakers (pause, forbid)
- **Anti-Scope:**
  - Do not explain bad debt handling (see `loss-policy.md`)
- **Outbound Links:**
  - `loss-policy.md` (bad debt prevention mechanism which reinforces the dual-oracle system)
  - `../price-oracle.md` (all the prices used for this calculation logic anyway come from price oracle contract being a registry of all feeds in the market)

### 17. `economics-and-risk/smart-oracles/loss-policy.md`
- **Objective:** Explain the protocol response to bad debt.
- **Key Concepts:**
  - Deficit recognition
  - Treasury intervention
- **Anti-Scope:**
  - Do not explain liquidation triggers
- **Outbound Links:**
  - `core-architecture/pool.md` (bad debt socialization rules if it happens)


---

## Phase 5 — Governance & Operations

### 18. `governance-and-operations/market-curators.md`
- **Objective:** Explain the business logic of running a market.
- **Key Concepts:**
  - Roles (admin, pauser, fee collector)
  - Mandatory timelock as a user protection step
  - Fee-sharing model
  - Permissionless market creation
- **Anti-Scope:**
  - Do not explain technical deployment
- **Outbound Links:**
  - `../reference/risk-configuration-dictionary.md` (complete list of parameters subject to curators' decisions)

### 19. `governance-and-operations/instance-owner.md`
- **Objective:** Explain the technical gatekeeper.
- **Key Concepts:**
  - Price feed store control
  - Multisig composition
  - Neutrality principle
- **Anti-Scope:**
  - Do not explain market parameters
- **Outbound Links:**
  - `../economics-and-risk/price-oracle.md` (where the feeds are used)

### 20. `governance-and-operations/protocol-dao.md`
- **Objective:** Explain protocol-level governance.
- **Key Concepts:**
  - Upgrades (new logic)
  - Chain activation
  - Incentives (GEAR token)
- **Anti-Scope:**
  - Do not explain market parameters
- **Outbound Links:**
  - `market-curators.md`

---

## Phase 6 — Reference

### 21. `reference/risk-configuration-dictionary.md`
- **Objective:** Serve as the canonical parameter dictionary.
- **Key Concepts:**
  - Parameter table (name, description, range, timelock)
  - Role table (who can change what)
- **Anti-Scope:**
  - No narrative. Facts only.
- **Outbound Links:**
  - None (leaf node)

### 22. `reference/supply-information.md`
- **Objective:** Detail token supply dynamics and emission schedules.
- **Outbound Links:**
  - `../governance-and-operations/protocol-dao.md`

### 23. `reference/direct-redemptions.md`
- **Objective:** Technical guide for redeeming from Pool directly (bypassing UI).
- **Outbound Links:**
  - `../core-architecture/pool.md`