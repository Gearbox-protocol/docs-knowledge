# Risk configuration dictionary

Flexibility is at the core of Gearbox’s design. Credit Accounts support a wide range of on-chain assets as collateral, which requires a risk framework capable of handling diverse asset properties.&#x20;

Gearbox’s risk controls are built to operate under uncertainty and adapt to any market conditions.

{% hint style="info" %}
Gearbox is a platform for the permissionless creation and curation of lending markets.&#x20;

To participate safely, both Curators and Users should understand the risk-control allowlist: Curators need to know the capabilities it grants, while Users should understand the trust assumptions they accept when engaging in lending activity.
{% endhint %}

Curator has 2 main roles to modify markets' parameters:

*   **Admin**

    Can modify all configurable parameters, subject to a minimum 24-hour timelock.
*   **Emergency Admin**

    Can update a limited set of risk parameters without a timelock in emergency situations.

All the rules below will have a specification based on which access those roles have.

## Pool-level rules

If a user disagrees with these terms, they need to select another pool.

* **Total debt limit:** maximum that can be borrowed across the entire pool
* **Collateral limit:** maximum that can be borrowed against each token
* **Main Price Feed:** price source for calculating account value and triggering liquidations
* **Reserve Price Feed:** runs safety checks on operations and can block Credit Account actions to protect LPs
* **Increase Rate:** one-time fee whenever exposure to a collateral increases
* **Collateral-specific rate:** extra interest for borrowing against a given collateral
* **IRM:** utilization-based interest rate model
* **Loss Policy:** additional liquidation logic for cases that create bad debt
* **Emergency liquidators whitelist:** when Credit Manager is paused, liquidations are performed in "Emergency" mode which allows to restrict access to liquidations. By default they are permissionless
* **Loss liquidators whitelist:** when a liquidation creates bad debt, it's performed in "Loss" mode mode which allows to restrict access to liquidations. By default they are permissionless

<table data-full-width="false"><thead><tr><th width="271.18359375">Parameter</th><th width="91.41796875">Admin</th><th>Emergency admin</th></tr></thead><tbody><tr><td><strong>Total debt limit</strong></td><td>✅</td><td>⚠️ Reduce to zero-only</td></tr><tr><td><strong>Collateral limit</strong></td><td>✅</td><td>⚠️ Reduce to zero-only</td></tr><tr><td><strong>Main Price Feed</strong></td><td>✅</td><td>⚠️ Limited choice</td></tr><tr><td><strong>Loss Policy</strong></td><td>✅</td><td>⚠️ Can turn off</td></tr><tr><td><strong>Loss liquidators whitelist</strong></td><td>✅</td><td>⚠️ Can turn off</td></tr><tr><td><strong>Emergency liquidators whitelist</strong></td><td>✅</td><td>⚠️ Can turn off</td></tr><tr><td><strong>Reserve Price Feed</strong></td><td>✅</td><td>❌</td></tr><tr><td><strong>Increase Rate</strong></td><td>✅</td><td>❌</td></tr><tr><td><strong>Collateral-specific rate</strong></td><td>✅</td><td>❌</td></tr><tr><td><strong>IRM</strong></td><td>✅</td><td>❌</td></tr></tbody></table>

### **Credit Manager-level rules**

If a user disagrees with these terms, they can choose another Credit Manager within the same pool.

* **Total debt limit:** maximum aggregate debt of all Credit Accounts created from this Credit Manager
* **MinDebt:** minimum required debt for a Credit Account
* **MaxDebt:** maximum permitted debt for a Credit Account
* **Liquidation Premium:** portion of collateral value paid to the liquidator during liquidation
* **Liquidation Fee:** portion of collateral value paid to the curator and Gearbox DAO during liquidation
* **Max Enabled Tokens:** number of different collateral tokens that can count toward account value
* **Interest Fee:** extra rate on top of the IRM and collateral-specific rate, split between the curator and DAO
* **Collateral's LT** (loan to value)
* **Collateral's forbidden status**
* **List of allowed adapters:** restricts which external contracts a Credit Account can use
* **Expiration Policy:** curator may set an expiration; after the cutoff date, all Credit Accounts become liquidatable regardless of Health Factor with penalties set by the expired liquidation fee and premium parameters.

<table data-full-width="false"><thead><tr><th width="271.18359375">Parameter</th><th width="91.41796875">Admin</th><th>Emergency admin</th></tr></thead><tbody><tr><td><strong>Total debt limit</strong></td><td>✅</td><td>⚠️ Reduce to zero-only</td></tr><tr><td><strong>List of allowed adapters</strong></td><td>✅</td><td>⚠️ Forbid-only</td></tr><tr><td><strong>Collaterals list</strong></td><td>✅</td><td>⚠️ Forbid-only</td></tr><tr><td><strong>Liquidation Premium</strong></td><td>✅</td><td>❌</td></tr><tr><td><strong>Liquidation Fee</strong></td><td>✅</td><td>❌</td></tr><tr><td><strong>Collaterals' LT</strong></td><td>✅</td><td>❌</td></tr><tr><td><strong>Expiration Policy</strong></td><td>✅</td><td>❌</td></tr><tr><td><strong>MinDebt</strong></td><td>❌</td><td>❌</td></tr><tr><td><strong>MaxDebt</strong></td><td>❌</td><td>❌</td></tr><tr><td><strong>Max Enabled Tokens</strong></td><td>❌</td><td>❌</td></tr><tr><td><strong>Interest Fee</strong></td><td>❌</td><td>❌</td></tr></tbody></table>
