# Configure a Market

### Assets

<figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FZIRByw2BXrrzjiaRc6Bf%2Fimage.png?alt=media&#x26;token=ded7bed0-a1af-4d35-9f03-26772bb7b8ad" alt=""><figcaption></figcaption></figure>

{% stepper %}
{% step %}
#### Add new asset and set Main Feed

**Asset:** Collateral token address. Select from PriceFeed Store or [add new if needed.](https://docs.gearbox.fi/gearbox-permissionless-doc/step-by-step-guides/adding-required-price-feeds)

**Price Feed:** Collateral token Main price feed. Select from PriceFeed Store or [add new if needed](https://docs.gearbox.fi/gearbox-permissionless-doc/step-by-step-guides/adding-required-price-feeds).

Main feed is used to for collateral pricing during liquidation checks.
{% endstep %}

{% step %}
#### Set Reserve Feed

Select from PriceFeed Store or [add new if needed](https://docs.gearbox.fi/gearbox-permissionless-doc/step-by-step-guides/adding-required-price-feeds).

{% hint style="success" %}
Used to protect the protocol against manipulations of Main Feeds’ price. See [Dual-oracle pricing](https://docs.gearbox.fi/gearbox-permissionless-doc/competitive-advantages/dual-oracle-pricing) for detailed explanation.
{% endhint %}

{% hint style="warning" %}
Set Reserve Feed equal to Main Feed if you have no other options.\
\&#xNAN;_**If reserve price feed is not set, part of the protocol functions (withdrawals, partial liquidations) won't be available.**_
{% endhint %}
{% endstep %}

{% step %}
#### Quota limit

Max amount of debt that can be backed by particular asset in the pool. Measured in amount of underlying asset. Used for calculation of Account Value and quota interest rate.\
see [Docs](https://docs.gearbox.finance/overview/liquidations#what-is-a-health-factor) for detailed explanation.
{% endstep %}

{% step %}
#### Increase Rate

**Rarely used, feel free to omit**\
When user increases Quota (CA-specific max amount of debt that can be backed by particular collateral), charge a fixed % fee on the quota difference: works like a one-time fee charged on swaps by exchanges.
{% endstep %}
{% endstepper %}

### Rates

<figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2F61ufP1u5cgCQA8HUMtmD%2Fimage.png?alt=media&#x26;token=d22ba306-29bc-4753-b7d6-f4b6a3d1c214" alt=""><figcaption></figcaption></figure>

{% stepper %}
{% step %}
#### Collateral-specific Rates

Additional rate which is applied on top of IRM-based utilization rate for borrowing against particular collaterals.

To modify collateral-specific rates, set the intended rates in front of each collateral and click "Update Rates".

See [Collateral-specific rates](https://docs.gearbox.fi/gearbox-permissionless-doc/permissionless-curation/fee-sharing) for detailed explanation.

{% hint style="success" %}
Setting IRM in a way that **borrow rate at target utilization (\~80-85%)** equals **60-70% of expected collateral yield** will allow you to bootstrap utilization by allowing favorable rates.\
Equlibrium rate can then be found by increasing collateral-specific rates.
{% endhint %}
{% endstep %}
{% endstepper %}

### IRM

<figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2F8n8Pni8kyixjGPzwK7eS%2FScreenshot%202025-08-06%20at%2023.46.29.png?alt=media&#x26;token=33c7b2c3-890b-4d9c-a563-84ce0846e392" alt=""><figcaption></figcaption></figure>

{% stepper %}
{% step %}
#### IRM parameters

Rate curve parameters can be changed after the creation of Market by executing transactions generated from "Change Model" action.
{% endstep %}
{% endstepper %}

### Loss policy

Additional logic applied during CA liquidation if it results in creation of Bad Debt.\
Properly set loss policy is especially helpful in cases when secondary market oracle is used as a Main feed.

**Risks of using secondary market price as Main price feed**

\
\&#xNAN;_**Example**:_

* Main ezETH feed - Market price
