# Prime Brokerage for RWA Credit Positions

Pool-based lending protocols — Morpho, Euler, Aave — accept standard ERC-20 collateral. They lack native support for transition-state assets: pending deposit tokens, redemption receipts, and other non-standard representations that exist during RWA settlement cycles. Gearbox provides per-position isolation and composable collateral management that bridges this gap through `CreditAccountV3` (FACT-003), with all operations executing as batched `MultiCall` arrays through `CreditFacadeV3` (FACT-004).

**Scope:** Multi-protocol integration architecture for RWA-backed leveraged positions. Defines actors, state transitions, migration mechanisms, and failure modes.

**Anti-scope:** Settlement speed comparison and end-to-end entry/exit flows → [RWA Settlement](rwa-settlement.md). Direct issuer redemption mechanics → [Direct Redemptions](direct-redemptions.md). Curator parameter configuration details → [Risk Configuration Dictionary](risk-configuration-dictionary.md).

---

## Why Pool-Based Lenders Alone Are Insufficient

Pool-based lending protocols optimize for a binary collateral model: an asset is an accepted ERC-20 token or it is not. Three structural gaps prevent them from supporting RWA-backed credit:

1. **No transition-state collateral support.** Pending deposit tokens and redemption receipts are non-standard representations. Pool-based protocols cannot accept them as collateral during settlement windows because their collateral registries only recognize finalized ERC-20 tokens.

2. **No per-position collateral isolation.** Pool-based systems aggregate positions — each borrower's collateral is not held in a separate contract with independent token tracking. A pending deposit and a mature token cannot carry separate risk parameters within the same pool.

3. **No per-token valuation differentiation.** A pending deposit token and a mature token carry different risk profiles. A pool that accepts both must value them identically or not accept one at all.

Gearbox Credit Account architecture resolves all three gaps:

- **Isolation:** Each `CreditAccountV3` is an independent smart contract (FACT-003). The Credit Manager tracks active tokens per account via a bitmask — `enabledTokensMaskOf(address creditAccount)` (FACT-101).
- **Heterogeneous collateral:** The Risk Curator adds transition-state tokens (pending deposits, redemption receipts) as allowed collateral via `CreditConfiguratorV3`. Each token receives a distinct Liquidation Threshold — `liquidationThresholds(address token)` (FACT-104). A pending deposit token carries a lower LT (e.g., 70%) while the mature token carries a higher LT (e.g., 90%), reflecting the settlement risk differential.
- **Solvency enforcement:** `CreditFacadeV3` checks the Health Factor at the end of every `MultiCall` batch (FACT-050). HF = TWV / Total Debt, where TWV = Σ(Balance_i × Price_i × LT_i) for all enabled tokens (FACT-051). The transaction reverts if HF < 1.0.

---

## Actors and Contracts

| Actor | Role | On-Chain Mapping |
|---|---|---|
| **Borrower** | Opens and manages an RWA-backed debt position | Calls `CreditFacadeV3.openCreditAccount()` (FACT-010), `multicall()` (FACT-012) |
| **Risk Curator** | Creates the Gearbox market. Sets allowed tokens, adapters, Liquidation Thresholds, debt limits | Deploys via `MarketConfigurator.createMarket()` (FACT-080), configures via `CreditConfiguratorV3` |
| **Capital Allocator** | Manages liquidity allocation between the Partner Market and the Gearbox pool. May be the same entity as the Risk Curator | Partner allocator contracts (Morpho vault curator, Euler vault operator, Aave governance) |
| **Partner Market** | Lending infrastructure for mature ERC-20 positions | Aave pool, Euler vault, Morpho vault |
| **Gearbox Market** | Holds positions during deposit/redemption settlement windows | Market suite: `PoolV3` + `CreditManagerV3` + `CreditFacadeV3` + `PriceOracleV3` + IRM + RateKeeper + LossPolicy (FACT-081) |
| **RWA Issuer** | Asset issuer handling mint and redeem operations (e.g., Securitize for ACRED) | Token contract, mint contract, redeem contract |

### Curator Role Mapping

The term "Curator" maps to two distinct functions that may be performed by one entity or two:

**Risk Curator (Gearbox side):** Creates a Gearbox market via `MarketConfigurator.createMarket()` (FACT-080), which deploys the full market suite using factory-based Create2 deployment for deterministic addresses (FACT-082). The Risk Curator then configures the market to accept transition-state tokens — adding pending deposit tokens and redemption receipts as allowed collateral, setting Liquidation Thresholds per token, and authorizing adapters that permit the Credit Account to interact with issuer mint/redeem contracts.

**Capital Allocator (Partner side):** Controls liquidity allocation within the Partner Market — for example, a Morpho vault curator directing capital toward RWA-backed vaults, or an Euler vault operator managing deposit caps. This role is defined by the partner protocol's governance, not by Gearbox.

When one entity holds both roles, that entity coordinates liquidity movements between Gearbox and the Partner Market without cross-organizational dependency.

---

## One-Time Setup

Before borrowers can take RWA-backed debt positions, the Risk Curator configures the Gearbox market and the Capital Allocator prepares the partner venue.

### Gearbox Market Configuration

1. Deploy a new market via `MarketConfigurator.createMarket()` (FACT-080). This creates the full suite: `PoolV3`, `PoolQuotaKeeperV3`, `CreditManagerV3`, `CreditFacadeV3`, `PriceOracleV3`, IRM, RateKeeper, and LossPolicy (FACT-081).
2. Add transition-state tokens (pending deposit tokens, redemption receipts) as allowed collateral via `CreditConfiguratorV3`.
3. Set Liquidation Thresholds per token via `CreditConfiguratorV3` — lower LTs for tokens in settlement (reflecting redemption risk), higher LTs for mature tokens. Query thresholds via `liquidationThresholds(address token)` (FACT-104).
4. Configure price feeds for transition-state tokens in `PriceOracleV3` (FACT-070). Feed types depend on the asset: bounded feeds for tokens with known exchange rates (FACT-076), composite feeds for derived prices, or external Chainlink/Pyth/Redstone feeds (FACT-074).
5. Authorize adapters for the RWA issuer's mint and redeem contracts via `CreditConfiguratorV3`, enabling Credit Accounts to interact with those contracts directly.
6. Set debt limits: `setTotalDebtLimit(uint256 limit)` for aggregate pool borrowing (FACT-083), `setCreditManagerDebtLimit(address creditManager, uint256 limit)` per Credit Manager (FACT-084), and optionally `setTokenLimit(address token, uint96 limit)` for per-token exposure caps (FACT-085).

### Partner Market Coordination

1. The Capital Allocator creates or configures the partner vault/market for the mature RWA token.
2. Capital is allocated to be available for position migration once tokens mature.

---

## Position Lifecycle: State Transitions

A position moves through four states. Each transition changes the capital location and the applicable risk parameters.

```
┌─────────────┐    mint settles    ┌─────────────┐    migration    ┌─────────────┐
│   PENDING    │ ─────────────────→ │   MATURED    │ ──────────────→ │  MIGRATED    │
│  (Gearbox)   │                    │  (Gearbox)   │                 │  (Partner)   │
└─────────────┘                    └─────────────┘                 └─────────────┘
                                         │                               │
                                         │ redemption initiated          │ redemption initiated
                                         ↓                               ↓
                                   ┌─────────────┐                ┌─────────────┐
                                   │  REDEEMING   │                │  REDEEMING   │
                                   │  (Gearbox)   │                │  (Gearbox)   │
                                   └──────┬──────┘                └──────┬──────┘
                                          │ settlement completes          │
                                          ↓                               ↓
                                   ┌─────────────┐                ┌─────────────┐
                                   │   CLOSED     │                │   CLOSED     │
                                   └─────────────┘                └─────────────┘
```

| State | Collateral Type | Location | LT Range | Key Constraint |
|---|---|---|---|---|
| **PENDING** | Pending deposit token | Gearbox Pool | Lower (reflects settlement risk) | Cannot migrate until token matures |
| **MATURED** | Mature RWA token (e.g., ACRED) | Gearbox Pool | Higher (reflects full backing) | Eligible for migration to Partner Market |
| **MIGRATED** | Mature RWA token | Partner Market | Set by partner protocol | Gearbox Credit Account closed or holding partner receipt |
| **REDEEMING** | Redemption receipt token | Gearbox Pool | Lower (reflects redemption risk) | Debt continues accruing during settlement |
| **CLOSED** | None | N/A | N/A | Debt repaid, Credit Account closed via `closeCreditAccount()` (FACT-011) |

**Invariant:** At every state, the position must satisfy HF ≥ 1.0 (FACT-050). If HF drops below 1.0 during any state — including PENDING and REDEEMING — the position becomes liquidatable. Anyone can call `liquidateCreditAccount()` (FACT-014) or `partiallyLiquidateCreditAccount()` (FACT-015).

---

## Position Transfer Mechanism

When a position matures (PENDING → MATURED), it becomes eligible for migration from the Gearbox market to the Partner Market. Migration is capital-neutral: collateral and debt move simultaneously so that the financial position remains unchanged.

Two actors coordinate:
- **Capital Allocator** controls supply-side allocation — moves liquidity between the Gearbox Pool and the Partner Market.
- **Borrower** (via Credit Account) controls debt + collateral — repays one venue, borrows from the other.

### Option A: Adapter-Based Atomic Migration

Adapters are lightweight wrapper contracts that translate Credit Account operations into external protocol calls while enforcing safety constraints. If the destination partner market supports batched supply + borrow operations, an adapter executes the full migration atomically:

1. The borrower submits a `MultiCall` array via `CreditFacadeV3.multicall(creditAccount, calls)` (FACT-012).
2. Within the multicall, an authorized integration adapter calls the partner market's supply function, depositing the mature collateral from the Credit Account.
3. The adapter calls the partner market's borrow function against the deposited collateral.
4. The adapter repays the Gearbox debt using the borrowed funds — calling the repay operation within the same multicall.
5. `CreditFacadeV3` performs the health factor check at the end of the multicall (FACT-050). If the final state satisfies HF ≥ 1.0, the transaction succeeds. If not, the entire transaction reverts.
6. The Credit Account is closed via `closeCreditAccount()` (FACT-011) or left open if partial migration.

**Prerequisites:**
- The adapter must be authorized by the Risk Curator via `CreditConfiguratorV3`.
- The destination market must support supply + borrow within a single transaction context.
- The resulting partner-side position must be transferable to the borrower's address.

**Edge case:** If the partner market's supply function reverts (e.g., deposit cap reached, token paused), the entire multicall reverts. The position remains in the Gearbox market at its pre-migration state. No partial migration occurs — atomicity is guaranteed by the multicall pattern.

### Option B: Bot-Orchestrated Migration

If atomic transfer is unavailable (partner market does not support batched supply + borrow):

1. The borrower triggers migration by granting bot permissions.
2. The bot executes via `CreditFacadeV3.botMulticall(creditAccount, calls)` (FACT-013):
   - Borrow from Partner Market against an intermediate credit line.
   - Repay Gearbox debt from borrowed funds.
   - Move collateral from Credit Account to Partner Market.
   - Close Credit Account via `closeCreditAccount()` (FACT-011).
   - Transfer the partner-side position to the original owner — verified via `getBorrowerOrRevert(creditAccount)` (FACT-100).

**Safety constraints:** Bot permissions are defined as a `uint192` bitmask — the bot can execute only explicitly granted operation types. The bot can transfer only to the Credit Account owner. All actions are deterministic and auditable on-chain.

**Edge case:** If the bot's transaction fails mid-sequence (e.g., insufficient partner-side liquidity), the multicall reverts entirely. The Credit Account remains open with the original collateral and debt. The borrower retains ownership verified via `getBorrowerOrRevert()` (FACT-100).

### Partner Integration Matrix

| Partner | Integration Path | Atomicity | Key Consideration |
|---|---|---|---|
| **Morpho** | Adapter wrapping Morpho vault supply + borrow | Verify per-market | Whether atomic supply + borrow is supported depends on the target vault configuration |
| **Aave** | Bot-orchestrated (Option B) | Typically non-atomic | Aave's pool architecture requires an orchestrator rather than single-transaction migration |
| **Euler** | Adapter wrapping Euler vault operations | Verify per-vault | Whether the vault design supports atomic supply + borrow via adapter depends on configuration |

Each integration requires a purpose-built adapter contract authorized by the Risk Curator. The adapter translates the Gearbox multicall pattern into the partner protocol's interface while ensuring the Credit Account's collateral accounting remains consistent.

---

## Capital Flow Summary

| Stage | Capital Location | Collateral Held | Trigger for Transition |
|---|---|---|---|
| Entry (settlement pending) | Gearbox Pool | Pending deposit token | RWA issuer completes mint → token matures |
| Entry (matured) | Gearbox Pool → Partner Market | Mature ERC-20 (e.g., ACRED) | Borrower initiates migration via multicall or bot |
| Exit (redemption pending) | Gearbox Pool | Redemption receipt token | RWA issuer completes redemption → receipt settles |
| Exit (settled) | N/A | None | Borrower calls `closeCreditAccount()` (FACT-011) |

The Capital Allocator moves liquidity between venues: supplying the Gearbox Pool when transition-state positions are active and returning capital to the Partner Market after maturation or close.

---

## How Credit Accounts Enable Prime Brokerage

| Capability | Mechanism | Canon Reference |
|---|---|---|
| **Transition-state collateral** | Risk Curator adds pending-deposit tokens and redemption receipts as allowed collateral in `CreditConfiguratorV3` | FACT-003, FACT-101 |
| **Per-token risk differentiation** | Distinct Liquidation Thresholds per token — `liquidationThresholds(address token)` | FACT-104 |
| **Composable protocol interaction** | Authorized adapters enable Credit Accounts to call issuer mint/redeem contracts and partner market supply/borrow functions within a single `MultiCall` | FACT-004, FACT-012 |
| **Atomic solvency enforcement** | `CreditFacadeV3` checks HF only at the end of a `MultiCall` batch — complex multi-step operations succeed if the final state satisfies HF ≥ 1.0 | FACT-050, FACT-051 |
| **Isolated position accounting** | Each Credit Account is a separate smart contract; enabled tokens tracked via bitmask `enabledTokensMaskOf()` | FACT-003, FACT-101 |
| **Debt ceiling enforcement** | Per-pool (`setTotalDebtLimit`), per-CM (`setCreditManagerDebtLimit`), and per-token (`setTokenLimit`) caps bound exposure | FACT-083, FACT-084, FACT-085 |

Pool-based lending protocols would require fundamental architectural changes to replicate per-position isolation with heterogeneous collateral types and custom risk parameters per token.

---

## Risk Disclosures

⚠️ **Settlement delay extends debt accrual.** During PENDING and REDEEMING states, the position holds transition-state collateral while debt continues accruing interest. If the RWA issuer delays settlement (extended mint processing, paused redemptions, or contract bugs), debt grows against collateral that cannot be liquidated at full value. The borrower bears this cost. If accrued debt causes HF to drop below 1.0, the position becomes liquidatable — the borrower loses the position and the liquidator seizes the transition-state collateral at a discount (FACT-053).

⚠️ **Transition-state token oracle risk.** The Health Factor calculation for PENDING and REDEEMING positions depends on the price feed configured for the transition-state token in `PriceOracleV3` (FACT-070). If the feed cannot accurately track the token's redemption value — for example, if the issuer devalues pending claims — the HF calculation diverges from actual risk. Bounded feeds (FACT-076) cap and floor the rate, but bounds are governance-set parameters that require periodic review by the Risk Curator.

⚠️ **Migration failure leaves position in Gearbox.** If adapter-based migration (Option A) fails due to partner-side conditions (deposit caps, token pauses, liquidity shortfall), the multicall reverts and the position remains in the Gearbox market. The borrower continues paying Gearbox pool interest rates. If the Capital Allocator has already moved liquidity to the partner venue, the Gearbox Pool may have reduced available liquidity, potentially affecting other borrowers' ability to open new positions or increase debt.

⚠️ **Bot permission scope.** In Option B, the bot operates under a `uint192` permission bitmask. If the bitmask grants broader permissions than intended, the bot could execute operations beyond the migration scope. The Risk Curator and borrower must verify the permission bitmask before granting bot access. Misconfigured permissions are not recoverable within a transaction — the bot executes whatever the bitmask allows.

⚠️ **Partner market risk is additive.** After migration, the position is subject to the partner protocol's risk model (oracle configuration, liquidation parameters, governance decisions) in addition to any residual Gearbox exposure. Gearbox has no control over partner-side liquidation thresholds, oracle feeds, or governance actions. The borrower bears risk from both protocols during the migration window and from the partner protocol afterward.

---

## Related Pages

- How do entry and exit flows work end-to-end, including settlement timing? → [RWA Settlement](rwa-settlement.md)
- How does direct redemption work for semi-liquid assets without DEX liquidity? → [Direct Redemptions](direct-redemptions.md)
- What parameters does the Risk Curator control and how are markets configured? → [Market Curators](../governance/market-curators.md)
- What is the full parameter reference for collateral and Credit Manager configuration? → [Risk Configuration Dictionary](risk-configuration-dictionary.md)
- How does the oracle system value transition-state tokens? → [Smart Oracles](../economics-and-risk/smart-oracles.md)
