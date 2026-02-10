# Credit Account Workflows

Manage leveraged positions on Gearbox from Solidity. This guide covers discovering markets, opening accounts, managing positions, and monitoring health.

> For SDK credit account operations, see [Credit Accounts](../sdk-guide/credit-accounts.md).

## Discovering Markets

Find credit managers and their facades programmatically using ContractsRegister:

```solidity
import {IAddressProviderV3} from "@gearbox-protocol/core-v3/contracts/interfaces/IAddressProviderV3.sol";
import {IContractsRegister} from "@gearbox-protocol/core-v3/contracts/interfaces/IContractsRegister.sol";
import {ICreditManagerV3} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditManagerV3.sol";

IAddressProviderV3 ap = IAddressProviderV3(ADDRESS_PROVIDER);
address cr = ap.getAddressOrRevert("CONTRACTS_REGISTER", 3_00);

// Get all credit managers
address[] memory allCMs = IContractsRegister(cr).getCreditManagers();
```

**Example:** Find USDC credit managers

```solidity
function findUSDCCreditManagers(address addressProvider, address usdc)
    external view returns (address[] memory facades)
{
    IAddressProviderV3 ap = IAddressProviderV3(addressProvider);
    address cr = ap.getAddressOrRevert("CONTRACTS_REGISTER", 3_00);
    address[] memory allCMs = IContractsRegister(cr).getCreditManagers();

    uint256 count;
    for (uint256 i = 0; i < allCMs.length; i++) {
        if (ICreditManagerV3(allCMs[i]).underlying() == usdc) count++;
    }

    facades = new address[](count);
    uint256 j;
    for (uint256 i = 0; i < allCMs.length; i++) {
        ICreditManagerV3 cm = ICreditManagerV3(allCMs[i]);
        if (cm.underlying() == usdc) {
            facades[j++] = cm.creditFacade();
        }
    }
}
```

## Opening a Credit Account

Open a leveraged position by providing collateral and borrowing funds through the CreditFacade:

```solidity
import {ICreditFacadeV3} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditFacadeV3.sol";
import {ICreditFacadeV3Multicall} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditFacadeV3Multicall.sol";
import {MultiCall} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditFacadeV3.sol";

function openCreditAccount(
    address onBehalfOf,
    MultiCall[] calldata calls,
    uint256 referralCode
) external payable returns (address creditAccount);
```

**Example:**

```solidity
ICreditFacadeV3 facade = ICreditFacadeV3(facadeAddress);
ICreditManagerV3 creditManager = ICreditManagerV3(facade.creditManager());
address underlying = creditManager.underlying();

// Build initial multicall: add collateral + increase debt
MultiCall[] memory calls = new MultiCall[](2);
calls[0] = MultiCall({
    target: facadeAddress,
    callData: abi.encodeCall(
        ICreditFacadeV3Multicall.addCollateral,
        (underlying, 10_000e6)
    )
});
calls[1] = MultiCall({
    target: facadeAddress,
    callData: abi.encodeCall(
        ICreditFacadeV3Multicall.increaseDebt,
        (40_000e6)
    )
});

// Approve collateral to Credit Manager (not Facade!)
IERC20(underlying).approve(address(creditManager), 10_000e6);

// Open account
address creditAccount = facade.openCreditAccount(
    msg.sender,  // onBehalfOf
    calls,       // initial operations
    0            // referralCode
);
```

### Debt Limits

Check borrowing constraints before opening:

```solidity
// Get min and max debt allowed
(uint128 minDebt, uint128 maxDebt) = facade.debtLimits();
require(borrowAmount >= minDebt && borrowAmount <= maxDebt, "Invalid debt");
```

## Managing Active Positions

Execute operations on existing credit accounts using multicalls:

```solidity
function multicall(
    address creditAccount,
    MultiCall[] calldata calls
) external payable;
```

### Adding Collateral

Deposit additional tokens to improve health factor:

```solidity
MultiCall[] memory calls = new MultiCall[](1);
calls[0] = MultiCall({
    target: address(facade),
    callData: abi.encodeCall(
        ICreditFacadeV3Multicall.addCollateral,
        (tokenAddress, amount)
    )
});

// Approve to Credit Manager first
IERC20(tokenAddress).approve(address(creditManager), amount);

facade.multicall(creditAccount, calls);
```

### Increasing Debt

Borrow more funds from the pool:

```solidity
MultiCall[] memory calls = new MultiCall[](1);
calls[0] = MultiCall({
    target: address(facade),
    callData: abi.encodeCall(
        ICreditFacadeV3Multicall.increaseDebt,
        (additionalDebt)
    )
});

facade.multicall(creditAccount, calls);
```

### Executing Swaps via Adapters

Trade collateral through whitelisted protocols. First, discover the adapter:

```solidity
// Get adapter for target protocol
address uniswapAdapter = creditManager.contractToAdapter(UNISWAP_V3_ROUTER);
require(uniswapAdapter != address(0), "Protocol not allowed");
```

**Example:** Swap using Uniswap V3 adapter

```solidity
MultiCall[] memory calls = new MultiCall[](1);
calls[0] = MultiCall({
    target: uniswapAdapter,
    callData: abi.encodeCall(
        ISwapRouter.exactInputSingle,
        ISwapRouter.ExactInputSingleParams({
            tokenIn: usdc,
            tokenOut: weth,
            fee: 3000,
            recipient: creditAccount,
            deadline: block.timestamp,
            amountIn: 10_000e6,
            amountOutMinimum: 3e18,
            sqrtPriceLimitX96: 0
        })
    )
});

facade.multicall(creditAccount, calls);
```

### Withdrawing Collateral

Remove excess collateral while maintaining health:

```solidity
MultiCall[] memory calls = new MultiCall[](1);
calls[0] = MultiCall({
    target: address(facade),
    callData: abi.encodeCall(
        ICreditFacadeV3Multicall.withdrawCollateral,
        (tokenAddress, amount, msg.sender)
    )
});

facade.multicall(creditAccount, calls);
```

## Monitoring Account Health

Calculate health factor to check liquidation risk:

```solidity
import {ICreditManagerV3} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditManagerV3.sol";

enum CollateralCalcTask {
    GENERIC_PARAMS,              // Basic info (debt, cumulative index)
    DEBT_ONLY,                   // Detailed debt (base + quota interest)
    FULL_COLLATERAL_CHECK_LAZY,  // Internal use
    DEBT_COLLATERAL,             // Full debt + Total Value (for Health Factor)
    DEBT_COLLATERAL_SAFE_PRICES  // Uses safe pricing
}

function calcDebtAndCollateral(
    address creditAccount,
    CollateralCalcTask task
) external view returns (CollateralDebtData memory cdd);
```

**Example:**

```solidity
ICreditManagerV3 cm = ICreditManagerV3(creditManagerAddress);

CollateralDebtData memory cdd = cm.calcDebtAndCollateral(
    creditAccount,
    CollateralCalcTask.DEBT_COLLATERAL
);

// Health factor: 10000 = 100% = HF of 1.0
uint256 healthFactor = (cdd.twvUSD * 10000) / cdd.totalDebtUSD;

// Account is liquidatable if HF < 10000
bool liquidatable = healthFactor < 10000;

// Account has buffer if HF > 10100 (1% above liquidation)
bool safe = healthFactor > 10100;
```

### CollateralDebtData Structure

```solidity
struct CollateralDebtData {
    uint256 totalDebtUSD;      // Total debt in USD
    uint256 twvUSD;            // Total Weighted Value in USD
    uint256 enabledTokensMask; // Bitmask of enabled tokens
    uint256 quotedTokensMask;  // Bitmask of tokens with quota
    address[] quotedTokens;    // Addresses of quoted tokens
    address _poolQuotaKeeper;  // Pool quota keeper address
}
```

## Closing Positions

Close account and return remaining funds after repaying debt:

```solidity
function closeCreditAccount(
    address creditAccount,
    MultiCall[] calldata calls
) external payable;
```

**Example:** Unwind position and close

```solidity
// Build multicall to:
// 1. Swap all tokens back to underlying
// 2. Repay remaining debt
// 3. Withdraw leftover to owner

MultiCall[] memory calls = new MultiCall[](3);

// Swap collateral token to underlying via adapter
calls[0] = MultiCall({
    target: uniswapAdapter,
    callData: abi.encodeCall(
        ISwapRouter.exactInputSingle,
        ISwapRouter.ExactInputSingleParams({
            tokenIn: weth,
            tokenOut: underlying,
            fee: 3000,
            recipient: creditAccount,
            deadline: block.timestamp,
            amountIn: wethBalance,
            amountOutMinimum: minUnderlyingOut,
            sqrtPriceLimitX96: 0
        })
    )
});

// Decrease debt to zero (protocol calculates exact amount)
calls[1] = MultiCall({
    target: address(facade),
    callData: abi.encodeCall(
        ICreditFacadeV3Multicall.decreaseDebt,
        (type(uint256).max)  // max = full repayment
    )
});

// Withdraw remaining underlying
calls[2] = MultiCall({
    target: address(facade),
    callData: abi.encodeCall(
        ICreditFacadeV3Multicall.withdrawCollateral,
        (underlying, type(uint256).max, msg.sender)
    )
});

facade.closeCreditAccount(creditAccount, calls);
```

## Configuration and Limits

Query market parameters and restrictions:

### Debt Limits

```solidity
// Min and max borrowable amount
(uint128 minDebt, uint128 maxDebt) = facade.debtLimits();
```

### Liquidation Thresholds

```solidity
// Get liquidation threshold for specific token (basis points)
uint16 lt = creditManager.liquidationThresholds(tokenAddress);

// LT of 8000 = 80% = token contributes 80% of value to collateral
```

### Forbidden Tokens

```solidity
// Bitmask of forbidden tokens
uint256 forbiddenMask = facade.forbiddenTokenMask();

// Check if specific token mask is forbidden
bool isForbidden = (forbiddenMask & tokenMask) != 0;
```

### Collateral Tokens

Enumerate all allowed collateral:

```solidity
uint8 tokenCount = creditManager.collateralTokensCount();

for (uint8 i = 0; i < tokenCount; i++) {
    uint256 mask = 1 << i;
    (address token, uint16 lt) = creditManager.collateralTokenByMask(mask);
    // token address and liquidation threshold
}
```

### Fee Configuration

```solidity
(
    uint16 feeInterest,              // Interest fee (bp)
    uint16 feeLiquidation,           // Liquidation fee (bp)
    uint16 liquidationPremium,       // Liquidator premium (bp)
    uint16 feeLiquidationExpired,    // Expired liquidation fee (bp)
    uint16 liquidationPremiumExpired // Expired liquidator premium (bp)
) = creditManager.fees();
```

## Complete Example

Full integration showing position lifecycle:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

import {ICreditFacadeV3} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditFacadeV3.sol";
import {ICreditFacadeV3Multicall} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditFacadeV3Multicall.sol";
import {ICreditManagerV3} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditManagerV3.sol";
import {MultiCall} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditFacadeV3.sol";
import {CollateralDebtData, CollateralCalcTask} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditManagerV3.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract LeveragedTrading {
    ICreditFacadeV3 public immutable facade;
    ICreditManagerV3 public immutable creditManager;
    address public immutable underlying;

    constructor(address _facade) {
        facade = ICreditFacadeV3(_facade);
        creditManager = ICreditManagerV3(facade.creditManager());
        underlying = creditManager.underlying();
    }

    function openPosition(
        uint256 collateral,
        uint256 leverage
    ) external returns (address creditAccount) {
        // Calculate debt for desired leverage
        uint256 borrowAmount = (collateral * (leverage - 1));

        // Validate against limits
        (uint128 minDebt, uint128 maxDebt) = facade.debtLimits();
        require(borrowAmount >= minDebt && borrowAmount <= maxDebt, "Invalid debt");

        // Build multicall: add collateral + increase debt
        MultiCall[] memory calls = new MultiCall[](2);
        calls[0] = MultiCall({
            target: address(facade),
            callData: abi.encodeCall(
                ICreditFacadeV3Multicall.addCollateral,
                (underlying, collateral)
            )
        });
        calls[1] = MultiCall({
            target: address(facade),
            callData: abi.encodeCall(
                ICreditFacadeV3Multicall.increaseDebt,
                (borrowAmount)
            )
        });

        // Transfer collateral from user
        IERC20(underlying).transferFrom(msg.sender, address(this), collateral);

        // Approve to credit manager
        IERC20(underlying).approve(address(creditManager), collateral);

        // Open account
        creditAccount = facade.openCreditAccount(msg.sender, calls, 0);
    }

    function getHealthFactor(address creditAccount)
        external view returns (uint256 healthFactor, bool liquidatable)
    {
        CollateralDebtData memory cdd = creditManager.calcDebtAndCollateral(
            creditAccount,
            CollateralCalcTask.DEBT_COLLATERAL
        );

        healthFactor = (cdd.twvUSD * 10000) / cdd.totalDebtUSD;
        liquidatable = healthFactor < 10000;
    }

    function addCollateralToPosition(
        address creditAccount,
        uint256 amount
    ) external {
        MultiCall[] memory calls = new MultiCall[](1);
        calls[0] = MultiCall({
            target: address(facade),
            callData: abi.encodeCall(
                ICreditFacadeV3Multicall.addCollateral,
                (underlying, amount)
            )
        });

        // Transfer from user and approve
        IERC20(underlying).transferFrom(msg.sender, address(this), amount);
        IERC20(underlying).approve(address(creditManager), amount);

        facade.multicall(creditAccount, calls);
    }

    function closePosition(address creditAccount) external {
        // Build multicall to repay debt and withdraw
        MultiCall[] memory calls = new MultiCall[](2);

        calls[0] = MultiCall({
            target: address(facade),
            callData: abi.encodeCall(
                ICreditFacadeV3Multicall.decreaseDebt,
                (type(uint256).max)  // full repayment
            )
        });

        calls[1] = MultiCall({
            target: address(facade),
            callData: abi.encodeCall(
                ICreditFacadeV3Multicall.withdrawCollateral,
                (underlying, type(uint256).max, msg.sender)
            )
        });

        facade.closeCreditAccount(creditAccount, calls);
    }
}
```

For architectural background, see [Credit Suite Architecture](../concepts/credit-suite.md).
