# Interest Rate Model

The Interest Rate Model (IRM) functions as the protocol's algorithmic central bank. Its primary objective is to balance **capital efficiency** (maximizing yield for lenders) with **liquidity availability** (ensuring lenders can withdraw assets).

It achieves this by dynamically adjusting the Base Borrow Rate based on the **Utilization Rate** of the Liquidity Pool.

### The Utilization Curve

The cost of borrowing is a function of demand. As the pool becomes more utilized (more funds borrowed), the interest rate rises to incentivize repayments and attract new deposits.

Gearbox employs a **Two-Kink Piecewise Linear Model**. This design creates a specific "Optimal Zone" where rates remain stable, preventing volatility during normal market activity while aggressively penalizing over-utilization.

#### Mathematical Structure

The curve is defined by two utilization thresholds (Kinks), denoted as U\_1 and U\_2, creating three distinct slope zones:

1. **Growth Zone (0% to U\_1):**
   * **Behavior:** Rates increase slowly.
   * **Intent:** Incentivize early borrowing and ramp up utilization to efficient levels.
2. **Optimal Zone (U\_1 to U\_2):**
   * **Behavior:** Rates remain relatively stable or rise moderately.
   * **Intent:** Create a predictable cost of capital for borrowers while ensuring sufficient yield for lenders. This is the target operating range of the pool.
3. **Liquidity Crunch Zone (> U\_2):**
   * **Behavior:** Rates spike exponentially (High Slope).
   * **Intent:** Force immediate deleveraging. When utilization breaches U\_2, the cost of capital exceeds market returns, compelling borrowers to close positions and restoring liquidity for lender withdrawals.

#### Formula

The Borrow Rate R(U) is calculated as:

$$
R(U)=
\begin{cases}
R_{\text{base}} + \dfrac{U}{U_1} R_{\text{slope1}},
& U \le U_1 \\[6pt]

R_{\text{base}} + R_{\text{slope1}}
+ \dfrac{U - U_1}{U_2 - U_1} R_{\text{slope2}},
& U_1 < U \le U_2 \\[6pt]

R_{\text{base}} + R_{\text{slope1}} + R_{\text{slope2}}
+ \dfrac{U - U_2}{1 - U_2} R_{\text{slope3}},
& U > U_2
\end{cases}
$$



Where:

* U: Current Utilization Rate (Total Debt / Total Assets).
* R\_base: The minimum starting rate (y-intercept).
* R\_slope: The rate of change in each zone.

_**Reference:**_

* [Desmos IRM visualizer](https://www.desmos.com/calculator/d281eeb4a9)

### Liquidity Reservation

A critical feature of the Gearbox IRM is the enforcement of **Exit Liquidity**.

In standard lending protocols, 100% utilization means lenders cannot withdraw their funds until a borrower repays. Gearbox mitigates this risk through **Liquidity Reservation**.

#### The Reservation Cap

Curators can configure the market to strictly forbid new borrowing once utilization reaches U\_2.

* **Mechanism:** If `isBorrowingMoreU2Forbidden` is enabled, any transaction attempting to increase debt beyond the U\_2 threshold will revert.
* **Result:** The remaining liquidity (from U\_2 to 100%) is effectively reserved for lender withdrawals. Even in periods of peak demand, a buffer of liquid assets remains available in the pool.

### Total Cost of Capital

The Interest Rate Model determines the **Base Rate** of the pool. The final cost to a borrower includes additional collateral-specific rate.

#### Learn More

* **Asset-specific risk premiums:** Borrowers holding specific collateral assets may incur an additional Quota Rate on top of the base rate.
  * [quota-controls.md](quota-controls.md "mention")
* **Protocol fees:** A portion of the interest paid is captured as revenue for the Protocol DAO and the Market Curator.
  * [dao-and-curators-business-model.md](dao-and-curators-business-model.md "mention")
