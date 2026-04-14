# Bot System

Gearbox V3 features a sophisticated bot permission system that allows automated management of Credit Accounts. Bots can execute operations on behalf of account owners with granular, revocable permissions.

## BotList Architecture

### Components

| Component | Description |
|-----------|-------------|
| **BotListV3** | Registry storing `(bot, creditManager, creditAccount)` -> permissions |
| **IBot interface** | Bots implement `requiredPermissions()` to declare needed permissions |
| **CreditFacadeV3** | Entry point for bot execution via `botMulticall` |

### Permission Storage

```solidity
// BotListV3 storage
mapping(address bot =>
    mapping(address creditManager =>
        mapping(address creditAccount => uint192 permissions)
    )
) internal _permissions;
```

***

## Permission Model

### Permission Flags

Permissions are stored as a `uint192` bitmask:

| Permission | Value | Operation |
|------------|-------|-----------|
| `ADD_COLLATERAL_PERMISSION` | `1 << 0` | Add funds to account |
| `INCREASE_DEBT_PERMISSION` | `1 << 1` | Borrow more from pool |
| `DECREASE_DEBT_PERMISSION` | `1 << 2` | Repay debt |
| `WITHDRAW_COLLATERAL_PERMISSION` | `1 << 5` | Withdraw assets |
| `UPDATE_QUOTA_PERMISSION` | `1 << 6` | Change token quotas |
| `SET_BOT_PERMISSIONS_PERMISSION` | `1 << 8` | Manage other bots |
| `EXTERNAL_CALLS_PERMISSION` | `1 << 16` | Execute adapter calls |

### ALL_PERMISSIONS Constant

```solidity
uint192 ALL_PERMISSIONS = ADD_COLLATERAL_PERMISSION
    | INCREASE_DEBT_PERMISSION
    | DECREASE_DEBT_PERMISSION
    | WITHDRAW_COLLATERAL_PERMISSION
    | UPDATE_QUOTA_PERMISSION
    | EXTERNAL_CALLS_PERMISSION;
```

Note: `SET_BOT_PERMISSIONS_PERMISSION` is excluded from `ALL_PERMISSIONS` - bots cannot grant permissions to other bots.

***

## Granting Permissions

### Setting Bot Permissions

Account owners grant permissions through a multicall:

```solidity
function _setBotPermissions(address creditAccount, bytes calldata callData) internal {
    (address bot, uint192 permissions) = abi.decode(callData, (address, uint192));

    // Cannot grant SET_BOT_PERMISSIONS_PERMISSION
    uint192 allowedPermissions = ALL_PERMISSIONS & ~SET_BOT_PERMISSIONS_PERMISSION;
    uint192 unexpectedPermissions = permissions & ~allowedPermissions;
    if (unexpectedPermissions != 0) revert UnexpectedPermissionsException(unexpectedPermissions);

    uint256 remainingBots = IBotListV3(botList).setBotPermissions({
        bot: bot,
        creditAccount: creditAccount,
        permissions: permissions
    });

    // Update BOT_PERMISSIONS_SET_FLAG
    // ...
}
```

### Process

1. Owner calls `setBotPermissions(botAddress, permissions)` in multicall
2. BotListV3 validates permissions match bot's `requiredPermissions()`
3. Max 5 active bots per account (`MAX_SANE_ACTIVE_BOTS`)
4. Revoke by setting `permissions = 0`
5. `eraseAllBotPermissions()` clears all (called automatically on account close)

### BOT_PERMISSIONS_SET_FLAG

This optimization flag indicates whether an account has any authorized bots:
- Set `true` when first bot is added
- Set `false` when last bot is removed
- Checked in `botMulticall` before querying BotListV3

```typescript
// TypeScript: Setting bot permissions
import { encodeFunctionData } from 'viem';

const ADD_COLLATERAL = 1n << 0n;
const DECREASE_DEBT = 1n << 2n;
const EXTERNAL_CALLS = 1n << 16n;

// Grant bot permission to add collateral, repay debt, and make external calls
const permissions = ADD_COLLATERAL | DECREASE_DEBT | EXTERNAL_CALLS;

const calls = [
  {
    target: facadeAddress,
    callData: encodeFunctionData({
      abi: creditFacadeMulticallAbi,
      functionName: 'setBotPermissions',
      args: [botAddress, permissions]
    })
  }
];

await creditFacade.write.multicall([creditAccount, calls]);
```

***

## Bot Operations

### botMulticall Execution

```solidity
function botMulticall(address creditAccount, MultiCall[] calldata calls)
    external whenNotPaused whenNotExpired nonReentrant
{
    _getBorrowerOrRevert(creditAccount);

    // Check bot status
    (uint256 botPermissions, bool forbidden) =
        IBotListV3(botList).getBotStatus({bot: msg.sender, creditAccount: creditAccount});

    if (forbidden || botPermissions == 0 ||
        _flagsOf(creditAccount) & BOT_PERMISSIONS_SET_FLAG == 0) {
        revert NotApprovedBotException(msg.sender);
    }

    // Execute with permission checks
    _multicall(creditAccount, calls, _enabledTokensMaskOf(creditAccount), botPermissions);
}
```

### Execution Flow

1. **Status Check**: Query BotListV3 for permissions & forbidden status
2. **Flag Check**: Verify `BOT_PERMISSIONS_SET_FLAG` is set
3. **Granular Authorization**: Each call checked against permission bitmask
4. **Solvency Guard**: Always `fullCollateralCheck` after all calls
5. **Revert**: If HF < 1 after execution

### Permission Enforcement

```solidity
function _revertIfNoPermission(uint256 flags, uint256 permission) internal pure {
    if (flags & permission == 0) {
        revert NoPermissionException(permission);
    }
}
```

Used throughout multicall processing:
```solidity
_revertIfNoPermission(flags, ADD_COLLATERAL_PERMISSION);
_revertIfNoPermission(flags, UPDATE_QUOTA_PERMISSION);
_revertIfNoPermission(flags, WITHDRAW_COLLATERAL_PERMISSION);
_revertIfNoPermission(flags, INCREASE_DEBT_PERMISSION);
_revertIfNoPermission(flags, EXTERNAL_CALLS_PERMISSION);
```

***

## Safety Model

### Security Properties

| Property | Mechanism |
|----------|-----------|
| **Isolation** | Permissions are account-specific (not global) |
| **Immutability** | Bots are typically immutable contracts |
| **DAO Override** | Global "forbid" list in BotListV3 |
| **Atomic Safety** | Post-execution collateral check prevents fund theft |
| **No Bad Debt** | Bots cannot leave protocol with losses |

### Forbidden Bot List

The DAO can globally forbid malicious bots:

```solidity
// In BotListV3
function setBotForbiddenStatus(address bot, bool forbidden) external;
```

A forbidden bot cannot execute on any account, regardless of individual permissions.

### Collateral Check Protection

Even with all permissions, a bot cannot:
- Leave account with HF < 1
- Increase forbidden token balances
- Bypass debt limits

The final collateral check after `botMulticall` ensures account remains healthy.

```typescript
// TypeScript: Bot executing operations
const botClient = createWalletClient({
  account: botAccount,
  chain: mainnet,
  transport: http(),
});

const creditFacade = getContract({
  address: facadeAddress,
  abi: creditFacadeV3Abi,
  client: botClient,
});

// Bot-initiated operations
const calls = [
  // Add collateral
  {
    target: facadeAddress,
    callData: encodeFunctionData({
      abi: creditFacadeMulticallAbi,
      functionName: 'addCollateral',
      args: [usdcAddress, parseUnits('1000', 6)]
    })
  },
  // Execute swap via adapter
  {
    target: uniswapAdapterAddress,
    callData: encodeFunctionData({
      abi: uniswapAdapterAbi,
      functionName: 'exactInputSingle',
      args: [swapParams]
    })
  }
];

// Execute as bot
await creditFacade.write.botMulticall([creditAccountAddress, calls]);
```

***

## Bot Development

### Implementing IBot Interface

```solidity
interface IBot {
    function requiredPermissions() external view returns (uint192);
}
```

Bots should declare minimum permissions needed:

```solidity
contract MyRebalanceBot is IBot {
    function requiredPermissions() external pure returns (uint192) {
        return UPDATE_QUOTA_PERMISSION | EXTERNAL_CALLS_PERMISSION;
    }

    function rebalance(address creditAccount, address creditFacade) external {
        // Build multicall
        MultiCall[] memory calls = _buildRebalanceCalls(creditAccount);

        // Execute
        ICreditFacadeV3(creditFacade).botMulticall(creditAccount, calls);
    }
}
```

### Common Bot Patterns

| Bot Type | Typical Permissions |
|----------|-------------------|
| **Rebalance Bot** | `UPDATE_QUOTA_PERMISSION`, `EXTERNAL_CALLS_PERMISSION` |
| **Collateral Manager** | `ADD_COLLATERAL_PERMISSION`, `WITHDRAW_COLLATERAL_PERMISSION` |
| **Debt Manager** | `INCREASE_DEBT_PERMISSION`, `DECREASE_DEBT_PERMISSION` |
| **Partial Liquidation Bot** | `DECREASE_DEBT_PERMISSION`, `EXTERNAL_CALLS_PERMISSION` |

```typescript
// TypeScript: Checking bot permissions
const botList = getContract({
  address: botListAddress,
  abi: botListV3Abi,
  client: publicClient,
});

// Get bot status for specific account
const [permissions, forbidden] = await botList.read.getBotStatus([
  botAddress,
  creditAccountAddress
]);

console.log(`Permissions: ${permissions.toString(2)}`); // Binary representation
console.log(`Forbidden: ${forbidden}`);

// Check specific permission
const hasExternalCalls = (permissions & (1n << 16n)) !== 0n;
console.log(`Can make external calls: ${hasExternalCalls}`);
```

<details>

<summary>Sources</summary>

* [contracts/core/BotListV3.sol](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/core/BotListV3.sol)
* [contracts/interfaces/IBotListV3.sol](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/interfaces/IBotListV3.sol)
* [contracts/interfaces/base/IBot.sol](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/interfaces/base/IBot.sol)
* [contracts/credit/CreditFacadeV3.sol](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/credit/CreditFacadeV3.sol)

</details>
