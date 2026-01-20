# Credit Accounts

Query and manage credit accounts using SDK services.

> For Solidity credit operations, see [Credit Operations](../solidity-guide/credit-operations.md).

## Creating a Service

Use `createCreditAccountService` for credit account operations:

```typescript
import { GearboxSDK, createCreditAccountService } from '@gearbox-protocol/sdk';

const sdk = await GearboxSDK.attach({ client, marketConfigurators: [] });

// Create service (310 = V3.1)
const service = createCreditAccountService(sdk, 310);
```

## Querying Credit Accounts

### Get All Accounts for a Credit Manager

```typescript
const accounts = await service.getCreditAccounts(
  { creditManager: cmAddress },
  sdk.currentBlock
);

for (const account of accounts) {
  console.log(`Account: ${account.addr}`);
  console.log(`  Owner: ${account.owner}`);
  console.log(`  Debt: ${account.debt}`);
  console.log(`  Health Factor: ${account.healthFactor}`);
}
```

### Filter by Owner

```typescript
const myAccounts = await service.getCreditAccounts(
  {
    creditManager: cmAddress,
    owner: myAddress,
  },
  sdk.currentBlock
);
```

### Account Data Structure

Each credit account includes:

| Field | Type | Description |
|-------|------|-------------|
| `addr` | `address` | Credit Account contract address |
| `owner` | `address` | Account owner |
| `creditManager` | `address` | Parent Credit Manager |
| `debt` | `uint256` | Total debt (principal + interest) |
| `healthFactor` | `uint256` | Current HF (10000 = 1.0) |
| `tokens` | `TokenInfo[]` | Token balances and values |
| `isLiquidatable` | `boolean` | Whether account can be liquidated |

## Reading Account State

### Health Factor

```typescript
const account = accounts[0];

// Health factor is scaled by 10000 (10000 = 1.0)
const hf = Number(account.healthFactor) / 10000;
console.log(`Health Factor: ${hf.toFixed(4)}`);

if (account.isLiquidatable) {
  console.log('Account is liquidatable!');
}
```

### Token Balances

```typescript
for (const token of account.tokens) {
  console.log(`${token.symbol}:`);
  console.log(`  Balance: ${token.balance}`);
  console.log(`  Value (underlying): ${token.balanceInUnderlying}`);
  console.log(`  LT: ${token.lt / 100}%`);
}
```

### Debt Breakdown

```typescript
console.log(`Total Debt: ${account.debt}`);
console.log(`Principal: ${account.borrowedAmount}`);
console.log(`Accrued Interest: ${account.cumulativeQuotaInterest}`);
console.log(`Quota Fees: ${account.quotaFees}`);
```

## Market Discovery

Find the market for a credit manager:

```typescript
const market = sdk.marketRegister.findByCreditManager(cmAddress);
const creditFacade = market.creditFacade;

console.log(`Credit Facade: ${creditFacade.address}`);
console.log(`Pool: ${market.pool.address}`);
```

## Opening a Credit Account

```typescript
// Build multicall with SDK helpers
const calls = [
  service.prepareAddCollateral(usdcAddress, 10000n * 10n ** 6n),
  service.prepareIncreaseDebt(40000n * 10n ** 6n),
];

// Get credit facade
const market = sdk.marketRegister.findByCreditManager(cmAddress);

// Open account
const hash = await market.creditFacade.write.openCreditAccount([
  ownerAddress,
  calls,
  0n, // referralCode
]);
```

## Closing a Credit Account

```typescript
// Build close multicall - typically repay and withdraw
const closeCalls = [
  service.prepareDecreaseDebt(account.debt), // Repay all debt
  // Withdraw remaining collateral handled automatically
];

const hash = await market.creditFacade.write.closeCreditAccount([
  account.addr,
  closeCalls,
]);
```

## Complete Example

```typescript
import { GearboxSDK, createCreditAccountService } from '@gearbox-protocol/sdk';
import { createPublicClient, http } from 'viem';
import { mainnet } from 'viem/chains';

async function queryAccounts(cmAddress: `0x${string}`) {
  const client = createPublicClient({
    chain: mainnet,
    transport: http(),
  });

  const sdk = await GearboxSDK.attach({
    client,
    marketConfigurators: [],
  });

  const service = createCreditAccountService(sdk, 310);

  // Get all accounts
  const accounts = await service.getCreditAccounts(
    { creditManager: cmAddress },
    sdk.currentBlock
  );

  console.log(`Found ${accounts.length} credit accounts\n`);

  for (const account of accounts) {
    const hf = Number(account.healthFactor) / 10000;

    console.log(`Account: ${account.addr}`);
    console.log(`  Owner: ${account.owner}`);
    console.log(`  Debt: ${account.debt}`);
    console.log(`  Health Factor: ${hf.toFixed(4)}`);
    console.log(`  Liquidatable: ${account.isLiquidatable}`);

    // Token breakdown
    console.log(`  Tokens:`);
    for (const token of account.tokens) {
      if (token.balance > 0n) {
        console.log(`    ${token.symbol}: ${token.balance}`);
      }
    }

    console.log('');
  }
}

queryAccounts('0x...').catch(console.error);
```

## Next Steps

- [Multicalls](multicalls.md) - Build complex operations

For architectural background, see [Credit Suite Architecture](../concepts/credit-suite.md).
