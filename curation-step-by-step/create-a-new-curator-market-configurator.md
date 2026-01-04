# Create a new Curator (Market Configurator)

The **Market Configurator** serves as the central administration contract for a lending business.

It acts as the root permission node. From this single point of control, Curators deploy new markets, adjust risk parameters, and manage fee distribution. This contract must be deployed once per blockchain network.

## Prerequisites

{% hint style="success" %}
## Separation of Drafting vs. Signing

The Gearbox Curation Interface is a **drafting tool**, not a signing terminal.

* **Drafting:** You may connect **any** standard wallet (e.g., a hot wallet) to the Gearbox UI to configure parameters and generate transaction files.
* **Signing:** The actual execution happens securely within the Gearbox Safe interface ([https://safe.gearbox.finance/](https://safe.gearbox.finance/))
* **Benefit:** Operations teams can draft complex updates without requiring the Admin/Signers to connect their high-security wallets to the web interface.
{% endhint %}

{% hint style="warning" %}
## Recommendation for MPC Users (Fordefi, Fireblocks, etc.)

Institutional MPC wallets often lack direct support for batch transaction builders.

* **Recommendation:** Deploy a **1/1 Safe Multisig** with your MPC address as the sole signer.
* **Why:** This acts as a compatibility layer, allowing you to utilize the Gearbox Safe interface and transaction batching flow while retaining the custody security of your MPC provider.
{% endhint %}

## Deployment walkthrough

**Access the Interface:** [https://permissionless.gearbox.foundation/curators](https://www.google.com/url?sa=E\&q=https%3A%2F%2Fpermissionless.gearbox.foundation%2Fcurators)

{% embed url="https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FuR65FqEWMVzqxHTPATPZ%2Fmc%20creation.mp4?alt=media&token=8f5d8f23-e731-4318-bf20-66cefab6f690" %}

{% stepper %}
{% step %}
## Define Governance Roles

* **Admin Address:**
  * _Function:_ Primary governance. Can modify all parameters subject to a **24-hour timelock**.
  * _Recommendation:_ Main Safe Multisig (or 1/1 Safe for MPC users).
* **Emergency Admin:**
  * _Function:_ Crisis response. Can disable specific tokens and perform limited list of emergency actions instantly (bypassing timelock).
  * _Recommendation:_ A separate Security Multisig or secure Hardware Wallet.
* **Fee Collector:**
  * _Function:_ Revenue destination. Receives all accrued interest and liquidation fees.
* **Transaction Format:**
  * Select **SAFE** to generate a compatible JSON file.

<details>

<summary>UI walkthrough</summary>

<figure><img src="../.gitbook/assets/Screenshot 2026-01-04 at 16.52.47.png" alt=""><figcaption></figcaption></figure>

<figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FY9PPOJEmHAPr2ISLMjCp%2Fimage.png?alt=media&#x26;token=6ca8fa03-654e-4f58-95d3-18a2319c10bd" alt=""><figcaption></figcaption></figure>

</details>
{% endstep %}

{% step %}
#### Execute transactions in Safe UI

The interface generates a JSON file containing the deployment bytecode.

1. Navigate to the **Safe App** (using the Admin wallet defined in Step 1).
2. Open the **Transaction Builder** application.
3. Upload the generated JSON file.
4. Review the transaction details and execute.

<details>

<summary>UI walkthrough</summary>

<figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FjkhEEqcsYRPDY81zZzi7%2FScreenshot%202025-06-29%20at%2020.50.25.png?alt=media&#x26;token=1230377c-9a90-44c3-ad33-564eddbca68f" alt=""><figcaption></figcaption></figure>

<figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FkwiGb4pH2pXY8kVP1EBH%2FScreenshot%202025-06-29%20at%2020.51.31.png?alt=media&#x26;token=550e47f5-df8e-4bf0-a5a2-c0f8e46d8340" alt=""><figcaption></figcaption></figure>



</details>
{% endstep %}

{% step %}
#### Sync Permissionless Interface

Once the transaction is confirmed onchain, the Gearbox interface must index the new Configurator.

1. Navigate to the **Instances Page** on the Gearbox UI.
2. Select the relevant chain and click **Sync**.
3. Wait for the sync to complete. The new Market Configurator will appear in the dashboard.

<details>

<summary>UI walkthrough</summary>

On Instances Page click on a chain where you've deployed Market Configurator

<figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2F0i6a7MWauVHrdABhDlqW%2Fimage.png?alt=media&#x26;token=be76ecfe-e927-42c1-9645-978bc33d1238" alt=""><figcaption></figcaption></figure>

Click on a Sync button and wait for Sync to end

<figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FiGHemRXlguvlrfdWh5ta%2FScreenshot%202025-06-29%20at%2020.57.33.png?alt=media&#x26;token=aa2dce2a-4c22-4d04-9465-f1d565e6056b" alt=""><figcaption></figcaption></figure>

</details>
{% endstep %}
{% endstepper %}

### Next Steps

With the Market Configurator deployed, the infrastructure is ready for the first lending Market.
