# For Ecosystems & Chains

Gearbox Protocol adds a composable leverage layer to an ecosystem's existing DeFi stack. Rather than operating as an isolated lending market, Gearbox routes leveraged capital directly into local protocols — DEXs, yield vaults, staking contracts — through onchain adapter contracts. Each leveraged position executes as a batched `MultiCall` array through `CreditFacadeV3`, directing borrowed capital into the chain's native applications. The economic result: increased volume and TVL across the chain's DeFi protocols, not within Gearbox alone.

---

## Deployment Requirements

Gearbox requires four infrastructure conditions before deployment is feasible.

### Block Gas Limit

`CreditFacadeV3.openCreditAccount()` opens a position and executes an arbitrary sequence of adapter calls in a single transaction. `CreditFacadeV3.multicall()` performs ongoing position management. Liquidation transactions carry similar complexity. The chain must support a block gas limit of **>30 million gas** to accommodate these operations.

### RPC Infrastructure

Offchain components — the interface, liquidator bots, monitoring systems — require stable RPC providers. Unreliable RPC infrastructure directly degrades liquidation reliability. If liquidation bots cannot submit transactions during price declines, bad debt accrues to the pool's lenders. RPC downtime is a solvency risk, not a convenience issue.

### Oracle Coverage

`PriceOracleV3` maps each token to a price feed. Every collateral asset requires a functioning feed before listing. The system supports a primary and a reserve (fallback) feed per token: if the primary exceeds its staleness threshold, the system falls back to the reserve; if no reserve exists, the transaction reverts.

Gearbox supports Chainlink (push-based), Redstone (signature-based), Pyth (pull-based), and computed LP feeds. All feeds standardize to **8 decimals** for USD pairs and conform to the Chainlink `AggregatorV3Interface`. At least one supported provider must offer feeds for each target collateral asset on the chain. See [Price Oracle](../economics-and-risk/price-oracle.md) for feed mechanics and failure modes.

### EVM Compatibility

Gearbox deploys on any EVM-compatible chain. No custom opcodes or precompiles are required. Factory-based deployment uses `Create2` for deterministic contract addresses across chains.

---

## Economic Prerequisites

### DEX Liquidity Depth

Liquidators swap collateral on local DEXs. DEX liquidity must support full liquidation of the largest expected position for each listed collateral type. Deeper liquidity enables higher per-token exposure limits (`PoolQuotaKeeperV3.setTokenLimit()`), tighter liquidation premiums, and higher aggregate borrowing caps (`setTotalDebtLimit()`). Thin liquidity forces lower caps and wider premiums, reducing capital efficiency. Initial markets should target assets with demonstrated swap depth on at least one local DEX.

### Liquidator Network

A functioning liquidation network is a prerequisite. Without active liquidators, Credit Accounts that breach health factor thresholds remain open, accumulating losses that pass to lenders via the pool. Gearbox provides open-source liquidator bot infrastructure. The ecosystem must:

1. **Onboard local MEV searchers and keepers before launch.** Liquidators must be operational when the first Credit Account opens.
2. **Verify profitability.** Bots must profitably execute given local gas costs, block times, and expected liquidation premiums.
3. **Ensure redundancy.** A minimum of 2–3 independent operators reduces the risk of simultaneous downtime.

See [Liquidation Dynamics](../economics-and-risk/liquidation-dynamics.md) for health factor mechanics and liquidation premium structure.

### Asset Selection

Yield-bearing assets (LSTs, LRTs, yield vaults) are the primary use case. Leverage on yield-bearing collateral attracts borrowers because leveraged yield exceeds borrowing cost. Leverage on zero-yield tokens generates insufficient demand — borrowers gain no yield advantage to offset borrowing cost.

Strongest initial markets: LST/underlying pairs (e.g., wstETH/ETH), ERC-4626 yield vault strategies, and liquid staking derivatives native to the chain.

---

## What Gets Deployed

A Risk Curator calls `MarketConfigurator.createMarket()` to deploy a full market suite as a single atomic operation:

| Component | Contract | Role |
|-----------|----------|------|
| Liquidity Hub | `PoolV3` | Receives lender deposits; CreditManagers borrow from this pool |
| Quota Manager | `PoolQuotaKeeperV3` | Per-token borrowing limits for each collateral asset |
| Price Registry | `PriceOracleV3` | Maps tokens to price feeds (primary + reserve per token) |
| Rate Curve | `LinearInterestRateModelV3` | Borrow rates based on pool utilization |
| Rate Keeper | `RateKeeper` | Quota rate premiums per collateral token |
| Loss Rules | `LossPolicy` | Rules for handling bad debt from underwater liquidations |

`PoolV3` is the liquidity hub. Multiple `CreditManagers` connect to one pool as independent spokes, each with its own collateral list, liquidation thresholds, and debt limits. Each borrower operates through an isolated `CreditAccountV3` — one borrower's positions cannot affect another's. See [One Pool, Many Markets](../introduction/one-pool-many-markets.md) for the hub-and-spoke architecture.

Curators control exposure at three levels: pool-wide (`setTotalDebtLimit()`), per-CreditManager (`setCreditManagerDebtLimit()`), and per-token (`setTokenLimit()`). This allows conservative initial limits that expand as liquidity and liquidator capacity mature.

---

## Operating Model

Three parties share responsibility for a Gearbox deployment.

### Gearbox DAO

**Provides:** Core protocol contracts, factory contracts for `Create2` deployment, open-source liquidator bot templates, standard adapter library (ERC-4626, Curve, Uniswap, Aave wrappers), interface and SDK components.

**Ongoing:** Protocol upgrades, security patches, audit coordination.

**Risk owned:** Smart contract correctness, protocol-level bugs.

### Risk Curators

**Provides:** Market creation via `MarketConfigurator.createMarket()`, risk parameter calibration (liquidation thresholds, collateral lists, debt limits, rate parameters), ongoing monitoring and adjustment.

**Ongoing:** Monitor oracle health and collateral risk, adjust limits as liquidity conditions evolve, respond to market stress by tightening parameters.

**Risk owned:** Market solvency, parameter calibration errors, bad debt from mispriced risk.

Curators are independent risk management entities — not Gearbox employees. The chain can recruit curators from its ecosystem or request introductions to existing active Gearbox curators. See [Market Curators](../governance/market-curators.md) for curator mechanics and track record.

### Ecosystem / Chain

**Must provide:** Sufficient DEX liquidity for listed collateral types, stable RPC infrastructure (>99.5% uptime target), at least 2–3 committed liquidator operators before launch, grant funding to incentivize curator onboarding and initial liquidity, local protocol teams willing to coordinate adapter development.

**Ongoing:** Maintain infrastructure reliability, support new adapter integrations as the DeFi stack evolves, recruit additional curators and liquidators as markets grow.

**Risk owned:** Liquidity conditions, infrastructure reliability, liquidator availability.

### Market Creation After Deployment

Once the protocol is deployed, market creation is permissionless. Any curator calls `MarketConfigurator.createMarket()` to deploy a full market suite without DAO approval. This enables rapid alignment with the chain's asset roadmap.

---

## Adapter Architecture

Adapters are the mechanism through which leveraged capital flows into local protocols. Each adapter is a lightweight wrapper contract that translates calls from a `CreditAccountV3` into calls to a target protocol.

An adapter exposes the same external interface as the target protocol (e.g., `deposit()`, `stake()`, `swap()`). All operations execute through `CreditFacadeV3` as batched `MultiCall` arrays. After the entire multicall batch completes, `CreditFacadeV3` runs a single solvency check — intermediate states within the batch are not validated (check-on-exit model). The target protocol receives standard function calls — no modifications to the integrated protocol are required.

The Gearbox DAO maintains standard adapters (ERC-4626, Curve, Uniswap v2/v3). Protocols sharing these interfaces can reuse existing adapters directly. Custom interfaces require new adapter development — typically 200–500 lines of Solidity per integration. See [Adapters & Integrations](../core-architecture/adapters-integrations.md) for technical details.

---

## Risk Disclosures

Deploying a leverage protocol introduces risks that ecosystem teams must evaluate before proceeding.

**Smart contract risk.** Gearbox core contracts have undergone multiple audits, but smart contract risk is never zero. A critical vulnerability in core contracts (`PoolV3`, `CreditManagerV3`, `CreditFacadeV3`) could result in loss of deposited funds. Each new adapter adds surface area.

**Oracle failure.** Stale feeds fall back to the reserve; if no reserve exists, transactions revert, freezing liquidations. Manipulated feeds can trigger unwarranted liquidations (pricing too low) or prevent necessary liquidations (pricing too high), causing bad debt.

**Liquidator failure.** If all operators go offline simultaneously — due to RPC outages, gas spikes, or coordinated failure — unhealthy Credit Accounts remain open. During rapid price declines, this converts to bad debt absorbed by lenders via the `LossPolicy`.

**Liquidity withdrawal.** If DEX liquidity deteriorates after markets launch, liquidators may be unable to execute swaps at acceptable prices. Curators must tighten parameters or wind down markets.

**Curator inaction.** If a curator fails to adjust risk parameters in response to changing conditions — declining liquidity, new oracle risks, protocol upgrades on integrated protocols — the market's risk profile diverges from its parameter settings.

---

## Launch Sequence

1. **Technical qualification.** Verify gas limits (>30M), RPC stability (>99.5% uptime over 30 days), oracle coverage for target assets, and DEX liquidity depth for expected position sizes.
2. **Curator recruitment.** Identify or recruit curators willing to manage markets. Ecosystem grants for initial curator compensation accelerate this step.
3. **Adapter development.** Build adapters for key protocols (DEXs, staking contracts, yield vaults). Audit the existing adapter library for reusability; custom adapters require development and audit.
4. **Liquidator onboarding.** Deploy open-source liquidator bots. Recruit 2–3 local keepers. Verify profitability under local gas costs and block times. Conduct test liquidations on testnet.
5. **Market launch.** Curators deploy markets via `MarketConfigurator.createMarket()`, producing the full suite: `PoolV3`, `PoolQuotaKeeperV3`, `PriceOracleV3`, `LinearInterestRateModelV3`, `RateKeeper`, and `LossPolicy`.

Chains typically accelerate adoption through curator grants for market creation, liquidity incentives for `PoolV3` deposits, and liquidator subsidies during the low-volume launch period.

---

## Cross-References

- How does the curator role work and what markets have curators launched? → [Market Curators](../governance/market-curators.md)
- How does liquidation infrastructure maintain market solvency? → [Liquidation Dynamics](../economics-and-risk/liquidation-dynamics.md)
- How do oracle price feeds work and what happens when feeds go stale? → [Price Oracle](../economics-and-risk/price-oracle.md)
- How does the hub-and-spoke pool architecture support multiple markets? → [One Pool, Many Markets](../introduction/one-pool-many-markets.md)
- How do adapters integrate with local protocols? → [Adapters & Integrations](../core-architecture/adapters-integrations.md)
- What is the full EVM deployment architecture? → [Omni-EVM Architecture](../introduction/omni-evm-architecture.md)
