# Dual-Oracle System

The Dual-Oracle System is the primary defense layer against price manipulation and oracle failure. By decoupling the valuation source used for liquidations from the source used for user operations, Gearbox ensures that short-term volatility or manipulation in one feed cannot be exploited to drain protocol liquidity.

### Dual-Feed Architecture

Every asset in a Gearbox Market is configured with two independent price feeds. The protocol applies distinct logic to each feed depending on the context of the transaction.

#### 1. Main Feed (Solvency & Liquidation)

The **Main Feed** serves as the authoritative source for the system's internal accounting.

* **Role:** Determines the Health Factor ($H\_f$) for liquidation triggers.
* **Objective:** To reflect the asset's valuation for long-term solvency.

#### 2. Reserve Feed (Safety & Operations)

The **Reserve Feed** acts as a sanity check for user-initiated actions.

* **Role:** Validates solvency during collateral withdrawals, debt increases, or complex multicall executions.
* **Objective:** To prevent users from exploiting temporary price divergences to withdraw more collateral than they are entitled to.

### Pricing Methodologies

To understand the utility of the Dual-Oracle system, one must first distinguish between the two primary methodologies for pricing DeFi assets.

#### 1. Fundamental Price (Hardcoded / Backing Value)

Prices the token based on the reserves that back it or its exchange rate (e.g., `1 stETH = 1 ETH` or `1 Stablecoin = $1`).

| Stakeholder   | Pros                                                                                                                                                                          | Cons                                                                                                                                                                                                                                             |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Borrowers** | <p><strong>Stability:</strong> Minimal risk of liquidation due to temporary market de-pegs.<br><strong>Accuracy:</strong> Reflects true staking appreciation immediately.</p> | —                                                                                                                                                                                                                                                |
| **Lenders**   | **Manipulation Resistance:** Immune to low-liquidity DEX manipulation.                                                                                                        | <p><strong>Insolvency Risk:</strong> May overprice assets during real backing failures.<br><strong>Liquidity Lock:</strong> Funds may become stuck if the market price drops below the fundamental price, removing incentives for repayment.</p> |

#### 2. Secondary Market Price

Prices the token based on buy/sell activity on DEXes or CEXes.

| Stakeholder   | Pros                                                                                                                                                                                              | Cons                                                                                                                                                                                                                             |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Borrowers** | —                                                                                                                                                                                                 | <p><strong>Capital Inefficiency:</strong> Must maintain higher Health Factors to buffer against volatility.<br><strong>Liquidation Risk:</strong> Susceptible to cascading liquidations during market panic.</p>                 |
| **Lenders**   | <p><strong>Pessimistic Pricing:</strong> Liquid tokens usually trade at a discount to backing, providing a safety buffer.<br><strong>Reactivity:</strong> Fast reaction to real market drops.</p> | <p><strong>Manipulation Risk:</strong> Illiquid markets can be pumped to drain pool reserves at inflated valuations.<br><strong>Bad Debt:</strong> Liquidation cascades can lead to overselling collateral below debt value.</p> |

### Comparison Logic: The "Safe Price"

When a Credit Account executes a transaction that reduces its collateralization (e.g., withdrawing funds or borrowing more), the protocol calculates the account's value using the **Safe Price**.

The Safe Price is derived dynamically for every asset in the portfolio:

$$
P_{Safe} = \min(P_{Main}, P_{Reserve})
$$

This `min()` logic creates an automatic circuit breaker. If the Main Feed and Reserve Feed diverge, the protocol enforces the lower (more pessimistic) valuation for all user operations, preventing the extraction of value during de-pegs or manipulation events.

### Scenario Analysis: The "Best of Both Worlds"

By configuring the **Main Feed** as a Fundamental source and the **Reserve Feed** as a Market source, Gearbox protects lenders from manipulation while preserving capital efficiency for borrowers.

The table below illustrates a scenario where a collateral token (e.g., sUSDe or deUSD) is used to borrow a stablecoin (USDC).

| Scenario                                                                                    | Dual-Oracle System                                                                                                                                                                                                                                       | Hardcoded Feed Only                                                                                                                                                                                                              | Market Feed Only                                                                                                                                                                                                                    |
| ------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p><strong>Market price drops > 2.5%</strong><br><em>(Normal Volatility)</em></p>           | <p>✅ <strong>No Liquidations</strong><br>Main feed remains stable.</p>                                                                                                                                                                                   | ✅ **No Liquidations**                                                                                                                                                                                                            | <p>⚠️ <strong>Liquidations Triggered</strong><br>Risky positions are closed due to volatility.</p>                                                                                                                                  |
| <p><strong>Market price drops > 10%</strong><br><em>(De-peg / Panic)</em></p>               | <p>⚠️ <strong>No Liquidations</strong><br><br>✅ <strong>Withdrawals Blocked</strong><br>Safe Price uses the lower Market price ($0.90). Users cannot withdraw the "overvalued" asset, trapping liquidity in the protocol until solvency is resolved.</p> | <p>⚠️ <strong>No Liquidations</strong><br><br>🚨 <strong>Attack Vector:</strong><br>Attacker buys asset at $0.90, borrows $0.915 against it (at Face Value).<br><strong>Result:</strong> Protocol drained; Bad Debt created.</p> | <p>🚨 <strong>Mass Liquidations</strong><br>Major portion of positions liquidated, potentially crashing price further.</p>                                                                                                          |
| <p><strong>Market price pumps > 2.5%</strong><br><em>(Normal Volatility)</em></p>           | ✅ **No Liquidations**                                                                                                                                                                                                                                    | ✅ **No Liquidations**                                                                                                                                                                                                            | ✅ **No Liquidations**                                                                                                                                                                                                               |
| <p><strong>Market price pumps > 10%</strong><br><em>(Illiquid Market Manipulation)</em></p> | <p>✅ <strong>No Liquidations</strong><br><br>✅ <strong>Borrowing Blocked</strong><br>Safe Price uses the lower Fundamental price ($1.00). User cannot borrow against the inflated Market price ($1.10).</p>                                              | ✅ **No Liquidations**                                                                                                                                                                                                            | <p>✅ <strong>No Liquidations</strong><br><br>🚨 <strong>Attack Vector:</strong><br>Attacker mints asset at $1.00, pumps market to $1.10, borrows $1.02.<br><strong>Result:</strong> Protocol drained due to inflated valuation.</p> |

### Circuit Breakers & Interaction Blocking

The Dual-Oracle system enforces logic that effectively forbids interactions when data integrity is compromised.

#### Transaction-Level Blocking

The system does not require a global pause to stop exploits. It blocks individual transactions based on real-time data divergence:

* **Withdrawal Block:** If $P\_{Main} \gg P\_{Reserve}$, the user's borrowing power is constrained by $P\_{Reserve}$. Users cannot withdraw funds based on the inflated Main price.
* **Liquidation Protection:** Liquidations rely solely on the **Main Feed**. If the Main Feed is accurate but the Reserve Feed is broken/manipulated, liquidations can still proceed to keep the pool solvent, while user withdrawals (which require Reserve validation) are temporarily blocked to prevent capital flight.

#### Divergence Thresholds

While the protocol uses the `min()` logic continuously, significant divergence between Main and Reserve feeds serves as an off-chain signal for Risk Curators.

* **Soft Breaker:** Small deviations are absorbed by the `min()` logic, simply reducing capital efficiency slightly.
* **Hard Breaker:** Large deviations typically indicate a de-peg or oracle failure. In these scenarios, the `min()` logic effectively freezes new borrowing and withdrawals for that specific asset until the feeds converge or the Instance Owner updates the configuration.

***

#### Learn More

* **Bad debt handling:** How does the protocol handle bad debt if price safety mechanisms fail?
  * [loss-policy.md](loss-policy.md "mention")
* **Price feed sources:** Where do the raw Main and Reserve price feeds originate?
  * [.](./ "mention")
