# Configure Credit Manager

### _**Setup examples**_

[setup example (BNB chain: USD1 pool, USDX collateral)](https://www.notion.so/Adapter-setup-example-BNB-chain-USD1-pool-USDX-collateral-208145c16224807fa1a0d318c01bc1ae?pvs=21)

[setup example (Ethereum chain: tBTC pool, uptBTC collateral)](https://www.notion.so/Adapter-setup-example-Ethereum-chain-tBTC-pool-uptBTC-collateral-20e145c1622480c886d8d43dc5e9f5bb?pvs=21)

[setup example (Ethereum chain: USDC pool, frxUSD/USDf collateral)](https://gearboxprotocol.notion.site/Adapter-setup-example-Ethereum-chain-USDC-pool-frxUSD-USDf-collateral-24c145c16224809d80d2d171e1128317?source=copy_link)

### _**Collaterals**_

<figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FX4XV5s21Q33tVleZJwWU%2Fimage.png?alt=media&#x26;token=2f06d21c-f9c2-4a13-96d2-21220baab358" alt=""><figcaption></figcaption></figure>

{% stepper %}
{% step %}
#### _**Add new collateral**_

Select token from those already added to Market. If not present, [add token to Market.](https://docs.gearbox.fi/gearbox-permissionless-doc/step-by-step-guides/configuring-a-market#add-new-asset-and-set-main-feed)

Set LT of a collateral - Liquidation Threshold (same as Liquidation LTV on other lending protocols)

{% hint style="info" %}
LT can't be higher than 100% - liquidation Fee - liquidation Premium
{% endhint %}
{% endstep %}

{% step %}
#### Modify LT of existing collateral

{% hint style="success" %}
To protect borrowers from immediate liquidations, LT can't be changed immediately.\
LT ramping makes LT linearly change current LT to target LT over a specified period.
{% endhint %}

{% hint style="warning" %}
The minimal Ramp duration is 2 days (172800 seconds).
{% endhint %}

Ramp starts when transactions are executed onchain (duration of ramp can be set in UI).

<figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2Fx7kSGZYx5BrolHtxzBXz%2Fimage.png?alt=media&#x26;token=5fae0304-a169-46f4-b0ab-852b75c55b1c" alt=""><figcaption></figcaption></figure>
{% endstep %}
{% endstepper %}

### _**Adapters**_

[_**Detailed section on adapters configuration.**_](https://docs.gearbox.fi/gearbox-permissionless-doc/step-by-step-guides/configuring-adapters)

<div data-full-width="false"><figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FxYjLFEUcb0pV71URiaOE%2Fimage.png?alt=media&#x26;token=1a47e097-8a7e-4cac-b257-eb8a1b7ffbdf" alt=""><figcaption></figcaption></figure></div>
