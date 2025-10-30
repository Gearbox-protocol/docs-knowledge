[Copy]

:

:
The video showcasing the process of setting up an example market, just to know what to prepare for.

:

iframe
:

:

###

Select from verified code versions (currently only v3.1)

2

###

Underlying (borrowable) token and Price Feed to use for it. Select from PriceFeed Store.

More info about Price Feed store and feeds configuration can be found [here](https://docs.gearbox.fi/gearbox-permissionless-doc/step-by-step-guides/adding-required-price-feeds).

For correlated Collateral/ Debt usecases it may be worth it to set an upper bound for Underlying Asset price feed to protect borrowers against unwanted liquidations.
###

Should usually include the symbol of underlying token and one-word description.

###

Max amount of underlying token that can be borrowed from entire pool.

Usually can be set to arbitrary high value (if you don\'t have special plan for it), because position-specific and token-specific limits will be granurarly configured further.

###

-
:

-
:

:

U1 - first curve kink
:

U2 - second curve kink
:

R_base - utilization rate at U = 0%
:

R_slope1 - utilization rate at U = U1
:

R_slope2 - utilization rate at U = U2
:

R_slope3 - utilization rate at U = 100%
:

If **isBorrowingMoreU2Forbidden** is true, borrowing is disabled when utilization is \> U2.

Setting IRM in a way that **borrow rate at target utilization (\~80-85%)** equals **60-70% of expected collateral yield** will allow you to bootstrap utilization and then find equlibrium rate using collateral-specific rates.

Curator\'s fee is added on top of interest paid by borrower. If the IRM + [collateral-specific rate](https://docs.gearbox.fi/gearbox-permissionless-doc/competitive-advantages/collateral-specific-rates) is 5% and the fee is 20% of the interest, then borrowers pay 6%.
-
:

:

[Desmos IRM visualizer](https://www.desmos.com/calculator/d281eeb4a9)
:

[Mainnet ETH pool](https://app.gearbox.fi/pools/0xda0002859b2d05f66a753d8241fcde8623f26f4f/utilization)
:

[Mainnet USDC pool](https://app.gearbox.fi/pools/0xda00000035fef4082f78def6a8903bee419fbf8e)

###

Determine how collateral-specific borrow rates are set.

-
:

:

**Tumbler** ***(Recommended option)*** Risk curator can manually set *token-specific rate*.
:

**Gauge** ***(Legacy option)*** Risk curator sets minRate and maxRate for each collateral. Then users can vote UP or DOWN with their staked \$GEAR to increase or decrease quota rate.

Curator\'s fee is added on top of interest paid by borrower. If the IRM + [collateral-specific rate](https://docs.gearbox.fi/gearbox-permissionless-doc/competitive-advantages/collateral-specific-rates) is 5% and the fee is 20% of the interest, then borrowers pay 6%.
-
:

*Example:* Epoch = 2 days. Curator decides to update rates on Monday 10:00 ⇒ Next update can happen no earlier than on Wednesday 10:00
###

**(Advanced feature, explanation and examples are WIP. Feel free to skip for now)**: Additional logic applied during CA liquidation if it results in creation of Bad Debt. ***Aliased*** policy reprices collateral tokens with aliased feeds (set separately). ***Example**: Main oracle for USDe can be set to Market Chainlink price while Aliased feed set to Proof Of Reserves feed. It means that in the scenario when USDe depegs but reserves are safe according to Proof Of Reserves feed, accounts will be liquidated until it can be done without creating Bad Debt.*

: