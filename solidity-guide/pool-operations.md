# Pool Operations

Interact with Gearbox pools directly from Solidity. Pools are ERC-4626 compliant vaults.

> For SDK data reading, see [Reading Data](../sdk-guide/reading-data.md).

## IPoolV3

```solidity
import {IPoolV3} from "@gearbox-protocol/core-v3/contracts/interfaces/IPoolV3.sol";

IPoolV3 pool = IPoolV3(poolAddress);
```

## ERC-4626 Standard Functions

Gearbox pools implement the full ERC-4626 tokenized vault standard:

### Deposit

Deposit underlying assets and receive diesel tokens (shares):

```solidity
function deposit(uint256 assets, address receiver) external returns (uint256 shares);
```

**Example:**

```solidity
// Approve underlying first
IERC20(underlying).approve(address(pool), assets);

// Deposit and receive shares
uint256 shares = pool.deposit(assets, msg.sender);

// Preview how many shares you'd receive
uint256 expectedShares = pool.previewDeposit(assets);
```

### Deposit with Referral

Track referrals on-chain:

```solidity
function depositWithReferral(
    uint256 assets,
    address receiver,
    uint256 referralCode
) external returns (uint256 shares);
```

**Example:**

```solidity
IERC20(underlying).approve(address(pool), assets);
uint256 shares = pool.depositWithReferral(assets, msg.sender, 123);
```

### Mint

Mint exact shares, depositing required assets:

```solidity
function mint(uint256 shares, address receiver) external returns (uint256 assets);
```

**Example:**

```solidity
// Preview required assets
uint256 requiredAssets = pool.previewMint(shares);

// Approve and mint
IERC20(underlying).approve(address(pool), requiredAssets);
uint256 assets = pool.mint(shares, msg.sender);
```

### Withdraw

Withdraw exact assets, burning required shares:

```solidity
function withdraw(
    uint256 assets,
    address receiver,
    address owner
) external returns (uint256 shares);
```

**Example:**

```solidity
// Withdraw exact assets
uint256 sharesBurned = pool.withdraw(assets, msg.sender, msg.sender);

// Preview how many shares would be burned
uint256 expectedShares = pool.previewWithdraw(assets);
```

### Redeem

Burn exact shares, receiving assets:

```solidity
function redeem(
    uint256 shares,
    address receiver,
    address owner
) external returns (uint256 assets);
```

**Example:**

```solidity
// Redeem shares for underlying
uint256 assets = pool.redeem(shares, msg.sender, msg.sender);

// Preview how many assets you'd receive
uint256 expectedAssets = pool.previewRedeem(shares);
```

## Gearbox Extensions

### Diesel Rate (Share Price)

```solidity
// Get current share price (in RAY - 27 decimals)
uint256 rate = pool.dieselRate();

// 1 diesel token = rate / 10^27 underlying tokens
```

### Interest Rates

```solidity
// Annual supply rate for lenders (RAY)
uint256 supplyRate = pool.supplyRate();

// Annual borrow rate for Credit Accounts (RAY)
uint256 borrowRate = pool.baseInterestRate();

// Convert to percentage
uint256 supplyAPY = supplyRate * 10000 / 10**27; // basis points
```

### Liquidity State

```solidity
// Total assets in pool
uint256 totalAssets = pool.totalAssets();

// Available for borrowing
uint256 available = pool.availableLiquidity();

// Total supply of diesel tokens
uint256 totalSupply = pool.totalSupply();

// Calculate utilization
uint256 utilization = ((totalAssets - available) * 10000) / totalAssets; // basis points
```

### Underlying Asset

```solidity
// Get underlying token address
address underlying = pool.asset();

// Pool decimals (matches underlying)
uint8 decimals = pool.decimals();

// Pool name and symbol (e.g., "diesel USDC", "dUSDC")
string memory name = pool.name();
string memory symbol = pool.symbol();
```

### Maximum Operations

```solidity
// Maximum depositable assets
uint256 maxDeposit = pool.maxDeposit(receiver);

// Maximum mintable shares
uint256 maxMint = pool.maxMint(receiver);

// Maximum withdrawable assets
uint256 maxWithdraw = pool.maxWithdraw(owner);

// Maximum redeemable shares
uint256 maxRedeem = pool.maxRedeem(owner);
```

## Credit Manager Interaction

Only whitelisted Credit Managers can borrow. Regular users cannot call these:

```solidity
// Credit Manager borrows from pool (CM-only)
function lendCreditAccount(uint256 borrowedAmount, address creditAccount) external;

// Credit Manager repays to pool (CM-only)
function repayCreditAccount(uint256 repaidAmount, uint256 profit, uint256 loss) external;
```

## Related Contracts

### Quota Keeper

```solidity
// Get quota keeper address
address quotaKeeper = pool.poolQuotaKeeper();

// Query quota parameters
IPoolQuotaKeeperV3 qk = IPoolQuotaKeeperV3(quotaKeeper);
(uint16 rate, , , uint96 totalQuoted, uint96 limit, bool isActive) =
    qk.getTokenQuotaParams(tokenAddress);
```

### Interest Rate Model

```solidity
// Get IRM address
address irm = pool.interestRateModel();

// Query model parameters
ILinearInterestRateModelV3 model = ILinearInterestRateModelV3(irm);
(uint16 U1, uint16 U2, uint16 Rbase, uint16 Rslope1, uint16 Rslope2, uint16 Rslope3) =
    model.getModelParameters();
```

## Complete Example

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

import {IPoolV3} from "@gearbox-protocol/core-v3/contracts/interfaces/IPoolV3.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract PoolInteraction {
    IPoolV3 public immutable pool;
    address public immutable underlying;

    constructor(address _pool) {
        pool = IPoolV3(_pool);
        underlying = pool.asset();
    }

    function depositAndGetState(uint256 amount) external returns (
        uint256 shares,
        uint256 supplyAPY,
        uint256 utilization
    ) {
        // Transfer underlying from user
        IERC20(underlying).transferFrom(msg.sender, address(this), amount);

        // Approve and deposit
        IERC20(underlying).approve(address(pool), amount);
        shares = pool.deposit(amount, msg.sender);

        // Read state
        uint256 supplyRate = pool.supplyRate();
        supplyAPY = supplyRate * 10000 / 10**27; // basis points

        uint256 totalAssets = pool.totalAssets();
        uint256 available = pool.availableLiquidity();
        utilization = ((totalAssets - available) * 10000) / totalAssets;
    }

    function redeemAll(address owner) external returns (uint256 assets) {
        uint256 shares = pool.balanceOf(owner);
        require(shares > 0, "No shares");

        // Transfer shares from owner
        IERC20(address(pool)).transferFrom(owner, address(this), shares);

        // Redeem
        assets = pool.redeem(shares, owner, address(this));
    }
}
```

For architectural background, see [Pool Architecture](../concepts/pools.md).
