# For Borrowers & Farmers

Gearbox Credit Accounts provide leveraged exposure to whitelisted DeFi strategies. Borrowed capital remains inside an isolated smart contract — the borrower directs it through pre-approved operations but cannot extract it. This page addresses position capacity, cost of carry, liquidation mechanics, parameter risk, and exit reliability: the information required to model a leveraged position or build an integration.

---

## Position Capacity and Eligibility

### Capacity Constraints

Position size is bounded by two independent limits:

1. **Pool liquidity** — the underlying capital available for borrowing (`PoolV3.availableLiquidity()`). Large positions may partially drain available liquidity, increasing utilization and raising the cost of carry for all active borrowers.

2. **Debt ceilings** — each CreditManager has a per-market debt limit (`setCreditManagerDebtLimit()`), and per-token exposure limits are enforced by the PoolQuotaKeeperV3 (`setTokenLimit()`). Even if pool liquidity is sufficient, exposure to a specific collateral asset or borrowing market may be fully allocated.

### Collateral Eligibility

Each CreditManager enforces a strict collateral allowlist. Only explicitly whitelisted tokens can be held within a Credit Account. Tokens not on the allowlist cannot be received, and attempting to interact with non-whitelisted protocols or assets will revert. The allowlist is maintained by the Market Curator.

### Interaction Model

All borrower operations flow through CreditFacadeV3 as batched MultiCall arrays:

- `openCreditAccount()` — opens a new Credit Account and executes initial actions (deposits, swaps) in a single transaction
- `multicall()` — executes a batch of operations on an existing account
- `closeCreditAccount()` — repays debt and returns remaining collateral

Borrowers never interact with the Credit Account contract directly. Permitted DeFi operations (swaps, LP deposits, staking) are executed through Adapters — pre-audited contract wrappers that translate standard protocol calls into Credit Account-compatible operations.

---

## Cost of Carry

The total borrowing cost comprises three additive components:

| Component | Mechanism | Behavior |
|---|---|---|
| **Base interest rate** | Determined by pool utilization via LinearInterestRateModelV3 | Variable. Increases with utilization; scales steeply above U_optimal |
| **Quota rate premium** | Per-asset rate set by RateKeeper/Gauge on quoted tokens | Variable per asset. Higher for illiquid or volatile collateral |
| **Interest fee** | Fixed percentage markup captured by Curator + DAO treasury | Additive to borrower cost; does not accrue to LPs |

**Total borrower rate = Base rate + Quota rate + Interest fee**

### Rate Dynamics

The base rate is purely utilization-driven. When large LP withdrawals spike utilization, the base rate increases immediately — potentially within a single block. A borrower holding a position through a utilization spike absorbs the increased cost from the moment it occurs, compounding into total debt.

Quota rates apply only to quoted tokens (checked via `isQuotedToken()`). Non-quoted collateral carries no quota premium. The quota rate can change via governance action by the RateKeeper or Gauge mechanism.

⚠️ **Rate risk:** Borrowing costs are entirely variable. A sudden utilization spike (from LP withdrawals or competing borrowing demand) can increase the effective rate by an order of magnitude. There is no rate cap. Sustained high rates erode the Health Factor through debt accumulation, potentially triggering liquidation even without collateral price movement.

---

## Liquidation Rules

### Trigger Conditions

A Credit Account becomes liquidatable when the Health Factor drops below 1.0:

> **HF = TWV / Total Debt**

Where:
- **TWV** = Σ(Balance_i × Price_i × LT_i) for all enabled collateral tokens
- **Total Debt** = Principal + Base Interest + Quota Interest + Fees

Three independent vectors can cause HF to breach 1.0:

1. **Collateral depreciation** — price decline in held assets reduces TWV
2. **Debt asset appreciation** — if borrowing a non-stablecoin asset, debt value increases in USD terms
3. **Interest accrual** — accumulated borrowing costs increase Total Debt over time, even when collateral prices are stable

### Liquidation Execution

Liquidation is permissionless. Any address can call `liquidateCreditAccount()` on an unhealthy account. The liquidator repays the pool's debt, receives the account's collateral at a discount (the liquidation premium = 1 - liquidation discount), and the protocol treasury takes a liquidation fee.

**Partial liquidation** is available via `partiallyLiquidateCreditAccount()`. The liquidator repays a specified debt amount and receives a proportional amount of a specific collateral token at a discount, plus a fee to the treasury. Partial liquidation restores solvency without fully closing the position.

### Consequence for the Borrower

Upon full liquidation, the borrower forfeits the liquidation premium and fee. Any remaining value after debt repayment, premium, and fee is returned to the borrower. If collateral is insufficient to cover debt (bad debt scenario), the borrower loses the entire position and the pool absorbs the shortfall.

Upon partial liquidation, the borrower retains the position but at a reduced collateral level. The remaining position must maintain HF ≥ 1.0 after the partial liquidation.

### Expired Account Liquidation

CreditManagers may enforce expiration dates. After expiry, accounts are liquidatable regardless of Health Factor. Expired account liquidations carry separate (typically lower) discount and fee parameters compared to undercollateralized liquidations.

⚠️ **Liquidation timing risk:** Liquidation depends on third-party actors monitoring positions and executing transactions. In periods of extreme network congestion or gas price spikes, liquidation may be delayed. The Emergency Liquidator role can execute liquidations even when the CreditFacade is paused, but standard liquidation has no guaranteed execution latency.

---

## Parameter Risk

Market Curators control risk parameters that directly affect open positions:

### Modifiable Parameters

| Parameter | Impact on Borrowers | Protection |
|---|---|---|
| Liquidation thresholds (LTs) | Lowering an LT reduces TWV, potentially triggering liquidation | Subject to mandatory timelock |
| Collateral allowlist | Forbidding a token prevents increasing exposure to that asset | Existing balances remain but cannot be added to |
| Adapter whitelist | Removing an adapter blocks that protocol interaction | Existing positions in that protocol remain |
| Debt ceilings | Reducing a ceiling may prevent opening new positions | Does not force-close existing positions |
| Interest rate model | Replacing the IRM changes the cost of carry | Old model deauthorized, new model authorized |

### Circuit Breakers

Two automated mechanisms can halt operations:

1. **Oracle deviation protection:** When the primary and reserve price feeds for a token diverge significantly, sensitive operations (including new borrows) are blocked. This prevents position manipulation during oracle instability.

2. **Administrative pause:** Curators and administrators can pause individual CreditManagers. During a pause, new borrows and multicalls are blocked. Liquidations continue — and the Emergency Liquidator role can operate even during a pause.

⚠️ **Governance risk:** Parameter changes are subject to timelock, but the timelock provides a finite window. Borrowers must monitor parameter change proposals and adjust positions before new parameters take effect. A reduction in LT that is not anticipated can convert a healthy position into a liquidatable one.

---

## Exit Reliability

### Standard Close

Calling `closeCreditAccount()` with appropriate MultiCall instructions executes debt repayment and collateral return atomically. If the collateral held differs from the debt asset, the MultiCall must include swap instructions to convert collateral into the debt token.

**External DEX dependency:** Atomic close relies on external DEX liquidity (Uniswap, Curve, or other approved adapters) to execute collateral-to-debt swaps. Thin liquidity or high slippage on the required trading pair can cause the close transaction to revert.

### Manual Unwind

If atomic close fails (due to DEX liquidity, slippage, or gas constraints), the borrower must unwind manually:

1. Execute individual swaps within the Credit Account via `multicall()` to convert collateral to the debt asset
2. Repay debt
3. Close the account and withdraw remaining assets

Each step is subject to solvency checks — the Health Factor must remain ≥ 1.0 throughout the unwind sequence.

### Bot-Assisted Operations

Authorized bots can execute operations on a Credit Account via `botMulticall()` within predefined safety constraints. This enables automated deleveraging, stop-loss execution, or position rebalancing without manual intervention. Bot permissions are granted per-account by the borrower.

⚠️ **Exit risk under stress:** During market crashes, multiple conditions compound: collateral values decline (reducing HF), DEX liquidity thins (increasing slippage on close), and network congestion rises (increasing gas costs and transaction failure rates). A position that is healthy in normal conditions may become both difficult to close and approaching liquidation simultaneously. Maintaining a Health Factor buffer well above 1.0 is the primary mitigation.

---

## Decision Paths

| Next Question | Reference |
|---|---|
| How does the Health Factor calculation work in detail? | [Liquidation Dynamics](../economics-and-risk/liquidation-dynamics.md) |
| What are the current interest rate model parameters? | [Interest Rate Model](../economics-and-risk/interest-rate-model.md) |
| Which assets and protocols are whitelisted? | [Credit Suite](../core-architecture/credit-suite.md) / [Adapters & Integrations](../core-architecture/adapters-integrations.md) |
| How do price feeds work and what are failure modes? | [Price Oracle](../economics-and-risk/price-oracle.md) / [Smart Oracles](../economics-and-risk/smart-oracles.md) |
| What are quota limits and how are quota rates set? | [Quota Controls](../economics-and-risk/quota-controls.md) |
| What does the lender/LP experience look like? | [For Lenders & LPs](./for-lenders-lps.md) |
