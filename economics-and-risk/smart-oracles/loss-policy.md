# Loss Policy

### The Problem: Market Price Cascades

Using market oracles can sometimes trigger liquidation cascades, where a rapid price drop causes mass liquidations and further depresses the asset’s price. An example is the [ezETH cascading liquidations in April 2024](https://www.google.com/url?sa=E\&q=https%3A%2F%2Fprotos.com%2Fdepeg-of-3b-restaking-token-ezeth-causes-over-60m-in-defi-liquidations%2F).

<figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FvLBAJy4BkD0dgDGr0GHY%2Fimage.png?alt=media&#x26;token=8bf0df44-378a-4b67-ad15-16d0efdb1b8e" alt=""><figcaption></figcaption></figure>

When prices fall too quickly, liquidators may be unable to react in time. As a result, positions can become insolvent before liquidation completes. In such scenarios, continuing to liquidate at the current market price may actually create bad debt, because collateral can be sold far below its fair or medium-term value.

### The Solution: Aliased Pricing

To protect liquidity providers (LPs) in these situations, Gearbox implements a Loss Policy mechanism.

**The logic is as follows:**

1. Positions are liquidated using market prices under normal conditions.
2. If a liquidation would create bad debt (Collateral Value < Debt), the protocol reprices the collateral using the **aliased price**, which can be configured to the asset’s fundamental value (e.g., Exchange Rate or 1.00 for stablecoins).
3. If the position is healthy under this fundamental pricing, the liquidation is halted.

<figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2F7hbEfHnQ0j2k7pKazlHo%2FGearbox%20protocol%20-%20Frame%207.jpg?alt=media&#x26;token=519ef1c8-a128-4ae0-8e9f-09e5f16baf2b" alt=""><figcaption></figcaption></figure>

### Execution Flow

The Loss Policy acts as a conditional circuit breaker during the liquidation process.

1. **Standard Check:** Is Health Factor < 1 using the **Main Feed** (Market Price)?
   * **No:** Account is healthy. Do nothing.
   * **Yes:** Proceed to step 2.
2. **Bad Debt Check:** Does `Collateral Value < Debt`?
   * **No:** Liquidation proceeds normally. Liquidator repays debt and claims collateral.
   * **Yes:** The liquidation is flagged as a "Loss Liquidation". Proceed to step 3.
3. **Fundamental Check:** Is Health Factor < 1 using the **Aliased Feed** (Fundamental Price)?
   * **No:** The protocol assumes the market price is temporarily dislocated (flash crash). Liquidation is blocked to prevent realizing the loss at a distressed price.
   * **Yes:** The asset is fundamentally insolvent. Liquidation proceeds.

#### Learn More

* **Bad debt acknowledgment:** What happens when a liquidation proceeds under the Loss Policy and bad debt is realized?
  * [liquidation-dynamics.md](../liquidation-dynamics.md "mention")
