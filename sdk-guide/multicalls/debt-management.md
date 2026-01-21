# Debt Management

Borrow from or repay to the pool.

> For Solidity implementation, see [Debt Management](../../solidity-guide/multicalls.md#debt-management).

## Why

You manage debt when:

- **Increasing leverage** - Borrow more to amplify exposure
- **Taking profit** - Repay debt while keeping collateral positions
- **Reducing risk** - Lower debt to improve health factor
- **Closing account** - Repay all debt before withdrawal

Debt operations affect your health factor: borrowing decreases it, repaying increases it.

## What

### Increase Debt

`increaseDebt` borrows the underlying asset from the pool to your Credit Account:

1. Pool transfers underlying to Credit Account
2. Debt parameters (principal + interest) are recalculated
3. Health factor decreases

### Decrease Debt

`decreaseDebt` repays debt from Credit Account's underlying balance:

1. Underlying is transferred from Credit Account to pool
2. Debt parameters are recalculated
3. Health factor increases

**Repayment order** (when not paying full debt):
1. Quota-related fees (quota increase fees)
2. Accrued quota interest
3. Interest + interest fee (split pro-rata if partial)
4. Principal

This means partial payments may not reduce your principal at all.

## How

### Borrow More

```typescript
import { GearboxSDK, createCreditAccountService } from '@gearbox-protocol/sdk';

const sdk = await GearboxSDK.attach({ client, marketConfigurators: [] });
const service = createCreditAccountService(sdk, 310);
const market = sdk.marketRegister.findByCreditManager(cmAddress);

const calls = [
  service.prepareIncreaseDebt(40_000n * 10n ** 6n), // Borrow 40,000 USDC
];

await market.creditFacade.write.multicall([creditAccountAddress, calls]);
```

### Repay Debt

```typescript
const calls = [
  service.prepareDecreaseDebt(10_000n * 10n ** 6n), // Repay 10,000 USDC
];

await market.creditFacade.write.multicall([creditAccountAddress, calls]);
```

### Repay All Debt

Pass `type(uint256).max` equivalent to repay everything:

```typescript
const MAX_UINT256 = 2n ** 256n - 1n;

const calls = [
  // Zero all quotas FIRST (required before full repayment)
  service.prepareUpdateQuota(quotedToken1, BigInt.asIntN(96, -1n * 2n ** 95n), 0n),
  service.prepareUpdateQuota(quotedToken2, BigInt.asIntN(96, -1n * 2n ** 95n), 0n),
  // Then repay all debt
  service.prepareDecreaseDebt(MAX_UINT256),
];

await market.creditFacade.write.multicall([creditAccountAddress, calls]);
```

### Common Pattern: Add Collateral + Borrow

```typescript
const calls = [
  // First add collateral
  service.prepareAddCollateral(usdcAddress, 10_000n * 10n ** 6n),
  // Then borrow (5x leverage)
  service.prepareIncreaseDebt(40_000n * 10n ** 6n),
  // Set quota for destination token
  service.prepareUpdateQuota(wethAddress, 50_000n * 10n ** 6n, 50_000n * 10n ** 6n),
];

// Don't forget approval to Credit Manager!
await usdcContract.write.approve([market.creditManager.address, 10_000n * 10n ** 6n]);

await market.creditFacade.write.openCreditAccount([ownerAddress, calls, 0n]);
```

## Gotchas

### One Debt Update Per Block

You cannot increase AND decrease debt in the same block. This constraint prevents manipulation:

```typescript
// WRONG - will revert on second operation
const calls = [
  service.prepareIncreaseDebt(amount1),
  service.prepareDecreaseDebt(amount2), // Reverts!
];

// CORRECT - one multicall, one debt operation
const calls = [
  service.prepareIncreaseDebt(netAmount),
];
```

### Zero All Quotas Before Full Repayment

Non-zero quotas with zero debt is an invalid state. Zero your quotas BEFORE the final debt repayment:

```typescript
const INT96_MIN = BigInt.asIntN(96, -1n * 2n ** 95n);

const calls = [
  // Zero quotas first
  service.prepareUpdateQuota(token1, INT96_MIN, 0n),
  service.prepareUpdateQuota(token2, INT96_MIN, 0n),
  // Then full repayment
  service.prepareDecreaseDebt(MAX_UINT256),
];
```

### Debt Must Stay in Range

After any debt change, the principal must be either:
- Zero (fully repaid), OR
- Within `[minDebt, maxDebt]` range

You cannot have debt between 0 and `minDebt`.

### Forbidden Tokens Block Borrowing

If your account has forbidden tokens enabled as collateral, you cannot increase debt. Disable them first.

### Interest Accrues Continuously

When repaying "the full amount", the debt may have grown since you read it. Add a buffer:

```typescript
// Read current total debt
const accountData = await service.getCreditAccountData(creditAccountAddress);
const totalDebt = accountData.debt;

// Add 0.1% buffer for interest accrual
const repayAmount = totalDebt + (totalDebt / 1000n);

// Or just use MAX_UINT256 to repay whatever the current amount is
const calls = [service.prepareDecreaseDebt(MAX_UINT256)];
```

### Cannot Decrease on Open / Increase on Close

- `decreaseDebt` is prohibited when opening an account
- `increaseDebt` is prohibited when closing an account

This prevents gaming the system by borrowing during liquidation or repaying during account creation.

## See Also

- [Updating Quotas](./updating-quotas.md) - Quota interest affects total debt
- [Adding Collateral](./adding-collateral.md) - Often combined with borrowing
- [Withdrawing Collateral](./withdrawing-collateral.md) - Often combined with repaying
