# Credit Manager

The **CreditManagerV3** is the core accounting engine of the Gearbox Protocol. It manages Credit Account lifecycle, tracks debt and collateral, calculates health factors, and enforces risk parameters. All Credit Account state is stored and managed through this contract.

## Core State: CreditAccountInfo

Every Credit Account's state is tracked in a `CreditAccountInfo` struct:

| Field | Type | Description |
|-------|------|-------------|
| `debt` | `uint256` | Principal amount borrowed from the pool |
| `cumulativeIndexLastUpdate` | `uint256` | Pool's interest index at last debt update |
| `cumulativeQuotaInterest` | `uint128` | Accrued quota interest not yet added to debt |
| `quotaFees` | `uint128` | Quota fees owed |
| `enabledTokensMask` | `uint256` | Bitmask of currently enabled collateral tokens |
| `flags` | `uint16` | Account state flags (e.g., `BOT_PERMISSIONS_SET_FLAG`) |
| `lastDebtUpdate` | `uint64` | Timestamp of last debt change (flash-loan protection) |
| `borrower` | `address` | Current account owner |

***

## Debt Tracking Architecture

### Indexed Interest Accrual

The Credit Manager uses an indexed interest model rather than storing accrued interest directly. This approach is gas-efficient because it doesn't require per-block updates.

**Formula:**
```
accruedInterest = debt * (currentIndex - lastIndex) / lastIndex
totalDebt = principal + accruedInterest + quotaInterest + fees
```

The `cumulativeIndexLastUpdate` is snapshotted whenever debt changes, allowing the contract to calculate exact interest at any time by comparing against the Pool's current `baseInterestIndex()`.

### Flash-Loan Protection

The `lastDebtUpdate` timestamp prevents multiple debt changes in the same block. This protects against flash-loan attacks where an attacker could:
1. Borrow heavily
2. Manipulate prices
3. Close position profitably

Any second debt change in the same block will revert.

***

## Collateral Management

### Token Masking System

Every collateral token has a unique `uint256` mask (power of 2). An account's `enabledTokensMask` is the bitwise OR of all enabled token masks.

**Benefits:**
- **O(enabled_tokens) iteration**: Health checks only iterate over enabled tokens, not all possible collateral
- **Gas efficiency**: Single storage slot tracks all enabled/disabled states
- **Atomic updates**: Enable/disable multiple tokens in one operation

```typescript
// TypeScript: Checking enabled tokens
const enabledMask = await creditManager.read.enabledTokensMaskOf([creditAccount]);

// Get all enabled token addresses
const collateralTokens = [];
for (let i = 0; i < 256; i++) {
  if (enabledMask & (1n << BigInt(i))) {
    const tokenData = await creditManager.read.getTokenByMask([1n << BigInt(i)]);
    collateralTokens.push(tokenData);
  }
}
```

### Liquidation Thresholds (LT)

Each collateral token has a Liquidation Threshold determining how much of its value counts toward collateralization:

| Parameter | Description |
|-----------|-------------|
| `ltInitial` | Starting LT value (e.g., 8500 = 85%) |
| `ltFinal` | Final LT after ramping |
| `timestampRampStart` | When LT ramping begins |
| `rampDuration` | Duration of linear interpolation |

**LT Ramping** allows gradual changes to risk parameters without sudden liquidation cascades. The current LT is linearly interpolated between `ltInitial` and `ltFinal` over the ramp period.

### Phantom Tokens

Phantom tokens are virtual representations of staked/LP positions (e.g., staked Curve LP tokens). They implement `IPhantomToken.getPhantomTokenInfo()` which returns the underlying deposited token.

During health factor calculations, phantom tokens are resolved to their underlying value, ensuring proper collateral accounting for wrapped positions.

***

## Health Factor Calculation

### TWV Formula

The Health Factor determines whether an account is solvent:

```
TWV (Threshold Weighted Value) = Sum(Balance_i * Price_i * LT_i)
TotalDebt = principal + baseInterest + quotaInterest + fees
HealthFactor = TWV / TotalDebt
```

An account is:
- **Healthy**: HF >= 1.0 (10000 in basis points)
- **Liquidatable**: HF < 1.0

### Collateral Calculation Modes

The Credit Manager supports different calculation modes for gas optimization:

| Mode | Use Case |
|------|----------|
| `DEBT_ONLY` | Calculate debt + interest without collateral |
| `DEBT_COLLATERAL` | Full TWV + HF calculation |
| `FULL_COLLATERAL_CHECK_LAZY` | Optimized: stops early when HF exceeds threshold |

The lazy mode is used during multicalls where we only need to verify HF > 1, not calculate the exact value.

```typescript
// TypeScript: Reading account health
import { getContract } from 'viem';

const creditManager = getContract({
  address: creditManagerAddress,
  abi: creditManagerV3Abi,
  client: publicClient,
});

// Get full debt breakdown
const debtData = await creditManager.read.calcDebtAndCollateral([
  creditAccount,
  2 // CollateralCalcTask.DEBT_COLLATERAL
]);

// debtData returns: { debt, accruedInterest, accruedFees, totalDebtUSD,
//                     totalValue, twvUSD, enabledTokensMask, ... }

const healthFactor = debtData.twvUSD * 10000n / debtData.totalDebtUSD;
console.log(`Health Factor: ${Number(healthFactor) / 100}%`);
```

***

## Pool and Oracle Coordination

### Pool Interaction

The Credit Manager coordinates with PoolV3 for all debt operations:

| Operation | Pool Function |
|-----------|---------------|
| Borrow | `pool.lendCreditAccount(debt, creditAccount)` |
| Repay | `pool.repayCreditAccount(debt, profit, loss)` |
| Interest tracking | `pool.baseInterestIndex()` |

On liquidation with loss, the Credit Manager reports the loss to the Pool, which may burn Treasury shares or incur "uncovered loss" that's socialized across LPs.

### Oracle Interaction

Price data comes from `PriceOracleV3`:

| Function | Description |
|----------|-------------|
| `convertToUSD(amount, token)` | Convert token amount to USD value |
| `getPrice(token)` | Get token price (respects `USE_SAFE_PRICES_FLAG`) |

**Dual Price Safety**: When `USE_SAFE_PRICES_FLAG` is set (for forbidden tokens), the oracle returns `min(primaryPrice, reservePrice)` to protect against price manipulation.

***

## Access Control

The Credit Manager restricts sensitive operations:

| Caller | Allowed Operations |
|--------|-------------------|
| `CreditFacadeV3` | All account operations (open, close, multicall) |
| `CreditConfiguratorV3` | Parameter updates (tokens, adapters, fees) |
| Credit Account (via execute) | Adapter calls during multicall |

External contracts cannot directly manipulate Credit Account state - all operations must flow through the Facade.

<details>

<summary>Sources</summary>

* [contracts/credit/CreditManagerV3.sol](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/credit/CreditManagerV3.sol)
* [contracts/interfaces/ICreditManagerV3.sol](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/interfaces/ICreditManagerV3.sol)
* [contracts/libraries/CreditLogic.sol](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/libraries/CreditLogic.sol)
* [contracts/libraries/CollateralLogic.sol](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/libraries/CollateralLogic.sol)

</details>
