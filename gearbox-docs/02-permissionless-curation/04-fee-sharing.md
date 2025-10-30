:

# Fee sharing
:
##

-
:

-
:

------------------------------------------------------------------------

##

Both Interest Fee and Liquidation fee is controlled only by a Curator.

------------------------------------------------------------------------

##

Both Curator and DAO fees are accumulated on Treasury Splitter contract which is unique for every curator. Curator and DAO have to claim accrued fees from the contract.

If a liquidation happens with bad debt, fees from Treasury Splitter contract are burnt to cover loss, so unclaimed fees act as an insurance buffer.

------------------------------------------------------------------------

##

All the fees taken by the protocol are split 50/50 between DAO and Curator by default.

To change this proportion both Gearbox DAO and Curator should sign transactions on TreasurySplitter contract (requires DAO proposal).

------------------------------------------------------------------------

##

Both Interest and Liquidation fees are set on Credit Manager level. Some examples when it can be useful:

-
:

:

Create Credit Manager with limit of 5,000,000 and set its fee to 0%
:

Once the limit is reached set it to 0. It will allow existing CM users to stay at 0% while disallowing new positions to be opened
:

Create a new Credit Manager with nonzero Interest Fee keeping other parameters untouched. That will result in new users opening positions with nonzero fee.

-
:

:

Create Credit Manager specifically for collaterals with boosts negotiated by curator
:

Projects issuing the collateral may have private lp deals or offer higher rewards for position opened for specified period of time. Curator may charge additional fee for bringing the opportunity to borrowers

:

[[[Previous][Market]]](/gearbox-permissionless-doc/market)[[[Next][Curation iceberg]]](/gearbox-permissionless-doc/curation-iceberg)

Last updated 2 months ago