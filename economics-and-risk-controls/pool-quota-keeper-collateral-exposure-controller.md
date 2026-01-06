# Pool Quota Keeper (Collateral Exposure Controller)

## Pool Quota Keeper (Collateral Exposure Controller)

While the Pool manages the liquidity of the _underlying_ asset, the Quota Keeper restricts how much of that liquidity can be borrowed against specific _collateral_ assets across all Credit Managers.

It also serves as a "collateral-specific interest rate mechanism," allowing the protocol to charge specific rates for holding risky or illiquid assets, independent of the base borrow rate.

#### Core Functions

The Quota Keeper enforces three main constraints on the system:

1. Total Exposure Limits (Quota limits): It enforces a global cap on the amount of debt that can be backed by particular caollateral on all Credit Accounts combined. If a user tries to swap collateral into a token that has reached its quota limit, the transaction reverts.
2. Collateral-Specific Interest Rates: It calculates and accrues "Quota Interest." This is an additional APR charged on the _amount of collateral held_, separate from the APR charged on the _amount borrowed_. \
   This allows Curators to price the risk of holding specific assets (e.g., charging 5% APR for holding a volatile long-tail asset).
3. Quota Increase Fees: It manages one-time fees charged when a user increases their position in a specific token. This functions similarly to a swap fee but is retained by the protocol/quota reserves.

#### Curator Controls

* Token Exposure Limit: Sets the hard cap on how much of a specific token the Market is willing to accept as collateral. Curators use this to prevent the protocol from holding more of an asset than can be safely liquidated in the open market.
* Collateral Onboarding: Whitelists a new token to be counted towards quotas. Before a Credit Manager can accept a token as collateral, the Curator must enable it here first.
* Token Entry Fee: Sets a one-time fee charged when a borrower increases their exposure to a specific token.&#x20;
