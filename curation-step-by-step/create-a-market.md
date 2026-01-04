# Create a Market

### Prerequisites: The Price Feed Check

Before creating a market, the underlying asset (the token you want lenders to deposit) must be whitelisted in the **Price Feed Store** of the current chain.

**Check Availability:**

1. Go to the **Price Feed Store** section in the interface (click on the needed chain on [Instances page](https://permissionless.gearbox.foundation/instances))
2. Search for your target token (e.g., USDC, WETH).
3. **If it exists:** Proceed to the steps below.
4.  **If it is missing:** You must add it first.

    Guide: [add-required-price-feeds.md](../advanced-configuration/add-required-price-feeds.md "mention")

### Configuration Walkthrough

{% embed url="https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FNanWPyWjWeYcVHjUKlJQ%2Fwhole%20flow.mp4?alt=media&token=152a96d8-9927-425c-b657-cbce5669e7b0" %}

## Market Parameters

{% stepper %}
{% step %}
#### Asset & Identity

* **Pool Version:** Select the latest verified version (currently **v3.1**).
* **Underlying Asset:** Select the token lenders will deposit (e.g., USDC).
* **Price Feed:** Select the Oracle feed used to value this asset.
* **Market Name:** A descriptive name for your dashboard (e.g., "USDC Core Market").
{% endstep %}

{% step %}
## Global Capacity (Total Debt Limit)

Max amount of underlying token that can be borrowed from entire pool.

* **Tip:** Setting this higher than your immediate target TVL will help to avoid frequent updates.
* _Note:_ You will set more granular limits for specific strategies later.
{% endstep %}

{% step %}
#### Interest Rate Model (The Cost Engine)

The IRM determines the base borrowing rate based on pool utilization. Gearbox uses a **Two-Kink Model** to create a stable "Optimal Zone" for utilization.

**Key Parameters:**

* **U1 (Optimal Low):** The start of your target utilization range.
* **U2 (Optimal High):** The end of your target utilization range.
* **R\_base:** The interest rate at 0% utilization (The minimum cost of capital).
* **R\_slope1 / R\_slope2:** The rate increase as utilization rises to U1 and U2.
* **R\_slope3 (Penalty):** The sharp rate spike after U2. This forces borrowers to repay if liquidity becomes scarce.

{% hint style="success" %}
**Strategy Tip:** A common approach is to target **80-85% utilization**. Set the borrow rate at this level to be roughly **60-70% of the expected yield** of the collateral strategies. This leaves a healthy spread for borrowers while attracting lenders.\
\{% endhint %\}
{% endhint %}

{% hint style="warning" %}
**Important: The Curator Fee is additive.**\
The Interest Fee (curator's & DAO's revenue) is charged **on top** of the rate paid to lenders.

_Example:_ If the IRM rate is **5%** and your Interest Fee is **20%**, the borrower pays **6%** total (5% to LPs + 1% Fee). Ensure your IRM leaves room for this markup while remaining competitive.
{% endhint %}

* _**Reference:**_
  * [Desmos IRM visualizer](https://www.desmos.com/calculator/d281eeb4a9)
  * [Mainnet ETH pool](https://app.gearbox.fi/pools/0xda0002859b2d05f66a753d8241fcde8623f26f4f/utilization)
  * [Mainnet USDC pool](https://app.gearbox.fi/pools/0xda00000035fef4082f78def6a8903bee419fbf8e)
{% endstep %}

{% step %}
## Rate Governance (The "Tumbler")

This determines how you manage **Collateral-Specific Rates** (add-on fees for specific collaterals of increased demand).

* **Type:** Select **Tumbler**. This allows the Risk Curator to manually update rates as needed.
* **Epoch Length:** The mandatory waiting period between rate updates.
  * _Example:_ If set to **2 days**, you can only adjust rates once every 48 hours. This gives borrowers predictability.
{% endstep %}

{% step %}
#### Safety (Loss Policy)

This defines the logic for handling "Bad Debt" (when a position is insolvent even after liquidation).

* **Policy Type:** Select **Aliased**.
* **Function:** This protects Liquidity Providers during market de-pegs. If the market price of a collateral crashes (e.g., a flash crash), the system can switch to a "Fundamental Price" (e.g., Exchange Rate) to prevent selling collateral at a massive loss, effectively pausing liquidations until the market stabilizes.
{% endstep %}
{% endstepper %}

### Next Steps

The Liquidity Pool is now deployed. However, users cannot borrow yet because there are no **Strategies** (Credit Managers) attached to it.
