# Collateral-specific rates

## One IRM - capital inefficient; Many IRMs - ops-heavy

Multicollateral lending protocols like Aave and Euler use a single interest rate curve to determine borrow rates for all collaterals, despite varying demand for each collateral type. This leads to issues, particularly when the supply cap for a specific collateral is low compared to lending-side TVL in the pool:

* **Underpricing of High-Demand Loans in multicollateral pools**\
  Loans against collaterals with low supply caps minimally affect the pool's overall utilization rate
* **Underpayment of Lenders and Curators**\
  Lenders and curators receive lower returns, effectively subsidizing borrowers who secure loans against these constrained collaterals
* **Curators are involved in high-frequency capital reallocation**\
  As of 06/06/2025 just a single "MEVCapital USDC" Morpho vault had executed 3595 reallocation transactions operations since its deployment date of 07/24/2024 ([source](https://dune.com/queries/5244280)).

{% hint style="info" %}
**Reducing compliance overhead:** By eliminating the need for manual liquidity management, Curators can avoid activities that in many jurisdictions could be classified as financial intermediation (managing liquidity directly).
{% endhint %}

## Improving capital-efficiency, streamlining operations

Curator controls individual rates for collaterals to better adjust to their demand and supply dynamics. —

* _**Rate discovery efficiency**_ of isolated market designs (e.g., Morpho, Silo)\
  Rates in different markets are set independently for different collaterals
* **User experience and capital efficiency** of multicollateral designs (e.g., Aave, Euler)\
  Curators don't need to participate in capital allocation process
* **Rate Adjustment Frequency**: Curators can update rates for each collateral no more frequently than once every 24 hours and can self-enforce longer intervals if desired.

This approach combines _**efficiency of rate discovery**_ of the isolated markets design (e.g. Morpho, Silo) and _**UX and capital efficiency**_ of multicollateral design (e.g. Aave, Euler).

## How does it work in practice?

Each Collateral in Gearbox can have its own additional rate.

**Example:**

* Utilization borrow rate defined by IRM \~ 5%
* Curator sets 3% additional borrow rate for high-yield collateral like RLP ⇒ Users borrowing against it pay \~8%
* Curator sets minimal additional rate to sUSDe ⇒ Users borrowing against it pay \~5%
