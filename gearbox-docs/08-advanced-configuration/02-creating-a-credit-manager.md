[Copy]

:

:

##

Name can reflect the properties of collaterals and position size:

-
:

-
:

-
:

Simple notation is calling naming it with tiers: Tier 1; Tier 2; Tier 3 Higher tier means larger positions and safer collaterals.

2

##

\% of borrowing interest taken by DAO and Curator Default fee split is 50/50 between DAO and Curator

Interest fee of a Credit Manager ***can't be changed*** after it's deployed.

Curator\'s fee is added ***on top of interest paid*** by borrower. If the IRM + [collateral-specific rate](https://docs.gearbox.fi/gearbox-permissionless-doc/competitive-advantages/collateral-specific-rates) is 5% and the fee is 20% of the interest, then borrowers pay 6%.

Interest fee & Credit Manager\'s debt limit can be used to ***bootstrap Market utilization.***

e.g. Create Credit Manager with limit of 5,000,000 USD and Interest Fee of 0% can be created to incentivize first borrowers as they will get more favorable borrow rates.
##

-
:

Liquidation premium & fee of a credit manager can't be modified after it's deployed.
-
:

It's not recommended to set liquidation fee to be lower than 0.01%. If the fee is set to 0, then account that fully consists of leveraged underlying token will create bad debt upon liquidation.
Borrower loses Liquidation Premium + Liquidation Fee from liquidation collateral.

Expired liquidation premium and fee are useful only if Credit Manager is expirable, which is a rare case, so you can freely omit that parameters. If set, \"Expired\" versions of liquidation premium and fee are applied after Credit Manager expiration.

4

##

-
:

-
:

**maxDebt/minDebt \*+*]:mt-5 .-mt-9}
##

**Whitelist** - Allow borrowing only to owners of particular NFT.

**Expiration** - Credit Manager can be shut down following specified schedule. May be useful for time-sensitive types of collaterals.

6

##

Maximal sum debt on all credit accounts created in this Credit Manager.

Interest fee & Credit Manager\'s debt limit can be used to ***bootstrap Market utilization.***

e.g. Create Credit Manager with limit of 5,000,000 USD and Interest Fee of 0% can be created to incentivize first borrowers as they will get more favorable borrow rates.
: