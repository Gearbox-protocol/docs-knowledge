# Dual-Oracle System

Two independent price feeds per asset create automatic circuit breakers against oracle manipulation and de-peg events. Manipulation of a single feed cannot drain the protocol. No global pause is required — circuit breaking is per-asset and per-transaction.

## Two Feeds, Two Purposes

Every collateral asset is configured with two independent price feeds. The protocol applies distinct logic depending on the transaction context:

### Main Feed (Solvency & Liquidation)

- Determines the Health Factor for liquidation triggers
- Serves as the authoritative source for internal accounting
- Typically configured as a **fundamental feed** (exchange rate, backing value)
- Liquidations proceed on the Main Feed even if the Reserve Feed is broken

### Reserve Feed (User Operations)

- Validates solvency during collateral withdrawals, debt increases, and multicall executions
- Acts as a sanity check against the Main Feed
- Typically configured as a **market feed** (Chainlink, Redstone, Pyth)

## The Safe Price: Automatic Circuit Breaker

When a Credit Account executes any operation that reduces its collateralization, the protocol calculates value using the **Safe Price**:

$$
P_{\text{Safe}} = \min(P_{\text{Main}},\ P_{\text{Reserve}})
$$

The `min()` logic enforces the lower (more pessimistic) valuation for all user operations. If the Main Feed and Reserve Feed diverge, the protocol automatically restricts activity without human intervention or global pauses.

## Scenario Analysis

The following table illustrates outcomes for a collateral token (e.g., sUSDe, deUSD) borrowing against a stablecoin (USDC), with Main Feed = Fundamental and Reserve Feed = Market:

| Scenario | Dual-Oracle System | Fundamental Feed Only | Market Feed Only |
|----------|-------------------|----------------------|-----------------|
| **Market drops >2.5%** (normal volatility) | ✅ No liquidations — Main Feed stable | ✅ No liquidations | ⚠️ Liquidations triggered |
| **Market drops >10%** (de-peg) | ✅ Withdrawals blocked — Safe Price uses lower market price ($0.90). Cannot borrow against fundamental at $1.00 while market is at $0.90 | 🚨 Attack vector: buy asset at $0.90, borrow $0.915 at face value. Protocol drained. | 🚨 Mass liquidations, potential price cascade |
| **Market pumps >2.5%** (normal volatility) | ✅ No liquidations | ✅ No liquidations | ✅ No liquidations |
| **Market pumps >10%** (manipulation) | ✅ Borrowing blocked — Safe Price uses lower fundamental ($1.00). Cannot borrow at inflated $1.10 | ✅ No liquidations | 🚨 Attack vector: pump market to $1.10, borrow $1.02 at inflated value. Protocol drained. |

**Key outcome:** The Dual-Oracle System prevents attack vectors that both fundamental-only and market-only oracles are individually vulnerable to.

## Divergence Handling

### Small Divergence

Absorbed naturally by the `min()` logic. Capital efficiency is slightly reduced (borrowing power constrained by the lower price), but no operations are blocked.

### Large Divergence

Effectively freezes new borrowing and withdrawals for the affected asset until feeds converge or the Instance Owner updates the configuration. Liquidations continue to proceed on the Main Feed to maintain pool solvency.

### Feed Failure

If the Main Feed is accurate but the Reserve Feed is broken or stale:

- **Liquidations** — Proceed normally (rely on Main Feed only)
- **User withdrawals** — Blocked (require Reserve Feed validation)

This asymmetry ensures the protocol stays solvent (liquidations always work) while preventing capital extraction during data integrity failures.

---

**Related pages:**

- [Loss Policy](loss-policy.md) — How the protocol handles liquidations that would create bad debt
- [Price Oracle](price-oracle.md) — Feed types, normalization, and staleness enforcement
- [Smart Oracles Overview](smart-oracles.md) — Architecture overview of the oracle safety system
