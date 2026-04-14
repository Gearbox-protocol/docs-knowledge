# Protocol Integration

Build smart contracts that compose with Gearbox Credit Accounts.

## Overview

Protocol integration means building contracts that:

* Call Gearbox Credit Accounts from external contracts
* Create automated strategies using multicalls
* Compose Gearbox with your own protocol logic

Unlike adapters (which are called BY Credit Accounts), protocol integrations CALL Credit Accounts from outside.

## Architecture

```
Your Contract -> CreditFacade -> Credit Account -> Adapters -> DeFi Protocols
                      |
                      +-> Multicall execution
                      +-> Collateral checks
                      +-> Access control
```

## Basic Integration Pattern

### 1. Find the Right Market

```solidity
import {IAddressProviderV3} from "@gearbox-protocol/core-v3/contracts/interfaces/IAddressProviderV3.sol";
import {IContractsRegister} from "@gearbox-protocol/core-v3/contracts/interfaces/IContractsRegister.sol";
import {ICreditFacadeV3} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditFacadeV3.sol";

contract MyStrategy {
    IAddressProviderV3 public constant ADDRESS_PROVIDER =
        IAddressProviderV3(0x9ea7b04Da02a5373317D745c1571c84aaD03321D);

    ICreditFacadeV3 public creditFacade;
    address public creditManager;

    function initialize(address _creditManager) external {
        creditManager = _creditManager;

        // Get CreditFacade from CreditManager
        creditFacade = ICreditFacadeV3(
            ICreditManagerV3(_creditManager).creditFacade()
        );
    }
}
```

### 2. Build and Execute Multicalls

```solidity
import {ICreditFacadeV3Multicall} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditFacadeV3Multicall.sol";
import {MultiCall} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditFacadeV3.sol";

function depositToStrategy(
    address creditAccount,
    address token,
    uint256 amount
) external {
    MultiCall[] memory calls = new MultiCall[](1);

    calls[0] = MultiCall({
        target: address(creditFacade),
        callData: abi.encodeCall(
            ICreditFacadeV3Multicall.addCollateral,
            (token, amount)
        )
    });

    // Caller must approve creditManager first
    creditFacade.multicall(creditAccount, calls);
}
```

## Common Integration Patterns

### Automated Strategy Contract

A contract that executes predefined strategies:

```solidity
// SPDX-License-Identifier: GPL-2.0-or-later
pragma solidity ^0.8.17;

import {ICreditFacadeV3} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditFacadeV3.sol";
import {ICreditFacadeV3Multicall} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditFacadeV3Multicall.sol";
import {ICreditManagerV3} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditManagerV3.sol";
import {MultiCall} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditFacadeV3.sol";
import {IUniswapV3Adapter} from "@gearbox-protocol/integrations-v3/contracts/interfaces/uniswap/IUniswapV3Adapter.sol";
import {ISwapRouter} from "@uniswap/v3-periphery/contracts/interfaces/ISwapRouter.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract LeveragedYieldStrategy {
    ICreditFacadeV3 public immutable creditFacade;
    ICreditManagerV3 public immutable creditManager;

    address public immutable underlying;
    address public immutable targetAsset;
    address public immutable uniswapAdapter;
    address public immutable yieldAdapter;

    constructor(
        address _creditManager,
        address _targetAsset,
        address _yieldVault
    ) {
        creditManager = ICreditManagerV3(_creditManager);
        creditFacade = ICreditFacadeV3(creditManager.creditFacade());

        underlying = creditManager.underlying();
        targetAsset = _targetAsset;

        // Find adapters
        uniswapAdapter = creditManager.contractToAdapter(
            0xE592427A0AEce92De3Edee1F18E0157C05861564 // Uniswap V3 Router
        );
        yieldAdapter = creditManager.contractToAdapter(_yieldVault);

        require(uniswapAdapter != address(0), "Uniswap adapter not found");
        require(yieldAdapter != address(0), "Yield adapter not found");
    }

    /// @notice Open leveraged yield position
    /// @param collateralAmount Initial collateral
    /// @param leverage Leverage multiplier (e.g., 4 for 4x)
    /// @param minYieldTokens Minimum yield tokens to receive
    function openPosition(
        uint256 collateralAmount,
        uint256 leverage,
        uint256 minYieldTokens
    ) external returns (address creditAccount) {
        require(leverage >= 1 && leverage <= 10, "Invalid leverage");

        uint256 borrowAmount = collateralAmount * (leverage - 1);

        MultiCall[] memory calls = new MultiCall[](4);

        // 1. Add collateral
        calls[0] = MultiCall({
            target: address(creditFacade),
            callData: abi.encodeCall(
                ICreditFacadeV3Multicall.addCollateral,
                (underlying, collateralAmount)
            )
        });

        // 2. Borrow
        calls[1] = MultiCall({
            target: address(creditFacade),
            callData: abi.encodeCall(
                ICreditFacadeV3Multicall.increaseDebt,
                (borrowAmount)
            )
        });

        // 3. Swap to target asset
        uint256 totalAmount = collateralAmount + borrowAmount;
        ISwapRouter.ExactInputSingleParams memory swapParams = ISwapRouter.ExactInputSingleParams({
            tokenIn: underlying,
            tokenOut: targetAsset,
            fee: 500,
            recipient: address(0),
            deadline: block.timestamp + 3600,
            amountIn: totalAmount,
            amountOutMinimum: 0, // Using yield token check instead
            sqrtPriceLimitX96: 0
        });

        calls[2] = MultiCall({
            target: uniswapAdapter,
            callData: abi.encodeCall(
                IUniswapV3Adapter.exactInputSingle,
                (swapParams)
            )
        });

        // 4. Deposit to yield vault using diff pattern
        calls[3] = MultiCall({
            target: yieldAdapter,
            callData: abi.encodeCall(
                IYearnV2Adapter.depositDiff,
                (1) // Leave 1 wei
            )
        });

        // Approve and open
        IERC20(underlying).transferFrom(msg.sender, address(this), collateralAmount);
        IERC20(underlying).approve(address(creditManager), collateralAmount);

        creditAccount = creditFacade.openCreditAccount(msg.sender, calls, 0);
    }
}
```

### Strategy with Price Updates

When using Pyth or Redstone oracles, your contract must accept and forward price data:

```solidity
/// @notice Execute strategy with price updates
/// @param creditAccount Target Credit Account
/// @param priceUpdates Array of (token, reserve, data) for on-demand oracles
/// @param strategyParams Your strategy-specific parameters
function executeWithPriceUpdates(
    address creditAccount,
    bytes[] calldata priceUpdates,
    StrategyParams calldata strategyParams
) external {
    uint256 numUpdates = priceUpdates.length;

    // Build calls with price updates first
    MultiCall[] memory calls = new MultiCall[](numUpdates + strategyParams.numCalls);

    // Add all price updates at the beginning
    for (uint256 i = 0; i < numUpdates; i++) {
        (address token, bool reserve, bytes memory data) =
            abi.decode(priceUpdates[i], (address, bool, bytes));

        calls[i] = MultiCall({
            target: address(creditFacade),
            callData: abi.encodeCall(
                ICreditFacadeV3Multicall.onDemandPriceUpdate,
                (token, reserve, data)
            )
        });
    }

    // Add strategy calls after price updates
    _buildStrategyCalls(calls, numUpdates, strategyParams);

    creditFacade.multicall(creditAccount, calls);
}
```

### Keeper/Bot Integration

For automated position management:

```solidity
contract PositionKeeper {
    ICreditFacadeV3 public immutable creditFacade;
    address public keeper;

    mapping(address => bool) public managedAccounts;

    modifier onlyKeeper() {
        require(msg.sender == keeper, "Not keeper");
        _;
    }

    /// @notice Rebalance position when health factor is low
    function rebalance(
        address creditAccount,
        address tokenToSell,
        uint256 sellAmount,
        uint256 minRepay
    ) external onlyKeeper {
        require(managedAccounts[creditAccount], "Not managed");

        MultiCall[] memory calls = new MultiCall[](2);

        // 1. Swap collateral for underlying
        calls[0] = MultiCall({
            target: uniswapAdapter,
            callData: abi.encodeCall(
                IUniswapV3Adapter.exactInputSingle,
                (swapParams)
            )
        });

        // 2. Repay debt using diff pattern
        calls[1] = MultiCall({
            target: address(creditFacade),
            callData: abi.encodeCall(
                ICreditFacadeV3Multicall.decreaseDebt,
                (minRepay)
            )
        });

        // Execute as bot (requires bot permissions on account)
        creditFacade.botMulticall(creditAccount, calls);
    }
}
```

## Access Control Considerations

### Account Ownership

Only the account owner (or approved bots) can execute multicalls:

```solidity
// This will revert if msg.sender is not account owner
creditFacade.multicall(creditAccount, calls);

// For keeper/bot access, the owner must grant permissions first
// This is done via setBotPermissions in a multicall
```

### Bot Permissions

To allow external contracts to manage accounts:

```solidity
// Owner grants bot permissions
MultiCall[] memory calls = new MultiCall[](1);
calls[0] = MultiCall({
    target: address(creditFacade),
    callData: abi.encodeCall(
        ICreditFacadeV3Multicall.setBotPermissions,
        (
            botAddress,
            uint192(1 << 0 | 1 << 1) // Permission flags for allowed operations
        )
    )
});

creditFacade.multicall(creditAccount, calls);
```

Then the bot can use `botMulticall`:

```solidity
// Bot executes with limited permissions
creditFacade.botMulticall(creditAccount, calls);
```

## Error Handling

### Reading Account State Before Operations

```solidity
function getAccountHealth(address creditAccount) external view returns (uint256) {
    (
        uint256 debt,
        uint256 cumulativeIndexLastUpdate,
        uint128 cumulativeQuotaInterest,
        uint128 quotaFees,
        uint256 enabledTokensMask,
        uint16 flags,
        uint64 lastDebtUpdate,
        address borrower
    ) = creditManager.creditAccountInfo(creditAccount);

    // Calculate health factor using collateral values
    // ...
}
```

### Handling Reverts

```solidity
function safeExecute(
    address creditAccount,
    MultiCall[] memory calls
) external returns (bool success) {
    try creditFacade.multicall(creditAccount, calls) {
        success = true;
    } catch Error(string memory reason) {
        emit ExecutionFailed(creditAccount, reason);
        success = false;
    }
}
```

## Gas Optimization

### Use Collateral Hints

For accounts with many tokens, provide hints to reduce oracle calls:

```solidity
// Get token masks for primary collateral
uint256 usdcMask = creditManager.getTokenMaskOrRevert(usdc);
uint256 wethMask = creditManager.getTokenMaskOrRevert(weth);

uint256[] memory hints = new uint256[](2);
hints[0] = usdcMask;
hints[1] = wethMask;

// Add setFullCheckParams as first non-price-update call
calls[0] = MultiCall({
    target: address(creditFacade),
    callData: abi.encodeCall(
        ICreditFacadeV3Multicall.setFullCheckParams,
        (hints, 10000) // 1.0 min health factor
    )
});
```

### Batch Operations

Combine related operations in single multicalls rather than multiple transactions:

```solidity
// GOOD - single multicall
MultiCall[] memory calls = new MultiCall[](4);
calls[0] = addCollateralCall;
calls[1] = borrowCall;
calls[2] = swapCall;
calls[3] = depositCall;
creditFacade.multicall(account, calls);

// BAD - multiple transactions (more gas, atomicity issues)
creditFacade.multicall(account, [addCollateralCall]);
creditFacade.multicall(account, [borrowCall]);
creditFacade.multicall(account, [swapCall]);
```

## Testing

### Foundry Setup

```solidity
import {Test} from "forge-std/Test.sol";

contract StrategyTest is Test {
    LeveragedYieldStrategy strategy;
    address user = address(0x1);

    function setUp() public {
        // Fork mainnet
        vm.createSelectFork("mainnet");

        // Deploy strategy
        strategy = new LeveragedYieldStrategy(
            CREDIT_MANAGER,
            TARGET_ASSET,
            YIELD_VAULT
        );
    }

    function test_openPosition() public {
        // Setup
        deal(USDC, user, 10_000e6);
        vm.startPrank(user);
        IERC20(USDC).approve(address(strategy), 10_000e6);

        // Execute
        address account = strategy.openPosition(10_000e6, 4, 0);

        // Verify
        assertTrue(account != address(0));
        assertGt(IERC20(YIELD_TOKEN).balanceOf(account), 0);
        vm.stopPrank();
    }
}
```

## Security Considerations

1. **Reentrancy** - Multicalls are atomic, but be careful with callbacks
2. **Slippage** - Always use `storeExpectedBalances`/`compareBalances` for swaps
3. **Access control** - Verify account ownership before operations
4. **Oracle manipulation** - Use safe pricing for withdrawals
5. **Flash loan attacks** - Consider same-block restrictions on debt changes

## Related

* [Multicalls](../multicalls/) - Core encoding patterns
* [Making External Calls](../multicalls/multicalls/making-external-calls.md) - Using adapters
* [Controlling Slippage](../multicalls/multicalls/controlling-slippage.md) - Protecting operations
* [Adapter Development](adapter-development.md) - Building adapters
