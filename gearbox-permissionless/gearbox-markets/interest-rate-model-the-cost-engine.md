# Interest Rate Model (The Cost Engine)

The Interest Rate Model (IRM) is the algorithmic engine that manages the cost of borrowing. It acts as the market's central bank, automatically adjusting interest rates based on the real-time supply and demand for liquidity.

Core Functions

* Dynamic Pricing: It continuously updates the borrow APR based on the utilization rate (Total Debt / Total Assets). As demand rises, the cost of capital increases to incentivize repayments and attract new deposits.
* Liquidity Reservation: Uniquely, Gearbox V3 uses a Two-Point Linear Model ($$U_1$$ and $$U_2$$) to create a "buffer zone". This intermediate slope prevents massive interest rate spikes during large withdrawals, stabilizing the APY.
* Exit Liquidity Enforcement: It can enforce a strict borrowing limit (at the $$U_2$$ threshold). If enabled, the protocol effectively reserves the remaining liquidity (e.g., the last 10%) exclusively for lender withdrawals, preventing a "bank run" scenario.

Curator Controls

*   Kink Points ($$U_1$$, $$U_2$$):

    Defines the "optimal" utilization range. Curators typically set these to target a specific efficiency level (e.g., 80-90%). The area between $$U_1$$ and $$U_2$$ acts as a stable buffer where rates don't fluctuate wildly.
*   Rate Slopes ($$R_{base}$$, $$R_{slope1}$$, $$R_{slope2}$$, $$R_{slope3}$$):

    Sets the price of money at different utilization levels.

    * Base: The minimum rate at 0% utilization.
    * Slopes: How fast rates rise. Curators set the final slope ($$R_{slope3}$$) extremely high to penalize utilizing 100% of the pool, which forces debt repayments to keep LP withdrawals allowed.
*   Liquidity Reservation Cap (isBorrowingMoreU2Forbidden):

    A safety toggle. If set to true, borrowing is completely disabled once utilization hits the $$U_2$$            threshold. This ensures there is always exit liquidity available for lenders, even during periods of peak demand.
