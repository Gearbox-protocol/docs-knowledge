# Adapter Development

Build adapters to integrate new DeFi protocols with Gearbox Credit Accounts.

## When to Build an Adapter

Build an adapter when you want to enable Credit Accounts to interact with a new DeFi protocol. Consider these options:

| Approach                 | When to Use                                                                                                       |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------- |
| **Build an Adapter**     | The protocol is mature, has significant TVL, and you want it available across all Gearbox Credit Managers         |
| **Protocol Integration** | You're building a protocol that wants to accept Credit Accounts as users (e.g., a DEX accepting leveraged trades) |
| **Direct Contract**      | Your use case doesn't need leverage or margin trading features                                                    |

Adapters make sense for:

* DEX protocols (Uniswap, Curve, Balancer)
* Yield vaults (Yearn, ERC-4626 vaults)
* Liquid staking protocols (Lido, Rocket Pool)
* Lending protocols (Aave, Compound)

Do not build adapters for:

* Protocols with admin keys that can rug users
* Protocols without audits or battle-testing
* Highly experimental or unproven contracts

## Architecture Overview

Adapters sit between Credit Accounts and external protocols:

```
User -> CreditFacade -> CreditAccount -> Adapter -> Target Protocol
                            |               |
                            |               +-> Security enforcement
                            |               +-> Token state updates
                            |               +-> Approval management
                            |
                            +-> Receives output tokens
```

The adapter's job is to:

1. Accept calls from the CreditFacade (not users directly)
2. Translate the call to the target protocol's interface
3. Override recipient addresses to always be the Credit Account
4. Manage token approvals safely
5. Update token states (enable outputs, optionally disable inputs)

For architectural background, see [Multicall System](../../concepts/multicall-system.md).

## Building Your First Adapter

### Step 1: Inherit AbstractAdapter

All adapters extend `AbstractAdapter`:

```solidity
import {AbstractAdapter} from "@gearbox-protocol/core-v3/contracts/adapters/AbstractAdapter.sol";

contract MyVaultAdapter is AbstractAdapter {
    constructor(
        address _creditManager,
        address _targetContract
    ) AbstractAdapter(_creditManager, _targetContract) {}
}
```

**Example:**

```solidity
// Adapter for an ERC-4626 vault
contract ERC4626Adapter is AbstractAdapter {
    constructor(address _creditManager, address _vault)
        AbstractAdapter(_creditManager, _vault)
    {}
}
```

### Step 2: Implement Core Functions

Add wrapper functions that call the target protocol:

```solidity
function deposit(uint256 assets) external creditFacadeOnly returns (uint256 shares) {
    address creditAccount = _creditAccount();
    // Get token addresses
    address asset = IERC4626(targetContract).asset();
    address vault = targetContract;
    // Build the call
    bytes memory callData = abi.encodeCall(
        IERC4626.deposit,
        (assets, creditAccount)  // Override recipient to creditAccount
    );
    // Execute with safe approval pattern
    shares = abi.decode(
        _executeSwapSafeApprove(asset, vault, callData, false),
        (uint256)
    );
}
```

**Example:**

```solidity
// Withdraw function - burn shares, receive assets
function redeem(uint256 shares) external creditFacadeOnly returns (uint256 assets) {
    address creditAccount = _creditAccount();
    address vault = targetContract;
    address asset = IERC4626(vault).asset();

    bytes memory callData = abi.encodeCall(
        IERC4626.redeem,
        (shares, creditAccount, creditAccount)
    );

    assets = abi.decode(
        _executeSwapSafeApprove(vault, asset, callData, false),
        (uint256)
    );
}
```

### Step 3: Implement Diff Functions

Diff functions calculate the input amount from the current balance:

```solidity
// Standard: requires exact amount
function deposit(uint256 assets) external creditFacadeOnly returns (uint256);

// Diff: calculates amount as (balance - leftoverAmount)
function depositDiff(uint256 leftoverAmount) external creditFacadeOnly returns (uint256);
```

**Example:**

```solidity
function depositDiff(uint256 leftoverAmount) external creditFacadeOnly returns (uint256 shares) {
    address creditAccount = _creditAccount();
    address asset = IERC4626(targetContract).asset();

    // Calculate actual deposit amount
    uint256 balance = IERC20(asset).balanceOf(creditAccount);
    uint256 amount = balance - leftoverAmount;

    // Call the standard deposit function
    return deposit(amount);
}
```

**Why diff functions exist:**

When chaining operations, you often don't know exact amounts:

* After a swap, you don't know exact output until execution
* After partial withdrawals, remaining balance is variable
* Diff functions say "use everything except X" instead of "use exactly Y"

### Step 4: Add Security Modifiers

Every external function must use `creditFacadeOnly`:

```solidity
// WRONG - allows anyone to call
function deposit(uint256 amount) external returns (uint256) { ... }

// CORRECT - only CreditFacade can call
function deposit(uint256 amount) external creditFacadeOnly returns (uint256) { ... }
```

**Example:**

```solidity
// All user-facing functions need the modifier
function deposit(uint256 assets) external creditFacadeOnly returns (uint256 shares) { ... }
function depositDiff(uint256 leftover) external creditFacadeOnly returns (uint256 shares) { ... }
function redeem(uint256 shares) external creditFacadeOnly returns (uint256 assets) { ... }
function redeemDiff(uint256 leftover) external creditFacadeOnly returns (uint256 assets) { ... }
```

## Complete Example: ERC-4626 Vault Adapter

Here's a complete adapter for an ERC-4626 vault with all essential patterns:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

import {AbstractAdapter} from "@gearbox-protocol/core-v3/contracts/adapters/AbstractAdapter.sol";
import {AdapterType} from "@gearbox-protocol/core-v3/contracts/interfaces/IAdapter.sol";
import {IERC4626} from "@openzeppelin/contracts/interfaces/IERC4626.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract ERC4626Adapter is AbstractAdapter {
    AdapterType public constant override _gearboxAdapterType = AdapterType.VAULT;

    constructor(address _creditManager, address _vault)
        AbstractAdapter(_creditManager, _vault)
    {}

    // Deposit assets, receive shares
    function deposit(uint256 assets) external creditFacadeOnly returns (uint256 shares) {
        address creditAccount = _creditAccount();
        address asset = IERC4626(targetContract).asset();

        bytes memory callData = abi.encodeCall(
            IERC4626.deposit,
            (assets, creditAccount)
        );

        shares = abi.decode(
            _executeSwapSafeApprove(asset, targetContract, callData, false),
            (uint256)
        );
    }

    // Deposit all assets except leftoverAmount
    function depositDiff(uint256 leftoverAmount) external creditFacadeOnly returns (uint256 shares) {
        address creditAccount = _creditAccount();
        address asset = IERC4626(targetContract).asset();
        uint256 balance = IERC20(asset).balanceOf(creditAccount);

        return deposit(balance - leftoverAmount);
    }

    // Redeem shares, receive assets
    function redeem(uint256 shares) external creditFacadeOnly returns (uint256 assets) {
        address creditAccount = _creditAccount();
        address asset = IERC4626(targetContract).asset();

        bytes memory callData = abi.encodeCall(
            IERC4626.redeem,
            (shares, creditAccount, creditAccount)
        );

        assets = abi.decode(
            _executeSwapSafeApprove(targetContract, asset, callData, false),
            (uint256)
        );
    }

    // Redeem all shares except leftoverAmount
    function redeemDiff(uint256 leftoverAmount) external creditFacadeOnly returns (uint256 assets) {
        address creditAccount = _creditAccount();
        uint256 balance = IERC20(targetContract).balanceOf(creditAccount);

        return redeem(balance - leftoverAmount);
    }
}
```

## Security Patterns Deep Dive

### Why creditFacadeOnly Matters

Without this modifier, an attacker could call adapter functions directly:

**Attack scenario without creditFacadeOnly:**

1. Attacker calls `adapter.deposit(1000)` directly
2. Adapter tries to pull tokens from "current" Credit Account
3. Without CreditFacade context, `_creditAccount()` returns address(0) or wrong account
4. Tokens could be pulled from wrong account or transaction reverts unpredictably

**With creditFacadeOnly:**

1. Only CreditFacade can call the adapter
2. CreditFacade sets the active Credit Account before calling
3. Adapter correctly identifies which account to operate on
4. No unauthorized access possible

```solidity
// The modifier checks that msg.sender is the CreditFacade
modifier creditFacadeOnly() {
    if (msg.sender != creditFacade) revert CallerNotCreditFacadeException();
    _;
}
```

### Recipient Override Pattern

Always hardcode the recipient as the Credit Account. Never accept user-specified recipients.

**Attack scenario without recipient override:**

```solidity
// DANGEROUS - user controls recipient
function withdraw(uint256 shares, address recipient) external creditFacadeOnly {
    IVault(targetContract).redeem(shares, recipient, _creditAccount());
}

// Attacker multicall:
// 1. Deposit 100 ETH to vault
// 2. Call withdraw(shares, attackerAddress)
// 3. Funds sent to attacker instead of Credit Account
// 4. Credit Account has no collateral, but debt remains
```

**Safe pattern:**

```solidity
// CORRECT - recipient is always the Credit Account
function withdraw(uint256 shares) external creditFacadeOnly {
    address creditAccount = _creditAccount();
    IVault(targetContract).redeem(shares, creditAccount, creditAccount);
}
```

### Safe Approval Pattern

Approvals are reset to 1 (not 0) after each operation. This prevents:

* Approval racing attacks
* Gas waste from 0 -> N transitions
* Front-running of approval transactions

```solidity
// _executeSwapSafeApprove does this internally:
// 1. Approve tokenIn to target contract
// 2. Execute the call
// 3. Set approval to 1 (not 0)
// 4. Enable tokenOut
// 5. Optionally disable tokenIn if balance is 1 wei

_executeSwapSafeApprove(
    tokenIn,      // Token being spent
    tokenOut,     // Token being received
    callData,     // The encoded call
    false         // Don't disable tokenIn if non-zero balance remains
);
```

**Why reset to 1 instead of 0:**

* ERC-20 standard: 0 -> N costs more gas than 1 -> N
* Prevents approval race conditions
* Future operations don't need expensive zero-to-nonzero transition

### Token State Management

Adapters automatically update which tokens are "enabled" on the Credit Account:

```solidity
// After a swap USDC -> WETH:
// - WETH mask is enabled (counts toward collateral)
// - USDC mask disabled if balance = 1 wei and disableTokenIn = true

// If disableTokenIn = false:
// - USDC remains enabled even with low balance
// - Useful for partial swaps or when you'll receive more USDC later
```

## Testing with Foundry

Test adapters using Foundry fork tests:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

import {Test} from "forge-std/Test.sol";
import {ERC4626Adapter} from "../adapters/ERC4626Adapter.sol";
import {ICreditManagerV3} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditManagerV3.sol";

contract ERC4626AdapterTest is Test {
    ERC4626Adapter adapter;
    address creditManager = 0x...; // Existing CM on mainnet
    address vault = 0x...;         // Target vault

    function setUp() public {
        // Fork mainnet
        vm.createSelectFork(vm.envString("ETH_RPC_URL"));

        // Deploy adapter
        adapter = new ERC4626Adapter(creditManager, vault);
    }

    function test_deposit() public {
        // Setup: get a credit account with assets
        address creditAccount = _openCreditAccount();

        // Execute deposit via CreditFacade
        uint256 assets = 100e18;
        uint256 shares = adapter.deposit(assets);

        // Assertions
        assertGt(shares, 0, "Should receive shares");
        assertEq(IERC20(vault).balanceOf(creditAccount), shares);
    }

    function test_depositDiff() public {
        address creditAccount = _openCreditAccount();
        uint256 initialBalance = 100e18;
        uint256 leftover = 1;

        uint256 shares = adapter.depositDiff(leftover);

        assertEq(shares, adapter.previewDeposit(initialBalance - leftover));
    }

    function test_cannotCallDirectly() public {
        vm.expectRevert(); // CallerNotCreditFacadeException
        adapter.deposit(100e18);
    }
}
```

**Key test patterns:**

1. **Fork testing** - Test against real protocols on mainnet/testnet
2. **Access control** - Verify creditFacadeOnly works
3. **Balance checks** - Assert correct token transfers
4. **Diff functions** - Verify correct amount calculation
5. **Edge cases** - Test with zero amounts, max values, etc.

## Deployment and Whitelisting

After writing and testing your adapter:

1. **Deploy the adapter** - Deploy to mainnet with CreditManager and target addresses
2. **Submit governance proposal** - Request adapter whitelisting via Gearbox governance
3. **Governance vote** - DAO votes on adding adapter to Credit Manager(s)
4. **Adapter registration** - If approved, adapter is added to allowedAdapters mapping

**Governance process:**

* Submit proposal on Gearbox governance forum
* Include audit report (required for new adapters)
* Specify which Credit Manager(s) should whitelist it
* DAO votes on proposal
* If passed, adapter becomes available for Credit Accounts

**Note:** Each Credit Manager has its own adapter whitelist. An adapter approved for one Credit Manager isn't automatically available on others.

For architectural background, see [Multicall System](../../concepts/multicall-system.md).

## Best Practices

1. **Keep it simple** - Adapters should be thin wrappers, not business logic
2. **No state** - Adapters should be stateless (except immutables)
3. **Comprehensive diff** - Implement diff functions for all variable-amount operations
4. **Always override recipients** - Never let users specify where funds go
5. **Test thoroughly** - Test both success and failure paths
6. **Document clearly** - Write NatSpec comments explaining each function
7. **Declare adapter type** - Set `_gearboxAdapterType` for proper categorization

## Key Inherited Functions

AbstractAdapter provides these helper functions:

| Function                       | Description                             |
| ------------------------------ | --------------------------------------- |
| `_creditAccount()`             | Returns current Credit Account address  |
| `_creditManager()`             | Returns Credit Manager address          |
| `_creditFacade()`              | Returns Credit Facade address           |
| `_getMaskOrRevert(token)`      | Gets token mask, reverts if not allowed |
| `_execute(callData)`           | Executes call on target contract        |
| `_executeSwapSafeApprove(...)` | Executes call with approval management  |
| `targetContract`               | Immutable address of wrapped protocol   |

## Related

* [Making External Calls](../multicalls/multicalls/making-external-calls.md) - Using adapters in multicalls
* [Multicall System](../../concepts/multicall-system.md) - Architectural overview
