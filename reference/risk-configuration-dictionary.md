# Risk Configuration Dictionary

Flexibility is at the core of Gearbox’s design. Credit Accounts support a wide range of on-chain assets as collateral, which requires a risk framework capable of handling diverse asset properties. Gearbox’s risk controls are built to operate under uncertainty and adapt to any market conditions.

Gearbox is a platform for the permissionless creation and curation of lending markets. To participate safely, both Curators and Users must understand the risk-control allowlist: Curators need to know the capabilities it grants, while Users should understand the trust assumptions they accept when engaging in lending activity.

### Curator Roles

The Curator utilizes two primary roles to modify market parameters:

* **Admin**\
  Can modify all configurable parameters, subject to a minimum **24-hour timelock**.
* **Emergency Admin**\
  Can update a limited set of risk parameters **instantly** (without timelock) to mitigate immediate threats.

### Pool-Level Rules

These parameters define the global constraints for the Liquidity Pool. If a user disagrees with these terms, they must select a different pool.

#### Definitions

* **Total debt limit:** Maximum amount of underlying assets that can be borrowed across the entire pool.
* **Collateral limit:** Maximum amount of debt that can be backed by a specific collateral token (Quota Limit).
* **Main Price Feed:** Primary price source used for calculating account value and triggering liquidations.
* **Reserve Price Feed:** Secondary price source used to run safety checks on operations; can block Credit Account actions to protect LPs.
* **Increase Rate:** One-time fee charged whenever exposure to a collateral increases.
* **Collateral-specific rate:** Additional interest rate (APR) charged for borrowing against a specific collateral.
* **IRM:** The Utilization-based Interest Rate Model contract.
* **Loss Policy:** The logic executed when a liquidation results in bad debt.
* **Emergency liquidators whitelist:** Addresses authorized to liquidate accounts when the Credit Manager is paused (Default: Permissionless).
* **Loss liquidators whitelist:** Addresses authorized to execute liquidations that result in bad debt (Default: Permissionless).

#### Permissions Matrix

| Parameter                           | Admin (24h Delay) | Emergency Admin (Instant) |
| ----------------------------------- | :---------------: | ------------------------- |
| **Total debt limit**                |         ✅         | ⚠️ Reduce to zero-only    |
| **Collateral limit**                |         ✅         | ⚠️ Reduce to zero-only    |
| **Main Price Feed**                 |         ✅         | ⚠️ Limited choice         |
| **Loss Policy**                     |         ✅         | ⚠️ Can turn off           |
| **Loss liquidators whitelist**      |         ✅         | ⚠️ Can turn off           |
| **Emergency liquidators whitelist** |         ✅         | ⚠️ Can turn off           |
| **Reserve Price Feed**              |         ✅         | ❌                         |
| **Increase Rate**                   |         ✅         | ❌                         |
| **Collateral-specific rate**        |         ✅         | ❌                         |
| **IRM**                             |         ✅         | ❌                         |

### Credit Manager-Level Rules

These parameters define the strategy for a specific Credit Manager. If a user disagrees with these terms, they can choose another Credit Manager within the same pool.

#### Definitions

* **Total debt limit:** Maximum aggregate debt of all Credit Accounts created from this Credit Manager.
* **MinDebt:** Minimum required debt to open a Credit Account.
* **MaxDebt:** Maximum permitted debt per Credit Account.
* **Liquidation Premium:** Percentage of collateral value paid to the liquidator as an incentive.
* **Liquidation Fee:** Percentage of collateral value paid to the Protocol (Curator & DAO).
* **Max Enabled Tokens:** Maximum number of collateral tokens a single account can enable simultaneously.
* **Interest Fee:** Percentage of borrowing interest captured as revenue (split between Curator & DAO).
* **Collateral's LT:** The Liquidation Threshold (Loan-to-Value ratio).
* **Collateral's forbidden status:** Controls whether a token is allowed or forbidden.
* **List of allowed adapters:** Restricts which external contracts (e.g., Uniswap, Curve) a Credit Account can interact with.
* **Expiration Policy:** Date after which the strategy winds down. After this date, all Credit Accounts become liquidatable regardless of Health Factor.

#### Permissions Matrix

| Parameter                    | Admin (24h Delay) | Emergency Admin (Instant) |
| ---------------------------- | :---------------: | ------------------------- |
| **Total debt limit**         |         ✅         | ⚠️ Reduce to zero-only    |
| **List of allowed adapters** |         ✅         | ⚠️ Forbid-only            |
| **Collaterals list**         |         ✅         | ⚠️ Forbid-only            |
| **Liquidation Premium**      |         ✅         | ❌                         |
| **Liquidation Fee**          |         ✅         | ❌                         |
| **Collaterals' LT**          |         ✅         | ❌                         |
| **Expiration Policy**        |         ✅         | ❌                         |
| **MinDebt**                  |         ❌         | ❌                         |
| **MaxDebt**                  |         ❌         | ❌                         |
| **Max Enabled Tokens**       |         ❌         | ❌                         |
| **Interest Fee**             |         ❌         | ❌                         |

\</file>









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
