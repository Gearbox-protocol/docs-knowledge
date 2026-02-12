# Core Extension

Advanced patterns for extending Gearbox protocol contracts beyond standard adapter integration.

> This is advanced material. For standard integrations, see [Adapter Development](adapter-development.md) or [Protocol Integration](protocol-integration.md).

## When to Extend vs Integrate

Different levels of integration require different approaches:

| Approach                 | Complexity | When to Use                                                          |
| ------------------------ | ---------- | -------------------------------------------------------------------- |
| **Adapter**              | Low        | Wrap existing DeFi protocols for Credit Account access               |
| **Protocol Integration** | Medium     | Build contracts that compose with Credit Accounts externally         |
| **Core Extension**       | High       | Modify Credit Manager/Pool behavior, create protocol-specific spokes |

Examples by approach:

**Adapter:** Wrapping Uniswap, Curve, Yearn for Credit Account users

**Protocol Integration:** Strategy vaults that open/manage Credit Accounts

**Core Extension:** Custom Credit Manager for protocol-specific accounting, custom interest rate models, pool hooks for fee distribution

Build a core extension when you need to:

* Modify how debt/collateral calculations work
* Change liquidity flow patterns between pools and Credit Managers
* Implement protocol-specific Credit Manager variants ("spokes")
* Create custom interest rate logic beyond linear models
* Add lifecycle hooks to pool operations

## Understanding Money Flows

Core extensions require deep understanding of how liquidity moves through the protocol.

### The Fundamental Flow

```
Lenders → Pool → Credit Manager → Credit Account → DeFi Protocols
         (ERC-4626)      |              |
                         |              +-> Holds collateral
                         +-> Tracks debt
```

**Key invariants:**

1. Pool lends only to whitelisted Credit Managers
2. Credit Managers borrow on behalf of Credit Accounts
3. Credit Accounts hold all collateral and debt
4. All value flows are tracked via indexed interest and quota systems

### Detailed Liquidity Flow

**When borrowing:**

```solidity
// 1. User opens Credit Account via CreditFacade
CreditFacade.openCreditAccount(owner, calls, referralCode)
  |
  v
// 2. Facade instructs Manager to borrow
CreditManager.openCreditAccount(debt, onBehalfOf)
  |
  v
// 3. Manager requests liquidity from Pool
Pool.lendCreditAccount(borrowedAmount, creditAccount)
  |
  v
// 4. Pool transfers underlying directly to Credit Account
IERC20(underlying).transfer(creditAccount, borrowedAmount)
```

**When repaying:**

```solidity
// 1. User closes account via CreditFacade
CreditFacade.closeCreditAccount(creditAccount, calls)
  |
  v
// 2. Manager calculates total debt
totalDebt = principal + accruedInterest + quotaInterest + fees
  |
  v
// 3. Underlying transfers from Credit Account to Pool
IERC20(underlying).transferFrom(creditAccount, pool, totalDebt)
  |
  v
// 4. Manager reports repayment to Pool
Pool.repayCreditAccount(repaidAmount, profit, loss)
```

**Critical detail:** The Credit Manager never holds funds. It orchestrates transfers between Pool and Credit Account while maintaining accounting state.

## Pool Extension Patterns

### Custom Interest Rate Models

The pool queries an external IRM contract for interest rates. You can implement custom logic by deploying a new IRM.

**IInterestRateModel interface:**

```solidity
interface ILinearInterestRateModelV3 {
    function calcBorrowRate(
        uint256 expectedLiquidity,
        uint256 availableLiquidity,
        bool checkOptimalBorrowing
    ) external view returns (uint256 borrowRate);

    function getModelParameters() external view returns (
        uint16 U_1,
        uint16 U_2,
        uint16 R_base,
        uint16 R_slope1,
        uint16 R_slope2,
        uint16 R_slope3
    );
}
```

**Example: Time-weighted interest model**

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

import {ILinearInterestRateModelV3} from "@gearbox-protocol/core-v3/contracts/interfaces/ILinearInterestRateModelV3.sol";

contract TimeWeightedIRM is ILinearInterestRateModelV3 {
    uint16 public immutable U_1 = 7000;  // 70%
    uint16 public immutable U_2 = 9000;  // 90%
    uint16 public immutable R_base = 100;   // 1%
    uint16 public immutable R_slope1 = 200; // 2%
    uint16 public immutable R_slope2 = 500; // 5%

    // Time-based slope adjustment
    uint16 public immutable peakHourMultiplier = 150; // 1.5x during peak hours

    function calcBorrowRate(
        uint256 expectedLiquidity,
        uint256 availableLiquidity,
        bool checkOptimalBorrowing
    ) external view returns (uint256 borrowRate) {
        uint256 utilizationBps = (expectedLiquidity - availableLiquidity)
            * 10_000 / expectedLiquidity;

        // Apply time-based multiplier during peak hours (12-18 UTC)
        uint256 hour = (block.timestamp / 3600) % 24;
        uint16 multiplier = (hour >= 12 && hour < 18) ? peakHourMultiplier : 100;

        // Standard linear calculation with time adjustment
        uint256 baseRate = R_base;

        if (utilizationBps <= U_1) {
            borrowRate = baseRate + (R_slope1 * utilizationBps * multiplier) / 10_000 / 100;
        } else if (utilizationBps <= U_2) {
            borrowRate = baseRate + (R_slope2 * utilizationBps * multiplier) / 10_000 / 100;
        } else {
            borrowRate = baseRate + (R_slope3 * utilizationBps * multiplier) / 10_000 / 100;
        }

        // Convert to RAY (27 decimals)
        borrowRate = borrowRate * 10**27 / 10_000;
    }

    function getModelParameters() external view returns (
        uint16, uint16, uint16, uint16, uint16, uint16
    ) {
        // Return adjusted slope based on current time
        uint256 hour = (block.timestamp / 3600) % 24;
        uint16 adjustedSlope1 = (hour >= 12 && hour < 18)
            ? R_slope1 * peakHourMultiplier / 100
            : R_slope1;

        return (U_1, U_2, R_base, adjustedSlope1, R_slope2, R_slope3);
    }
}
```

**Deploying custom IRM:**

Custom IRMs can be set via governance:

```solidity
// Only CONFIGURATOR can update IRM
IPoolV3(pool).setInterestRateModel(newIRMAddress);
```

### Pool Withdrawal Hooks

Pools in V3 support withdrawal fees. These are not "hooks" in the callback sense, but configurable parameters:

```solidity
// Read current withdrawal fee
uint16 withdrawFee = IPoolV3(pool).withdrawFee(); // basis points

// Fee is applied during withdraw/redeem
uint256 assets = pool.withdraw(amount, receiver, owner);
// Actual received = amount - (amount * withdrawFee / 10000)
```

For custom fee distribution logic, you would typically:

1. Deploy a fee collector contract
2. Configure the pool's treasury address to your collector
3. Implement distribution logic in your collector

## Credit Manager Extension Patterns

### Spoke Development Concept

A "spoke" is a specialized Credit Manager variant designed for protocol-specific use cases. Unlike standard Credit Managers, spokes extend core functionality for unique accounting or liquidity patterns.

**When to build a spoke:**

* Your protocol needs custom collateral valuation logic
* You're integrating Credit Accounts as a core protocol primitive
* You need specialized debt/liquidation mechanics
* You want to modify how positions are opened/closed

**Example use case:** A derivatives protocol where Credit Accounts are used as margin accounts with custom position tracking.

### Spoke Architecture Pattern

```solidity
import {CreditManagerV3} from "@gearbox-protocol/core-v3/contracts/credit/CreditManagerV3.sol";

contract DerivativesSpoke is CreditManagerV3 {
    // Custom state for protocol-specific tracking
    mapping(address => PositionData) public positions;

    struct PositionData {
        uint256 longExposure;
        uint256 shortExposure;
        int256 unrealizedPnL;
    }

    constructor(
        address _pool,
        address _addressProvider
    ) CreditManagerV3(_pool, _addressProvider) {}

    // Override collateral calculation to include unrealized PnL
    function calcDebtAndCollateral(
        address creditAccount,
        CollateralCalcTask task
    ) public view override returns (
        CollateralDebtData memory cdd
    ) {
        // Call parent implementation
        cdd = super.calcDebtAndCollateral(creditAccount, task);

        // Adjust TWV based on unrealized PnL
        PositionData memory pos = positions[creditAccount];
        if (pos.unrealizedPnL > 0) {
            // Add unrealized profit to collateral
            cdd.twvUSD += uint256(pos.unrealizedPnL);
        } else {
            // Subtract unrealized loss from collateral
            cdd.twvUSD -= uint256(-pos.unrealizedPnL);
        }
    }

    // Protocol-specific function to update position state
    function updatePosition(
        address creditAccount,
        uint256 longExposure,
        uint256 shortExposure,
        int256 pnl
    ) external {
        // Only allow calls from authorized adapters
        require(
            adapterToContract[msg.sender] != address(0),
            "Not authorized adapter"
        );

        positions[creditAccount] = PositionData({
            longExposure: longExposure,
            shortExposure: shortExposure,
            unrealizedPnL: pnl
        });
    }
}
```

### Custom Collateral Valuation

Extend collateral calculations for protocol-specific assets:

```solidity
// Override token price resolution
function priceOracle() public view override returns (IPriceOracleV3) {
    return IPriceOracleV3(customOracleAddress);
}

// Implement custom oracle with protocol-specific pricing
contract CustomOracle is IPriceOracleV3 {
    function convertToUSD(
        uint256 amount,
        address token
    ) external view override returns (uint256) {
        if (token == protocolSpecificToken) {
            // Custom valuation logic
            return amount * getCustomPrice() / 10**tokenDecimals;
        }
        return defaultOracle.convertToUSD(amount, token);
    }
}
```

### Extending Liquidation Logic

Custom liquidation premiums based on collateral type:

```solidity
contract CustomLiquidationCM is CreditManagerV3 {
    mapping(address => uint16) public tokenLiquidationPremiums;

    function liquidateCreditAccount(
        address creditAccount,
        address to,
        MultiCall[] calldata calls
    ) external override {
        // Calculate custom premium based on collateral composition
        uint256 enabledMask = enabledTokensMaskOf(creditAccount);
        uint16 premium = _calculatePremium(enabledMask);

        // Set premium temporarily
        uint16 oldPremium = liquidationPremium;
        liquidationPremium = premium;

        // Execute standard liquidation
        super.liquidateCreditAccount(creditAccount, to, calls);

        // Restore
        liquidationPremium = oldPremium;
    }

    function _calculatePremium(uint256 mask) internal view returns (uint16) {
        uint16 maxPremium = 0;
        for (uint256 i = 0; i < 256; i++) {
            if (mask & (1 << i) != 0) {
                address token = getTokenByMask(1 << i);
                if (tokenLiquidationPremiums[token] > maxPremium) {
                    maxPremium = tokenLiquidationPremiums[token];
                }
            }
        }
        return maxPremium;
    }
}
```

## Working with Configurators

The CreditConfigurator provides governance interface for Credit Manager parameters. When building spokes, you typically extend the configurator as well.

### Standard Configurator Usage

```solidity
import {ICreditConfiguratorV3} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditConfiguratorV3.sol";

ICreditConfiguratorV3 configurator = ICreditConfiguratorV3(configuratorAddress);

// Add new collateral token
configurator.addCollateralToken(
    tokenAddress,
    8500  // liquidationThreshold (85% = 8500 basis points)
);

// Add adapter
configurator.allowAdapter(adapterAddress);

// Set fees
configurator.setFees(
    500,   // feeInterest (5%)
    150,   // feeLiquidation (1.5%)
    500,   // liquidationPremium (5%)
    100,   // feeLiquidationExpired (1%)
    500    // liquidationPremiumExpired (5%)
);
```

### Custom Configurator for Spokes

```solidity
import {CreditConfiguratorV3} from "@gearbox-protocol/core-v3/contracts/credit/CreditConfiguratorV3.sol";

contract DerivativesSpokeConfigurator is CreditConfiguratorV3 {
    DerivativesSpoke public immutable spoke;

    constructor(
        address _creditManager,
        address _creditFacade
    ) CreditConfiguratorV3(_creditManager, _creditFacade) {
        spoke = DerivativesSpoke(_creditManager);
    }

    // Protocol-specific configuration
    function setPositionLimits(
        uint256 maxLongExposure,
        uint256 maxShortExposure
    ) external configuratorOnly {
        spoke.setPositionLimits(maxLongExposure, maxShortExposure);
    }

    function setCustomLiquidationPremium(
        address token,
        uint16 premium
    ) external configuratorOnly {
        spoke.setTokenLiquidationPremium(token, premium);
    }
}
```

### Governance Integration

For production deployments, configurator changes should go through governance:

```solidity
// Propose change via governance forum
// After approval, execute via timelock

// Example: Adding new collateral token
bytes memory data = abi.encodeCall(
    ICreditConfiguratorV3.addCollateralToken,
    (newTokenAddress, 8000)
);

// Submit to governance contract
governance.propose(
    configuratorAddress,
    0, // value
    data,
    "Add NEWTOKEN as collateral with 80% LT"
);
```

**Key patterns demonstrated:**

1. **State extension**: Added `Position` tracking on top of base Credit Manager
2. **Collateral override**: Modified TWV calculation to include unrealized PnL
3. **Protocol-specific logic**: Market management and position tracking
4. **Governance integration**: `configuratorOnly` modifier for admin functions

For architectural background, see [Credit Suite Architecture](../../concepts/credit-suite.md) and [Pool Architecture](../../concepts/pools.md).

## Security Considerations

When extending core contracts:

1. **Preserve invariants** - Never break core protocol assumptions (debt tracking, collateral checks)
2. **Test extensively** - Fork mainnet and test against real pools/Credit Managers
3. **Audit thoroughly** - Core extensions require professional audits
4. **Consider upgrade paths** - Plan for parameter changes and emergency controls
5. **Monitor gas costs** - Overrides affect every user operation
6. **Validate inputs** - Custom logic must not allow manipulation of debt/collateral calculations

## Deployment Checklist

* [ ] Core contracts audited by reputable firm
* [ ] Fork tests against production Gearbox contracts
* [ ] Governance proposal prepared with detailed specification
* [ ] Documentation for users and integrators
* [ ] Emergency pause mechanisms tested
* [ ] Oracle manipulation scenarios analyzed
* [ ] Gas profiling completed for all overridden functions
* [ ] Upgradeability plan documented

## Related

* [Adapter Development](adapter-development.md) - Standard integration path
* [Protocol Integration](protocol-integration.md) - Building on top of Credit Accounts
* [Credit Suite Architecture](../../concepts/credit-suite.md) - Core architecture reference
* [Pool Architecture](../../concepts/pools.md) - Pool mechanics reference
