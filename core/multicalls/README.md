# Multicalls

The multicall logic is primarily orchestrated by the `CreditFacadeV3`. Every multicall must end with a **collateral check** performed by the `CreditManagerV3` to ensure the account remains solvent (Health Factor > 1).

**The MultiCall Structure**

A multicall is an array of the `MultiCall` struct:

```solidity
struct MultiCall {
    address target;   // The address of the CreditFacade or an allowed Adapter
    bytes callData;   // The encoded function call
}
```

#### Execution Flow

When a developer executes `CreditFacadeV3.multicall(...)`, the following sequence occurs:

1. **Start MultiCall**: The Facade emits a `StartMultiCall` event.
2. **Execution Loop**: The Facade iterates through the `MultiCall[]` array.
   * **Target = CreditFacade**: If the target is the Facade itself, it executes internal protocol logic (e.g., `addCollateral`, `increaseDebt`).
   * **Target = Adapter**: If the target is a whitelisted adapter, the Facade sets the account as "active" in the Credit Manager. The adapter then instructs the Credit Account to execute a call on the target DeFi protocol (e.g., Uniswap).
3. **End MultiCall**: The Facade unsets the active account status.
4. **Security Checks**:
   * **Slippage**: Any stored expected balances are compared against current balances.
   * **Forbidden Tokens**: If risky tokens are enabled, the Facade checks that their balances didn't increase.
   * **Full Collateral Check**: The `CreditManager` verifies that the total value of collateral (adjusted by Liquidation Thresholds) covers the debt plus interest.

#### Key Multicall Methods

Developers can use methods defined in [ICreditFacadeV3Multicall.sol](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/interfaces/ICreditFacadeV3Multicall.sol) to compose strategies:

**Protocol Logic**

* **`addCollateral(address token, uint256 amount)`**: Moves tokens from the user's wallet to the Credit Account.
* **`increaseDebt(uint256 amount)`**: Borrows the underlying asset from the Gearbox Pool.
* **`updateQuota(address token, int96 quotaChange, uint96 minQuota)`**: Purchases "quota" for a specific token, which is required to use that token as collateral.
* **`withdrawCollateral(address token, uint256 amount, address to)`**: Removes assets from the account (triggers "Safe Pricing" checks).

**Advanced Safety & Performance**

* **`onDemandPriceUpdates(PriceUpdate[] updates)`**: Must be the **first** call in the array. It pushes fresh price data (e.g., Pyth/Redstone) to the protocol before any math occurs.
* **`storeExpectedBalances(BalanceDelta[] deltas)`**: Records current balances + requested changes to prevent slippage.
* **`compareBalances()`**: Manually triggers a check against the values stored by `storeExpectedBalances`.
* **`setFullCheckParams(uint256[] hints, uint16 minHF)`**: Optimizes the final collateral check by providing "hints" (which tokens to check first) or setting a custom Health Factor threshold higher than 1.0.

### Multicall-supporting functions

All functions in `CreditFacade` that touch the contracts in some way support multicalls. These include:

```solidity
function openCreditAccount(address onBehalfOf, MultiCall[] calldata calls, uint256 referralCode)
    external
    payable
    returns (address creditAccount);

function closeCreditAccount(address creditAccount, MultiCall[] calldata calls) external payable;

function liquidateCreditAccount(address creditAccount, address to, MultiCall[] calldata calls) external;

function multicall(address creditAccount, MultiCall[] calldata calls) external payable;

function botMulticall(address creditAccount, MultiCall[] calldata calls) external;
```

This allows users to do all their required account management in one call. As each multicall (except when closing/liquidating an account) is followed by a collateral check, this helps minimize the gas overhead by batching any required management actions under a single check.

### Multicall flow

All multicalls, regardless of the function, are performed as follows:

1. The Credit Facade receives the `calls` array;
2. The Credit Facade saves the balances of forbidden tokens on the Credit Account (if any);
3. The Credit Facade applies on-demand price feed updates. The Credit Facade always assumes that all price updates are at the beginning of the `calls` array.
4. The Credit Facade goes through `MultiCall` structs one-by-one and parses data depending on the target. If the target is the Credit Facade itself, it attempts to decode the `callData` selector and execute an internal function corresponding to that selector with passed parameters. If the target is a (valid) adapter, the Credit Facade just routes the call to it as-is;
5. After processing all structs, the Credit Facade calls `CreditManagerV3.fullCollateralCheck()` in order to verify account solvency, and checks that forbidden token balances were not increased, and no new forbidden tokens were enabled.

### Simple multicall usage example

```solidity
address accountOwner;

address creditManager;
address creditFacade;

address usdc;
address weth;
address yvWETH;

address uniswapV3Router;

bytes memort yvWETH_priceData;
```

Assume that the expected exchange rate between USDC and ywWETH is 2000 USDC/ywWETH. The following is an example for constructing a multicall that implements this strategy and opening an account with it.

\<Tabs items={\["Solidity"]}>

```solidity

    MultiCall[] memory calls = new MultiCall[](8);

    // All on-demand price feed updates must always go first in the calls array
    calls[0] = MultiCall({
        target: creditFacade,
        callData: abi.encodeCall(ICreditFacadeV3Multicall.onDemandPriceUpdate, (yvWETH, false, ywWETH_priceData))
    });

    calls[1] = MultiCall({
        target: creditFacade,
        callData: abi.encodeCall(ICreditFacadeV3Multicall.addCollateral, (usdc, 10_000 * 10**6))
    });

    calls[2] = MultiCall({
        target: creditFacade,
        callData: abi.encodeCall(ICreditFacadeV3Multicall.increaseDebt, (40_000 * 10**6))
    });

    // Before the external calls, we need to set up a slippage check
    // The minimum output yvWETH amount is (50000 / 2000) * 0.995 = 24.875

    BalanceDelta[] memory deltas = new BalanceDelta[](1);
    deltas[0] = BalanceDelta({
        token: yvWETH,
        amount: (25 * 10**18) * 995 / 1000;
    })

    calls[3] = MultiCall({
        target: creditFacade,
        callData: abi.encodeCall(ICreditFacadeV3Multicall.storeExpectedBalances, (deltas))
    })

    // For external calls, we need to retrieve the adapter addresses, which are unique to each Credit Manager

    address uniswapV3Adapter = ICreditManagerV3(creditManager).contractToAdapter(uniswapV3Router);
    address yvWETHAdapter = ICreditManagerV3(creditManager).contractToAdapter(yvWETH);

    // This is a parameter struct passed into Uniswap's `exactInputSingle`. See
    // https://github.com/Uniswap/v3-periphery/blob/697c2474757ea89fec12a4e6db16a574fe259610/contracts/interfaces/ISwapRouter.sol#L10

    ISwapRouter.ExactInputSingleParams memory params = ISwapRouter.ExactInputSingleParams({
        tokenIn: usdc,
        tokenOut: weth,
        fee: 500,
        recipient: address(0), // For obvious reasons, the adapter overrides this parameter to the credit account address automatically
        deadline: block.timestamp + 3600,
        amountIn: 50_000 * 10**6,
        amountOutMinimum: 0 // We can omit the slippage check here, since we will use Gearbox's native slippage check
        sqrtPriceLimitX96: 0
    });

    calls[4] = MultiCall({
        target: uniswapV3Adapter,
        callData: abi.encodeCall(IUniswapV3Adapter.exactInputSingle, (params))
    });

    // This external call uses a function `depositDiff` unique to the YearnV2 adapter
    // See the `Adapters` section for more info

    calls[5] = MultiCall({
        target: yvWETHAdapter,
        callData: abi.encodeCall(IYearnV2Adapter.depositDiff, (1))
    });

    // After external calls, we perform a slippage check
    calls[6] = MultiCall({
        target: creditFacade,
        callData: abi.encodeCall(ICreditFacadeV3Multicall.compareBalances, ())
    });

    // Finally, we set a quota

    calls[7] = MultiCall({
        target: creditFacade,
        callData: abi.encodeCall(ICreditFacadeV3Multicall.updateQuota, (yvWETH, 50_000 * 10 ** 6, 50_000 * 10 ** 6))
    });

    // Since we are adding collateral from this account, we need to approve tokens
    // Note that the contract to give approval to is Credit Manager, not Credit Facade

    IERC20(usdc).approve(creditManager, 10_000 * 10 ** 6);

    ICreditFacadeV3(creditFacade).openCreditAccount(accountOwner, calls, 0);
```

For details regarding any of the mentioned functions, see the following sections. The specifications for Credit Facade multicall functions can be found [here](https://github.com/Gearbox-protocol/core-v3/blob/ca43d1b9bf79a0c2a71ce4ad6fdcc562bb525ba4/contracts/interfaces/ICreditFacadeV3Multicall.sol#L44).

### TypeScript/viem Example

The same multicall can be constructed in TypeScript using viem's `encodeFunctionData`:

```typescript
import { encodeFunctionData, getContract } from 'viem';
import { iCreditFacadeV300MulticallAbi } from '@gearbox-protocol/sdk';

// Contract setup
const creditFacade = getContract({
  address: creditFacadeAddress,
  abi: creditFacadeAbi,
  client: walletClient,
});

// Build multicall array
const calls: MultiCall[] = [
  // 1. On-demand price update (must be first)
  {
    target: creditFacadeAddress,
    callData: encodeFunctionData({
      abi: iCreditFacadeV300MulticallAbi,
      functionName: 'onDemandPriceUpdates',
      args: [[{ token: yvWETH, reserve: false, data: priceData }]],
    }),
  },
  // 2. Add collateral
  {
    target: creditFacadeAddress,
    callData: encodeFunctionData({
      abi: iCreditFacadeV300MulticallAbi,
      functionName: 'addCollateral',
      args: [usdc, 10_000n * 10n ** 6n],
    }),
  },
  // 3. Borrow
  {
    target: creditFacadeAddress,
    callData: encodeFunctionData({
      abi: iCreditFacadeV300MulticallAbi,
      functionName: 'increaseDebt',
      args: [40_000n * 10n ** 6n],
    }),
  },
  // 4. Store expected balances for slippage check
  {
    target: creditFacadeAddress,
    callData: encodeFunctionData({
      abi: iCreditFacadeV300MulticallAbi,
      functionName: 'storeExpectedBalances',
      args: [[{ token: yvWETH, amount: 24_875n * 10n ** 15n }]], // 24.875 with 0.5% slippage
    }),
  },
  // 5. Swap via adapter (get adapter address from Credit Manager)
  {
    target: uniswapV3Adapter,
    callData: encodeFunctionData({
      abi: uniswapV3AdapterAbi,
      functionName: 'exactInputSingle',
      args: [{
        tokenIn: usdc,
        tokenOut: weth,
        fee: 500,
        recipient: '0x0000000000000000000000000000000000000000', // Adapter overrides
        deadline: BigInt(Math.floor(Date.now() / 1000) + 3600),
        amountIn: 50_000n * 10n ** 6n,
        amountOutMinimum: 0n,
        sqrtPriceLimitX96: 0n,
      }],
    }),
  },
  // 6. Deposit to Yearn
  {
    target: yvWETHAdapter,
    callData: encodeFunctionData({
      abi: yearnV2AdapterAbi,
      functionName: 'depositDiff',
      args: [1n], // Leave 1 wei
    }),
  },
  // 7. Compare balances (slippage check)
  {
    target: creditFacadeAddress,
    callData: encodeFunctionData({
      abi: iCreditFacadeV300MulticallAbi,
      functionName: 'compareBalances',
      args: [],
    }),
  },
  // 8. Set quota for yvWETH
  {
    target: creditFacadeAddress,
    callData: encodeFunctionData({
      abi: iCreditFacadeV300MulticallAbi,
      functionName: 'updateQuota',
      args: [yvWETH, 50_000n * 10n ** 6n, 50_000n * 10n ** 6n],
    }),
  },
];

// Approve collateral to Credit Manager (not Facade!)
await usdc.write.approve([creditManagerAddress, 10_000n * 10n ** 6n]);

// Open account with multicall
const txHash = await creditFacade.write.openCreditAccount([
  accountOwner,
  calls,
  0n, // referralCode
]);
```

**ABI Sources:**

* `iCreditFacadeV300MulticallAbi` - From `@gearbox-protocol/sdk` package
* Adapter ABIs - Generate from contract JSON artifacts or import from SDK

#### Composition Patterns

**1. The "Open and Leverage" Strategy**

A common pattern for opening a position:

1. `addCollateral`: User deposits 1000 USDC.
2. `increaseDebt`: User borrows 4000 USDC (5x leverage).
3. `updateQuota`: User buys quota for WETH.
4. `UniswapAdapter.swap`: Swap 5000 USDC for WETH.

**2. The "Diff" Pattern**

Gearbox adapters often implement `*_diff` functions (e.g., `exactDiffInputSingle`). These are critical for developers because the exact amount of tokens resulting from a previous swap or yield-claiming event is often unknown.

* **Standard swap**: Needs exact `amountIn`.
* **Diff swap**: Calculates `amountIn = currentBalance - leftoverAmount`.

## Using Bots (Security Constraints & Permissions)

Multicalls enforce a granular permission system using a `uint192` bitmask:

| Permission       | Bit       | Purpose                             |
| ---------------- | --------- | ----------------------------------- |
| `ADD_COLLATERAL` | `1 << 0`  | Allow moving funds into the CA.     |
| `INCREASE_DEBT`  | `1 << 1`  | Allow borrowing more from the pool. |
| `UPDATE_QUOTA`   | `1 << 6`  | Allow modifying quota settings.     |
| `EXTERNAL_CALLS` | `1 << 16` | Allow calling external adapters.    |

These permissions are vital when using **Authorized Bots**. A user can delegate `EXTERNAL_CALLS` to a stop-loss bot without granting it `WITHDRAW_COLLATERAL` permission, ensuring the bot can only trade within the account but never steal the funds.

#### Implementation Best Practices

1. **Ordering**: Always put `onDemandPriceUpdates` first if using pull-based oracles.
2. **Slippage**: Always use `storeExpectedBalances` when performing swaps to prevent sandwich attacks.
3. **Dust Management**: Use `type(uint256).max` in `withdrawCollateral` to fully empty a token balance, but be aware it subtracts 1 wei to prevent certain rounding issues in underlying protocols.
4. **Gas Optimization**: Use `setFullCheckParams` with hints for accounts holding many tokens. The collateral check stops as soon as the debt is covered; hinting at the largest positions saves gas.

<details>

<summary>Sources</summary>

* [contracts/credit/CreditFacadeV3.sol](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/credit/CreditFacadeV3.sol)
* [contracts/interfaces/ICreditFacadeV3.sol](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/interfaces/ICreditFacadeV3.sol)
* [contracts/interfaces/ICreditFacadeV3Multicall.sol](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/interfaces/ICreditFacadeV3Multicall.sol)
* [specs/adapters/AdaptersGeneral.spec.md](https://github.com/Gearbox-protocol/integrations-v3/blob/main/specs/adapters/AdaptersGeneral.spec.md)
* [contracts/test/lib/MultiCallBuilder.sol](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/test/lib/MultiCallBuilder.sol)

</details>
