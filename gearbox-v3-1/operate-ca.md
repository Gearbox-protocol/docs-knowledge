# Operate with Credit Account

When using credit accounts, users should track several metrics that govern how a position behaves:

## Total Value:
  - Value of collateral tokens admallowed itted in the pool (tokens with a quota limit and LT)
  - Measured in the underlying token
  - **Influenced by:**
    - Collateral prices
    - Underlying token price
  - **Formula:** $Total Value = \frac{\sum_{i}^{MaxEnabledTokens}{CollateralBalance_i \times CollateralOraclePrice_i}}{UnderlyingOraclePrice}$
  - Rewards earned in collateral may or may not appear in Total Value. Some rewards auto-compound into collateral price (e.g. sUSDe), others accrue separately (e.g. CRV rewards for Curve LP tokens) and may not be properly priced
## Debt
  - Amount of underlying borrowed
  - **Influenced by:**
    - Borrowed principal
    - Accrued interest
  - Grows over time from interest accrual
## Quota
  - Measured in the underlying token
  - Portion of account debt that a specific collateral may secure
  - Adjustable by the account owner
## Total Weighted Value
  - Primary measure for overcollateralization of the account
  - Measured in the underlying token 
  - **Influenced by:**
    - Collateral prices
    - Underlying price
    - Collateral LT
    - Quota activated for each collateral in the account
  - **Formula:** $TWV = \frac{\sum_{i}^{MaxEnabledTokens}{\min{(Quota_i,LT_i \times CollateralBalance_i \times CollateralOraclePrice_i)}}}{UnderlyingOraclePrice}$
## Health Factor
  - **Formula:** $HF = \frac{TWV}{Debt}$
## Liquidation Premium
  - Portion of collateral the account forfeits on liquidation
