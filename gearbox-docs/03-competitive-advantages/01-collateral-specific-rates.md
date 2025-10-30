[Copy]

:

[](#problem)

Problem
:

**Underpricing of High-Demand Loans in multicollateral pools** Loans against collaterals with low supply caps minimally affect the pool\'s overall utilization rate
:

**Underpayment of Lenders and Curators** Lenders and curators receive lower returns, effectively subsidizing borrowers who secure loans against these constrained collaterals
:

**Curators are involved in high-frequency capital reallocation** As of 06/06/2025 just a single \"MEVCapital USDC\" Morpho vault had executed 3595 reallocation transactions operations since its deployment date of 07/24/2024 ([source](https://dune.com/queries/5244280)).

[](#solution)

Solution
:

***Rate discovery efficiency*** of isolated market designs (e.g., Morpho, Silo) Rates in different markets are set independently for different collaterals
:

**User experience and capital efficiency** of multicollateral designs (e.g., Aave, Euler) Curators don\'t need to participate in capital allocation process
:

**Rate Adjustment Frequency**: Curators can update rates for each collateral no more frequently than once every 24 hours and can self-enforce longer intervals if desired.

[](#how-does-it-work-in-practice)

How does it work in practice?
:

Utilization borrow rate induced by IRM \~ 5%
:

Curator sets 3% additional borrow rate for high-yield collateral like RLP ⇒ Users borrowing against it pay \~8%
:

Curator sets minimal additional rate 0.01% to sUSDe ⇒ Users borrowing against it pay \~5%