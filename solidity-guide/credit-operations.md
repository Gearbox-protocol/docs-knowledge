# Credit Operations

Interact with CreditFacade and CreditManager from Solidity.

> For SDK credit account operations, see [Credit Accounts](../sdk-guide/credit-accounts.md).

## ICreditFacadeV3

The CreditFacade is the primary entry point for all user operations.

### Core Functions

```solidity
import {ICreditFacadeV3} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditFacadeV3.sol";
import {MultiCall} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditFacadeV3.sol";

ICreditFacadeV3 facade = ICreditFacadeV3(facadeAddress);
```

| Function | Purpose |
|----------|---------|
| `openCreditAccount` | Create new credit account |
| `closeCreditAccount` | Close and return funds |
| `multicall` | Execute operations on existing account |
| `botMulticall` | Bot-initiated operations |
| `liquidateCreditAccount` | Liquidate unhealthy account |

### Opening a Credit Account

```solidity
function openCreditAccount(
    address onBehalfOf,
    MultiCall[] calldata calls,
    uint256 referralCode
) external payable returns (address creditAccount);
```

**Example:**

```solidity
// Build initial multicall (see Multicalls page for encoding)
MultiCall[] memory calls = new MultiCall[](2);
calls[0] = MultiCall({
    target: facadeAddress,
    callData: abi.encodeCall(ICreditFacadeV3Multicall.addCollateral, (usdc, 10_000 * 10**6))
});
calls[1] = MultiCall({
    target: facadeAddress,
    callData: abi.encodeCall(ICreditFacadeV3Multicall.increaseDebt, (40_000 * 10**6))
});

// Approve collateral to Credit Manager (not Facade!)
IERC20(usdc).approve(creditManager, 10_000 * 10**6);

// Open account
address creditAccount = ICreditFacadeV3(facade).openCreditAccount(
    msg.sender,  // onBehalfOf
    calls,       // initial multicall
    0            // referralCode
);
```

### Closing a Credit Account

```solidity
function closeCreditAccount(
    address creditAccount,
    MultiCall[] calldata calls
) external payable;
```

The close multicall typically includes operations to:
1. Swap all tokens back to underlying
2. Repay remaining debt
3. Withdraw remaining funds to owner

### Executing Operations on Existing Account

```solidity
function multicall(
    address creditAccount,
    MultiCall[] calldata calls
) external payable;
```

## ICreditManagerV3

The CreditManager handles internal logic. Use it for reading state, not for user operations.

```solidity
import {ICreditManagerV3} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditManagerV3.sol";

ICreditManagerV3 cm = ICreditManagerV3(creditManagerAddress);
```

### Reading Account State

The most important function for determining solvency:

```solidity
enum CollateralCalcTask {
    GENERIC_PARAMS,      // Basic info (debt, cumulative index)
    DEBT_ONLY,           // Detailed debt (base + quota interest)
    FULL_COLLATERAL_CHECK_LAZY, // Internal use
    DEBT_COLLATERAL,     // Full debt + Total Value (for Health Factor)
    DEBT_COLLATERAL_SAFE_PRICES // Uses safe pricing
}

function calcDebtAndCollateral(
    address creditAccount,
    CollateralCalcTask task
) external view returns (CollateralDebtData memory cdd);
```

**Example:**

```solidity
CollateralDebtData memory cdd = cm.calcDebtAndCollateral(
    creditAccount,
    CollateralCalcTask.DEBT_COLLATERAL
);

// Calculate health factor (10000 = 100% = HF of 1.0)
uint256 healthFactor = (cdd.twvUSD * 10000) / cdd.totalDebtUSD;

// Account is liquidatable if HF < 10000
bool liquidatable = healthFactor < 10000;
```

### Reading Configuration

```solidity
// Debt limits
(uint128 minDebt, uint128 maxDebt) = facade.debtLimits();

// Forbidden tokens
uint256 forbiddenMask = facade.forbiddenTokenMask();

// Liquidation threshold for specific token
uint16 lt = cm.liquidationThresholds(tokenAddress);

// Fee configuration
(
    uint16 feeInterest,
    uint16 feeLiquidation,
    uint16 liquidationPremium,
    uint16 feeLiquidationExpired,
    uint16 liquidationPremiumExpired
) = cm.fees();
```

### Collateral Tokens

```solidity
// Get number of allowed tokens
uint8 tokenCount = cm.collateralTokensCount();

// Iterate through tokens using bitmask
for (uint8 i = 0; i < tokenCount; i++) {
    uint256 mask = 1 << i;
    (address token, uint16 lt) = cm.collateralTokenByMask(mask);
    // token and its liquidation threshold
}
```

### Adapter Discovery

```solidity
// Get adapter for a protocol (e.g., Uniswap V3 Router)
address adapter = cm.contractToAdapter(UNISWAP_V3_ROUTER);

// Adapter is address(0) if protocol not allowed
require(adapter != address(0), "Protocol not allowed");
```

## Complete Example

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

import {ICreditFacadeV3} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditFacadeV3.sol";
import {ICreditFacadeV3Multicall} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditFacadeV3Multicall.sol";
import {ICreditManagerV3} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditManagerV3.sol";
import {MultiCall} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditFacadeV3.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract GearboxIntegration {
    ICreditFacadeV3 public immutable facade;
    ICreditManagerV3 public immutable creditManager;
    address public immutable underlying;

    constructor(address _facade) {
        facade = ICreditFacadeV3(_facade);
        creditManager = ICreditManagerV3(facade.creditManager());
        underlying = creditManager.underlying();
    }

    function openLeveragedPosition(
        uint256 collateral,
        uint256 borrowAmount
    ) external returns (address creditAccount) {
        // Build multicall
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

    function getAccountHealth(address creditAccount) external view returns (uint256 healthFactor) {
        CollateralDebtData memory cdd = creditManager.calcDebtAndCollateral(
            creditAccount,
            CollateralCalcTask.DEBT_COLLATERAL
        );

        healthFactor = (cdd.twvUSD * 10000) / cdd.totalDebtUSD;
    }
}
```

## Next Steps

- [Multicalls](multicalls.md) - MultiCall struct encoding and patterns
- [Pool Operations](pool-operations.md) - Direct pool interaction

For architectural background, see [Credit Suite Architecture](../concepts/credit-suite.md).
