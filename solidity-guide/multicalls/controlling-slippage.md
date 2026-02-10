# Controlling Slippage

Protect against price movement during swaps and other operations.

> For SDK implementation, see [Controlling Slippage](../../sdk-guide/multicalls/controlling-slippage.md).

## Why

Slippage protection is critical for:

- **Swaps** - Ensure minimum output from DEX trades
- **Deposits/Withdrawals** - Protect against unfavorable rates
- **Multi-step strategies** - Verify final position matches expectations

Without slippage protection, MEV bots can sandwich your transactions, extracting value through price manipulation.

## What

Two operations work together for slippage control:

| Operation | Description |
|-----------|-------------|
| `storeExpectedBalances` | Record expected token balances (current + delta) |
| `compareBalances` | Verify current balances meet expectations, revert if not |

The pattern: Store expectations before swaps, compare after swaps.

## How

### Basic Slippage Check

```solidity
import {ICreditFacadeV3Multicall} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditFacadeV3Multicall.sol";
import {BalanceDelta} from "@gearbox-protocol/core-v3/contracts/libraries/BalancesLogic.sol";
import {MultiCall} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditFacadeV3.sol";

address creditFacade;
address creditAccount;
address usdc;
address weth;
address uniswapAdapter;

// Calculate minimum expected output (with 0.5% slippage tolerance)
// If swapping 50,000 USDC at rate of 2000 USDC/ETH:
// Expected: 25 ETH, with 0.5% slippage: 24.875 ETH
int256 minWethOut = int256(24.875 ether);

MultiCall[] memory calls = new MultiCall[](3);

// 1. Store expected balance (current + delta)
BalanceDelta[] memory deltas = new BalanceDelta[](1);
deltas[0] = BalanceDelta({
    token: weth,
    amount: minWethOut  // Can be negative for tokens spent
});

calls[0] = MultiCall({
    target: creditFacade,
    callData: abi.encodeCall(
        ICreditFacadeV3Multicall.storeExpectedBalances,
        (deltas)
    )
});

// 2. Perform swap via adapter
calls[1] = MultiCall({
    target: uniswapAdapter,
    callData: abi.encodeCall(
        IUniswapV3Adapter.exactInputSingle,
        (swapParams)
    )
});

// 3. Compare balances - reverts if WETH balance < expected
calls[2] = MultiCall({
    target: creditFacade,
    callData: abi.encodeCall(
        ICreditFacadeV3Multicall.compareBalances,
        ()
    )
});

ICreditFacadeV3(creditFacade).multicall(creditAccount, calls);
```

### Multiple Token Checks

Check multiple tokens in one comparison:

```solidity
BalanceDelta[] memory deltas = new BalanceDelta[](2);

// Expect to receive WETH
deltas[0] = BalanceDelta({
    token: weth,
    amount: int256(minWethOut)
});

// Expect to spend USDC (negative delta)
deltas[1] = BalanceDelta({
    token: usdc,
    amount: -int256(maxUsdcIn)
});

calls[0] = MultiCall({
    target: creditFacade,
    callData: abi.encodeCall(
        ICreditFacadeV3Multicall.storeExpectedBalances,
        (deltas)
    )
});
```

### Complete Strategy with Slippage Protection

8-step leveraged yield farming with full slippage protection:

```solidity
MultiCall[] memory calls = new MultiCall[](8);

// 1. Price update (if using pull oracles)
calls[0] = MultiCall({
    target: creditFacade,
    callData: abi.encodeCall(
        ICreditFacadeV3Multicall.onDemandPriceUpdate,
        (yvWETH, false, priceData)
    )
});

// 2. Add collateral
calls[1] = MultiCall({
    target: creditFacade,
    callData: abi.encodeCall(
        ICreditFacadeV3Multicall.addCollateral,
        (usdc, 10_000 * 10**6)
    )
});

// 3. Borrow
calls[2] = MultiCall({
    target: creditFacade,
    callData: abi.encodeCall(
        ICreditFacadeV3Multicall.increaseDebt,
        (40_000 * 10**6)
    )
});

// 4. Store expected: min yvWETH output after swap + deposit
// 50k USDC -> ~25 WETH -> ~25 yvWETH, minus 0.5% slippage
BalanceDelta[] memory deltas = new BalanceDelta[](1);
deltas[0] = BalanceDelta({
    token: yvWETH,
    amount: int256(24.875 ether)
});

calls[3] = MultiCall({
    target: creditFacade,
    callData: abi.encodeCall(
        ICreditFacadeV3Multicall.storeExpectedBalances,
        (deltas)
    )
});

// 5. Swap USDC -> WETH
calls[4] = MultiCall({
    target: uniswapAdapter,
    callData: abi.encodeCall(IUniswapV3Adapter.exactInputSingle, (swapParams))
});

// 6. Deposit WETH -> yvWETH (using diff pattern)
calls[5] = MultiCall({
    target: yearnAdapter,
    callData: abi.encodeCall(IYearnV2Adapter.depositDiff, (1))  // Leave 1 wei
});

// 7. Compare balances - CRITICAL slippage check
calls[6] = MultiCall({
    target: creditFacade,
    callData: abi.encodeCall(
        ICreditFacadeV3Multicall.compareBalances,
        ()
    )
});

// 8. Set quota for yvWETH
calls[7] = MultiCall({
    target: creditFacade,
    callData: abi.encodeCall(
        ICreditFacadeV3Multicall.updateQuota,
        (yvWETH, int96(50_000 * 10**6), uint96(50_000 * 10**6))
    )
});
```

## Gotchas

### Expected Balances Must Not Already Be Set

`storeExpectedBalances` reverts if already called without a `compareBalances`:

```solidity
// First store - OK
storeExpectedBalances(deltas1);

// Second store without compare - REVERTS
storeExpectedBalances(deltas2);

// Correct pattern:
storeExpectedBalances(deltas1);
// ... operations ...
compareBalances();
storeExpectedBalances(deltas2);  // Now OK
```

### Compare Reverts If Not Stored

`compareBalances` reverts if no expected balances were stored:

```solidity
// This reverts - nothing to compare against
compareBalances();
```

### Delta Calculation

The delta is added to CURRENT balance, not starting balance:

```solidity
// If account has 10 WETH and you set delta = +5
// Expected balance = 10 + 5 = 15 WETH

// For spending tokens, use negative delta
// If spending up to 1000 USDC:
BalanceDelta({token: usdc, amount: -1000 * 10**6})
```

### Available in All Multicalls

Unlike most operations, slippage checks work in:
- `openCreditAccount`
- `multicall`
- `closeCreditAccount`
- `botMulticall`
- `liquidateCreditAccount`

### Gas Optimization

For simple swaps, you can rely on the DEX's slippage parameter:

```solidity
// Uniswap's amountOutMinimum is often sufficient
ISwapRouter.ExactInputSingleParams({
    // ...
    amountOutMinimum: minWethOut,  // Built-in slippage protection
    // ...
})
```

Use `storeExpectedBalances`/`compareBalances` for:
- Multi-hop routes where intermediate tokens aren't checked
- Complex strategies with multiple operations
- When you need to check multiple tokens atomically

## See Also

- [Making External Calls](./making-external-calls.md) - Swap via adapters
- [Updating Price Feeds](./updating-price-feeds.md) - Price updates before operations
- [The Diff Pattern](../multicalls.md#the-diff-pattern) - Handling unknown amounts
