# Controlling Slippage

Protect swaps from sandwich attacks and price movement.

> For Solidity implementation, see [Controlling Slippage](../../solidity-guide/multicalls.md#controlling-slippage).

## Why

You need slippage protection when:

- **Swapping tokens** - DEX prices can move between quote and execution
- **Multi-step operations** - Swap + deposit combos need end-to-end protection
- **Large trades** - Bigger trades have higher slippage impact
- **Protecting against MEV** - Sandwich bots exploit unprotected swaps

Without slippage protection, you might receive significantly fewer tokens than expected. Gearbox provides native slippage controls that work across any sequence of operations.

## What

Gearbox uses a two-step pattern:

1. **`storeExpectedBalances`** - Record expected minimum balances BEFORE operations
2. **`compareBalances`** - Verify actual balances meet expectations AFTER operations

If the final balance is less than expected, the entire multicall reverts.

**Why not use DEX slippage parameters?**
- Multi-step operations (swap → deposit) can't use single slippage value
- Some protocols (ERC4626 vaults) have no built-in slippage protection
- Gearbox slippage works at the account level, across any operation sequence

## How

```typescript
import { encodeFunctionData } from 'viem';
import { iCreditFacadeV300MulticallAbi } from '@gearbox-protocol/sdk';

// Calculate minimum expected output with 0.5% slippage tolerance
const expectedOutput = 25n * 10n ** 18n; // 25 WETH
const slippageBps = 50n; // 0.5%
const minExpected = expectedOutput - (expectedOutput * slippageBps / 10000n);

const calls = [
  // 1. Store expected balance BEFORE swap
  {
    target: creditFacadeAddress,
    callData: encodeFunctionData({
      abi: iCreditFacadeV300MulticallAbi,
      functionName: 'storeExpectedBalances',
      args: [[{ token: wethAddress, amount: minExpected }]],
    }),
  },

  // 2. Perform the swap
  {
    target: uniswapV3Adapter,
    callData: encodeFunctionData({
      abi: uniswapV3AdapterAbi,
      functionName: 'exactInputSingle',
      args: [swapParams],
    }),
  },

  // 3. Verify slippage AFTER swap
  {
    target: creditFacadeAddress,
    callData: encodeFunctionData({
      abi: iCreditFacadeV300MulticallAbi,
      functionName: 'compareBalances',
      args: [],
    }),
  },
];
```

### Multiple Tokens

Check slippage on multiple output tokens:

```typescript
const calls = [
  // Store expectations for both tokens
  {
    target: creditFacadeAddress,
    callData: encodeFunctionData({
      abi: iCreditFacadeV300MulticallAbi,
      functionName: 'storeExpectedBalances',
      args: [[
        { token: wethAddress, amount: minWethExpected },
        { token: usdcAddress, amount: minUsdcExpected },
      ]],
    }),
  },

  // Multiple swaps...
  { /* swap 1 */ },
  { /* swap 2 */ },

  // Single compare covers all stored expectations
  {
    target: creditFacadeAddress,
    callData: encodeFunctionData({
      abi: iCreditFacadeV300MulticallAbi,
      functionName: 'compareBalances',
      args: [],
    }),
  },
];
```

### Negative Deltas (Expected to Spend)

You can also specify tokens you expect to decrease:

```typescript
// Expect to spend at most 50,000 USDC
const maxSpend = 50_000n * 10n ** 6n;

const calls = [
  {
    target: creditFacadeAddress,
    callData: encodeFunctionData({
      abi: iCreditFacadeV300MulticallAbi,
      functionName: 'storeExpectedBalances',
      args: [[
        { token: usdcAddress, amount: -maxSpend }, // Negative = expect decrease
        { token: wethAddress, amount: minWethExpected },
      ]],
    }),
  },
  // ...
];
```

## Gotchas

### Keep Slippage Checks Close to Operations

Place `storeExpectedBalances` immediately before the first external call, and `compareBalances` immediately after the last:

```typescript
// CORRECT - slippage checks wrap the swap tightly
const calls = [
  service.prepareAddCollateral(usdcAddress, amount), // Internal op
  storeExpectedBalances,  // Right before swap
  swap,                   // External call
  compareBalances,        // Right after swap
  service.prepareUpdateQuota(wethAddress, quota, quota), // Internal op
];

// WRONG - addCollateral between store and compare affects balances
const calls = [
  storeExpectedBalances,
  swap,
  service.prepareAddCollateral(usdcAddress, amount), // Changes balances!
  compareBalances, // May fail incorrectly
];
```

### compareBalances Fails Without storeExpectedBalances

Calling `compareBalances` without a prior `storeExpectedBalances` in the same multicall reverts.

### Auto-Compare at Multicall End

If you call `storeExpectedBalances` but forget `compareBalances`, the check happens automatically at the end of the multicall. However, it's better to be explicit.

### BalanceDelta Type

The `amount` in `BalanceDelta` is the **change** you expect, not the final balance:

```typescript
// Current WETH balance: 10
// Swap adds 25 WETH
// Final balance: 35

// CORRECT - amount is the delta (change)
{ token: wethAddress, amount: 25n * 10n ** 18n }

// WRONG - this would require 35 WETH increase
{ token: wethAddress, amount: 35n * 10n ** 18n }
```

### Slippage Check Works on balanceOf

The check reads actual token balances via `balanceOf`. This means:
- Internal transfers (like `addCollateral`) affect the balance
- Token rebases affect the balance
- Any balance change, regardless of source, is included

### Cannot Reuse Stored Balances

After `compareBalances` runs, the stored expectations are cleared. For multiple swap sequences, call `storeExpectedBalances` again:

```typescript
const calls = [
  // First swap
  storeExpectedBalances1,
  swap1,
  compareBalances, // Clears stored values

  // Second swap needs new store
  storeExpectedBalances2, // Must call again
  swap2,
  compareBalances,
];
```

## See Also

- [Making External Calls](./making-external-calls.md) - Adapter calls that need slippage protection
- [Multicalls Overview](../multicalls.md) - Basic slippage example
- [Price Updates](./updating-price-feeds.md) - Stale prices can cause unexpected slippage
