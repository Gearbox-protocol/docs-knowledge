# Prime Brokerage for RWA Credit Positions

Pool-based lending protocols — Morpho, Euler, Aave — accept standard ERC20 collateral. They lack native support for transition-state assets: pending deposit tokens, redemption receipts, and other non-standard representations that exist during RWA settlement cycles. Gearbox provides the per-position isolation and composable collateral management required to bridge this gap.

This page focuses on multi-protocol integration architecture. For settlement speed comparison and end-to-end flow details, see [RWA Settlement](rwa-settlement.md).

---

## Why Pool-Based Lenders Alone Are Insufficient

Pool-based lending protocols are optimized for a binary collateral model: an asset is an accepted ERC20 token or it is not. This creates three specific gaps for RWA-backed credit:

- **No native transition-state collateral support.** Pending deposit tokens and redemption receipts are not standard ERC20s. Pool-based protocols cannot accept them as collateral during settlement windows.
- **No per-position collateral isolation.** These systems pool positions — each borrower's collateral is not held in a separate contract with independent token tracking. A pending deposit and a mature token cannot be managed with separate risk parameters within the same pool.
- **No custom transition-stage valuation logic.** A pending deposit and a mature token carry different risk profiles but cannot be valued differently within a pooled model.

Gearbox Credit Account architecture addresses all three gaps. Each Credit Account is an independent smart contract (FACT-003) that can hold any combination of enabled tokens — including transition-state collateral. The Credit Manager tracks which tokens are active in each account via a bitmask (`enabledTokensMaskOf`), and the Curator assigns distinct Liquidation Thresholds per token type. A pending deposit token can carry an LT of 70% while the mature token carries 90%, reflecting the settlement risk differential within the same account.

---

## Actors and Contracts

| Actor | Role | On-Chain Mapping |
|---|---|---|
| **Borrower** | Opens an RWA-backed debt position | Interacts via `CreditFacadeV3` using batched `MultiCall` arrays |
| **Risk Curator** | Creates and configures the Gearbox market. Sets allowed tokens, adapters, Liquidation Thresholds, and debt limits for transition-state collateral. | Deploys market via `MarketConfigurator.createMarket()`, configures parameters via `CreditConfiguratorV3` |
| **Capital Allocator** | Manages liquidity allocation between the Partner Market and the Gearbox pool. May be the same entity as the Risk Curator. | Partner allocator contracts (Morpho vault curator, Euler vault operator, Aave governance) |
| **Partner Market** | Lending infrastructure for mature ERC20 positions | Aave pool, Euler vault, Morpho vault |
| **Gearbox Market** | Holds positions during deposit/redemption windows | Market suite: `PoolV3` + `CreditManagerV3` + `CreditFacadeV3` + `PriceOracleV3` + IRM + RateKeeper + LossPolicy |
| **RWA Issuer** | Asset issuer handling mint and redeem operations (e.g., Securitize for ACRED) | Token contract, mint contract, redeem contract |

### Curator Role Mapping

The term "Curator" maps to two distinct functions that may be performed by one entity or two:

**Risk Curator (Gearbox side):** Creates a Gearbox market via `MarketConfigurator.createMarket()`, which deploys the full market suite. The Risk Curator then configures the market to accept transition-state tokens — adding pending deposit tokens and redemption receipts as allowed collateral, setting their Liquidation Thresholds, and authorizing adapters that permit the Credit Account to interact with issuer mint/redeem contracts.

**Capital Allocator (Partner side):** Controls liquidity allocation within the Partner Market — for example, a Morpho vault curator directing capital toward RWA-backed vaults, or an Euler vault operator managing deposit caps. This role is defined by the partner protocol's own governance, not by Gearbox.

When one entity holds both roles, that entity can coordinate liquidity movements between Gearbox and the Partner Market without cross-organizational dependency.

---

## One-Time Setup

Before borrowers can take RWA-backed debt positions, the Risk Curator configures the Gearbox market:

**Gearbox market configuration:**
1. Deploy a new market via `MarketConfigurator.createMarket()`. This creates the `PoolV3`, `CreditManagerV3`, `CreditFacadeV3`, `PriceOracleV3`, IRM, RateKeeper, and LossPolicy as a suite.
2. Add transition-state tokens (pending deposit tokens, redemption receipts) as allowed collateral via `CreditConfiguratorV3`.
3. Set Liquidation Thresholds per token — lower LTs for tokens in settlement (reflecting redemption risk), higher LTs for mature tokens.
4. Authorize adapters for the RWA issuer's mint and redeem contracts, enabling Credit Accounts to interact with those contracts directly.
5. Configure price feeds for transition-state tokens in `PriceOracleV3`.

**Partner market coordination:**
1. The Capital Allocator creates or configures the partner vault/market for the mature RWA token.
2. Capital is allocated to be available for position migration once tokens mature.

---

## Position Transfer Mechanism

When a position matures (pending-deposit → mature token like ACRED), it can be migrated from the Gearbox market to the Partner Market. Migration is capital-neutral: both sides of the position move simultaneously.

- **Capital Allocator** controls supply-side allocation — moves liquidity between the Gearbox Pool and the Partner Market.
- **Borrower** (via Credit Account) controls debt + collateral — repays one venue, borrows from the other.

When Capital Allocator and borrower operations are coordinated, supply and debt move together. The financial position remains unchanged: same collateral, same debt, same health factor. Only the infrastructure changes.

### Option A: Adapter-Based Atomic Migration

Gearbox adapters are lightweight wrapper contracts that translate Credit Account operations into external protocol calls while enforcing safety constraints. If the destination partner market supports batched operations, an adapter can execute the full migration atomically:

1. The borrower submits a `MultiCall` array via `CreditFacadeV3.multicall()`.
2. Within the multicall, an integration adapter calls the partner market's supply function, depositing the mature collateral.
3. The adapter borrows from the partner market against the deposited collateral.
4. The adapter repays the Gearbox debt from borrowed funds.
5. `CreditFacadeV3` performs the health factor check at the end of the multicall. If the final state is overcollateralized, the transaction succeeds.

**Prerequisites:** The adapter must be authorized by the Risk Curator via `CreditConfiguratorV3`. The destination market must support supply + borrow within a single transaction context. The resulting position must be transferable to the borrower's address.

### Option B: Automated Bot / Orchestrator

If atomic transfer is unavailable:

1. The borrower triggers migration (single action).
2. A restricted-permission bot executes via `CreditFacadeV3.botMulticall()`: borrow from Partner Market, repay Gearbox debt, move collateral, close Credit Account, transfer position to original owner.

**Safety constraints:** Bot permissions are defined as a `uint192` bitmask — the bot can execute only explicitly granted operation types. It can transfer only to the Credit Account owner (`getBorrowerOrRevert()`). All actions are deterministic and auditable.

### Partner Integration Requirements

| Partner | Integration Path | Key Consideration |
|---|---|---|
| **Morpho** | Adapter wrapping Morpho vault supply + borrow | Verify per-market whether atomic supply+borrow is supported in the target vault configuration |
| **Aave** | Bot-orchestrated (Option B) by default | Aave's pool architecture typically requires an orchestrator rather than single-transaction migration |
| **Euler** | Adapter wrapping Euler vault operations | Verify per-vault whether the design supports atomic supply+borrow via adapter |

Each integration requires a purpose-built adapter contract authorized by the Risk Curator. The adapter translates Gearbox's multicall pattern into the partner protocol's interface while ensuring the Credit Account's collateral accounting remains consistent.

---

## Capital Flow Summary

| Stage | Capital Location | Reason |
|---|---|---|
| Entry (settlement pending) | Gearbox Pool | Position holds transition-state collateral (pending deposit token) |
| Entry (matured) | Partner Market | Position holds mature ERC20 — migrated via adapter or bot |
| Exit (redemption pending) | Gearbox Pool | Position holds redemption receipt token during settlement |
| Exit (settled) | N/A | Position closed, debt repaid |

The Capital Allocator actively manages liquidity allocation between venues — moving capital to the Gearbox Pool when transition-state positions are active and returning it to the Partner Market after maturation or close.

---

## How Credit Accounts Enable Prime Brokerage

| Capability | Mechanism | Outcome |
|---|---|---|
| **Transition-stage collateral** | Risk Curator adds pending-deposit tokens and redemption receipts as allowed collateral in `CreditConfiguratorV3` | Credit Accounts hold non-standard tokens as valid, priced collateral during settlement |
| **Per-token risk differentiation** | Distinct Liquidation Thresholds per token (`liquidationThresholds(address token)`) | Pending tokens carry lower LTs than mature tokens, reflecting settlement risk |
| **Composable protocol interaction** | Authorized adapters enable Credit Accounts to call issuer mint/redeem contracts and partner market supply/borrow functions | Single Credit Account orchestrates the full lifecycle without manual token transfers |
| **Atomic solvency enforcement** | `CreditFacadeV3` checks health factor only at the end of a `MultiCall` batch | Complex multi-step operations (migrate collateral, swap debt venue) succeed if the final state is overcollateralized |
| **Isolated position accounting** | Each Credit Account is a separate smart contract; enabled tokens tracked via bitmask (`enabledTokensMaskOf`) | No cross-contamination between borrower positions; each account's collateral and debt are independently verifiable |

These capabilities are structural to Gearbox's Credit Account architecture. Pool-based lending protocols would require fundamental architectural changes to replicate per-position isolation with heterogeneous collateral types and custom risk parameters per token.

---

## Related Pages

- How do entry and exit flows work end-to-end, including settlement speed? → [RWA Settlement](rwa-settlement.md)
- How does direct redemption work for semi-liquid assets without DEX liquidity? → [Direct Redemptions](direct-redemptions.md)
- How are Curator roles structured and what parameters do they control? → [Market Curators](../governance/market-curators.md)
- What is the full parameter reference for collateral and Credit Manager configuration? → [Risk Configuration Dictionary](risk-configuration-dictionary.md)
