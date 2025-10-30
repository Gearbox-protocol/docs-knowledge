[Copy]

:

:
Morpho has pioneered the concept of curated lending markets in DeFi, but its approach differs significantly from Gearbox\'s model. Below is a clear comparison of how curators function in each protocol:

###

In Morpho, curators are active capital allocators. They:

-
:

-
:

###

In Gearbox, curators have a more limited role, focusing solely on risk management. They:

-
:

-
:

:
:

:

:
:

:
:

Set collateral limit, LTV and oracle for a new token in Market
:

Borrowers can now use pool\'s liquidity

:
:

Add nonzero supply cap for existing market (LTV and oracle are pre-configured)
:

Deposit vault\'s funds to the new market
:

Borrowers can now use vault\'s liquidity

:

:
:

Set new price feed
:

Start ramp of LTV to target value
:

Feed & LTV for old and new borrowers are changed

:
:

Deploy a market with needed LTV and oracle and set nonzero supply cap for it
:

Feed & LTV are changed only for new borrowers
:

Start withdrawing liquidity from old market & push borrowers out by raising rate

:

:
:

Set a new collateral-specific rate in addition to IRM utilization rate

:
:

Move vault\'s allocation in/out of the Market to move dynamic IRM

:

:
:

Allow the list of needed adapters in the Market

:
:

Contact contango or another strategy provider to integrate your collateral

:
:
: