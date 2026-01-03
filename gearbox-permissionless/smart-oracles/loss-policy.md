# Loss policy

## Loss policy: if you chose to use Market prices

Using market oracles can sometimes trigger liquidation cascades, where a rapid price drop causes mass liquidations and further depresses the asset’s price. An example is the [ezETH cascading liquidations in April 2024](https://protos.com/depeg-of-3b-restaking-token-ezeth-causes-over-60m-in-defi-liquidations/).

<figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FvLBAJy4BkD0dgDGr0GHY%2Fimage.png?alt=media&#x26;token=8bf0df44-378a-4b67-ad15-16d0efdb1b8e" alt=""><figcaption></figcaption></figure>

When prices fall too quickly, liquidators may be unable to react in time. As a result, positions can become insolvent before liquidation completes. In such scenarios, continuing to liquidate at the current market price may actually create bad debt, because collateral can be sold far below its fair or medium-term value.

To protect liquidity providers (LPs) in these situations, Gearbox implements a Loss Policy mechanism.

**The logic is as follows:**

1. Positions are liquidated using market prices under normal conditions.
2. If a liquidation would create bad debt, the protocol reprices the collateral using the aliased price, which can be configured to the asset’s fundamental value, and halts the liquidation if the position is healthy under this pricing.

<figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2F7hbEfHnQ0j2k7pKazlHo%2FGearbox%20protocol%20-%20Frame%207.jpg?alt=media&#x26;token=519ef1c8-a128-4ae0-8e9f-09e5f16baf2b" alt=""><figcaption></figcaption></figure>
