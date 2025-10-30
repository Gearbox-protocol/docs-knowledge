:

[Copy]

:

:

##

:

##

The Emergency Admin role has a very limited set of actions that can be executed immediately, without a timelock. These actions are designed to let curators respond quickly to incidents and protect the solvency of the market.

------------------------------------------------------------------------

##

Only one address can have Emergency Admin role. It is set at the moment of creating a Market Configurator. See more here:

------------------------------------------------------------------------

##

:

Action

New positions

Borrow

Withdraw

Adapter call

Liquidate

:

:

:

:

:

:

:

:

:

:

:

:

:

:

:

:

:

:

:

:

:

:

:

:

:

:

:

:

:

:

:

:

:

:

:

:

:

:

:

:

:

:

:

:

:

:

:

:

------------------------------------------------------------------------

##

:

iframe
:

:

------------------------------------------------------------------------

##

Collateral token incident[](#collateral-token-incident)

:

[**Low severity** ]*[(incident status is unclear)]*

-
:

:

Collateral exposure can\'t be increased
:

Existing positions operations are not limited

:

[**Medium severity** ]*[(collateral behavior is unhealthy, but no immediate bad debt risk)]*

-
:

:

Collateral exposure can\'t be increased
:

Existing positions operations are limited

-
:

-
:

:

[**High severity** ]*[(collateral poses risk to market solvency)]*

-
:

:

No user-side operations are allowed
:

Only emergency liquidators can liquidate accounts

Price feed incident[](#price-feed-incident)

[](#overpricing-token)

**Overpricing token**
:

**Feed price is higher than market price enough to block liquidations** In cases when price feeds deviates from market price by more than liquidation premium, liquidations become unprofitable.

-
:

:

Set **Token Limit = 0** in Pool to limit increasing exposure to Asset.
:

Consider creating a new Credit Manager with higher liquidation premium.

-
:

:

**Set Main Feed** of token to one that is closer to market value.

-
:

-
:

:

**Feed price is higher than market price enough to drain Pool** In cases when price feeds higher than market price by more than 1/LT of a token, one can buy token on secondary market and borrow more than was the cost, repeating it until \"buy\" liquidity or the pool is exhausted. *This risk is mitigated if at least one of Main and Reserve feeds returns adequate value, as the token at risk will be priced at minimal price during collateral withdrawals.*

-
:

:

**Forbid token** in Credit Manager

-
:

-
:

External protocol incident[](#external-protocol-incident)

###

####

**`setTokenLimit(token, 0)`**

-
:

-
:

-
:

-
:

**`forbidToken(token)`**

-
:

-
:

:

Operations which decrease HF are blocked (increase debt, withdraw collateral, swap into different collateral with lower LT)
:

Operations which increase balance of forbidden token are blocked

-
:

####

**`setMainPriceFeed(token, feed)`**

-
:

-
:

-
:

:

If the new main feed equals the current reserve feed, the reserve feed is removed (token ends up with only one feed).
:

New main price may be low enough to trigger immediate liquidations of Credit Accounts.

####

**`forbidAdapter(adapter)`**

-
:

-
:

-
:

:

If the forbidden adapter highly contributes to some tokens\' liquidity, forbidding it may break liquidations, since most of Gearbox\'s internal liquidators rely on allowed adapters for searching tokens\' swap paths. External liquidators may or may not be affected.

####

**`pausePool(pool)`**

-
:

:

Designed to be combined with Credit Manager pause to prevent bank runs in the most extremal scenarios.

**`setCreditManagerDebtLimit(cm, 0)`**

-
:

-
:

####

**`pauseCreditManager(cm)`**

-
:

:

Borrowing, withdrawing collateral, opening & closing credit accounts, performing adapter calls are blocked.

-
:

**`forbidBorrowing(cm)`**

-
:

-
:

####

**`setAccessMode(mode)`**

-
:

-
:

**`setChecksEnabled(flag)`**

-
:

: