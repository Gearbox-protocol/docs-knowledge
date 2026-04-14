# Enabling/Disabling Tokens

Explicitly manage which tokens count as collateral.

> For Solidity implementation, see [Enabling and Disabling Tokens](../../../solidity-guide/multicalls/#enabling-and-disabling-tokens).

## Why

You manually enable/disable tokens when:

* **Direct transfers** - Tokens sent directly to Credit Account aren't auto-enabled
* **Gas optimization** - Disable unused tokens to reduce collateral check cost
* **Risk management** - Prevent certain tokens from counting in health factor
* **Edge cases** - Override automatic enable/disable behavior

Most of the time you don't need this - tokens auto-enable/disable based on balance changes. But sometimes manual control is necessary.

## What

Non-quoted tokens have automatic enable/disable behavior:

| Balance Change | Action       |
| -------------- | ------------ |
| 0/1 to > 1     | Auto-enable  |
| > 1 to 0/1     | Auto-disable |

`enableToken` and `disableToken` let you override this when needed.

**Important:** These functions only work on **non-quoted tokens**. Quota tokens can only be enabled/disabled via `updateQuota`.

## How

### Enable a Token

```typescript
import { encodeFunctionData } from 'viem';
import { iCreditFacadeV300MulticallAbi } from '@gearbox-protocol/sdk';

const calls = [
  {
    target: creditFacadeAddress,
    callData: encodeFunctionData({
      abi: iCreditFacadeV300MulticallAbi,
      functionName: 'enableToken',
      args: [tokenAddress],
    }),
  },
];
```

### Disable a Token

```typescript
const calls = [
  {
    target: creditFacadeAddress,
    callData: encodeFunctionData({
      abi: iCreditFacadeV300MulticallAbi,
      functionName: 'disableToken',
      args: [tokenAddress],
    }),
  },
];
```

### Enable Token After Direct Transfer

If someone sends tokens directly to your Credit Account:

```typescript
// Token was transferred directly to Credit Account
// It won't count as collateral until enabled

const calls = [
  {
    target: creditFacadeAddress,
    callData: encodeFunctionData({
      abi: iCreditFacadeV300MulticallAbi,
      functionName: 'enableToken',
      args: [directlyTransferredToken],
    }),
  },
];

await market.creditFacade.write.multicall([creditAccountAddress, calls]);
```

### Disable Unused Tokens to Save Gas

Each enabled token requires a price oracle call during collateral check. Disable tokens with zero balance:

```typescript
// Check which tokens have zero balance
const accountData = await service.getCreditAccountData(creditAccountAddress);

const tokensToDisable = accountData.tokens
  .filter(t => t.balance <= 1n && t.isEnabled)
  .map(t => t.token);

const calls = tokensToDisable.map(token => ({
  target: creditFacadeAddress,
  callData: encodeFunctionData({
    abi: iCreditFacadeV300MulticallAbi,
    functionName: 'disableToken',
    args: [token],
  }),
}));
```

## Gotchas

### No-Op for Quota Tokens

Calling `enableToken` or `disableToken` on a quota token does nothing:

```typescript
// This does nothing - quota tokens use updateQuota
{
  functionName: 'enableToken',
  args: [quotaTokenAddress], // No effect
}

// Use this instead for quota tokens
service.prepareUpdateQuota(quotaTokenAddress, quotaAmount, minQuota);
```

### Cannot Enable Forbidden Tokens

Some tokens are marked as "forbidden" and cannot be enabled:

```typescript
// This will revert
{
  functionName: 'enableToken',
  args: [forbiddenTokenAddress], // Reverts!
}
```

Forbidden tokens must be swapped away, not disabled.

### Auto-Enable Usually Works

Adapter calls and standard operations auto-enable tokens when balance increases:

```typescript
// This swap auto-enables WETH
{
  target: uniswapAdapter,
  callData: encodeSwap(/* USDC → WETH */),
}
// No need to call enableToken(wethAddress) after
```

You only need manual enable when:

* Tokens are transferred directly to Credit Account (not via adapter)
* You want to enable a zero-balance token preemptively

### Max Enabled Tokens Limit

Each Credit Manager has a maximum number of enabled tokens per account. Exceeding this reverts the multicall:

```typescript
// Check the limit
const maxTokens = await creditManager.read.maxEnabledTokens();

// Count currently enabled tokens
const enabledCount = accountData.tokens.filter(t => t.isEnabled).length;

if (enabledCount >= maxTokens) {
  // Must disable some tokens before enabling new ones
}
```

### Disabled Tokens Still on Account

Disabling a token doesn't remove it from the account - it just excludes it from health factor calculation. The balance remains:

```typescript
// Token is disabled but balance stays
disableToken(wethAddress);

// Balance is still there, just not counted as collateral
// Liquidators can claim disabled token balances as bonus!
```

**Warning:** Don't keep significant value in disabled tokens. During liquidation, liquidators can withdraw disabled tokens on top of their normal premium.

### Balance of 1 is "Zero"

Gearbox treats balance of 0 and 1 the same (due to ERC20 rounding issues). Auto-disable triggers at balance <= 1:

```typescript
// These are equivalent from Gearbox perspective
balance = 0n // Disabled
balance = 1n // Also disabled

// This is enabled
balance = 2n
```

## See Also

* [Updating Quotas](updating-quotas.md) - How to enable/disable quota tokens
* [Making External Calls](making-external-calls.md) - Auto-enable behavior with adapters
* [Collateral Check Params](collateral-check-params.md) - Optimize checks for enabled tokens
