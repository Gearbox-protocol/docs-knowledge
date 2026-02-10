# Enabling and Disabling Tokens

Explicitly manage which tokens count as collateral.

> For SDK implementation, see [Enabling and Disabling Tokens](../../sdk-guide/multicalls/enabling-disabling-tokens.md).

## Why

You manually enable/disable tokens when:

- **Direct transfers** - Tokens sent directly to Credit Account aren't auto-enabled
- **Gas optimization** - Disable unused tokens to reduce collateral check cost
- **Risk management** - Prevent certain tokens from counting in health factor
- **Edge cases** - Override automatic enable/disable behavior

Most of the time you don't need this - tokens auto-enable/disable based on balance changes. But sometimes manual control is necessary.

## What

Non-quoted tokens have automatic enable/disable behavior:

| Balance Change | Action |
|----------------|--------|
| 0/1 to > 1 | Auto-enable |
| > 1 to 0/1 | Auto-disable |

`enableToken` and `disableToken` let you override this when needed.

**Important:** These functions only work on **non-quoted tokens**. Quota tokens can only be enabled/disabled via `updateQuota`.

## How

### Enable a Token

```solidity
import {ICreditFacadeV3Multicall} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditFacadeV3Multicall.sol";
import {MultiCall} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditFacadeV3.sol";

address creditFacade;
address creditAccount;
address tokenToEnable;

MultiCall[] memory calls = new MultiCall[](1);

calls[0] = MultiCall({
    target: creditFacade,
    callData: abi.encodeCall(
        ICreditFacadeV3Multicall.enableToken,
        (tokenToEnable)
    )
});

ICreditFacadeV3(creditFacade).multicall(creditAccount, calls);
```

### Disable a Token

```solidity
// Disable a token to reduce collateral check gas cost
calls[0] = MultiCall({
    target: creditFacade,
    callData: abi.encodeCall(
        ICreditFacadeV3Multicall.disableToken,
        (tokenToDisable)
    )
});
```

### Enable Token After Direct Transfer

If tokens are sent directly to your Credit Account (not through an adapter):

```solidity
// Token was transferred directly - won't count as collateral until enabled
// First, some external contract sends tokens:
// IERC20(token).transfer(creditAccount, amount);

// Now enable it to count as collateral
MultiCall[] memory calls = new MultiCall[](1);

calls[0] = MultiCall({
    target: creditFacade,
    callData: abi.encodeCall(
        ICreditFacadeV3Multicall.enableToken,
        (directlyTransferredToken)
    )
});

ICreditFacadeV3(creditFacade).multicall(creditAccount, calls);
```

### Disable Multiple Unused Tokens

Reduce gas costs by disabling tokens with zero balance:

```solidity
// Get enabled token mask from credit manager
uint256 enabledTokensMask = ICreditManagerV3(creditManager).enabledTokensMaskOf(creditAccount);

// Build calls to disable each zero-balance token
// This is a simplified example - in practice, iterate through mask
MultiCall[] memory calls = new MultiCall[](2);

calls[0] = MultiCall({
    target: creditFacade,
    callData: abi.encodeCall(
        ICreditFacadeV3Multicall.disableToken,
        (unusedToken1)
    )
});

calls[1] = MultiCall({
    target: creditFacade,
    callData: abi.encodeCall(
        ICreditFacadeV3Multicall.disableToken,
        (unusedToken2)
    )
});
```

## Gotchas

### No-Op for Quota Tokens

Calling `enableToken` or `disableToken` on a quota token does nothing:

```solidity
// This does nothing - quota tokens use updateQuota
MultiCall({
    target: creditFacade,
    callData: abi.encodeCall(
        ICreditFacadeV3Multicall.enableToken,
        (quotaTokenAddress)  // No effect!
    )
});

// Use this instead for quota tokens
MultiCall({
    target: creditFacade,
    callData: abi.encodeCall(
        ICreditFacadeV3Multicall.updateQuota,
        (quotaTokenAddress, int96(quotaAmount), uint96(minQuota))
    )
});
```

### Cannot Enable Forbidden Tokens

Some tokens are marked as "forbidden" and cannot be enabled:

```solidity
// This will revert
MultiCall({
    target: creditFacade,
    callData: abi.encodeCall(
        ICreditFacadeV3Multicall.enableToken,
        (forbiddenTokenAddress)  // Reverts!
    )
});
```

Forbidden tokens must be swapped away, not disabled.

### Auto-Enable Usually Works

Adapter calls automatically enable tokens when balance increases:

```solidity
// This swap auto-enables WETH - no need to call enableToken
MultiCall({
    target: uniswapAdapter,
    callData: abi.encodeCall(
        IUniswapV3Adapter.exactInputSingle,
        (swapParams)  // Swaps USDC -> WETH
    )
});
// WETH is now enabled automatically
```

You only need manual enable when:
- Tokens are transferred directly to Credit Account (not via adapter)
- You want to enable a zero-balance token preemptively

### Max Enabled Tokens Limit

Each Credit Manager has a maximum number of enabled tokens per account:

```solidity
// Check the limit
uint8 maxTokens = ICreditManagerV3(creditManager).maxEnabledTokens();

// Check current count via enabled mask popcount
uint256 enabledMask = ICreditManagerV3(creditManager).enabledTokensMaskOf(creditAccount);
// Count set bits in enabledMask to get current token count

// Exceeding limit reverts the multicall
```

### Disabled Tokens Still on Account

Disabling a token doesn't remove it from the account - just excludes it from health factor:

```solidity
// Token is disabled but balance stays
disableToken(wethAddress);

// Balance remains, just not counted as collateral
// WARNING: Liquidators can claim disabled token balances as bonus!
```

**Warning:** Don't keep significant value in disabled tokens. During liquidation, liquidators can withdraw disabled tokens on top of their normal premium.

### Balance of 1 is "Zero"

Gearbox treats balance of 0 and 1 the same (due to ERC20 rounding issues). Auto-disable triggers at balance <= 1:

```solidity
// These are equivalent from Gearbox perspective
// balance = 0  -> Disabled
// balance = 1  -> Also disabled

// This is enabled
// balance = 2
```

## See Also

- [Updating Quotas](./updating-quotas.md) - How to enable/disable quota tokens
- [Making External Calls](./making-external-calls.md) - Auto-enable behavior with adapters
- [Collateral Check Params](./collateral-check-params.md) - Optimize checks for enabled tokens
