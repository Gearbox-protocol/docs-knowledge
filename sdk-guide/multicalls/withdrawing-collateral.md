# Withdrawing Collateral

Remove tokens from your Credit Account.

> For Solidity implementation, see [Withdrawing Collateral](../../solidity-guide/multicalls.md#withdrawing-collateral).

## Why

You withdraw collateral when:

- **Taking profit** - Extract gains while keeping the position open
- **Rebalancing** - Move assets between Credit Account and wallet
- **Closing positions** - Extract remaining value after repaying debt
- **Emergency exit** - Quickly reduce exposure

Withdrawals decrease your health factor since you're removing value from the account.

## What

`withdrawCollateral` transfers tokens from Credit Account to a specified address:

1. Token is transferred from Credit Account to `to` address
2. If balance goes to zero, token is auto-disabled
3. **Safe pricing** is triggered for the final collateral check

**Safe pricing** is critical to understand: when any withdrawal occurs in a multicall, the final health check uses `min(mainPrice, reservePrice)` for ALL collateral. This can cause withdrawals to fail even when the account looks healthy based on main prices alone.

## How

```typescript
import { GearboxSDK, createCreditAccountService } from '@gearbox-protocol/sdk';

const sdk = await GearboxSDK.attach({ client, marketConfigurators: [] });
const service = createCreditAccountService(sdk, 310);
const market = sdk.marketRegister.findByCreditManager(cmAddress);

// Withdraw 5,000 USDC to your wallet
const calls = [
  service.prepareWithdrawCollateral(
    usdcAddress,
    5_000n * 10n ** 6n,
    myWalletAddress,
  ),
];

await market.creditFacade.write.multicall([creditAccountAddress, calls]);
```

### Withdraw Entire Balance

Pass max uint256 to withdraw all of a token:

```typescript
const MAX_UINT256 = 2n ** 256n - 1n;

const calls = [
  service.prepareWithdrawCollateral(usdcAddress, MAX_UINT256, myWalletAddress),
];
```

### Withdraw to Different Address

The `to` parameter can be any address:

```typescript
const calls = [
  service.prepareWithdrawCollateral(
    usdcAddress,
    amount,
    recipientAddress, // Can be different from caller
  ),
];
```

### Common Pattern: Repay + Withdraw

After repaying debt, withdraw remaining funds:

```typescript
const MAX_UINT256 = 2n ** 256n - 1n;
const INT96_MIN = BigInt.asIntN(96, -1n * 2n ** 95n);

const calls = [
  // Zero quotas
  service.prepareUpdateQuota(wethAddress, INT96_MIN, 0n),
  // Repay all debt
  service.prepareDecreaseDebt(MAX_UINT256),
  // Withdraw remaining collateral
  service.prepareWithdrawCollateral(usdcAddress, MAX_UINT256, myWalletAddress),
  service.prepareWithdrawCollateral(wethAddress, MAX_UINT256, myWalletAddress),
];
```

## Gotchas

### Safe Pricing Can Block Withdrawals

This is the biggest surprise for developers. When you withdraw, ALL collateral is valued at `min(mainPrice, reservePrice)`:

```
Regular check:  collateral valued at main price
Withdrawal:     collateral valued at min(main, reserve)
```

An account that looks healthy at main prices may fail the withdrawal check at safe prices.

**Example:**
- Main price: $100
- Reserve price: $80
- Regular health check uses $100
- Withdrawal health check uses $80

Your account might have HF 1.2 normally but only HF 0.96 under safe pricing.

**Workaround:** Add extra collateral buffer or reduce debt before withdrawing if you're close to the threshold.

### Forbidden Tokens Block Withdrawals

If your account has forbidden tokens enabled, withdrawals are prohibited. You must disable forbidden tokens first (usually by swapping them away).

### Token Auto-Disables at Zero Balance

When you withdraw the entire balance of a token:
- Non-quota tokens are auto-disabled
- Quota tokens remain enabled until quota is zeroed

This is usually what you want, but be aware if you're tracking enabled tokens.

### Reserve Price May Be Zero

Some tokens have a reserve price of zero (untrusted tokens). Any withdrawal will fail if such tokens are enabled, because their value becomes zero under safe pricing.

Check the price feed configuration before withdrawing:

```typescript
// If reserve price is 0, safe pricing makes this collateral worthless
const priceFeed = await priceOracle.read.priceFeedsRaw([tokenAddress, true]);
```

### Withdrawal Doesn't Auto-Disable Quota Tokens

Unlike non-quota tokens, quota tokens remain enabled even at zero balance. You must explicitly zero the quota:

```typescript
const MAX_UINT256 = 2n ** 256n - 1n;
const INT96_MIN = BigInt.asIntN(96, -1n * 2n ** 95n);

const calls = [
  // Zero quota first
  service.prepareUpdateQuota(wethAddress, INT96_MIN, 0n),
  // Then withdraw
  service.prepareWithdrawCollateral(wethAddress, MAX_UINT256, myWalletAddress),
];
```

### Can't Withdraw Below Minimum Debt

After withdrawal, your account must still satisfy debt constraints. If withdrawal would leave you with debt between 0 and `minDebt`, it fails.

## See Also

- [Adding Collateral](./adding-collateral.md) - The reverse operation
- [Debt Management](./debt-management.md) - Often combined with withdrawals
- [Updating Quotas](./updating-quotas.md) - Zero quotas before withdrawing quota tokens
