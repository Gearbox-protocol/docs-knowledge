# Credit Configurator

The **CreditConfiguratorV3** is the administrative gateway for the Credit Suite. It validates parameter changes and propagates them to the Credit Manager and Credit Facade. Importantly, it does not store configuration state itself - it acts as a validation layer.

## Architecture

```
User/DAO -> CreditConfiguratorV3 (validation) -> CreditManagerV3/CreditFacadeV3 (state)
```

The Configurator ensures all changes are valid before forwarding them to the appropriate contract. This separation allows for:
- Centralized validation logic
- Consistent access control
- Audit trail through events

***

## Token & Risk Management

### Adding Collateral Tokens

```solidity
function addCollateralToken(address token, uint16 liquidationThreshold);
```

**Validation:**
- Token must be valid ERC-20
- Must have price feed in PriceOracle
- Must be quoted in PoolQuotaKeeper
- LT cannot exceed underlying's LT

**For Phantom Tokens:**
- The deposited (underlying) token must already exist as collateral
- Phantom token represents staked/wrapped position

### Adjusting Liquidation Thresholds

```solidity
// Immediate change
function setLiquidationThreshold(address token, uint16 liquidationThreshold);

// Gradual change (ramping)
function rampLiquidationThreshold(
    address token,
    uint16 ltFinal,
    uint40 rampStart,
    uint24 rampDuration
);
```

**Ramping** allows gradual LT changes over time, preventing sudden liquidation cascades when risk parameters are adjusted.

### Forbidding/Allowing Tokens

| Function | Access | Use Case |
|----------|--------|----------|
| `forbidToken(address token)` | Pausable Admins | Emergency: mark token as risky |
| `allowToken(address token)` | Configurator | Restore normal token status |

Forbidden tokens still count toward collateral (with safe pricing) but have restrictions on quota increases and balance changes.

```typescript
// TypeScript: Reading token configuration
const creditManager = getContract({
  address: cmAddress,
  abi: creditManagerV3Abi,
  client: publicClient,
});

// Get collateral token data
const tokenMask = await creditManager.read.getTokenMaskOrRevert([tokenAddress]);
const tokenData = await creditManager.read.collateralTokenByMask([tokenMask]);
// Returns: { token, ltInitial, ltFinal, timestampRampStart, rampDuration }

// Check if token is forbidden
const forbiddenMask = await creditManager.read.forbiddenTokenMask();
const isForbidden = (tokenMask & forbiddenMask) !== 0n;
```

***

## Fee Management

### Configurable Fees

```solidity
function setFees(
    uint16 feeLiquidation,
    uint16 liquidationPremium,
    uint16 feeLiquidationExpired,
    uint16 liquidationPremiumExpired
);
```

| Parameter | Description |
|-----------|-------------|
| `feeLiquidation` | DAO fee on standard liquidations |
| `liquidationPremium` | Reward for liquidators |
| `feeLiquidationExpired` | Higher DAO fee for expired accounts |
| `liquidationPremiumExpired` | Higher reward for expired liquidations |

**Constraints:**
- `feeLiquidation <= liquidationPremium`
- `feeLiquidationExpired <= feeLiquidation`
- `liquidationPremium + feeLiquidation < 100%`
- Fee sum must remain constant (prevents sudden changes)

The relationship ensures liquidators are always incentivized and the protocol takes a smaller cut than the liquidator reward.

***

## Borrowing Limits

### Debt Bounds

```solidity
function setDebtLimits(uint128 newMinDebt, uint128 newMaxDebt);
```

**Validation:**
- `minDebt <= maxDebt`
- `maxDebt * maxEnabledTokens <= minDebt * 100` (safety ratio)
- USD value of minDebt must be non-zero

The safety ratio ensures accounts aren't opened with tiny debt that would be uneconomical to liquidate.

### Per-Block Multiplier

```solidity
function setMaxDebtPerBlockMultiplier(uint8 multiplier);
function forbidBorrowing();  // Sets multiplier to 0
```

**`forbidBorrowing()`** is an emergency action available to Pausable Admins. It immediately halts all new borrowing without requiring a DAO vote.

***

## Adapter Management

### Allowing Adapters

```solidity
function allowAdapter(address adapter);
function forbidAdapter(address adapter);
```

**Validation:**
- Adapter must implement `creditManager()` returning this Credit Manager
- Adapter must implement `targetContract()` returning the DeFi protocol
- Cannot target the Facade or Manager itself

**Registration:**
- Creates bidirectional mapping: `adapter <-> targetContract`
- Credit Account can only call whitelisted adapters
- Each target protocol has exactly one adapter

```typescript
// TypeScript: Checking adapter status
const creditManager = getContract({
  address: cmAddress,
  abi: creditManagerV3Abi,
  client: publicClient,
});

// Get adapter for a target protocol
const adapterAddress = await creditManager.read.contractToAdapter([uniswapRouterAddress]);

if (adapterAddress === '0x0000000000000000000000000000000000000000') {
  console.log('No adapter registered for this protocol');
} else {
  console.log(`Adapter: ${adapterAddress}`);
}

// Get all adapters
const adaptersData = await creditManager.read.adapters();
```

***

## System Upgrades

### Oracle Updates

```solidity
function setPriceOracle(address newPriceOracle);
```

Allows switching to a new price oracle implementation. The new oracle must support all currently configured collateral tokens.

### Facade Migration

```solidity
function setCreditFacade(address newCreditFacade, bool migrateParams);
```

When `migrateParams` is true, debt limits and other Facade parameters are copied to the new contract. This enables upgrading the user-facing interface while preserving configuration.

### Configurator Upgrade

```solidity
function upgradeCreditConfigurator(address newCreditConfigurator);
```

Transfers configurator role to a new contract. Used when the validation logic itself needs updating.

***

## Access Control Model

### Role Hierarchy

| Role | Capabilities |
|------|-------------|
| **Configurator** | All structural changes: tokens, fees, adapters, debt limits, upgrades |
| **Pausable Admin** | Emergency actions: `forbidToken`, `forbidBorrowing` (no DAO vote required) |

### Cross-Contract Verification

The Credit Manager and Facade verify that configuration calls come from the registered Configurator:

```solidity
modifier creditConfiguratorOnly() {
    require(msg.sender == creditConfigurator);
    _;
}
```

This prevents unauthorized parameter changes even if an attacker gains access to admin keys for other contracts.

```typescript
// TypeScript: Reading configurator address
const creditManager = getContract({
  address: cmAddress,
  abi: creditManagerV3Abi,
  client: publicClient,
});

const configuratorAddress = await creditManager.read.creditConfigurator();
console.log(`Configurator: ${configuratorAddress}`);

// Check access control roles (from ACL contract)
const acl = getContract({
  address: aclAddress,
  abi: aclAbi,
  client: publicClient,
});

const isPausableAdmin = await acl.read.isPausableAdmin([someAddress]);
const isConfigurator = await acl.read.isConfigurator([someAddress]);
```

<details>

<summary>Sources</summary>

* [contracts/credit/CreditConfiguratorV3.sol](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/credit/CreditConfiguratorV3.sol)
* [contracts/interfaces/ICreditConfiguratorV3.sol](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/interfaces/ICreditConfiguratorV3.sol)
* [contracts/core/ACL.sol](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/core/ACL.sol)

</details>
