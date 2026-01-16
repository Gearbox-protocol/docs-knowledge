# Create Credit Manager

{% stepper %}
{% step %}
### Name

Name can reflect the properties of collaterals and position size:

* Volatile/ Correlated
* Blue-chip/ Experimental
* Small/ Medium/ Big (depending on account debt limit)

Simple notation is calling naming it with tiers: Tier 1; Tier 2; Tier 3\
Higher tier means larger positions and safer collaterals.
{% endstep %}

{% step %}
### **Interest Fee**

% of borrowing interest taken by DAO and Curator\
Default fee split is 50/50 between DAO and Curator

{% hint style="info" %}
Interest fee of a Credit Manager _**can’t be changed**_ after it’s deployed.
{% endhint %}

{% hint style="warning" %}
Curator's fee is added _**on top of interest paid**_ by borrower.\
If the IRM + [collateral-specific rate](https://docs.gearbox.fi/gearbox-permissionless-doc/competitive-advantages/collateral-specific-rates) is 5% and the fee is 20% of the interest, then borrowers pay 6%.
{% endhint %}

{% hint style="success" %}
Interest fee & Credit Manager's debt limit can be used to _**bootstrap Market utilization.**_

e.g. Create Credit Manager with limit of 5,000,000 USD and Interest Fee of 0% can be created to incentivize first borrowers as they will get more favorable borrow rates.
{% endhint %}
{% endstep %}

{% step %}
### Liquidation Premium & Fee

* **Premium -** % of liquidated collateral taken by liquidator

{% hint style="warning" %}
Liquidation premium & fee of a credit manager can’t be modified after it’s deployed.
{% endhint %}

* **Fee -** % of liquidated collateral taken by DAO and Curator

{% hint style="info" %}
It’s not recommended to set liquidation fee to be lower than 0.01%. If the fee is set to 0, then account that fully consists of leveraged underlying token will create bad debt upon liquidation.
{% endhint %}

{% hint style="success" %}
There is no impact of liquidation fee on the safety of liquidations (it doesn't increase or decrease probability of succesfull liquidations with profit).
{% endhint %}

Borrower loses Liquidation Premium + Liquidation Fee from liquidation collateral.

Expired liquidation premium and fee are useful only if Credit Manager is expirable, which is a rare case, so you can freely omit that parameters.\
If set, "Expired" versions of liquidation premium and fee are applied after Credit Manager expiration.
{% endstep %}

{% step %}
### Minimum debt, Maximum debt, Max. enabled tokens

* **Minimum & Maximum debt** - Credit account created in this Credit Manager can't have debt less than minimum and more than maximum.
* **Max. enabled tokens** - maximal amount of different tokens that can be counted towards account value (used as cross-collateral margin).

{% hint style="warning" %}
**maxDebt/minDebt <= 100/max enabled tokens**\
\
\&#xNAN;_Example: If max enabled tokens = 4 and minimum debt = 10k USDC, maximum debt can't be larger than 250k USDC._
{% endhint %}
{% endstep %}

{% step %}
### Whitelist policy, Expiration

**Whitelist** - Allow borrowing only to owners of particular NFT.

**Expiration** - Credit Manager can be shut down following specified schedule. May be useful for time-sensitive types of collaterals.
{% endstep %}

{% step %}
### Total Debt Limit

Maximal sum debt on all credit accounts created in this Credit Manager.

{% hint style="success" %}
Interest fee & Credit Manager's debt limit can be used to _**bootstrap Market utilization.**_

e.g. Create Credit Manager with limit of 5,000,000 USD and Interest Fee of 0% can be created to incentivize first borrowers as they will get more favorable borrow rates.
{% endhint %}
{% endstep %}
{% endstepper %}
