# Liquidation Process

When a Credit Account's risk-adjusted collateral value falls below its total debt, the protocol enforces liquidation to protect liquidity providers. The process is deterministic, on-chain, and permissionless — anyone can execute a liquidation. This page covers the full sequence from healthy position to liquidation, what each party gains and loses, and how bad debt is handled.

## When Is a Position Liquidatable?

The core solvency metric is the **Health Factor (HF)**:

$$
HF = \frac{TWV}{Total\ Debt}
$$

Where **Total Weighted Value (TWV)** is the risk-adjusted, quota-limited value of all collateral:

$$
TWV = \frac{\sum_{i}^{} \min(Quota_i,\ Balance_i \times Price_i \times LT_i)}{Price_{\text{underlying}}}
$$

- **Quota_i** — Maximum debt that can be backed by token i
- **Balance_i** — Quantity of token i in the Credit Account
- **Price_i** — Current oracle price of token i
- **LT_i** — Liquidation Threshold for token i (a discount factor reflecting asset risk)
- **Price_underlying** — Oracle price of the borrowed asset

The `min()` function ensures that no single collateral asset can secure more debt than its allocated quota, regardless of its market value.

An account is liquidatable when:

1. **HF < 1** — Total Weighted Value is less than Total Debt
2. **Expiration** — The Credit Manager has reached its configured maturity date

## Partial Liquidation: The First Line of Defense

Before full liquidation, the protocol supports **partial liquidation** (deleverage). Automated bots sell just enough collateral to restore the Health Factor above a target threshold, preserving most of the borrower's position.

- A deleverage bot monitors HF and triggers when it drops below a configured `minHF`
- Only the minimum necessary collateral is sold to bring HF back to `maxHF`
- The bot operator earns a premium (scaled from the full liquidation premium)
- Bot deployment is fully permissionless; no DAO or curator approval required

**Implication for partners:** Most minor market dips result in partial deleverage, not full liquidation. Borrowers retain the majority of their position.

See [Deleverage Bot](deleverage-bot.md) for detailed mechanics and parameter rationale.

## Full Liquidation: The Fallback

If partial liquidation is insufficient or HF drops significantly below 1, full liquidation occurs.

### How It Works

1. The liquidator repays the total debt to the pool
2. The liquidator claims all collateral assets at a discount (the **Liquidation Premium**)
3. A **Liquidation Fee** is paid to the protocol treasury (split between Curator and DAO)

### Economics

$$
\text{Liquidator Profit} = \text{Total Value} \times \text{Liquidation Premium} - \text{Gas Cost}
$$

$$
\text{Borrower Loss} = \min(\text{Total Value} \times (\text{Liquidation Premium} + \text{Liquidation Fee}),\ \text{Total Value} - \text{Total Debt})
$$

| Component | Recipient | Purpose |
|-----------|-----------|---------|
| Liquidation Premium | Liquidator | Execution incentive |
| Liquidation Fee | DAO & Curator | Protocol revenue |

Full liquidation is **permissionless**: anyone can call `liquidateCreditAccount()` on an undercollateralized or expired account. No reliance on a single operator.

**Implication for partners:** Borrowers lose collateral value equal to the premium plus the fee. Partners should communicate these costs so borrowers can set appropriate Health Factor buffers.

## Bad Debt: When Collateral Is Insufficient

Bad debt occurs when an account is liquidated but Total Value < Total Debt. The collateral cannot fully cover the outstanding loan.

### Resolution Order

1. **Fee buffer absorption** — The pool burns LP shares held by the Treasury (unclaimed protocol fees) equal to the deficit. The Treasury "pays" by giving up its claim on pool liquidity. Remaining lender claims are preserved.

2. **Socialization (last resort)** — If the Treasury's LP shares are insufficient, the remaining loss reduces the LP token exchange rate, distributing the deficit among all liquidity providers proportionally.

**Implication for partners:** The insurance fund absorbs bad debt first. LP dilution is the last resort. This is the residual risk that lenders accept by providing capital to the pool.

---

**Related pages:**

- [Deleverage Bot](deleverage-bot.md) — Automated partial liquidation mechanics
- [Price Oracle](price-oracle.md) — How asset prices are determined for TWV calculations
- [Loss Policy](loss-policy.md) — How the protocol prevents unnecessary bad debt during flash crashes
- [Insurance & Solvency Reserves](insurance-and-solvency.md) — How the reserve fund absorbs losses
