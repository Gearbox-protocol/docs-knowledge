# For Ecosystems & Chains

Gearbox Protocol adds a composable leverage layer to an ecosystem's existing DeFi stack. Rather than operating as an isolated lending market, Gearbox routes leveraged capital directly into local protocols — DEXs, yield vaults, staking contracts — through onchain adapters. The economic effect: increased volume and TVL across the chain's native applications, not just within Gearbox itself.

---

## Deployment Requirements

Gearbox requires four infrastructure conditions before deployment is feasible.

### Block Gas Limit

Gearbox contracts execute complex multi-call transaction batches (open, multicall, liquidate). The chain must support a block gas limit of **>30 million gas** to accommodate core contract deployment and typical user operations.

### RPC Infrastructure

Offchain components — the Gearbox interface, liquidator bots, monitoring systems — require stable RPC providers with consistent uptime. Unreliable RPC infrastructure directly degrades liquidation reliability, which degrades market solvency.

### Oracle Coverage

Reliable price feeds are required for every collateral asset before that asset can be listed. Gearbox supports multiple oracle providers:

| Provider | Model | Key Constraint |
|----------|-------|----------------|
| Chainlink | Push-based | Standard, widely available |
| Redstone | Signature-based | Validates unique signatures from authorized signers; max delay 10 min |
| Pyth | Pull-based | Includes confidence interval safety checks (reverts if too wide) |
| API3 | Push-based | Alternative coverage |

All feeds conform to the Chainlink AggregatorV3Interface and standardize to 8 decimals for USD pairs. Staleness checks apply: if a feed exceeds its staleness period, the system falls back to a reserve feed (if configured) or reverts. At least one of these providers must cover each target collateral asset.

### EVM Compatibility

Gearbox deploys on any EVM-compatible chain. No custom opcodes or precompiles are required. Factory-based deployment uses Create2 for deterministic contract addresses across chains.

---

## Economic Prerequisites

Infrastructure alone is insufficient. Leveraged markets require specific economic conditions to function.

### DEX Liquidity Depth

Gearbox liquidations involve swapping collateral on local DEXs. DEX liquidity must support liquidation of all listed collateral types. Deeper liquidity enables higher borrowing limits and tighter liquidation premiums. Thin liquidity forces lower caps and wider premiums, reducing capital efficiency. Initial markets should target assets with demonstrated swap depth.

### Liquidator Network

A functioning liquidation network is a prerequisite, not an afterthought. Without liquidators, markets cannot maintain solvency. Gearbox provides open-source liquidator bot infrastructure. The chain should plan to:

1. Onboard local MEV searchers and keepers before launch
2. Verify that liquidator bots can profitably execute given local gas costs and block times
3. Ensure at least 2–3 independent liquidator operators are committed at launch

### Asset Selection

Productive yield-bearing assets (LSTs, LRTs, vaults) are the primary use case. Leverage on yield-bearing collateral attracts borrowers because leveraged yield exceeds borrowing cost. Leverage on zero-yield tokens generates insufficient demand to justify deployment — borrowers gain no yield advantage to offset the cost of leverage.

Strongest initial markets: LST/underlying pairs, yield vault strategies, liquid staking derivatives.

---

## What Gets Deployed: The Market Suite

Each market deployment creates a full suite of contracts via `MarketConfigurator.createMarket()`:

| Component | Function |
|-----------|----------|
| **PoolV3** | Liquidity hub — lenders deposit here, CreditManagers borrow from here |
| **PoolQuotaKeeperV3** | Manages per-token borrowing limits (quotas) for risky assets |
| **PriceOracleV3** | Central price registry — maps tokens to price feeds |
| **InterestRateModel** | Utilization-based rate curve (LinearInterestRateModelV3) |
| **RateKeeper** | Sets quota rate premiums per collateral token |
| **LossPolicy** | Defines rules for handling bad debt liquidations |

The hub-and-spoke model: PoolV3 is the liquidity hub; multiple CreditManagers connect as spokes, each with independent risk parameters. A single pool can serve multiple strategies and collateral configurations simultaneously.

Curators also control granular risk limits:
- `setTotalDebtLimit()` — cap on aggregate pool borrowing
- `setCreditManagerDebtLimit()` — per-CreditManager borrowing cap
- `setTokenLimit()` — per-token exposure limit

---

## Operating Model: Roles and Responsibilities

Three parties share responsibility for a Gearbox deployment:

| Role | Responsibility | Risk Ownership |
|------|---------------|----------------|
| **Gearbox DAO** (Service Provider) | Deploys and maintains core protocol contracts, oracle infrastructure, and liquidator bot templates. Provides the technology stack. | Smart contract correctness, protocol upgrades |
| **Risk Curators** (Operators) | Create markets, set risk parameters (LTs, limits, rates), and manage ongoing risk. Independent entities — not Gearbox employees. | Market solvency, parameter calibration |
| **Ecosystem / Chain** (Distribution) | Provides liquidity depth, onboards local projects for adapter integration, recruits curators and users. | Liquidity conditions, infrastructure reliability |

**Who runs the markets?** Curators. The chain can recruit trusted curators from its ecosystem or request introductions to active Gearbox curators. The DAO does not operate markets directly.

**Is market creation gated?** No. Once the protocol is deployed on a chain, market creation is permissionless. Curators call `MarketConfigurator.createMarket()` to deploy a full market suite without requiring DAO approval. This enables rapid alignment with the chain's roadmap and new asset launches.

---

## Composability Value Proposition

A standard lending protocol creates an isolated liquidity pool. Gearbox operates differently:

- **Volume amplification.** Credit Accounts execute trades on local DEXs, stake in local validators, and deposit into local yield vaults — all with leverage. Every leveraged action generates real volume for the chain's native protocols.
- **Productive collateral support.** Gearbox supports complex assets: LP tokens, vault shares, LSTs, LRTs, Pendle PTs. Ecosystems with unique yield-bearing assets can offer leverage on those assets specifically, creating differentiated products unavailable on other chains.
- **Adapter-based integration.** Each integration with a local protocol requires an adapter — a lightweight wrapper contract. Once deployed, leveraged users interact with the local protocol through the same function calls (`deposit()`, `stake()`, `swap()`), preserving the native UX while adding leverage.

Gearbox does not compete with existing protocols on the chain. It amplifies demand for them.

---

## Launch Sequence

1. **Technical qualification.** Verify gas limits (>30M), RPC stability, oracle coverage for target assets, and DEX liquidity depth.
2. **Curator recruitment.** Identify or recruit curators willing to manage markets on the chain. Incentive grants from the ecosystem fund accelerate this step.
3. **Adapter development.** Build adapters for the chain's key protocols (DEXs, staking contracts, yield vaults). Gearbox DAO maintains a library of standard adapters (ERC-4626, Curve, Uniswap) that may be reusable.
4. **Liquidator onboarding.** Deploy open-source liquidator bots; recruit local keepers. Verify profitability under local gas costs.
5. **Market launch.** Curators deploy markets via `MarketConfigurator.createMarket()`. Joint announcements and incentive campaigns with the chain's existing DeFi ecosystem.

### Incentive Alignment

Chains typically accelerate adoption by offering grants or incentives to curators for initial market creation. The Gearbox DAO frequently coordinates joint incentive programs and promotes chain launches to the existing user base.

---

## Cross-References

- How does the curator role work and what markets have curators launched? → [Market Curators](../governance/market-curators.md)
- How does liquidation infrastructure maintain market solvency? → [Liquidation Dynamics](../economics-and-risk/liquidation-dynamics.md)
- How do oracle price feeds work and what happens when feeds go stale? → [Price Oracle](../economics-and-risk/price-oracle.md)
- How does the hub-and-spoke pool architecture support multiple markets? → [One Pool, Many Markets](../introduction/one-pool-many-markets.md)
- How do adapters integrate with local protocols? → [Adapters & Integrations](../core-architecture/adapters-integrations.md)
- What is the full EVM deployment architecture? → [Omni-EVM Architecture](../introduction/omni-evm-architecture.md)
