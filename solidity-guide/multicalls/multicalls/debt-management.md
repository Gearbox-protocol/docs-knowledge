# Debt Management

Borrow and repay the underlying token.

> For SDK implementation, see [Debt Management](../../../sdk-guide-typescript/multicalls/multicalls/debt-management.md).

## Why

Debt management enables leveraged positions:

* **Increase debt** - Borrow to deploy capital into DeFi strategies
* **Decrease debt** - Repay to reduce interest costs or close position
* **Partial repayment** - Reduce exposure while keeping position open

Debt directly affects your health factor. Higher debt lowers health factor; lower debt raises it.

## What

Two operations manage debt:

| Operation      | Description                           |
| -------------- | ------------------------------------- |
| `increaseDebt` | Borrow underlying token from the pool |
| `decreaseDebt` | Repay underlying token to the pool    |

### Increase Debt Flow

1. Pool transfers underlying to Credit Account
2. Debt counter incremented
3. Interest starts accruing immediately

### Decrease Debt Flow

1. Underlying transferred from Credit Account to pool
2. Debt counter decremented
3. Full repayment enables special "zero debt" mode

## How

### Borrowing

```solidity
import {ICreditFacadeV3Multicall} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditFacadeV3Multicall.sol";
import {MultiCall} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditFacadeV3.sol";

address creditFacade;
address creditAccount;

MultiCall[] memory calls = new MultiCall[](1);

// Borrow 40,000 USDC
calls[0] = MultiCall({
    target: creditFacade,
    callData: abi.encodeCall(
        ICreditFacadeV3Multicall.increaseDebt,
        (40_000 * 10**6)
    )
});

ICreditFacadeV3(creditFacade).multicall(creditAccount, calls);
```

### Repaying

```solidity
// Repay 10,000 USDC
calls[0] = MultiCall({
    target: creditFacade,
    callData: abi.encodeCall(
        ICreditFacadeV3Multicall.decreaseDebt,
        (10_000 * 10**6)
    )
});

// Or repay everything
calls[0] = MultiCall({
    target: creditFacade,
    callData: abi.encodeCall(
        ICreditFacadeV3Multicall.decreaseDebt,
        (type(uint256).max)  // Full repayment
    )
});
```

### Combined Strategy: Add Collateral + Borrow

Typical account opening pattern:

```solidity
MultiCall[] memory calls = new MultiCall[](2);

// 1. Add initial collateral
calls[0] = MultiCall({
    target: creditFacade,
    callData: abi.encodeCall(
        ICreditFacadeV3Multicall.addCollateral,
        (usdc, 10_000 * 10**6)  // 10k USDC as collateral
    )
});

// 2. Borrow against it
calls[1] = MultiCall({
    target: creditFacade,
    callData: abi.encodeCall(
        ICreditFacadeV3Multicall.increaseDebt,
        (40_000 * 10**6)  // Borrow 40k USDC (4x leverage)
    )
});

// Approve collateral to Credit Manager first
IERC20(usdc).approve(creditManager, 10_000 * 10**6);

// Open account with collateral and debt
ICreditFacadeV3(creditFacade).openCreditAccount(owner, calls, 0);
```

## Gotchas

### Same-Block Restriction

Debt cannot be increased AND decreased in the same block:

```solidity
// Block N: increase debt
ICreditFacadeV3(creditFacade).multicall(account, increaseCalls);

// Block N: try to decrease - REVERTS!
ICreditFacadeV3(creditFacade).multicall(account, decreaseCalls);

// Block N+1: now decrease works
ICreditFacadeV3(creditFacade).multicall(account, decreaseCalls);
```

### Debt Limits

The resulting debt must be within configured limits:

```solidity
(uint128 minDebt, uint128 maxDebt) = ICreditFacadeV3(creditFacade).debtLimits();

// Debt after operation must satisfy:
// 0 (for full closure) OR minDebt <= debt <= maxDebt
```

### Per-Block Borrowing Limit

Total borrowing in a block is limited:

```solidity
uint8 multiplier = ICreditFacadeV3(creditFacade).maxDebtPerBlockMultiplier();
// maxDebtPerBlock = maxDebt * multiplier

// If block limit reached, increaseDebt reverts
```

### Forbidden Tokens Block Borrowing

If account has forbidden tokens enabled as collateral, borrowing is blocked:

```solidity
// This reverts if account has forbidden tokens
ICreditFacadeV3Multicall.increaseDebt(amount);
```

Solution: Swap forbidden tokens to allowed ones first.

### Zero Debt Mode

Full repayment (`decreaseDebt(type(uint256).max)`) enables zero debt mode:

* Collateral checks are skipped
* All quotas must be disabled (zero)
* Account can be closed without collateral check

```solidity
MultiCall[] memory calls = new MultiCall[](2);

// 1. Disable all quotas first
calls[0] = MultiCall({
    target: creditFacade,
    callData: abi.encodeCall(
        ICreditFacadeV3Multicall.updateQuota,
        (quotedToken, type(int96).min, 0)  // Disable quota
    )
});

// 2. Full repayment
calls[1] = MultiCall({
    target: creditFacade,
    callData: abi.encodeCall(
        ICreditFacadeV3Multicall.decreaseDebt,
        (type(uint256).max)
    )
});
```

### Opening vs Closing Restrictions

| Operation      | On Open    | On Close   |
| -------------- | ---------- | ---------- |
| `increaseDebt` | Allowed    | Prohibited |
| `decreaseDebt` | Prohibited | Allowed    |

```solidity
// Opening: can only borrow
openCreditAccount(owner, [increaseDebtCall], 0);  // OK
openCreditAccount(owner, [decreaseDebtCall], 0);  // REVERTS

// Closing: can only repay
closeCreditAccount(account, [decreaseDebtCall]);  // OK
closeCreditAccount(account, [increaseDebtCall]); // REVERTS
```

## See Also

* [Adding Collateral](adding-collateral.md) - Add before borrowing
* [Updating Quotas](updating-quotas.md) - Enable quoted tokens as collateral
* [Controlling Slippage](controlling-slippage.md) - Protect borrowed funds during swaps
