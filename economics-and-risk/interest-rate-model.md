# Interest Rate Model

Borrowing rates in Gearbox are determined algorithmically by pool utilization. The Interest Rate Model (IRM) uses a two-kink piecewise linear curve that keeps rates stable under normal conditions, spikes them during liquidity stress, and reserves a withdrawal buffer for lenders — enabling partners to predict rate behavior and communicate it to end users.

## How Rates Move with Utilization

The IRM defines three zones using two utilization thresholds (U₁ and U₂):

**Growth Zone (0% to U₁)** — Rates rise slowly. This is the ramp-up range where borrowing demand is below equilibrium. Borrowers face low, predictable costs.

**Optimal Zone (U₁ to U₂)** — Rates stabilize. The pool targets this operating range. Lenders earn competitive yield; borrowers face moderate, steady costs. Most normal market activity occurs here.

**Liquidity Crunch Zone (above U₂)** — Rates spike sharply. When utilization breaches U₂, the cost of capital exceeds market returns, compelling borrowers to close positions and freeing liquidity for lender withdrawals.

### Rate Formula

Partners modeling rate scenarios can use the following piecewise function:

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

- **U** — Current Utilization Rate (Total Debt / Total Assets)
- **R_base** — Minimum starting rate (y-intercept)
- **R_slope1, R_slope2, R_slope3** — Rate of change within each zone

An interactive visualizer is available at [Desmos IRM Calculator](https://www.desmos.com/calculator/d281eeb4a9).

## Can Lenders Always Withdraw?

When `isBorrowingMoreU2Forbidden` is enabled, new borrowing is blocked once utilization reaches U₂. Any transaction attempting to increase debt beyond U₂ reverts.

The liquidity between U₂ and 100% is reserved exclusively for lender withdrawals. Even at peak demand, a buffer of liquid assets remains in the pool.

**Implication for partners:** Lenders integrated through a partner product can exit positions without waiting for borrower repayments, up to the size of the reserved buffer. This is a structural guarantee, not a soft incentive.

## What Borrowers Actually Pay

The base rate from utilization is only one component of total borrowing cost.

$$
Rate_{\text{Borrower}} = (Rate_{\text{Base}} + Rate_{\text{Collateral-specific}}) \times (1 + Fee_{\text{Interest}})
$$

- **Base Rate** — Determined by pool utilization (the IRM curve above)
- **Collateral-specific Rate (Quota Rate)** — A risk premium tied to the specific collateral held (e.g., 0% for WETH, 5% for volatile tokens)
- **Interest Fee** — An additive markup that does NOT reduce lender yield

**Example:** At a 5% base rate with a 20% interest fee: lenders earn 5%, borrowers pay 6%. The fee is extracted from the borrower, not from lender returns.

**Implication for partners:** Lender yield equals base rate plus quota rate. Borrower cost equals that amount plus the fee markup. The fee structure is transparent and non-extractive from the lender side.

---

**Related pages:**

- [Collateral Limits & Specific Rates](quota-controls.md) — How quota rates and concentration limits work
- [Business Model](business-model.md) — How interest fees are split between curators and DAO
