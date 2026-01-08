# DAO & Curators' business model

### Interest Fee (Revenue from Borrowing)

The **Interest Fee** is the primary revenue source for the protocol and curators. It is a percentage markup applied to the borrowing interest paid by users.

#### How It Works

Unlike some protocols where the protocol fee is subtracted from the yield paid to liquidity providers (a “rake”), Gearbox uses an **additive model**. The fee is added on top of the base interest rate.

* **Base & Collateral-specific Rate**\
  The rate determined by the Interest Rate Model (IRM) plus any collateral-specific adjustments.\
  &#xNAN;_&#x54;his portion is paid entirely to Liquidity Providers._
* **Interest Fee**\
  A percentage markup applied to the Base Rate.\
  &#xNAN;_&#x54;his portion is paid to the Market Curator and the Gearbox DAO._

#### Borrower Rate Formula

$$
Rate_{Borrower} = (Rate_{Base} + Rate_{Collateral-specific}) \times (1 + Fee_{Interest})
$$

#### Example Calculation

If market conditions dictate a base rate of **5%**, and the Curator has configured an Interest Fee of **20%**:

1. **Liquidity Providers earn:** 5.00%
2. **Protocol markup:** 5.00% x 20% = 1.00%&#x20;
3. **Borrower pays:** 6.00%

***

### Revenue Split

By default, all collected Interest Fees are split:

* **50%** → Market Curator
* **50%** → Gearbox DAO

***

***

### Liquidation Economics (Revenue from Risk)

When a Credit Account becomes insolvent, it is liquidated. During liquidation, penalties are applied to the borrower for two purposes:

* Incentivizing liquidators
* Generating protocol revenue

#### Components

| Component               | Recipient     | Purpose                                            |
| ----------------------- | ------------- | -------------------------------------------------- |
| **Liquidation Premium** | Liquidator    | Incentive (“bounty”) for executing the liquidation |
| **Liquidation Fee**     | DAO & Curator | Protocol revenue from the liquidation              |
