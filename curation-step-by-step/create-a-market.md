# Create a Market

## Prerequisites

To create a market, you need to have the borrowable token whitelisted in Price Feed Store. You can achieve it by either:

* Doing it yourself following guide from Advanced Config Section [add-required-price-feeds.md](../advanced-configuration/add-required-price-feeds.md "mention")
* Asking Gearbox Contributors for help by providing:
  * Address of target token
  * Address of token's price feed
  * Heartbeat parameter of token's price feed

## Demo

The video showcasing the process of setting up an example market, just to know what to prepare for.

{% embed url="https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FNanWPyWjWeYcVHjUKlJQ%2Fwhole%20flow.mp4?alt=media&token=152a96d8-9927-425c-b657-cbce5669e7b0" %}

## Market Parameters

{% stepper %}
{% step %}
#### Pool version

Select from verified code versions (currently only v3.1)
{% endstep %}

{% step %}
#### Underlying Asset, Price Feed

Underlying (borrowable) token and Price Feed to use for it. Select from PriceFeed Store.

More info about Price Feed store and feeds configuration can be found [here](https://docs.gearbox.fi/gearbox-permissionless-doc/step-by-step-guides/adding-required-price-feeds).

{% hint style="info" %}
For correlated Collateral/ Debt usecases it may be worth it to set an upper bound for Underlying Asset price feed to protect borrowers against unwanted liquidations.
{% endhint %}
{% endstep %}

{% step %}
#### Market Name

Should usually include the symbol of underlying token and one-word description.
{% endstep %}

{% step %}
#### Total debt limit

Max amount of underlying token that can be borrowed from entire pool.

Usually can be set to arbitrary high value (if you don't have special plan for it), because position-specific and token-specific limits will be granurarly configured further.
{% endstep %}

{% step %}
#### Interest Rate Model

_**Type**_\
Currenly only linear with 2 kink points, which allows more flexible configuration compared to 1-kink. The list can be updated by adding new IRMs to Bytecode Repository.

_**Model parameters**_

* U1 - first curve kink
* U2 - second curve kink
* R\_base - utilization rate at U = 0%
* R\_slope1 - utilization rate at U = U1
* R\_slope2 - utilization rate at U = U2
* R\_slope3 - utilization rate at U = 100%
* If **isBorrowingMoreU2Forbidden** is true, borrowing is disabled when utilization is > U2.

{% hint style="success" %}
Setting IRM in a way that **borrow rate at target utilization (\~80-85%)** equals **60-70% of expected collateral yield** will allow you to bootstrap utilization and then find equlibrium rate using collateral-specific rates.
{% endhint %}

{% hint style="info" %}
Curator's fee is added on top of interest paid by borrower.\
If the IRM + [collateral-specific rate](https://docs.gearbox.fi/gearbox-permissionless-doc/competitive-advantages/collateral-specific-rates) is 5% and the fee is 20% of the interest, then borrowers pay 6%.
{% endhint %}

* _**Reference configs**_
  * [Desmos IRM visualizer](https://www.desmos.com/calculator/d281eeb4a9)
  * [Mainnet ETH pool](https://app.gearbox.fi/pools/0xda0002859b2d05f66a753d8241fcde8623f26f4f/utilization)
  * [Mainnet USDC pool](https://app.gearbox.fi/pools/0xda00000035fef4082f78def6a8903bee419fbf8e)
{% endstep %}

{% step %}
#### Rate keeper parameters

Determine how collateral-specific borrow rates are set.

_**Type**_

* **Tumbler&#x20;**_**(Recommended option)**_\
  Risk curator can manually set _token-specific rate_.
* **Gauge** _**(Legacy option)**_\
  Risk curator sets minRate and maxRate for each collateral. Then users can vote UP or DOWN with their staked $GEAR to increase or decrease quota rate.

{% hint style="success" %}
Curator's fee is added on top of interest paid by borrower.\
If the IRM + [collateral-specific rate](https://docs.gearbox.fi/gearbox-permissionless-doc/competitive-advantages/collateral-specific-rates) is 5% and the fee is 20% of the interest, then borrowers pay 6%.
{% endhint %}

**Epoch Length**

Epoch length sets the minimal time period between 2 consecutive rate keeper updates.

{% hint style="info" %}
_Example:_ Epoch = 2 days. Curator decides to update rates on Monday 10:00 ⇒ Next update can happen no earlier than on Wednesday 10:00
{% endhint %}
{% endstep %}

{% step %}
#### Loss policy

Additional logic applied during CA liquidation if it results in creation of Bad Debt.

_**Aliased**_ policy reprices collateral tokens with aliased feeds (set separately).

_**Example**:_

* Main ezETH feed - Market price
* Reserve ezETH feed - Exchange rate price
* Aliased ezETH feed - Exchange rate price&#x20;
{% endstep %}
{% endstepper %}
