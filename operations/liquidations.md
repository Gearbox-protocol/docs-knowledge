# Liquidations

Liquidations are the mechanism that ensures protocol solvency by closing undercollateralized positions. Gearbox V3 supports both **full liquidations** (complete account closure) and **partial liquidations** (debt reduction while keeping account open).

## Full Liquidation Flow

### When Liquidations Occur

An account becomes liquidatable when:
- **Health Factor < 1.0** (undercollateralized)
- **Account has expired** (past the configured expiration timestamp)

Anyone can liquidate an unhealthy account - there's no whitelist.

### Entry Point

```solidity
function liquidateCreditAccount(
    address creditAccount,
    address to,
    MultiCall[] calldata calls,
    bytes memory lossPolicyData
)
```

| Parameter | Description |
|-----------|-------------|
| `creditAccount` | The account to liquidate |
| `to` | Where liquidator receives remaining assets |
| `calls` | Multicall array for converting collateral |
| `lossPolicyData` | Custom data for loss handling |

***

## Liquidation Math

### Core Parameters

| Parameter | Description |
|-----------|-------------|
| **Liquidation Premium** | % of account value liquidator receives as reward |
| **Liquidation Discount** | % used to cover debt and fees (100% - Premium) |

### Fund Distribution Formula

```solidity
uint256 totalFunds = totalValue * liquidationDiscount / PERCENTAGE_FACTOR;
```

**Liabilities** = Total Debt (Principal + Interest + Quota Fees) + DAO Liquidation Fee

### Outcomes

**1. Solvent Liquidation** (`totalFunds > liabilities`)
- Pool repaid in full
- DAO receives liquidation fee
- Remaining funds go to original borrower

**2. Bad Debt** (`totalFunds < liabilities`)
- DAO profit reduced first
- If insufficient, loss reported to Pool
- Pool burns Treasury shares to cover
- If Treasury empty: "uncovered loss" (socialized across LPs)
- Emergency: `maxDebtPerBlockMultiplier` set to 0 to halt borrowing

***

## Step-by-Step Execution

### 1. Trigger and Multicall

Liquidator identifies account with HF < 1 and constructs multicall:

```typescript
// TypeScript: Liquidation bot example
const calls = [
  // Swap collateral tokens to underlying via adapters
  {
    target: uniswapAdapterAddress,
    callData: encodeFunctionData({
      abi: uniswapAdapterAbi,
      functionName: 'exactAllInputSingle',
      args: [{ tokenIn: wbtcAddress, tokenOut: usdcAddress, ... }]
    })
  },
  // Additional swaps as needed...
];

await creditFacade.write.liquidateCreditAccount([
  creditAccountAddress,
  liquidatorAddress,  // receives remaining assets
  calls,
  '0x'  // lossPolicyData
]);
```

### 2. Internal Execution

1. Calculate payments via `CreditLogic.calcLiquidationPayments`
2. Execute multicall (convert collateral to underlying)
3. Transfer `amountToPool` to PoolV3
4. Remove active quotas via PoolQuotaKeeper

### 3. Pool Distribution

**Profits:**
- Pool mints shares to Treasury

**Losses:**
- Burns Treasury shares
- If Treasury empty: emits `IncurUncoveredLoss`
- Triggers emergency borrowing halt

### 4. Remaining Funds

1. **Borrower's Share**: `minRemainingFunds` (if any)
2. **Liquidator's Share**: Everything else (includes premium)

***

## Fee Distribution

```solidity
function _calcPartialLiquidationPayments(
    uint256 amount,
    address token,
    bool isExpired
) returns (
    uint256 repaidAmount,
    uint256 feeAmount,
    uint256 seizedAmount
)
```

| Fee Type | Description |
|----------|-------------|
| `feeLiquidation` | Standard liquidation fee to DAO |
| `feeLiquidationExpired` | Higher fee for expired accounts |
| `liquidationDiscount` | Discount for healthy liquidations |
| `liquidationDiscountExpired` | Discount for expired liquidations |

Expired accounts have higher fees to incentivize timely liquidation.

***

## Partial Liquidation

### When Allowed

Partial liquidation is useful when:
- Market liquidity is insufficient for full conversion
- "Deleverage" strategy is preferred
- Account can remain healthy with reduced debt

### Constraints

- Account must remain open after liquidation
- Must pass collateral check post-liquidation (HF >= 1)
- Cannot leave "dust" debt below `minDebt`

### Execution

```solidity
function partiallyLiquidateCreditAccount(
    address creditAccount,
    address token,
    uint256 repaidAmount,
    uint256 minSeizedAmount,
    address to,
    PriceUpdate[] calldata priceUpdates
) external returns (uint256 seizedAmount)
```

**Steps:**
1. Update price feeds (if provided)
2. Verify account is liquidatable (HF < 1 or expired)
3. Liquidator provides underlying as collateral
4. Calculate payments (repaid, fee, seized)
5. Handle phantom token withdrawal if applicable
6. Decrease account debt
7. Withdraw fee to treasury
8. Transfer seized collateral to liquidator
9. Full collateral check (HF must be >= 1 after)

### Health Factor Thresholds

**Protocol Level:**
- **Liquidation Trigger**: HF < 1.0
- **Post-Liquidation**: HF >= 1.0 (enforced)

**Bot-Specific** (configurable in `PartialLiquidationBotV3`):
- `minHealthFactor`: HF threshold for intervention
- `maxHealthFactor`: Maximum HF after partial liquidation
- Prevents "over-liquidation"

```typescript
// TypeScript: Partial liquidation
const seizedAmount = await creditFacade.write.partiallyLiquidateCreditAccount([
  creditAccountAddress,
  wbtcAddress,         // token to seize
  parseUnits('1000', 6), // repaid USDC amount
  parseUnits('0.03', 8), // min BTC to receive
  liquidatorAddress,
  []                   // price updates
]);
```

***

## Emergency Liquidations

### Regular vs Emergency

| Type | When | Who |
|------|------|-----|
| **Regular** | Protocol functioning normally | Anyone |
| **Emergency** | Protocol/Facade paused | `EMERGENCY_LIQUIDATOR` role only |

### whenNotPausedOrEmergency Modifier

```solidity
modifier whenNotPausedOrEmergency() {
    require(
        !paused() || _hasRole("EMERGENCY_LIQUIDATOR", msg.sender),
        "Pausable: paused"
    );
    _;
}
```

This ensures liquidations can continue even during pause, preventing bad debt accumulation.

### Treasury Backstop

The `TreasuryLiquidator` contract allows the DAO treasury to provide emergency liquidity:
- Provides underlying funds when external liquidators are absent
- Acts as backstop during extreme market conditions
- Protects protocol from cascading losses

```typescript
// TypeScript: Checking if account can be liquidated
const creditFacade = getContract({
  address: facadeAddress,
  abi: creditFacadeV3Abi,
  client: publicClient,
});

const creditManager = getContract({
  address: cmAddress,
  abi: creditManagerV3Abi,
  client: publicClient,
});

// Get health factor
const debtData = await creditManager.read.calcDebtAndCollateral([
  creditAccount,
  2 // DEBT_COLLATERAL
]);

const hf = debtData.twvUSD * 10000n / debtData.totalDebtUSD;

// Check expiration
const expirationDate = await creditFacade.read.expirationDate();
const isExpired = BigInt(Math.floor(Date.now() / 1000)) > expirationDate;

const isLiquidatable = hf < 10000n || isExpired;
console.log(`Liquidatable: ${isLiquidatable}, HF: ${Number(hf) / 100}%`);
```

<details>

<summary>Sources</summary>

* [contracts/credit/CreditFacadeV3.sol](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/credit/CreditFacadeV3.sol) (lines 277-437)
* [contracts/credit/CreditManagerV3.sol](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/credit/CreditManagerV3.sol)
* [contracts/libraries/CreditLogic.sol](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/libraries/CreditLogic.sol)
* [contracts/emergency/TreasuryLiquidator.sol](https://github.com/Gearbox-protocol/periphery-v3/blob/main/contracts/emergency/TreasuryLiquidator.sol)
* [contracts/bots/PartialLiquidationBotV3.sol](https://github.com/Gearbox-protocol/bots-v3/blob/main/contracts/bots/PartialLiquidationBotV3.sol)

</details>
