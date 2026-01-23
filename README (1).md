# Manual Deleveraging When UI Actions Are Unavailable

If the **Close** or **Swap** action is unavailable or fails, you can exit your position manually by following the steps below.

{% stepper %}
{% step %}
## Withdraw collateral

Withdrawing collateral sends the token to your wallet, where you can swap it freely using external liquidity sources outside of Gearbox.

{% hint style="warning" %}
Withdrawing collateral reduces your position’s **Health Factor**. A large withdrawal may push the position into liquidation risk. \
\
Always check the projected **Health Factor** before each withdrawal.
{% endhint %}

<details>

<summary>Withdraw collateral in the UI</summary>

<figure><img src=".gitbook/assets/Screenshot 2025-12-23 at 13.34.37.png" alt=""><figcaption></figcaption></figure>

</details>

{% hint style="success" %}
If your current **Health Factor** does not allow for a safe withdrawal, repay part of your debt first using the Debt Token from your wallet (see **Step 3**).
{% endhint %}
{% endstep %}

{% step %}
## Swap collateral into the Debt Token

Swap the withdrawn collateral into the Debt Token using external liquidity sources.

Recommended options include:

* DEX aggregators
* Official liquidity venues provided by the collateral issuer
{% endstep %}

{% step %}
## Repay debt using Debt Token from your wallet

{% hint style="info" %}
Repay the debt using the **same token the debt is denominated in**, directly from your wallet.
{% endhint %}

{% hint style="success" %}
Check whether the updated **Health Factor** allows for further withdrawal.
{% endhint %}

<details>

<summary>Repay debt in the UI</summary>

<figure><img src=".gitbook/assets/Screenshot 2025-12-23 at 13.42.19.png" alt=""><figcaption></figcaption></figure>

</details>
{% endstep %}

{% step %}
## Repeat Steps 1-3 until your Credit Account reaches the desired state or is fully unwound
{% endstep %}
{% endstepper %}

