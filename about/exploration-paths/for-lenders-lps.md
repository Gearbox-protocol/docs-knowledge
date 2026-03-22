# For Lenders & LPs

Gearbox pools offer variable-rate yield on single-asset deposits, sourced exclusively from borrower interest payments. Capital is deployed into a segregated architecture where each borrowing market carries independent risk parameters and exposure limits. This page addresses the risk-adjusted return profile, withdrawal mechanics, and failure modes relevant to a capital allocation decision.

---

## Liability Architecture

Gearbox operates a hub-and-spoke model. A single PoolV3 (the hub) connects to multiple CreditManagers (the spokes). Each CreditManager defines an independent borrowing market with its own collateral whitelist, liquidation thresholds, and debt ceiling.

**Risk segregation consequence:** A collateral failure in one CreditManager does not propagate to another. If Market A experiences bad debt, Market B's parameters and exposure are unaffected. The pool's aggregate loss is bounded by the debt ceiling allocated to the impaired market, not by total pool TVL.

**Multi-chain isolation:** Each EVM deployment operates as an independent instance — not a bridged dependency. Capital on Arbitrum is not exposed to a contract vulnerability on Optimism.

---

## Yield Mechanics and Withdrawal Risk

### Yield Accrual

Depositors receive dTokens (ERC-4626 compliant shares) upon calling `PoolV3.deposit()`. The dToken exchange rate appreciates monotonically as borrowers pay interest. No rebasing occurs; the share price reflects accumulated yield.

**Yield composition per borrower:**

| Component | Source | Paid To |
|---|---|---|
| Base interest rate | Utilization-driven interest rate model | Pool (LP yield) |
| Quota rate premium | Asset-specific rate set by the RateKeeper/Gauge | Pool (LP yield) |
| Interest fee | Fixed percentage markup | Curator + DAO treasury |

The lender's effective APY equals the pool supply rate (`PoolV3.supplyRate()`), which reflects the weighted sum of base and quota interest paid by all active borrowers, minus the protocol fee take.

### Interest Rate Model

Rates follow a kinked utilization curve (LinearInterestRateModelV3). Below optimal utilization (U_optimal), rates increase gradually. Above U_optimal, rates scale steeply — incentivizing borrower repayment and restoring withdrawal liquidity.

### Withdrawal Constraints

Withdrawals via `PoolV3.withdraw()` or `PoolV3.redeem()` execute atomically against available pool liquidity (`PoolV3.availableLiquidity()`).

**When withdrawals may fail:** If utilization approaches 100%, available liquidity drops to zero. The lender cannot withdraw until borrowers repay or new deposits arrive. The steep post-kink interest rate is the primary mechanism to force this correction — it makes borrowing prohibitively expensive, creating economic pressure to repay.

**No lockup period exists.** Withdrawal is constrained only by available liquidity, not by a time-based lock.

⚠️ **Liquidity risk:** During extreme market events, borrowers may be unable or unwilling to repay even at elevated rates. Withdrawal delays are bounded in practice by liquidation enforcement (see below), but are not contractually guaranteed to resolve within a specific timeframe.

---

## Counterparty Risk and Solvency Enforcement

The lender's counterparty is not an individual borrower — it is the pool of Credit Accounts managed by each connected CreditManager.

### Fund Isolation

Borrowed capital is held within Credit Accounts — isolated smart contracts that borrowers interact with exclusively through CreditFacadeV3. Borrowers cannot withdraw the underlying loan. They can only execute whitelisted operations (swaps, deposits into approved protocols) via pre-audited Adapters. Direct token transfers out of a Credit Account are blocked.

### Health Factor and Liquidation

Solvency is enforced via the Health Factor:

> **HF = TWV / Total Debt**

Where TWV (Total Weighted Value) = Σ(Balance_i × Price_i × LT_i) across all enabled collateral tokens, and Total Debt = Principal + Base Interest + Quota Interest + Fees.

When HF falls below 1.0, the account becomes liquidatable. Anyone can call `liquidateCreditAccount()` — liquidation is permissionless. The liquidator repays the pool's debt, receives a premium (1 - liquidation discount), and the protocol treasury takes a fee. This three-party incentive structure ensures liquidations are economically motivated without relying on protocol-operated keepers.

### Partial Liquidation

Partial liquidation via `partiallyLiquidateCreditAccount()` enables incremental debt reduction without fully closing the position. The liquidator repays a specified debt amount and receives discounted collateral proportionally, plus a fee to the treasury.

⚠️ **Oracle dependency:** All collateral valuations rely on PriceOracleV3 price feeds. If a price feed fails or is manipulated, liquidation triggers may fire late (producing bad debt) or prematurely (causing unnecessary position closure). See Stress Resilience below.

---

## Stress Resilience and Failure Modes

### Oracle Resilience

PriceOracleV3 supports dual-feed architecture per token: a primary feed and a reserve fallback. If the primary feed becomes stale (exceeds its staleness period), the system falls back to the reserve feed. Supported feed types include Chainlink, Pyth (pull-based), Redstone (signature-based), LP price feeds, Composite, and Bounded feeds — all normalized to 8-decimal USD pricing.

**LP token price feeds** use a Limiter with a hard lower bound. If the rate falls below the lower bound, operations revert — preventing liquidations at manipulated prices. If the rate exceeds the upper bound (lower bound + 200 bps), the price is capped.

**Pyth feeds** enforce a maximum confidence-to-price ratio. If the confidence interval is too wide (indicating unreliable pricing), the feed reverts.

### Concentration Risk Controls

The Quota Keeper enforces per-token exposure limits (`setTokenLimit()`). Even if pool liquidity is abundant, aggregate exposure to a single volatile asset is capped globally. This prevents a scenario where a single collateral type dominates pool risk.

Additional layered limits:
- **Total debt limit** (`setTotalDebtLimit()`) — caps aggregate pool borrowing
- **Per-CreditManager debt limit** (`setCreditManagerDebtLimit()`) — caps borrowing per market

### Bad Debt Resolution

When collateral value falls below total debt (HF < 1.0 and liquidation does not fully cover the debt), bad debt occurs.

The AliasedLossPolicyV3 governs bad debt liquidation. Before permitting a loss-bearing liquidation, the policy re-checks account solvency using TWAP-based alias price feeds — preventing fire-sale liquidations during flash crashes where spot prices temporarily diverge from fundamental value. Only a designated Loss Liquidator role can execute these liquidations.

⚠️ **Bad debt risk:** If collateral experiences a sudden, sustained decline that exceeds the liquidation buffer (the gap between liquidation threshold and 100% collateralization), bad debt is absorbed by the pool. The dToken exchange rate may decrease, resulting in a loss of principal for depositors. No external insurance fund exists at the protocol level.

⚠️ **Smart contract risk:** All pools and Credit Accounts are smart contracts. Despite audits, undiscovered vulnerabilities could result in partial or total loss of deposited capital.

---

## Governance Protections

### Market Curators

Each market is operated by a Risk Curator who controls risk parameters: liquidation thresholds (LTs), collateral whitelists, debt ceilings, and interest rate model configuration. The curator creates markets via `MarketConfigurator.createMarket()` and manages ongoing parameter adjustments.

### Timelock Constraints

Critical parameter changes — including LT modifications that could affect existing depositor risk profiles — are subject to a mandatory timelock. This window allows depositors to evaluate changes and withdraw capital before new parameters take effect.

### Instance Owner

A chain-specific multisig (Instance Owner) serves as the technical gatekeeper for the Price Feed Store, managing oracle integrity independently of Market Curators. This separation of concerns ensures no single party controls both risk parameters and price inputs.

### Emergency Controls

- **Pause capability:** Administrators can pause individual CreditManagers during emergency scenarios, halting new borrowing while allowing liquidations to proceed
- **Emergency Liquidator:** A designated role that can execute liquidations even when the CreditFacade is paused, ensuring solvency enforcement continues during system emergencies

---

## Decision Paths

| Next Question | Reference |
|---|---|
| How does the interest rate model work in detail? | [Interest Rate Model](../economics-and-risk/interest-rate-model.md) |
| What are the specific liquidation parameters? | [Liquidation Dynamics](../economics-and-risk/liquidation-dynamics.md) |
| How do price oracles function and fail? | [Price Oracle](../economics-and-risk/price-oracle.md) / [Smart Oracles](../economics-and-risk/smart-oracles.md) |
| What is a Market Curator's role and authority? | [Market Curators](../governance-and-operations/market-curators.md) |
| How are per-asset exposure limits enforced? | [Quota Controls](../economics-and-risk/quota-controls.md) |
| What does the borrower experience look like? | [For Borrowers & Farmers](./for-borrowers-farmers.md) |
