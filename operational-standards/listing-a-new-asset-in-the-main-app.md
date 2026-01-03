# Listing a new asset in the main App

{% stepper %}
{% step %}
### If asset wasn't already present in Gearbox app

Make a PR with its icon in .svg format uploaded to [https://github.com/Gearbox-protocol/static/tree/main/public/tokens](https://github.com/Gearbox-protocol/static/tree/main/public/tokens)

<details>

<summary>Asset display example</summary>

<figure><img src="../.gitbook/assets/image (5).png" alt=""><figcaption></figcaption></figure>

</details>

**If there is a new Merkl reward campaign starting, ensure that its reward token also has supported icon.**

<details>

<summary>Merkl display example</summary>

<figure><img src="../.gitbook/assets/Screenshot 2025-12-16 at 12.31.53.png" alt=""><figcaption></figcaption></figure>

</details>

{% hint style="info" %}
**Image name should be lowercase token's symbol.**
{% endhint %}
{% endstep %}

{% step %}
### If asset should be listed on "Farm" page

1. Make a PR with strategy parameters to [https://github.com/Gearbox-protocol/static/blob/main/src/strategies/index.ts](https://github.com/Gearbox-protocol/static/blob/main/src/strategies/index.ts)\
   \
   For more info on Strategy parameters, please refer to [https://github.com/Gearbox-protocol/static/blob/main/src/core/strategy.ts](https://github.com/Gearbox-protocol/static/blob/main/src/core/strategy.ts)\
   \
   issuesOnClose: true should be set if the asset has limited secondary liquidity and its peg relies on delayed or KYC-gated redemptions.
2. If the strategy earns points of external protocol:
   1. Make a PR with point icon in .svg format uploaded to [https://github.com/Gearbox-protocol/static/tree/main/public/tokens](https://github.com/Gearbox-protocol/static/tree/main/public/tokens)
   2. Make a PR with point campaign terms to [https://github.com/Gearbox-protocol/apy-server/blob/main/src/tokens/points/constants.ts](https://github.com/Gearbox-protocol/apy-server/blob/main/src/tokens/points/constants.ts)\
      Campaign "type" should correspond to point's .svg file name
3. If the strategy earns yield (native or in form of **liquid** external rewards)\
   If its APR is available in DefiLlama or Merkl APIs - Make a PR to [Defillama Integration file](https://github.com/Gearbox-protocol/apy-server/blob/main/src/tokens/apy/llama/constants.ts) or [Merkl integration file](https://github.com/Gearbox-protocol/apy-server/blob/main/src/tokens/apy/merkle/apy.ts).
{% endstep %}
{% endstepper %}
