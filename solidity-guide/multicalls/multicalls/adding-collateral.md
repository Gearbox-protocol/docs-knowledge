# Adding Collateral

Deposit tokens from an external address to a Credit Account.

> For SDK implementation, see [Adding Collateral](../../../sdk-guide-typescript/multicalls/multicalls/adding-collateral.md).

## Why

You need to add collateral when:

* **Opening an account** - Initial deposit to enable borrowing
* **Improving health factor** - Account approaching liquidation threshold
* **Enabling more borrowing** - Current collateral limits how much you can borrow

Adding collateral increases your account's total weighted value (TWV), which improves the health factor and allows larger debt positions.

## What

`addCollateral` transfers tokens from the caller to the Credit Account. On execution:

1. The Credit Manager calls `transferFrom` to move tokens from caller to Credit Account
2. The token is enabled as collateral (if not already enabled)
3. Quoted tokens are NOT auto-enabled - you must set a quota separately

**Important:** Approve tokens to the **Credit Manager**, not the Credit Facade. The Credit Manager is the contract that actually executes the transfer.

## How

```solidity
import {ICreditFacadeV3Multicall} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditFacadeV3Multicall.sol";
import {MultiCall} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditFacadeV3.sol";

address creditFacade;
address creditManager;
address usdc;
address creditAccount;
address owner;

MultiCall[] memory calls = new MultiCall[](1);

// Add 10,000 USDC as collateral
calls[0] = MultiCall({
    target: creditFacade,
    callData: abi.encodeCall(
        ICreditFacadeV3Multicall.addCollateral,
        (usdc, 10_000 * 10**6)
    )
});

// First, approve tokens to Credit Manager (not Facade!)
IERC20(usdc).approve(creditManager, 10_000 * 10**6);

// Execute on existing account
ICreditFacadeV3(creditFacade).multicall(creditAccount, calls);

// Or open new account with collateral
ICreditFacadeV3(creditFacade).openCreditAccount(owner, calls, 0);
```

### Using Permit (No Separate Approval)

For EIP-2612 compatible tokens, avoid the separate approval transaction:

```solidity
// Sign permit off-chain, then use addCollateralWithPermit
calls[0] = MultiCall({
    target: creditFacade,
    callData: abi.encodeCall(
        ICreditFacadeV3Multicall.addCollateralWithPermit,
        (usdc, 10_000 * 10**6, deadline, v, r, s)
    )
});
```

## Gotchas

### Approve to Credit Manager, Not Facade

The most common mistake. The Credit Manager executes the `transferFrom`, so it needs the approval:

```solidity
// CORRECT
IERC20(token).approve(creditManager, amount);

// WRONG - will fail
IERC20(token).approve(creditFacade, amount);
```

### Quoted Tokens Need Quota

Adding a quoted token as collateral does NOT automatically enable it. You must also call `updateQuota`:

```solidity
MultiCall[] memory calls = new MultiCall[](2);

calls[0] = MultiCall({
    target: creditFacade,
    callData: abi.encodeCall(
        ICreditFacadeV3Multicall.addCollateral,
        (quotedToken, amount)
    )
});

calls[1] = MultiCall({
    target: creditFacade,
    callData: abi.encodeCall(
        ICreditFacadeV3Multicall.updateQuota,
        (quotedToken, int96(quotaAmount), uint96(minQuota))
    )
});
```

### Direct Transfers Don't Enable

Sending tokens directly to a Credit Account (via `transfer`) does NOT enable them as collateral. You still need a multicall with the proper operation to count them in the health factor.

### Invalid Collateral Tokens

Only tokens recognized by the Credit Manager can be used as collateral. Transferring unrecognized tokens to a Credit Account may result in them being stuck (only governance can recover).

Check if a token is valid:

```solidity
// This reverts if token is not valid collateral
uint256 mask = ICreditManagerV3(creditManager).getTokenMaskOrRevert(token);
```

## See Also

* [Withdrawing Collateral](withdrawing-collateral.md) - The reverse operation
* [Debt Management](debt-management.md) - Often combined with adding collateral
* [Updating Quotas](updating-quotas.md) - Required for quoted tokens
