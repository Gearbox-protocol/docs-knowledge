# Claim accrued fees

Unclaimed fees sit in the protocol and act as a first line of defense against bad debt. If a liquidation results in a loss, the protocol can burn these accrued fees to cover the deficit before touching the Liquidity Pool.

{% stepper %}
{% step %}
## Initiate a Proposal

Navigate to the **Permissionless Interface**.

1. Click **"New GIP"** (or select an existing draft).
2. Select the **Market** you want to claim fees from.

Then select a market you want to claim fees for.
{% endstep %}

{% step %}
## Add Distribution Action

1. Go to the **Details** tab of the Market.
2. Locate the **Accrued Fees** section.
3. Click the **"Distribute"** button.

* _Note:_ This adds a transaction to your GIP batch. It does not execute immediately.

<figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FIkJWNcNtUKO2syDyehvp%2FScreenshot%202025-09-29%20at%2013.05.53.png?alt=media&#x26;token=3eec1e97-e4df-412a-8805-b60d7958e53c" alt=""><figcaption></figcaption></figure>
{% endstep %}

{% step %}
## Execute via Timelock

Like all governance actions, claiming fees is subject to the standard proposal lifecycle.

1. **Finalize** the GIP.
2. **Queue** the transaction in your Safe (starts the 24h timelock).
3. **Execute** the transaction after the timelock expires.

Once executed, the funds will appear in your Fee Collector wallet.
{% endstep %}
{% endstepper %}

