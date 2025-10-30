[Copy]

:

[](#video-explainer)

Video explainer
:

[](#fill-in-the-required-parameters)

Fill in the required parameters

:
:

Admin address: The address having the most permissions to execute changes through Timelock *usually Safe multisig or MPC wallet*
:

Emergency Admin address: Has permissions to execute the emergency changes without timelock. More info on this: [https://docs.gearbox.fi/gearbox-permissionless-doc/emergency-roles/emergency-admin](https://docs.gearbox.fi/gearbox-permissionless-doc/emergency-roles/emergency-admin)
:

Fee Collector address: The address which receives Curator's share of fee split
:

Transaction format: SAFE is likely your to-go choice. Txns are downloaded in Safe-compatible format. The json file can be attached in the Safe Transaction Builder (see [safe explainer](https://help.safe.global/en/articles/234052-transaction-builder)).

2

[](#execute-transactions-in-safe-ui)

Execute transactions in Safe UI

:

:
3

[](#sync-permissionless-interface)

Sync Permissionless Interface

:

:
-
:

:

forbidAdapter

-
:

:

forbidBorrowing

-
:

:

forbidToken

-
:

:

Can't increase debt
:

Can't partially withdraw collateral
:

Can't interact with adapters

:

pause

-
:

-
:

:

Set limit in Credit Manager to zero:

-
:

:

Set token limit in Pool to zero:

-
:

:

Pause pool:

-
:

-
:

:

Set priceFeed for given token from PriceFeed Store It can be done if current timestamp \> priceFeed allowance timestamp + 1 da