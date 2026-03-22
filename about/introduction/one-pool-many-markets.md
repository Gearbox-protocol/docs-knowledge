# One Pool, Many Markets

Gearbox separates the source of liquidity from its utilization. A single passive Pool funds multiple isolated lending strategies simultaneously — lenders earn diversified yield while risk stays compartmentalized per strategy.

This page explains the capital flow model, the mechanism that contains risk, and the lender's experience.

---

## Why Separation of Liquidity and Strategy Matters

In monolithic lending protocols, a single exploited asset or failed strategy can drain the entire pool. Gearbox eliminates this structural vulnerability through architectural separation.

The capital flow works on a two-tier model:

**The Pool (Wholesale Bank)** holds all passive capital — a single underlying asset such as USDC or WETH. The Pool accepts deposits from lenders and issues yield-bearing tokens. It never lends directly to end-users.

**Credit Suites (Retail Branches)** borrow from the Pool and each operates a distinct lending strategy with its own risk rules. One Credit Suite might serve a low-risk stablecoin farming strategy; another might support high-leverage ETH staking. Each defines its own allowed collateral, Liquidation Thresholds, and borrowing limits.

This separation means an operator can offer high-risk and low-risk products side-by-side, drawing from the same liquidity base, without fragmenting capital across isolated pools.

---

## How Risk Stays Contained

Risk isolation is enforced through **Debt Ceilings**. The Pool assigns each connected Credit Suite a maximum borrowing capacity — the hard cap on how much capital that strategy can draw.

### Worked Example

A Pool holds $100M USDC with two connected Credit Suites:

| Credit Suite | Strategy | Debt Ceiling | Max Loss to Pool |
|---|---|---|---|
| Suite A | Blue-chip yield (low risk) | $80M | $80M |
| Suite B | Emerging asset exposure (high risk) | $10M | $10M |

If Suite B suffers a catastrophic failure — a collateral collapse, a liquidation cascade, an oracle exploit — the maximum loss to the Pool is $10M. The remaining $90M is mathematically isolated from that risk vector.

The remaining $10M of the Pool's capacity is unallocated, available for new strategies or as a liquidity buffer.

### What This Means for Capital Allocators

- **Lenders** are protected from tail risks of aggressive strategies while still earning yield from the utilization those strategies generate.
- **Market operators** can experiment with novel collateral types or higher-leverage products without jeopardizing the Pool's core capital.
- **Risk is bounded and transparent.** Every Debt Ceiling is an on-chain parameter, publicly visible and verifiable.

---

## What Lenders Experience

The lender's interaction with Gearbox is deliberately simple.

**Deposit:** The lender deposits the underlying asset (e.g., USDC) into the Pool and receives **Diesel Tokens** (dUSDC, dWETH) — a pro-rata share of the Pool's total assets.

**Yield:** Diesel Token value appreciates over time. Yield is aggregated from interest paid by all connected Credit Suites. Whether the capital is deployed for staking, farming, or trading, interest flows back to the Pool and accrues to the Diesel Token exchange rate.

**No market selection required.** The lender does not evaluate individual strategies, choose which Credit Suite to fund, or monitor per-market risk. Capital is deployed once; returns are blended across the entire basket of on-chain credit strategies connected to that Pool.

This is the core value proposition for passive capital: a single deposit point with diversified, utilization-driven yield.

---

## Learn More

- **How does the Pool technically handle deposits and share pricing?** → [Core Architecture: Pool](../core-architecture/pool.md)
- **How are strategy rules defined for each branch?** → [Core Architecture: Credit Suite](../core-architecture/credit-suite.md)
- **What is the primitive that borrowers interact with?** → [Credit Accounts](credit-accounts.md)
