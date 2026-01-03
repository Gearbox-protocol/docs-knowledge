# Test transaction on chain fork

## Test config and app on forks

### Automated tests

* Router tests
  * Ensure that adapters are configured correctly and execution paths are found as intended
* Insolvency tests
  * Essential check that ensures that the value of all collateral discounted by liquidation premium is no less than outstanding debt
* Open accounts
  * Test complex interaction, involving executing swaps through adapters and router with leverage and position solvency checks
* Optimistic liquidations
  * Simulate a scenario where accounts become liquidatable and check if atomic liquidations are profitable taken the liquidity profile allowed with adapters
* Market state
  * Compares Market states: the one simulated on backend based on transactions created in curator's app and the one that's present on fork after actual transaction execution

### Test app manually

After the fork setup is complete, you now can test the User-facing interactions in the test app deployment.

<figure><img src="../.gitbook/assets/Screenshot 2025-12-15 at 20.05.34.png" alt=""><figcaption></figcaption></figure>

#### Application test demo

{% embed url="https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FZkcPbFXhP4UHohwnCMF5%2Ffe%20test.mp4?alt=media&token=8c800320-c115-43a3-a612-7c31d1475e34" %}
