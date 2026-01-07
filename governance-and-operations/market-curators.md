# Market Curators

## What is Curator

Curator is a set of Chain-specific addresses which have access to modify key parameters of lending markets controlled by them.

<figure><img src="../.gitbook/assets/image (9).png" alt=""><figcaption></figcaption></figure>

### Curation Roles

*   **Admin**

    Can modify all configurable parameters, subject to a minimum 24-hour timelock.
*   **Emergency Admin**

    Can update a limited set of risk parameters without a timelock in emergency situations.
*   **Pausable Admin**

    Can pause market contracts, freezing most protocol operations.
*   **Unpausable Admin**

    Can unpause market contracts and restore normal operations.
*   **Fee Multisig**

    Can modify fee-sharing rules.
*   **Emergency Liquidator**

    Can liquidate accounts when contracts are paused.
*   **Loss Liquidator**

    Can liquidate accounts in scenarios where liquidation creates bad debt.
