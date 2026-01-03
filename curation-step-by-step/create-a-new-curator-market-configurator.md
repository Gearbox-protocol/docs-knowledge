# Create a new Curator (Market Configurator)

Market Configurator (MC) is a contract that has rights to change parameters of curated Markets. One MC can control multiple markets. The intended usage is for 1 Risk Curator to have 1 MC on each chain they want to deploy on.

#### Video explainer

The UI is located at [https://permissionless.gearbox.foundation/curators](https://permissionless.gearbox.foundation/curators)

{% hint style="success" %}
**You can use any wallet to connect to the curation UI - it's only a frontend + backend to provide no-code curation experience.**\
\
**You only need access to Admin wallet with real signers for executing onchain actions which is the final step of any setup.**
{% endhint %}

{% hint style="warning" %}
**If you're using MPC wallet, please create a safe multisig with MPS as 1/1 signer.**\
\
**Gearbox has a lot of tooling to work using Safe Multisigs.**
{% endhint %}

{% embed url="https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FuR65FqEWMVzqxHTPATPZ%2Fmc%20creation.mp4?alt=media&token=8f5d8f23-e731-4318-bf20-66cefab6f690" %}

{% stepper %}
{% step %}
#### Fill in the required parameters

<figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FY9PPOJEmHAPr2ISLMjCp%2Fimage.png?alt=media&#x26;token=6ca8fa03-654e-4f58-95d3-18a2319c10bd" alt=""><figcaption></figcaption></figure>

* **Admin address:**\
  Safe multisig having the most permissions to execute changes through Timelock.
* **Emergency Admin address:**\
  Has permissions to execute the emergency changes without timelock.
* **Fee Collector address:**\
  The address which receives Curator’s share of fee split
* **Transaction format:**\
  SAFE is likely your to-go choice. Txns are downloaded in Safe-compatible format. The json file can be attached in the Safe Transaction Builder (see [safe explainer](https://help.safe.global/en/articles/234052-transaction-builder)).
{% endstep %}

{% step %}
#### Execute transactions in Safe UI

<figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FjkhEEqcsYRPDY81zZzi7%2FScreenshot%202025-06-29%20at%2020.50.25.png?alt=media&#x26;token=1230377c-9a90-44c3-ad33-564eddbca68f" alt=""><figcaption></figcaption></figure>

<figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FkwiGb4pH2pXY8kVP1EBH%2FScreenshot%202025-06-29%20at%2020.51.31.png?alt=media&#x26;token=550e47f5-df8e-4bf0-a5a2-c0f8e46d8340" alt=""><figcaption></figcaption></figure>
{% endstep %}

{% step %}
#### Sync Permissionless Interface

On Instances Page click on a chain where you've deployed Market Configurator

<figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2F0i6a7MWauVHrdABhDlqW%2Fimage.png?alt=media&#x26;token=be76ecfe-e927-42c1-9645-978bc33d1238" alt=""><figcaption></figcaption></figure>

Click on a Sync button and wait for Sync to end

<figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FiGHemRXlguvlrfdWh5ta%2FScreenshot%202025-06-29%20at%2020.57.33.png?alt=media&#x26;token=aa2dce2a-4c22-4d04-9465-f1d565e6056b" alt=""><figcaption></figcaption></figure>
{% endstep %}
{% endstepper %}
