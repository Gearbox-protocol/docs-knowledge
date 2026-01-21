# Revoke Allowances

Revoke Credit Account's token approvals to external contracts.

> For Solidity implementation, see [Revoke Allowances](../../solidity-guide/multicalls.md#revoke-allowances).

## Why

You revoke allowances when:

- **Security incident** - Third-party contract may be compromised
- **Legacy cleanup** - Old accounts may have stale approvals from previous Gearbox versions
- **Defense in depth** - Proactively remove unnecessary approvals

Current Gearbox V3 automatically resets allowances to 1 after each interaction. However, older accounts from V2.1 may still have active allowances to external protocols.

## What

`revokeAdapterAllowances` resets token approvals from your Credit Account to specified contracts:

1. You specify which (spender, token) pairs to revoke
2. Credit Account sets allowance to 1 for each pair
3. External contracts can no longer spend those tokens

**Note:** Allowance is set to 1, not 0, due to gas optimization (writing non-zero to non-zero is cheaper than writing zero).

## How

```typescript
import { encodeFunctionData } from 'viem';
import { iCreditFacadeV300MulticallAbi } from '@gearbox-protocol/sdk';

// Define which approvals to revoke
const revocations = [
  {
    spender: uniswapRouterAddress,
    token: usdcAddress,
  },
  {
    spender: curvePoolAddress,
    token: daiAddress,
  },
];

const calls = [
  {
    target: creditFacadeAddress,
    callData: encodeFunctionData({
      abi: iCreditFacadeV300MulticallAbi,
      functionName: 'revokeAdapterAllowances',
      args: [revocations],
    }),
  },
];

await market.creditFacade.write.multicall([creditAccountAddress, calls]);
```

### Check Existing Allowances

Before revoking, you might want to see what allowances exist:

```typescript
import { erc20Abi, getContract } from 'viem';

const token = getContract({
  address: tokenAddress,
  abi: erc20Abi,
  client: publicClient,
});

// Check allowance from Credit Account to a spender
const allowance = await token.read.allowance([
  creditAccountAddress,
  spenderAddress,
]);

if (allowance > 1n) {
  console.log(`Credit Account has ${allowance} allowance to ${spenderAddress}`);
}
```

### Revoke All Known Adapters

If you want to revoke all adapter allowances for a token:

```typescript
// Get all adapters from Credit Manager
const adapters = await creditManager.read.adapters();

// Build revocations for all adapters
const revocations = adapters.map(adapter => ({
  spender: adapter,
  token: tokenAddress,
}));

const calls = [
  {
    target: creditFacadeAddress,
    callData: encodeFunctionData({
      abi: iCreditFacadeV300MulticallAbi,
      functionName: 'revokeAdapterAllowances',
      args: [revocations],
    }),
  },
];
```

## Gotchas

### Usually Not Needed in V3

Gearbox V3 automatically resets allowances after each adapter interaction. This function exists mainly for:

1. Legacy accounts migrated from V2.1
2. Paranoid security posture
3. Specific incident response

If you're using a fresh V3 account, allowances are already minimal.

### Revocation Struct Format

The `RevocationPair` struct has two fields:

```typescript
interface RevocationPair {
  spender: Address;  // Contract that has the allowance
  token: Address;    // Token that was approved
}
```

Both must be valid addresses. Invalid addresses may cause the call to revert or have no effect.

### Sets to 1, Not 0

For gas efficiency, allowances are set to 1 instead of 0:

```typescript
// Before revocation: allowance = 1000000000000000000 (1 token)
// After revocation: allowance = 1 (essentially zero for practical purposes)
```

An allowance of 1 wei is functionally zero for any realistic token amount.

### Can't Revoke Non-Existent Allowances

Revoking an allowance that doesn't exist (already 0 or 1) is a no-op - it won't revert, but wastes gas.

### Adapter vs External Contract

Revocations target the **spender** (usually an adapter), not the underlying protocol:

```typescript
// The adapter has the allowance, not Uniswap directly
const revocations = [
  {
    spender: uniswapAdapter,  // Adapter address, not Uniswap Router
    token: usdcAddress,
  },
];
```

Adapters are what actually interact with your Credit Account's tokens.

### Batch Multiple Revocations

You can revoke multiple (spender, token) pairs in one call:

```typescript
// Efficient - single call
const revocations = [
  { spender: adapter1, token: usdc },
  { spender: adapter1, token: dai },
  { spender: adapter2, token: usdc },
];
args: [revocations]

// Less efficient - multiple calls
[
  { args: [[{ spender: adapter1, token: usdc }]] },
  { args: [[{ spender: adapter1, token: dai }]] },
  { args: [[{ spender: adapter2, token: usdc }]] },
]
```

### When to Actually Use This

Real scenarios where revocation makes sense:

1. **Third-party exploit:** A protocol Gearbox integrates with gets hacked. Revoke allowances to that protocol's adapter as a precaution.

2. **Account migration:** Moving from V2.1 account with old allowances to ensure clean state.

3. **Compliance requirement:** Some regulatory frameworks require revoking unused approvals.

4. **Personal security policy:** You want explicit control over all approvals.

For normal operations, V3's automatic reset is sufficient.

## See Also

- [Making External Calls](./making-external-calls.md) - How adapters use allowances
- [Enabling/Disabling Tokens](./enabling-disabling-tokens.md) - Related account management
- [Credit Accounts](../credit-accounts.md) - Account overview and management
