# Execute transactions onchain

After the changes in GIP were tested and are ready to be executed onchain, go to the GIP page and click "Finalize GIP".

{% hint style="info" %}
If the only button you see is "Reopen for Changes", click it and you will be able to finalize the GIP again.
{% endhint %}

<figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2F24yEaWE95fs8ybIDXpVA%2FScreenshot%202025-08-08%20at%2011.43.06.png?alt=media&#x26;token=f028e511-124d-459b-8856-d566f5f24205" alt=""><figcaption></figcaption></figure>

#### How to set Earliest Execution Date?

The default timelock is 24h, so you need to get signatures in Owner Multisig before **Earliest Execution Date - 24h.**

E.g. if it takes 2h for you to get needed signatures, set **Earliest Execution Date** to _**current time + 2h + 24h.**_

### Executing with Gearbox open-sourced Safe Permissionless UI

After finalizing the batch link to the Safe UI with prepared txs will appear.

<figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2F4kDyE6zSErpHqIpAhTA0%2FScreenshot%202025-09-26%20at%2016.28.03.png?alt=media&#x26;token=7876a881-e702-4c4a-a103-eca852895b3d" alt=""><figcaption></figcaption></figure>

{% hint style="success" %}
[Permissionless Safe](https://docs.gearbox.fi/gearbox-permissionless-doc/competitive-advantages/essential-tooling-for-curators#permissionless-safe) is an open-source, IPFS-hosted version of the Safe Multisig UI designed to review and sign transactions securely in a human-readable format. It eliminates backend dependencies to mitigate risks like Bybit-type attacks and performs checks of IPFS CID signature to prevent phishing.
{% endhint %}

#### Transactions' lifecycle

<figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FEk1eobdHV2qeeJ9y85hP%2Ftimeline.jpg?alt=media&#x26;token=ffc0d09b-dfc0-4e6c-9fe1-f33a92f72c70" alt=""><figcaption></figcaption></figure>

## Queue transactions (start timelock countdown)

{% embed url="https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2Fyb33s6xLnXsLKLpRTyWw%2Fgip%20finalization.mp4?alt=media&token=02949fc6-5b9b-42f0-9926-da454ee91015" %}

## Execute transactions (apply changes onchain after the timelock)

{% embed url="https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FD996Q64luHv4QiwGPr9o%2FScreen%20Recording%202025-09-26%20at%2016.22.38.mp4?alt=media&token=560c82f9-1526-4a0e-b9f7-e7db93e75534" %}
