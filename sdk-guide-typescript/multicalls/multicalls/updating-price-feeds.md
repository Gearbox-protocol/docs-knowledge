# Updating Price Feeds

Push fresh price data for on-demand oracles (Pyth, Redstone).

> For Solidity implementation, see [Updating On-Demand Price Feeds](../../../solidity-guide/multicalls/#updating-on-demand-price-feeds).

## Why

You update price feeds when:

* **Using on-demand oracles** - Pyth and Redstone require fresh data with each transaction
* **Multicalls fail** - "Stale price" errors indicate missing price updates
* **Withdrawals** - Reserve price feeds may also need updates under safe pricing

Some tokens use "pull-based" oracles that don't update automatically. You must push fresh price data before operations that need it.

## What

`onDemandPriceUpdate` pushes oracle data to the price feed:

1. You obtain signed price data from the oracle provider (off-chain)
2. You include the price update as the FIRST call in your multicall
3. Credit Facade forwards the data to the price feed contract
4. The price feed validates the signature and updates

**Critical rule:** All price updates must be at the **beginning** of the calls array. Any `onDemandPriceUpdate` after another call type will revert.

## How

```typescript
import { encodeFunctionData } from 'viem';
import { iCreditFacadeV300MulticallAbi } from '@gearbox-protocol/sdk';

// Get price data from oracle provider (e.g., Pyth)
const priceData = await pythClient.getPriceUpdateData([feedId]);

const calls = [
  // Price update MUST be first
  {
    target: creditFacadeAddress,
    callData: encodeFunctionData({
      abi: iCreditFacadeV300MulticallAbi,
      functionName: 'onDemandPriceUpdate',
      args: [
        tokenAddress,  // Token to update price for
        false,         // reserve: false = main feed, true = reserve feed
        priceData,     // Signed price data from oracle
      ],
    }),
  },

  // Now other operations
  service.prepareAddCollateral(usdcAddress, amount),
  service.prepareIncreaseDebt(debtAmount),
];
```

### Multiple Price Updates

Update several tokens at once (all must be at the start):

```typescript
const calls = [
  // All price updates first
  {
    target: creditFacadeAddress,
    callData: encodeFunctionData({
      abi: iCreditFacadeV300MulticallAbi,
      functionName: 'onDemandPriceUpdate',
      args: [token1, false, priceData1],
    }),
  },
  {
    target: creditFacadeAddress,
    callData: encodeFunctionData({
      abi: iCreditFacadeV300MulticallAbi,
      functionName: 'onDemandPriceUpdate',
      args: [token2, false, priceData2],
    }),
  },

  // Then other operations
  // ...
];
```

### Updating Reserve Feed (For Withdrawals)

Withdrawals trigger safe pricing, which uses both main and reserve feeds:

```typescript
const calls = [
  // Main feed update
  {
    target: creditFacadeAddress,
    callData: encodeFunctionData({
      abi: iCreditFacadeV300MulticallAbi,
      functionName: 'onDemandPriceUpdate',
      args: [tokenAddress, false, mainPriceData],  // reserve = false
    }),
  },
  // Reserve feed update
  {
    target: creditFacadeAddress,
    callData: encodeFunctionData({
      abi: iCreditFacadeV300MulticallAbi,
      functionName: 'onDemandPriceUpdate',
      args: [tokenAddress, true, reservePriceData],  // reserve = true
    }),
  },

  // Now the withdrawal will work with safe pricing
  service.prepareWithdrawCollateral(otherToken, amount, recipient),
];
```

### Detecting Which Feeds Need Updates

```typescript
import { priceFeedCompressorAbi } from '@gearbox-protocol/sdk';

const feedInfo = await client.readContract({
  address: priceFeedCompressorAddress,
  abi: priceFeedCompressorAbi,
  functionName: 'getUpdatablePriceFeeds',
  args: [creditManagerAddress],
});

// feedInfo contains tokens that need on-demand updates
const tokensNeedingUpdate = feedInfo.filter(f => f.needsUpdate);
```

## Gotchas

### Price Updates MUST Be First

This is the most common mistake. Price updates after any other call type revert:

```typescript
// WRONG - price update after addCollateral
const calls = [
  service.prepareAddCollateral(token, amount),
  onDemandPriceUpdate, // Reverts!
];

// CORRECT - price update first
const calls = [
  onDemandPriceUpdate,
  service.prepareAddCollateral(token, amount),
];
```

### Fresh Data Required

Price data has a short validity window (usually a few minutes). Generate fresh data right before the transaction:

```typescript
// Get price data immediately before building transaction
const priceData = await pythClient.getPriceUpdateData([feedId]);

// Use it right away
const calls = [
  onDemandPriceUpdate(token, false, priceData),
  // ...
];

// DON'T cache price data for later
```

### Not All Tokens Need Updates

Only tokens with on-demand price feeds need updates. Tokens using Chainlink or other push-based oracles don't need `onDemandPriceUpdate`:

```typescript
// Check if token uses on-demand feed
const priceFeed = await priceOracle.read.priceFeedsRaw([tokenAddress, false]);
const feedType = priceFeed.feedType;

// Only PYTH and REDSTONE feeds need updates
if (feedType === 'PYTH' || feedType === 'REDSTONE') {
  // Include price update
}
```

### Disabled Tokens Don't Need Updates

If a token will be disabled by the end of the multicall, you don't need to update its price:

```typescript
// weth is getting swapped entirely (will be disabled)
const calls = [
  // No need for WETH price update since it's being disabled
  service.prepareAddCollateral(usdcAddress, amount),
  adapterSwap(weth, usdc, entireBalance),
  // WETH will auto-disable after swap
];
```

### Off-Chain Data Retrieval

You need to fetch price data from the oracle's API before building your transaction. This is protocol-specific:

```typescript
// Pyth example
const pythConnection = new PriceServiceConnection("https://hermes.pyth.network");
const priceUpdateData = await pythConnection.getPriceFeedsUpdateData([feedId]);

// Redstone example (simplified)
const redstonePayload = await getRedstonePayload([tokenSymbol]);
```

Your contract or frontend must handle this off-chain step.

### Contracts Need Price Data Input

If you're building a contract that interacts with Gearbox, it must accept price data as an input parameter:

```typescript
// Your contract function signature
function executeWithGearbox(
  bytes[] calldata priceUpdates,  // Must be passed from frontend
  // other params
) external {
  // Build multicall with price updates first
}
```

Contracts cannot fetch price data themselves - it must come from off-chain.

## See Also

* [Controlling Slippage](controlling-slippage.md) - Stale prices can cause slippage issues
* [Withdrawing Collateral](withdrawing-collateral.md) - May need reserve feed updates
* [Collateral Check Params](collateral-check-params.md) - Related to price feed behavior
