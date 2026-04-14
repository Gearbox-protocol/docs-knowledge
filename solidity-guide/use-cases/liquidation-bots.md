# Liquidation Bots

Build on-chain liquidation contracts that can be triggered by keepers or automation services.

> For SDK-based liquidation bots (recommended for most use cases), see [Liquidation Bots (SDK)](../../sdk-guide-typescript/use-cases/liquidation-bots.md).

## Overview

On-chain liquidation contracts are useful when you need:

* Atomicity with flash loans or other on-chain operations
* Integration with existing keeper infrastructure (Gelato, Chainlink Automation)
* Custom liquidation logic that must execute trustlessly
* Protocol-owned liquidation capability

Most liquidation bots use the SDK for monitoring and multicall building, then submit transactions off-chain. This guide covers the less common but important pattern of on-chain liquidation contracts.

***

## Understanding On-Chain Liquidation

**WHY:** Know when to build a contract vs. use the SDK.

### When to Use On-Chain Contracts

| Approach              | Best For                                                                   |
| --------------------- | -------------------------------------------------------------------------- |
| **SDK bot**           | Most liquidators - flexible routing, off-chain simulation, rapid iteration |
| **On-chain contract** | Flash loan liquidations, keeper automation, protocol-owned backstop        |

### The Liquidation Entry Point

```solidity
function liquidateCreditAccount(
    address creditAccount,
    address to,
    MultiCall[] calldata calls,
    bytes memory lossPolicyData
) external;
```

The liquidator provides:

* `creditAccount` - the account to liquidate
* `to` - where remaining funds go after debt repayment
* `calls` - multicall array that converts collateral to underlying
* `lossPolicyData` - custom data for loss handling

***

## Checking Liquidatability

**WHY:** Don't waste gas on accounts that can't be liquidated.

### Health Factor Check

```solidity
import {ICreditManagerV3} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditManagerV3.sol";
import {CollateralDebtData, CollateralCalcTask} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditManagerV3.sol";

function isLiquidatable(
    address creditManager,
    address creditAccount
) public view returns (bool, uint256 healthFactor) {
    CollateralDebtData memory cdd = ICreditManagerV3(creditManager)
        .calcDebtAndCollateral(
            creditAccount,
            CollateralCalcTask.DEBT_COLLATERAL
        );

    healthFactor = (cdd.twvUSD * 10000) / cdd.totalDebtUSD;
    return (healthFactor < 10000, healthFactor);
}
```

### Expiration Check

```solidity
import {ICreditFacadeV3} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditFacadeV3.sol";

function isExpired(address creditFacade) public view returns (bool) {
    uint40 expirationDate = ICreditFacadeV3(creditFacade).expirationDate();
    return expirationDate != 0 && block.timestamp > expirationDate;
}
```

***

## Building Liquidation Multicalls

**WHY:** The multicall converts collateral tokens to underlying. Efficient routing means higher profit.

### Basic Swap Pattern

For a single collateral token, swap it to underlying via the adapter:

```solidity
import {ICreditFacadeV3} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditFacadeV3.sol";
import {ICreditFacadeV3Multicall} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditFacadeV3Multicall.sol";
import {ICreditManagerV3} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditManagerV3.sol";
import {MultiCall} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditFacadeV3.sol";

function buildSwapCalls(
    address creditManager,
    address creditFacade,
    address tokenIn,
    address tokenOut,
    address dexRouter
) internal view returns (MultiCall[] memory calls) {
    // Get adapter for DEX
    address adapter = ICreditManagerV3(creditManager).contractToAdapter(dexRouter);
    require(adapter != address(0), "No adapter");

    calls = new MultiCall[](1);

    // Use diff function to swap entire balance minus 1 wei
    calls[0] = MultiCall({
        target: adapter,
        callData: abi.encodeCall(
            ISwapAdapter.exactAllInputSingle,
            ISwapAdapter.ExactAllInputSingleParams({
                tokenIn: tokenIn,
                tokenOut: tokenOut,
                fee: 3000,
                deadline: block.timestamp,
                rateMinRAY: 0, // Simplified: no slippage protection
                sqrtPriceLimitX96: 0
            })
        )
    });
}
```

### Multi-Collateral Pattern

When an account has multiple collateral tokens:

```solidity
function buildLiquidationCalls(
    address creditManager,
    address creditFacade,
    address underlying,
    address[] memory collateralTokens,
    address dexRouter
) internal view returns (MultiCall[] memory calls) {
    address adapter = ICreditManagerV3(creditManager).contractToAdapter(dexRouter);
    require(adapter != address(0), "No adapter");

    // One swap per non-underlying collateral token
    uint256 swapCount;
    for (uint256 i = 0; i < collateralTokens.length; i++) {
        if (collateralTokens[i] != underlying) swapCount++;
    }

    calls = new MultiCall[](swapCount);
    uint256 callIdx;

    for (uint256 i = 0; i < collateralTokens.length; i++) {
        if (collateralTokens[i] == underlying) continue;

        calls[callIdx] = MultiCall({
            target: adapter,
            callData: abi.encodeCall(
                ISwapAdapter.exactAllInputSingle,
                ISwapAdapter.ExactAllInputSingleParams({
                    tokenIn: collateralTokens[i],
                    tokenOut: underlying,
                    fee: 3000,
                    deadline: block.timestamp,
                    rateMinRAY: 0,
                    sqrtPriceLimitX96: 0
                })
            )
        });
        callIdx++;
    }
}
```

***

## Simple Liquidation Contract

**WHY:** A complete working example you can deploy and test.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

import {ICreditFacadeV3} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditFacadeV3.sol";
import {ICreditFacadeV3Multicall} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditFacadeV3Multicall.sol";
import {ICreditManagerV3} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditManagerV3.sol";
import {MultiCall} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditFacadeV3.sol";
import {CollateralDebtData, CollateralCalcTask} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditManagerV3.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract SimpleLiquidator {
    address public owner;
    address public immutable creditFacade;
    address public immutable creditManager;
    address public immutable underlying;
    address public immutable dexRouter;

    constructor(
        address _creditFacade,
        address _dexRouter
    ) {
        owner = msg.sender;
        creditFacade = _creditFacade;
        creditManager = ICreditFacadeV3(_creditFacade).creditManager();
        underlying = ICreditManagerV3(creditManager).underlying();
        dexRouter = _dexRouter;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    /// @notice Liquidate an account, swapping specified tokens to underlying
    /// @param creditAccount The account to liquidate
    /// @param tokensToSwap Collateral tokens to swap (excluding underlying)
    function liquidate(
        address creditAccount,
        address[] calldata tokensToSwap
    ) external onlyOwner {
        // Build multicall: swap each collateral token to underlying
        address adapter = ICreditManagerV3(creditManager)
            .contractToAdapter(dexRouter);
        require(adapter != address(0), "No adapter for DEX");

        MultiCall[] memory calls = new MultiCall[](tokensToSwap.length);

        for (uint256 i = 0; i < tokensToSwap.length; i++) {
            calls[i] = MultiCall({
                target: adapter,
                callData: abi.encodeCall(
                    ISwapAdapter.exactAllInputSingle,
                    ISwapAdapter.ExactAllInputSingleParams({
                        tokenIn: tokensToSwap[i],
                        tokenOut: underlying,
                        fee: 3000,
                        deadline: block.timestamp,
                        rateMinRAY: 0,
                        sqrtPriceLimitX96: 0
                    })
                )
            });
        }

        // Execute liquidation - remaining funds sent to this contract
        ICreditFacadeV3(creditFacade).liquidateCreditAccount(
            creditAccount,
            address(this), // Receive remaining funds here
            calls,
            "" // lossPolicyData
        );
    }

    /// @notice Check if liquidation would be profitable
    function estimateProfit(
        address creditAccount
    ) external view returns (bool profitable, uint256 healthFactor) {
        CollateralDebtData memory cdd = ICreditManagerV3(creditManager)
            .calcDebtAndCollateral(
                creditAccount,
                CollateralCalcTask.DEBT_COLLATERAL
            );

        healthFactor = (cdd.twvUSD * 10000) / cdd.totalDebtUSD;

        // Profitable if account is liquidatable and has excess value
        profitable = healthFactor < 10000 && cdd.twvUSD > cdd.totalDebtUSD;
    }

    /// @notice Withdraw profits
    function withdraw(address token) external onlyOwner {
        uint256 balance = IERC20(token).balanceOf(address(this));
        if (balance > 0) {
            IERC20(token).transfer(owner, balance);
        }
    }
}
```

***

## Flash Loan Liquidation

**WHY:** Flash loans let you liquidate without upfront capital.

For partial liquidations, the liquidator must provide underlying tokens. Flash loans make this capital-free:

```solidity
import {IFlashLoanReceiver} from "@aave/v3-core/contracts/flashloan/base/FlashLoanSimpleReceiverBase.sol";

contract FlashLiquidator is IFlashLoanReceiver {
    address public immutable creditFacade;
    address public immutable creditManager;
    address public immutable underlying;
    address public immutable aavePool;

    function flashLiquidate(
        address creditAccount,
        address token,
        uint256 repaidAmount
    ) external {
        // Initiate flash loan for repaidAmount of underlying
        bytes memory params = abi.encode(creditAccount, token, repaidAmount);
        IPool(aavePool).flashLoanSimple(
            address(this),
            underlying,
            repaidAmount,
            params,
            0 // referralCode
        );
    }

    function executeOperation(
        address asset,
        uint256 amount,
        uint256 premium,
        address initiator,
        bytes calldata params
    ) external returns (bool) {
        require(msg.sender == aavePool, "Not pool");

        (address creditAccount, address token, uint256 repaidAmount) =
            abi.decode(params, (address, address, uint256));

        // Approve underlying to credit manager
        IERC20(underlying).approve(creditManager, repaidAmount);

        // Execute partial liquidation
        uint256 seized = ICreditFacadeV3(creditFacade)
            .partiallyLiquidateCreditAccount(
                creditAccount,
                token,
                repaidAmount,
                0, // minSeizedAmount (simplified)
                address(this),
                new PriceUpdate[](0)
            );

        // Repay flash loan (amount + premium)
        uint256 amountOwed = amount + premium;
        IERC20(asset).approve(aavePool, amountOwed);

        // Profit = seized token value - flash loan cost
        return true;
    }
}
```

***

## Gotchas

### Approve to Credit Manager, Not Facade

For partial liquidations where you provide underlying:

```solidity
// WRONG
IERC20(underlying).approve(creditFacade, amount);

// CORRECT
IERC20(underlying).approve(creditManager, amount);
```

### Gas Costs Scale with Token Count

Liquidation gas depends on:

* Number of collateral tokens to swap
* Complexity of DEX routes
* Price feed updates needed

Estimate gas before submitting to ensure profitability.

### Race Conditions

Multiple liquidators compete for the same accounts. On-chain contracts are at a disadvantage vs. off-chain bots that can use Flashbots/MEV protection. Consider:

* Using higher priority fees for competitive scenarios
* Targeting accounts that off-chain bots may skip (complex collateral compositions)
* Bundling with Flashbots Protect for MEV protection

### exactAllInputSingle vs exactInputSingle

Use `exactAllInputSingle` (the "diff" pattern) for liquidation swaps. It swaps the entire balance minus dust, which is what you want when converting all collateral:

```solidity
// WRONG: Requires knowing exact balance
abi.encodeCall(ISwapAdapter.exactInputSingle, (...))

// CORRECT: Swaps entire balance automatically
abi.encodeCall(ISwapAdapter.exactAllInputSingle, (...))
```

***

## Next Steps

* [Liquidation Bots (SDK)](../../sdk-guide-typescript/use-cases/liquidation-bots.md) - SDK-based approach (recommended for most cases)
* [Liquidations Reference](../../operations/liquidations.md) - Full liquidation mechanics
* [Bot System Reference](../../operations/bots.md) - Permission system for authorized bots
* [Making External Calls](../multicalls/multicalls/making-external-calls.md) - Adapter patterns for swaps
* [Protocol Integration](protocol-integration.md) - General patterns for building on Gearbox
