# Protocol DAO

Unlike traditional DeFi protocols where the DAO manages risk parameters (like LTVs or Interest Rates) directly, Gearbox delegates these operational responsibilities to **Market Curators**. The DAO focuses on building the rails, while Curators operate the trains.

### Core Responsibilities

#### 1. System Upgrades & Versioning

The DAO maintains the core smart contracts that define the protocol's logic. It is the only entity capable of authorizing new versions of system components.

* **Contract Updates:** The DAO votes to deploy and authorize new implementations of core contracts (e.g., `PoolV3`, `CreditManagerV3`).
* **Bytecode Repository:** The DAO manages the onchain registry of verified contract bytecode. This ensures that when Curators deploy new markets, they are using secure, audited code approved by the protocol.

#### 2. Chain Activation

The DAO controls the expansion of the protocol to new blockchain networks.

* **Instance Deployment:** Before Gearbox can operate on a new chain (e.g., Arbitrum, Optimism), the DAO must authorize the deployment of the **Instance Owner** and **Treasury** contracts on that network.
* **Canonical Addressing:** The DAO ensures that there is a single, canonical instance of the protocol infrastructure on each supported chain, preventing fragmentation.

#### 3. Economic Alignment (GEAR Token)

The DAO utilizes the GEAR token to incentivize growth and align the interests of Curators, Liquidity Providers (LPs), and the protocol.

* **Incentive Programs:** The DAO can vote to allocate GEAR tokens for liquidity mining or grants to bootstrap specific markets or integrations.
* **Fee Split Configuration:** While Curators set the total fees for their markets, the DAO defines the protocol-level **Fee Split** (e.g., 50/50 split between Curator and DAO). Changing this global parameter requires a DAO vote.

### Limits of Authority

To preserve the permissionless nature of the protocol, the DAO's power is strictly limited at the smart contract level.

* **No Market Interference:** The DAO **cannot** change the risk parameters (LTVs, Liquidation Thresholds, Interest Rates) of a live market managed by a Curator.
* **No Asset Management:** The DAO **cannot** seize or reallocate funds deposited into Curator-managed pools.

This separation of powers ensures that Curators retain full sovereignty over their lending businesses.

### Related Pages

* **Who manages the risk parameters and daily operations?**
  * [Market Curators](https://www.google.com/url?sa=E\&q=market-curators.md)
