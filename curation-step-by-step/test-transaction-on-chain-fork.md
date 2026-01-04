# Verify & Simulate

Before executing any transaction on the mainnet (which costs gas, time and operations), it's better to verify that configuration works as intended.

Gearbox provides a **Simulation Service** (Fork Testing). The system spins up a temporary "Sandbox" copy of the blockchain, applies your changes, and runs a list of tests.

## Automated Safety Checks

The simulation runs a suite of automated checks to ensure your parameters are safe and functional. You should review the output of these tests (typically provided in the GIP report or Interface).

<table><thead><tr><th width="127.28125">Test Category</th><th width="357.36328125">What it checks</th><th>Why it matters</th></tr></thead><tbody><tr><td><strong>Router Paths</strong></td><td>Can the system find a path to swap your new collateral into the underlying asset?</td><td>If this fails, users won't be able to open leveraged positions in a single transactions. Atomic liquidations will also be harmed.</td></tr><tr><td><strong>Insolvency</strong></td><td>Does <code>Collateral Value * Liquidation Threshold</code> cover the debt?</td><td>Ensures there are no errors that allow immediate bad debt.</td></tr><tr><td><strong>Optimistic Liquidation</strong></td><td>Can a liquidator actually sell the collateral on a DEX to repay the debt profitably?</td><td>If liquidity is too low for the configured parameters, the system will flag it.</td></tr><tr><td><strong>State Diff</strong></td><td>Does the simulated blockchain state match your intended configuration?</td><td>Verifies that the transaction data you generated actually does what is expected.</td></tr></tbody></table>

## The "Staging" App (User Experience Test)

Automated tests check the math, but they don't check the experience. The simulation service generates a temporary **Staging Frontend** connected to the Sandbox fork.

**Action:** Open the Staging App link and act as a user.

1. **Connect Wallet:** Use a test wallet (the fork will impersonate your tokens).
2. **Open a Position:** Try to borrow funds using your new strategy.
3. **Execute a Trade:** Try to swap assets or deposit into a vault via the adapter.
4. **Close/Repay:** Ensure you can exit the position.

**After the fork has been created and the tests have passed, you can open the App connected to the test blockchain state.**

<figure><img src="../.gitbook/assets/Screenshot 2025-12-15 at 20.05.34.png" alt=""><figcaption></figcaption></figure>

#### Application test walkthrough

{% embed url="https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FZkcPbFXhP4UHohwnCMF5%2Ffe%20test.mp4?alt=media&token=8c800320-c115-43a3-a612-7c31d1475e34" %}

## Prepare the Main Interface

Once the contracts are deployed, they exist on the blockchain, but the official Gearbox Interface (app.gearbox.finance) may not know the imporant data: token icon, collateral APY, the list of points earned by borrowers or suppliers.

For the tokens and strategies to be supported by the app, ensure that frontend configuration has all the required data: [listing-a-new-asset-in-the-main-app.md](../operational-standards/listing-a-new-asset-in-the-main-app.md "mention")

## Next Steps

If the simulations pass and the UI looks correct, you are ready to execute the transactions onchain.
