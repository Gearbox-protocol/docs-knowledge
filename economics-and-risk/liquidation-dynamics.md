# Liquidation Dynamics

The solvency of a Credit Account is determined deterministically on-chain. If an account's risk-adjusted value falls below its liabilities, the protocol enforces liquidation to protect liquidity providers.

### Solvency Definition: The Health Factor

The core metric for solvency is the **Health Factor (HF)**.

$$
HF = \frac{TWV}{Total Debt}
$$

Where:

* **TWV (Total Weighted Value):** The risk-adjusted, quota-limited value of the collateral assets, measured in the underlying token.
* **Total Debt:** The total amount of underlying token owed, including principal, accrued interest, and quota interest.

#### Total Weighted Value (TWV)

TWV represents the maximum debt the current collateral portfolio can support. Unlike standard Net Asset Value, Gearbox discounts collateral based on its **Liquidation Threshold (LT)** and caps it by the **Quota** allocated to that asset.

$$
TWV = \frac{\sum_{i}^{MaxEnabledTokens}{\min{(Quota_i, Balance_i \times Price_i \times LT_i)}}}{Price_{underlying}}
$$

* **Quota\_i**: The specific portion of the account's debt limit allocated to token i.
* **Balance\_i**: The balance of token i in the Credit Account.
* **Price\_i**: The current oracle price of token i.
* **LT\_i**: The Liquidation Threshold for token i.
* **Price\_{underlying}**: The current oracle price of the underlying borrowed asset.

> **Note:** The `min` function ensures that a specific collateral asset cannot secure more debt than its allocated Quota allows, regardless of its market value.

#### Liquidation Condition

An account is liquidatable if:

1. **HF < 1**: The TWV is less than the Total Debt.
2. **Expiration**: The Credit Manager has reached its maturity date (for fixed-term strategies).

### Partial Liquidation (Deleverage)

To prevent total loss of user positions during minor market dips, the protocol supports **Partial Liquidation**. This mechanism sells only enough collateral to restore the Health Factor to a safe level, rather than closing the entire position.

This process is typically executed by a specialized Deleverage Bot.

#### Execution Logic

When HF drops below a configured `minHF` (but is typically still > 1), the bot executes a deleveraging transaction:

1. Calculates the amount of collateral required to be sold to raise HF to `targetHF`.
2. Repays a portion of the debt.
3. Charges a reduced premium compared to full liquidation.

#### Configuration Parameters

| Parameter        | Description                                                                             |
| ---------------- | --------------------------------------------------------------------------------------- |
| **minHF**        | The threshold triggering partial liquidation (e.g., 1.05).                              |
| **maxHF**        | The target Health Factor after deleveraging.                                            |
| **PremiumScale** | The percentage of the full Liquidation Premium charged (e.g., 50% of standard premium). |

### Full Liquidation

If Partial Liquidation is insufficient or if HF drops significantly below 1, a **Full Liquidation** occurs. The liquidator repays the total debt and claims the collateral assets at a discount.

#### Total Value Calculation

Liquidation math relies on the **Total Value** of the account (undiscounted NAV), measured in the underlying token.

$$
Total Value = \frac{\sum_{i}^{MaxEnabledTokens}{Balance_i \times Price_i}}{Price_{underlying}}
$$

#### Liquidator Incentive

The liquidator receives the collateral assets valued at a discount (the Liquidation Premium).

$$
LiquidatorProfit = TotalValue \times LiquidationPremium - GasCost
$$

#### Borrower Loss

The borrower loses the collateral used to pay the debt, the premium, and the protocol fee.

$$
AccountLoss = \min(TotalValue \times (LiquidationPremium + LiquidationFee), TotalValue - Total Debt)
$$

* **Liquidation Premium:** Paid to the liquidator.
* **Liquidation Fee:** Paid to the Protocol (Curator & DAO).

### Bad Debt & Socialization

**Bad Debt** occurs when a Credit Account is liquidated while its **Total Value** is less than its **Total Debt**.

#### Resolution Mechanism

1. **Fee Buffer:** Unclaimed protocol fees (Curator/DAO share) are burned to cover the deficit.
2. **Socialization:** If fees are insufficient, the remaining loss is socialized among Liquidity Providers by reducing the exchange rate of the Diesel Token (LP token).

### Further Reading

* **Data Sources:** How the protocol obtains asset prices for TWV calculations.
  * See: Price Oracle
* **Parameter Control:** Who sets the $LT$, Premiums, and Fees.
  * See: Risk Configuration Dictionary
* **Quota Mechanics:** How Quota limits are defined and adjusted.
  * See: Quota Limits & Concentration
