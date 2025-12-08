# Key operations with Credit Account

User can directly control the core Credit Account's metrics via Multicalls (read more about [Key Metrics](./account-metrics.md)).

> Multicall is a method which allowes to batch multiple onchain actions into one transaction.  
> e.g. one transaction can add collateral, claim rewards, swap tokens and repay debt.  
> For a techinical reference please see [Multicalls]().

## Modify Debt
- Increase Debt
  - Decreases HF
  - Can cause liquidation
  - Can't be performed if forbidden token is on account
  - The resulting debt amount must be within allowed limits
- Decrease Debt
  - The resulting debt amount must be either zero or above allowed minimum

## Operate with Collateral
- Add Collateral
  - Only the underlying token counts towards account's collateral value by default, while all other tokens must be enabled as collateral by activating quota for it. Holding non-enabled token on account with non-zero debt poses a risk of losing it entirely to the liquidator.
- Withdraw Collateral
  - Can't be performed if forbidden token is on account
  - Can be blocked if Reserve Price Feed returns price lower than Main

## Perform external calls
  - Can't be performed if forbidden token is on account
  - Can be blocked if Reserve Price Feed returns price lower than Main

## Operate with quota
Enables token as collateral if quota is increased from zero, disables if decreased to zero
Quota increase is prohibited for forbidden tokens
