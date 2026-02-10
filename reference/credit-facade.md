# Credit Facade

The **CreditFacadeV3** is the primary user-facing interface for Credit Account operations. It implements atomic multicall batching, enforces debt limits, manages bot permissions, and ensures all operations complete with a healthy account state.

## Multicall Execution Flow

All Credit Account operations are executed through multicalls - batched transactions that execute atomically.

### Entry Points

| Function | Caller | Description |
|----------|--------|-------------|
| `openCreditAccount(calls, onBehalfOf)` | Anyone | Create new account with initial operations |
| `closeCreditAccount(creditAccount, calls)` | Owner | Close account, repay all debt |
| `multicall(creditAccount, calls)` | Owner | Execute operations on existing account |
| `botMulticall(creditAccount, calls)` | Authorized bot | Bot-initiated operations |
| `liquidateCreditAccount(creditAccount, to, calls)` | Anyone | Liquidate unhealthy account |

### MultiCall Structure

```solidity
struct MultiCall {
    address target;   // Facade itself or whitelisted adapter
    bytes callData;   // Function selector + encoded arguments
}
```

### Four Execution Phases

**Phase 1: Initialization**
- Emit `StartMultiCall` event
- Snapshot forbidden token balances
- Set flags (e.g., `REVERT_ON_FORBIDDEN_TOKENS_FLAG`)

**Phase 2: Iterative Dispatch**
```solidity
for (uint256 i = 0; i < calls.length; ++i) {
    if (target == address(this)) {
        _processFacadeCall(callData);  // Internal operations
    } else {
        creditManager.setActiveCreditAccount(creditAccount);
        creditAccount.execute(target, callData);  // External adapter
    }
}
```

**Phase 3: Balance Tracking (Optional)**
- `storeExpectedBalances(balances[])`: Store expected amounts
- `compareBalances()`: Verify slippage protection

**Phase 4: Final Validation**
- Unset active account
- Full collateral check (HF must be >= 1)
- Verify forbidden token balances didn't increase

***

## Security Checks

### Access Control

| Modifier | Effect |
|----------|--------|
| `creditAccountOwnerOnly` | Only account owner can call |
| `nonReentrant` | Prevents reentrancy attacks |
| `whenNotPaused` | Blocks operations when paused |
| `whenNotExpired` | After expiration, only closures allowed |

### Bot Permission System

Bots operate with granular permissions stored as a `uint192` bitmask:

| Permission | Value | Operation |
|------------|-------|-----------|
| `ADD_COLLATERAL_PERMISSION` | `1 << 0` | Add funds to account |
| `INCREASE_DEBT_PERMISSION` | `1 << 1` | Borrow more from pool |
| `DECREASE_DEBT_PERMISSION` | `1 << 2` | Repay debt |
| `WITHDRAW_COLLATERAL_PERMISSION` | `1 << 5` | Withdraw assets |
| `UPDATE_QUOTA_PERMISSION` | `1 << 6` | Change token quotas |
| `EXTERNAL_CALLS_PERMISSION` | `1 << 16` | Execute adapter calls |

Each multicall operation checks against the caller's permission mask:

```solidity
function _revertIfNoPermission(uint256 flags, uint256 permission) internal pure {
    if (flags & permission == 0) {
        revert NoPermissionException(permission);
    }
}
```

***

## Debt Limits Enforcement

### Global Limits

Every Credit Facade enforces min/max debt bounds:

```solidity
struct DebtLimits {
    uint128 minDebt;  // Minimum principal (except 0)
    uint128 maxDebt;  // Maximum principal
}
```

**Validation:**
```solidity
require(newDebt == 0 || (newDebt >= minDebt && newDebt <= maxDebt));
```

Zero debt is always allowed (closing accounts), but any non-zero debt must fall within bounds.

### Per-Block Limit

To prevent flash-loan exploits and rate manipulation:

```solidity
uint8 maxDebtPerBlockMultiplier;
uint256 limit = maxDebt * maxDebtPerBlockMultiplier;
require(totalBorrowedInBlock[block.number] + amount <= limit);
```

This caps the total new debt that can be created in a single block across all Credit Accounts.

### Loss Policy

When bad debt occurs during liquidation:
1. `maxDebtPerBlockMultiplier` is set to 0
2. All new borrowing is halted
3. Governance must intervene to restore normal operation

This circuit breaker protects the protocol from cascading losses.

```typescript
// TypeScript: Checking debt limits
const facade = getContract({
  address: facadeAddress,
  abi: creditFacadeV3Abi,
  client: publicClient,
});

const [minDebt, maxDebt] = await facade.read.debtLimits();
const multiplier = await facade.read.maxDebtPerBlockMultiplier();

// Check if borrowing is allowed
if (multiplier === 0) {
  console.log('Borrowing is currently disabled');
}

console.log(`Debt range: ${minDebt} - ${maxDebt}`);
console.log(`Per-block limit: ${maxDebt * BigInt(multiplier)}`);
```

***

## Forbidden Tokens Logic

Forbidden tokens are high-risk assets that require special handling. They still count toward collateral value but have restrictions.

### Protection Flags

| Flag | Effect |
|------|--------|
| `REVERT_ON_FORBIDDEN_TOKENS_FLAG` | Revert if forbidden tokens are enabled |
| `USE_SAFE_PRICES_FLAG` | Use `min(primary, reserve)` price for valuation |

### Rules

1. **Cannot increase quota** for forbidden tokens
2. **Balance must NOT increase** during multicall
3. **Safe pricing** is used during collateral checks

This incentivizes users to reduce exposure to forbidden tokens while protecting the protocol from manipulation.

```typescript
// TypeScript: Checking for forbidden tokens
const creditManager = getContract({
  address: cmAddress,
  abi: creditManagerV3Abi,
  client: publicClient,
});

const forbiddenMask = await creditManager.read.forbiddenTokenMask();
const enabledMask = await creditManager.read.enabledTokensMaskOf([creditAccount]);

const hasForbidden = (enabledMask & forbiddenMask) !== 0n;
if (hasForbidden) {
  console.log('Account has forbidden tokens - consider reducing exposure');
}
```

***

## Account Lifecycle

### Opening an Account

```
User -> CreditFacade.openCreditAccount(calls, onBehalfOf)
  -> CreditManager.openCreditAccount(borrower, onBehalfOf)
  -> AccountFactory.takeCreditAccount(debt)
  -> Pool.lendCreditAccount(debt, account)
  -> _multicall(account, calls)
  -> CreditManager.fullCollateralCheck()
```

### Multicall with Adapter

```
User -> CreditFacade.multicall([{target: adapter, callData}])
  -> CreditManager.setActiveCreditAccount(account)
  -> CreditAccount.execute(adapter, callData)
  -> Adapter.someFunction(params)
  -> _execute(protocolCallData)
  -> CreditAccount -> DeFiProtocol.targetFunction()
  -> CreditManager.fullCollateralCheck()
```

### Closing an Account

```
User -> CreditFacade.closeCreditAccount(account, calls)
  -> _multicall(account, calls)  // Convert to underlying
  -> CreditManager.closeCreditAccount(account)
  -> Pool.repayCreditAccount(debt, profit, 0)
  -> Transfer remaining funds to user
```

<details>

<summary>Sources</summary>

* [contracts/credit/CreditFacadeV3.sol](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/credit/CreditFacadeV3.sol)
* [contracts/interfaces/ICreditFacadeV3.sol](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/interfaces/ICreditFacadeV3.sol)
* [contracts/interfaces/ICreditFacadeV3Multicall.sol](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/interfaces/ICreditFacadeV3Multicall.sol)

</details>
