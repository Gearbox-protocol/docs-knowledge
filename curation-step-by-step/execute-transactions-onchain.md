# Execute transactions onchain

This is the final step. With the market configured, parameters verified, and user experience tested, the changes are ready to be pushed to the live blockchain.

### The Timelock Lifecycle

Gearbox governance enforces a **24-hour Timelock** on all critical changes. This security feature provides users time to exit if they disagree with a parameter change.

Deployment consists of two distinct actions:

1. **Queue (Propose):** Submit the transaction to the Timelock contract. The 24-hour countdown begins.
2. **Execute (Apply):** After the countdown ends, submit a second transaction to apply the changes.

{% stepper %}
{% step %}
### Finalize the Proposal

Navigate to the GIP page in the interface.

1. **Finalize:** Click **"Finalize GIP"**. This locks the configuration and prepares the transaction data.
2. **Set Earliest Execution Date:**
   * The default timelock is 24 hours.
   * **Calculation:** `Current Time + Signing Buffer + 24 Hours`.
   * _Recommendation:_ Add a buffer (e.g., 2 hours) to allow sufficient time for collecting signatures from multisig signers before the target execution time.

{% hint style="info" %}
**Troubleshooting:** If last-minute edits are required, click **"Reopen for Changes"**. Re-finalization is required after editing.
{% endhint %}

<figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2F24yEaWE95fs8ybIDXpVA%2FScreenshot%202025-08-08%20at%2011.43.06.png?alt=media&#x26;token=f028e511-124d-459b-8856-d566f5f24205" alt=""><figcaption></figcaption></figure>
{% endstep %}

{% step %}
## Queue the Transaction

The interface generates a link to the **Permissionless Safe App**.

1. Click the link to open the Safe App.
2. **Sign & Submit:** Execute the transaction in the Safe. This initiates the onchain timer.

<figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2F4kDyE6zSErpHqIpAhTA0%2FScreenshot%202025-09-26%20at%2016.28.03.png?alt=media&#x26;token=7876a881-e702-4c4a-a103-eca852895b3d" alt=""><figcaption></figcaption></figure>

### Video walkthrough

{% embed url="https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2Fyb33s6xLnXsLKLpRTyWw%2Fgip%20finalization.mp4?alt=media&token=02949fc6-5b9b-42f0-9926-da454ee91015" %}
{% endstep %}

{% step %}
## Execute (After 24 Hours)

Once the timelock expires:

1. Return to the **Permissionless Safe App**.
2. **Sign & Submit:** Execute the final transaction.

### Video walkthrough

{% embed url="https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FD996Q64luHv4QiwGPr9o%2FScreen%20Recording%202025-09-26%20at%2016.22.38.mp4?alt=media&token=560c82f9-1526-4a0e-b9f7-e7db93e75534" %}
{% endstep %}
{% endstepper %}

<details>

<summary>Learn more: Transaction lifecycle details</summary>

<figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FEk1eobdHV2qeeJ9y85hP%2Ftimeline.jpg?alt=media&#x26;token=ffc0d09b-dfc0-4e6c-9fe1-f33a92f72c70" alt=""><figcaption></figcaption></figure>

</details>

### Deployment Complete

The market is now live on the blockchain.

* **New Pools:** Lenders can deposit assets.
* **New Strategies:** Borrowers can open Credit Accounts.

**Requirement:** Ensure the frontend PRs have been merged so users can view the new market and strategies in the app.

* Review [frontend listing guide](../operational-standards/listing-a-new-asset-in-the-main-app.md).
