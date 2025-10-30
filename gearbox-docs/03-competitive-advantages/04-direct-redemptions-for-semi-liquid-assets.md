:

# Direct redemptions for semi-liquid assets
:
##

One challenge in executing leveraged strategies is the high cost of converting collateral tokens back into their underlying assets. This happens because native redemptions are often time-locked, and secondary market liquidity is typically low relative to the size of leveraged positions.

Before Gearbox it was only possible to either repay the full debt and withdrawl collateral, or iteratively deleverage withdrawing and redeeming small portions of collateral. Read more about problems of this methods [here](https://hackmd.io/@desnake/ByismSraee).

##

**Benefits:**

-
:

-
:

-
:

The solution is based on unique features of Gearbox and therefore is impossible on other lending platforms:

-
:

-
:

##

1.
:

2.
:

:

The Credit Account sends the xRWA token to the redemption contract.
:

In return, the Credit Account receives a *redemption receipt token*, which represents a future claim on the underlying asset.

3.
:

4.
:

:

Once the redemption window has passed, the user can finalize the redemption.
:

The Credit Account burns the redemption receipt token.
:

The Credit Account receives the underlying asset.

:

##

:

##

When assets are in a transition state (e.g., during vault token redemption to the underlying asset), they become non-transferable and therefore cannot be liquidated. In addition, these tokens typically do not earn yield during this period.

As a result, a position's Health Factor may decrease due to:

-
:

-
:

To mitigate the risk of a position falling below the solvency threshold, it is recommended to set the reserve feed of the *phantom token* (the token representing a future claim on redeemed assets) to a discounted value.

This discount acts as a protective buffer, ensuring that only positions with a sufficient Health Factor can enter the transition state. In practice, it prevents unhealthy positions from initiating redemptions that could lead to insolvency.

For example, if a 4% reserve price discount is applied, only users with a Health Factor ≥ 1.04 will be able to initiate a full redemption of their collateral.

*Health Factor = Collateral value \* LTV / Debt Positions become liquidatable if Health Factor \<= 1*
**Example:**

-
:

:

User holds mHYPER with position Health Factor of 1.1

-
:

-
:

:

User holds mHYPER with position Health Factor of 1.03

-
:

-
:

**Result:**

-
:

-
:

[[[Previous][Multichain architecture]]](/gearbox-permissionless-doc/multichain-architecture)[[[Next][Creating a new Curator (Market Configurator)]]](/gearbox-permissionless-doc/step-by-step-guides/creating-a-new-curator-market-configurator)

Last updated 14 hours ago