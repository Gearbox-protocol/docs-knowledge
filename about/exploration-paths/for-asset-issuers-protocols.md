# For Asset Issuers & Protocols

Gearbox creates leveraged demand for listed assets. When a token is listed as collateral in a Gearbox market, borrowers acquire and hold that asset at multiples of their own capital — driving real TVL growth, protocol fee revenue, and secondary market volume for the issuer. Standard lending protocols allow borrowing *against* an asset. Gearbox allows borrowing *into* an asset: borrowed capital flows directly into the issuer's contracts via Credit Accounts.

---

## Economic Case for Integration

### TVL Amplification

A borrower deposits 100 ETH and opens a 4x leveraged position in an LST protocol. The issuer receives 400 ETH of staking deposits — 300 ETH of additional real capital, not synthetic exposure. This multiplier effect applies to every leveraged position holding the asset.

The mechanism: each Credit Account is an isolated smart contract wallet that holds real tokens. When a borrower enters a leveraged stETH position, the Credit Account calls `deposit()` or `stake()` on the issuer's contracts. The issuer's TVL metrics, protocol fees, and staking rewards all reflect the full leveraged amount.

### Sticky Capital via Yield Spread

Leveraged yield strategies remain profitable as long as asset yield exceeds borrowing cost (base interest rate + quota rate premium). For yield-bearing assets — LSTs, LRTs, yield vaults — this spread is often structurally positive. Positions persist without ongoing incentive spend from the issuer, unlike liquidity mining programs that expire.

### Reduced Liquidity Incentive Costs

Standard lending protocols require deep DEX liquidity pools so liquidators can swap collateral. Issuers often subsidize this liquidity through incentive programs. Gearbox adapters can route directly through the issuer's native mint/redeem functions (e.g., `requestWithdrawal()` → `claimWithdrawal()`) rather than relying solely on DEX swap paths. This reduces the issuer's DEX liquidity obligations.

---

## Structural Advantage: Borrow Into, Not Against

Most lending protocols treat listed assets as passive collateral — the borrower deposits the asset and borrows stablecoins against it. The asset sits locked; no additional demand flows to the issuer.

Gearbox inverts this. Borrowers borrow stablecoins (or ETH) and deploy that capital *into* the issuer's protocol. A Credit Account holding wstETH represents a borrower who actively acquired wstETH with leverage. Each leveraged position is net new demand for the asset, not existing supply locked away.

This distinction matters for:

- **LST/LRT issuers:** Each leveraged position increases total staked capital and validator participation
- **Vault protocols (e.g., ERC-4626):** Leveraged deposits increase vault TVL and proportional fee revenue
- **LP token issuers:** Leveraged LP positions deepen pool liquidity and trading volume

---

## Concrete Integration Scenarios

### Liquid Staking Token (LST)

An LST issuer (comparable to Lido, Rocket Pool) integrates with Gearbox. The adapter wraps `submit()` and `requestWithdrawals()`. Once a curator lists the LST as collateral with a liquidation threshold set via `liquidationThresholds(address token)`, borrowers can:

1. Open a Credit Account with ETH collateral
2. Borrow additional ETH from the pool
3. Stake all ETH via the adapter, receiving the LST within the Credit Account
4. Earn staking yield on the full leveraged amount; pay borrowing cost on the debt portion

If staking APR is 4% and borrowing cost is 2%, the borrower earns a positive spread on 3x capital. The issuer gains 3x the staking deposits from a single borrower.

### Liquid Restaking Token (LRT)

An LRT protocol integrates its deposit and withdrawal functions. The adapter handles the deposit path and, critically, the async withdrawal path — including receipt tokens for pending claims. Credit Accounts hold the receipt token through the settlement period and claim upon finalization. This is a structural advantage: most lending protocols cannot support delayed-settlement assets as collateral because they require instant liquidation.

### ERC-4626 Vault

Vaults conforming to ERC-4626 (`deposit()`, `withdraw()`, `redeem()`) can use Gearbox's standard ERC-4626 adapter with zero custom development. The curator sets the vault share token's liquidation threshold and quota limit via `setTokenLimit(address token, uint96 limit)`, and the vault becomes available for leveraged strategies immediately.

---

## Technical Integration Path

### Step 1: Adapter

An **adapter** is a wrapper contract that translates Gearbox's safety accounting into calls to the issuer's protocol functions. Every interaction between a Credit Account and an external protocol passes through an adapter.

The adapter enforces:
- Collateral balance tracking after each operation
- Mapping of the issuer's function signatures to Gearbox's MultiCall execution framework
- Prohibition of unauthorized calls or fund extraction

**Standard interfaces (ERC-4626, Curve, Uniswap):** Gearbox DAO maintains a library of audited adapters. If the issuer's protocol conforms to a standard interface, an existing adapter can be deployed as a configuration task — no new development required.

**Custom interfaces (non-standard staking, locking, vesting, async redemption):** The issuer's team forks a template adapter and implements the custom function mappings. Typical development time: 1–3 weeks including audit.

### Step 2: Oracle Coverage

Every collateral token requires a price feed registered in `PriceOracleV3`. Supported oracle types: Chainlink (push-based), Pyth (pull-based with confidence interval checks), Redstone (signature-based), LP price feeds, Composite feeds, Bounded feeds, and NAV-based feeds.

All feeds implement the Chainlink AggregatorV3Interface, standardized to 8 decimals for USD pairs. Staleness checks apply: if `block.timestamp >= updatedAt + stalenessPeriod`, the system falls back to a reserve feed or reverts.

For assets with thin secondary market liquidity but well-defined Net Asset Value (RWA tokens, structured products), NAV-based or Bounded oracle feeds avoid the circular dependency where an asset needs DEX depth to be listed, but needs listing to attract DEX depth.

**Issuer action:** Confirm that at least one supported oracle provider covers the asset. If not, coordinate with a provider to establish a feed, or propose a NAV-based pricing methodology.

### Step 3: Curator Engagement

There is no central listing committee. Risk Curators — independent operators who create and manage Gearbox markets via `MarketConfigurator.createMarket()` — decide which assets to list and bear the financial risk of those decisions.

---

## Risk Controls Available to Curators (and Relevant to Issuers)

Curators configure granular risk parameters per asset. Issuers benefit from understanding these controls because they determine how much leveraged demand the asset can attract.

| Parameter | Function | Effect on Issuer |
|-----------|----------|-----------------|
| **Liquidation Threshold (LT)** | `liquidationThresholds(address token)` — the LT determines how much of the asset's value counts toward collateral | Higher LT → higher maximum leverage → more capital flowing into the issuer's protocol |
| **Quota Limit** | `setTokenLimit(address token, uint96 limit)` — caps total exposure to the token across all Credit Accounts in a market | Controls concentration risk; issuers seeking higher caps can provide supporting data |
| **Quota Rate** | Premium charged to borrowers holding the asset, set via RateKeeper | Lower quota rate → cheaper leverage → more demand; issuers can subsidize this rate |
| **Total Debt Limit** | `setTotalDebtLimit(uint256 limit)` — aggregate borrowing cap for the pool | Determines overall market capacity |

These parameters are set per-market. Multiple curators can list the same asset with different parameters, creating competitive leverage markets.

---

## Improving Listing Probability

Curators bear direct financial risk from listing decisions. Issuers materially improve listing chances by reducing the risk curators take:

- **Oracle quality.** Provide a reliable, manipulation-resistant price feed. Propose the specific provider and feed configuration. Assets without oracle coverage cannot be listed.
- **Liquidation infrastructure.** Run a dedicated liquidator bot for the asset, ensuring position closure even in thin secondary markets. Alternatively, commit to a redemption backstop — a standing offer to purchase the asset at a defined floor during liquidation events.
- **Risk data package.** Provide historical volatility data, stress-test scenarios, DEX liquidity depth, audit reports, bug bounty details, and contract maturity metrics. Curators who can underwrite the asset faster will list it sooner.
- **Quota rate subsidy.** Borrowers pay a quota rate premium on listed assets. Issuers can fund a rate reduction, making leveraged positions more profitable and increasing demand.

---

## Listing Workflow

1. **Adapter availability.** Confirm an adapter exists or build one. Without an adapter, the asset cannot interact with Credit Accounts.
2. **Oracle setup.** Establish a price feed in a supported format. The Instance Owner multisig whitelists new oracle feeds — coordinate with Gearbox DAO contributors.
3. **Curator engagement.** Identify curators whose risk appetite aligns with the asset's profile. Present the risk data package.
4. **Parameter configuration.** The curator sets LT, quota limit, quota rate, and any asset-specific constraints. Adding a new collateral type to an existing CreditManager is permissionless — no DAO governance vote required.
5. **Launch.** The asset becomes available for leveraged strategies in the curator's market.

**Timeline:** Once an adapter and oracle exist and a curator agrees to underwrite, listing proceeds within days. The bottleneck is curator due diligence and oracle setup, not protocol governance.

---

## Decision Paths

| Issuer Profile | Starting Point |
|---------------|---------------|
| LST/LRT issuer seeking leveraged staking demand | Check adapter library for ERC-4626 or custom staking compatibility → engage curators → [Adapters & Integrations](../core-architecture/adapters-integrations.md) |
| RWA / tokenized fund with delayed redemption | Review NAV-based oracle options and async redemption adapter patterns → [Smart Oracles](../economics-and-risk/smart-oracles.md) |
| ERC-4626 vault seeking leveraged deposits | Standard adapter available — focus on oracle setup and curator engagement → [Adapters & Integrations](../core-architecture/adapters-integrations.md) |
| Protocol preparing a curator pitch | Assemble risk data package (volatility, liquidity, oracle, audits) → [Market Curators](../governance-and-operations/market-curators.md) |

---

## Cross-References

- How do adapters translate protocol interactions for Credit Accounts? → [Adapters & Integrations](../core-architecture/adapters-integrations.md)
- How do curators evaluate and list new collateral assets? → [Market Curators](../governance-and-operations/market-curators.md)
- How do oracle price feeds work, and what happens when feeds go stale? → [Price Oracle](../economics-and-risk/price-oracle.md)
- How do NAV-based and bounded oracle feeds support illiquid assets? → [Smart Oracles](../economics-and-risk/smart-oracles.md)
- How do quota limits control per-token concentration risk? → [Quota Limits & Concentration](../economics-and-risk/quota-limits-concentration.md)
- How does the liquidation system enforce solvency? → [Liquidation Dynamics](../economics-and-risk/liquidation-dynamics.md)
- How does the hub-and-spoke pool model support multiple markets from one liquidity source? → [One Pool, Many Markets](../introduction/one-pool-many-markets.md)
