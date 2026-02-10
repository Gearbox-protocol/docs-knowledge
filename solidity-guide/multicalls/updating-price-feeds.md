# Updating Price Feeds

Push fresh price data for on-demand oracles (Pyth, Redstone).

> For SDK implementation, see [Updating Price Feeds](../../sdk-guide/multicalls/updating-price-feeds.md).

## Why

You update price feeds when:

- **Using on-demand oracles** - Pyth and Redstone require fresh data with each transaction
- **Multicalls fail** - "Stale price" errors indicate missing price updates
- **Withdrawals** - Reserve price feeds may also need updates under safe pricing

Some tokens use "pull-based" oracles that don't update automatically. You must push fresh price data before operations that need it.

## What

`onDemandPriceUpdate` pushes oracle data to the price feed:

1. You obtain signed price data from the oracle provider (off-chain)
2. You include the price update as the FIRST call in your multicall
3. Credit Facade forwards the data to the price feed contract
4. The price feed validates the signature and updates

**Critical rule:** All price updates must be at the **beginning** of the calls array. Any `onDemandPriceUpdate` after another call type will revert.

## How

### Basic Price Update

```solidity
import {ICreditFacadeV3Multicall} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditFacadeV3Multicall.sol";
import {MultiCall} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditFacadeV3.sol";

address creditFacade;
address creditAccount;
address tokenWithPythFeed;
bytes memory priceData; // Obtained off-chain from Pyth/Redstone

MultiCall[] memory calls = new MultiCall[](2);

// Price update MUST be first
calls[0] = MultiCall({
    target: creditFacade,
    callData: abi.encodeCall(
        ICreditFacadeV3Multicall.onDemandPriceUpdate,
        (
            tokenWithPythFeed,  // Token to update price for
            false,              // reserve: false = main feed, true = reserve feed
            priceData           // Signed price data from oracle
        )
    )
});

// Now other operations
calls[1] = MultiCall({
    target: creditFacade,
    callData: abi.encodeCall(
        ICreditFacadeV3Multicall.addCollateral,
        (usdc, amount)
    )
});

ICreditFacadeV3(creditFacade).multicall(creditAccount, calls);
```

### Multiple Price Updates

Update several tokens at once (all must be at the start):

```solidity
MultiCall[] memory calls = new MultiCall[](4);

// All price updates first
calls[0] = MultiCall({
    target: creditFacade,
    callData: abi.encodeCall(
        ICreditFacadeV3Multicall.onDemandPriceUpdate,
        (token1, false, priceData1)
    )
});

calls[1] = MultiCall({
    target: creditFacade,
    callData: abi.encodeCall(
        ICreditFacadeV3Multicall.onDemandPriceUpdate,
        (token2, false, priceData2)
    )
});

// Then other operations
calls[2] = MultiCall({
    target: creditFacade,
    callData: abi.encodeCall(
        ICreditFacadeV3Multicall.addCollateral,
        (usdc, amount)
    )
});

calls[3] = MultiCall({
    target: creditFacade,
    callData: abi.encodeCall(
        ICreditFacadeV3Multicall.increaseDebt,
        (debtAmount)
    )
});
```

### Updating Reserve Feed (For Withdrawals)

Withdrawals trigger safe pricing, which uses both main and reserve feeds:

```solidity
MultiCall[] memory calls = new MultiCall[](3);

// Main feed update
calls[0] = MultiCall({
    target: creditFacade,
    callData: abi.encodeCall(
        ICreditFacadeV3Multicall.onDemandPriceUpdate,
        (tokenAddress, false, mainPriceData)  // reserve = false
    )
});

// Reserve feed update
calls[1] = MultiCall({
    target: creditFacade,
    callData: abi.encodeCall(
        ICreditFacadeV3Multicall.onDemandPriceUpdate,
        (tokenAddress, true, reservePriceData)  // reserve = true
    )
});

// Now the withdrawal will work with safe pricing
calls[2] = MultiCall({
    target: creditFacade,
    callData: abi.encodeCall(
        ICreditFacadeV3Multicall.withdrawCollateral,
        (otherToken, amount, recipient)
    )
});
```

### Contract Architecture for Price Updates

Your contract must accept price data as a parameter since it cannot fetch oracle data on-chain:

```solidity
contract MyGearboxStrategy {
    address public creditFacade;
    address public creditAccount;

    function executeStrategy(
        bytes[] calldata priceUpdates,  // Must be passed from frontend
        uint256 amount
    ) external {
        uint256 numUpdates = priceUpdates.length;
        MultiCall[] memory calls = new MultiCall[](numUpdates + 1);

        // Build price update calls first
        for (uint256 i = 0; i < numUpdates; i++) {
            (address token, bool reserve, bytes memory data) =
                abi.decode(priceUpdates[i], (address, bool, bytes));

            calls[i] = MultiCall({
                target: creditFacade,
                callData: abi.encodeCall(
                    ICreditFacadeV3Multicall.onDemandPriceUpdate,
                    (token, reserve, data)
                )
            });
        }

        // Then add strategy operations
        calls[numUpdates] = MultiCall({
            target: creditFacade,
            callData: abi.encodeCall(
                ICreditFacadeV3Multicall.addCollateral,
                (usdc, amount)
            )
        });

        ICreditFacadeV3(creditFacade).multicall(creditAccount, calls);
    }
}
```

## Gotchas

### Price Updates MUST Be First

This is the most common mistake. Price updates after any other call type revert:

```solidity
// WRONG - price update after addCollateral
MultiCall[] memory calls = new MultiCall[](2);
calls[0] = MultiCall({
    target: creditFacade,
    callData: abi.encodeCall(ICreditFacadeV3Multicall.addCollateral, (token, amount))
});
calls[1] = MultiCall({
    target: creditFacade,
    callData: abi.encodeCall(
        ICreditFacadeV3Multicall.onDemandPriceUpdate,
        (token, false, priceData)  // REVERTS!
    )
});

// CORRECT - price update first
calls[0] = MultiCall({
    target: creditFacade,
    callData: abi.encodeCall(
        ICreditFacadeV3Multicall.onDemandPriceUpdate,
        (token, false, priceData)
    )
});
calls[1] = MultiCall({
    target: creditFacade,
    callData: abi.encodeCall(ICreditFacadeV3Multicall.addCollateral, (token, amount))
});
```

### Fresh Data Required

Price data has a short validity window (usually a few minutes). Fetch fresh data right before the transaction:

```solidity
// Off-chain (e.g., in your frontend or bot):
// 1. Fetch price data from Pyth/Redstone API
// 2. Immediately use it in transaction
// 3. DON'T cache price data for later
```

### Not All Tokens Need Updates

Only tokens with on-demand price feeds need updates. Tokens using Chainlink or other push-based oracles don't need `onDemandPriceUpdate`:

```solidity
// Check feed type in your integration:
// - PYTH feeds: need onDemandPriceUpdate
// - REDSTONE feeds: need onDemandPriceUpdate
// - Chainlink feeds: no update needed
// - Other push oracles: no update needed
```

### Disabled Tokens Don't Need Updates

If a token will be disabled by the end of the multicall, you don't need to update its price:

```solidity
// WETH is getting swapped entirely (will be disabled)
MultiCall[] memory calls = new MultiCall[](2);

// No need for WETH price update since it's being fully swapped
calls[0] = MultiCall({
    target: creditFacade,
    callData: abi.encodeCall(ICreditFacadeV3Multicall.addCollateral, (usdc, amount))
});

calls[1] = MultiCall({
    target: uniswapAdapter,
    callData: abi.encodeCall(
        IUniswapV3Adapter.exactInputSingle,
        (swapAllWethToUsdc)  // WETH will auto-disable after swap
    )
});
```

### Contracts Cannot Fetch Price Data

The oracle's API must be called off-chain. Your smart contract receives price data as a parameter:

```solidity
// Your contract CANNOT do this:
// bytes memory priceData = pythOracle.fetchPrice(feedId);  // Not possible on-chain!

// Your contract MUST receive price data from caller:
function myFunction(bytes calldata priceData) external {
    // Use priceData in multicall
}
```

## See Also

- [Controlling Slippage](./controlling-slippage.md) - Stale prices can cause slippage issues
- [Withdrawing Collateral](./withdrawing-collateral.md) - May need reserve feed updates
- [Collateral Check Params](./collateral-check-params.md) - Related to price feed behavior
