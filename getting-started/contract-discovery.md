# Contract Discovery

Find any Gearbox contract address programmatically. Never hardcode addresses.

## AddressProviderV3

The only address you need to hardcode. All other contracts are discoverable from here.

| Network | AddressProvider |
|---------|-----------------|
| Mainnet | `0x...` (see [Deployment Addresses](https://github.com/Gearbox-protocol/deployments)) |
| Arbitrum | `0x...` (see [Deployment Addresses](https://github.com/Gearbox-protocol/deployments)) |

### Solidity

```solidity
import {IAddressProviderV3} from "@gearbox-protocol/core-v3/contracts/interfaces/IAddressProviderV3.sol";

IAddressProviderV3 ap = IAddressProviderV3(ADDRESS_PROVIDER);

// Get ContractsRegister (version 3.00)
address contractsRegister = ap.getAddressOrRevert("CONTRACTS_REGISTER", 3_00);

// Get Price Oracle (version 3.10)
address priceOracle = ap.getAddressOrRevert("PRICE_ORACLE", 3_10);

// Get WETH (no version control)
address weth = ap.getAddressOrRevert("WETH_TOKEN", 0);
```

### TypeScript (viem)

```typescript
import { getContract } from 'viem';
import { addressProviderAbi } from '@gearbox-protocol/sdk';

const addressProvider = getContract({
  address: ADDRESS_PROVIDER,
  abi: addressProviderAbi,
  client: publicClient,
});

// Get ContractsRegister
const contractsRegister = await addressProvider.read.getAddressOrRevert([
  'CONTRACTS_REGISTER',
  300n,
]);

// Get Price Oracle
const priceOracle = await addressProvider.read.getAddressOrRevert([
  'PRICE_ORACLE',
  310n,
]);

// Get WETH (no version control)
const weth = await addressProvider.read.getAddressOrRevert([
  'WETH_TOKEN',
  0n,
]);
```

## Standard Keys

| Key | Purpose |
|-----|---------|
| `CONTRACTS_REGISTER` | Registry of pools and credit managers |
| `PRICE_ORACLE` | Main price oracle router |
| `PRICE_FEED_STORE` | On-demand price feed storage |
| `ACCOUNT_FACTORY` | Credit account factory |
| `BOT_LIST` | Bot permissions registry |
| `TREASURY` | Protocol treasury |
| `WETH_TOKEN` | Wrapped ETH address |
| `ACL` | Access control list |

## Version Control

Pass version as the second parameter to `getAddressOrRevert()`:

- `3_00` (or `300n`) - V3.0 contracts
- `3_10` (or `310n`) - V3.1 contracts
- `0` - No version control (for static addresses like WETH)

```solidity
uint256 constant NO_VERSION_CONTROL = 0;
```

---

## ContractsRegister

Enumerates all pools and credit managers in the system.

### Get All Pools

```solidity
import {IContractsRegister} from "@gearbox-protocol/core-v3/contracts/interfaces/IContractsRegister.sol";

IContractsRegister cr = IContractsRegister(contractsRegister);

address[] memory pools = cr.getPools();
```

```typescript
const pools = await contractsRegister.read.getPools();
```

### Get All Credit Managers

```solidity
address[] memory creditManagers = cr.getCreditManagers();
```

```typescript
const creditManagers = await contractsRegister.read.getCreditManagers();
```

### Filter by Version

Check contract version to filter V3+ contracts:

```solidity
import {IVersion} from "@gearbox-protocol/core-v3/contracts/interfaces/base/IVersion.sol";

for (uint256 i = 0; i < pools.length; i++) {
    uint256 version = IVersion(pools[i]).version();
    if (version >= 3_00) {
        // V3.0+ pool
    }
}
```

```typescript
for (const pool of pools) {
  const version = await publicClient.readContract({
    address: pool,
    abi: [{ name: 'version', type: 'function', inputs: [], outputs: [{ type: 'uint256' }] }],
    functionName: 'version',
  });

  if (version >= 300n) {
    // V3.0+ pool
  }
}
```

---

## From Pool to Credit Suite

Navigate the relationship tree from a pool to its credit infrastructure.

```
Pool
 └── poolQuotaKeeper()
      └── creditManagers via ContractsRegister filter

CreditManager
 └── creditFacade()
 └── priceOracle()
 └── pool()
```

### Get Pool's Quota Keeper

```solidity
import {IPoolV3} from "@gearbox-protocol/core-v3/contracts/interfaces/IPoolV3.sol";

IPoolV3 pool = IPoolV3(poolAddress);
address quotaKeeper = pool.poolQuotaKeeper();
```

### Get Credit Manager's Facade

```solidity
import {ICreditManagerV3} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditManagerV3.sol";

ICreditManagerV3 cm = ICreditManagerV3(creditManagerAddress);
address facade = cm.creditFacade();
address oracle = cm.priceOracle();
address linkedPool = cm.pool();
```

### TypeScript

```typescript
// Get quota keeper from pool
const quotaKeeper = await pool.read.poolQuotaKeeper();

// Get facade from credit manager
const facade = await creditManager.read.creditFacade();
const oracle = await creditManager.read.priceOracle();
const linkedPool = await creditManager.read.pool();
```

---

## Complete Discovery Example

Find all USDC lending pools and their credit managers:

```solidity
function findUSDCMarkets(address addressProvider, address usdc) external view returns (address[] memory) {
    IAddressProviderV3 ap = IAddressProviderV3(addressProvider);
    address cr = ap.getAddressOrRevert("CONTRACTS_REGISTER", 3_00);

    address[] memory allPools = IContractsRegister(cr).getPools();

    uint256 count;
    for (uint256 i = 0; i < allPools.length; i++) {
        if (IPoolV3(allPools[i]).underlyingToken() == usdc) {
            count++;
        }
    }

    address[] memory usdcPools = new address[](count);
    uint256 j;
    for (uint256 i = 0; i < allPools.length; i++) {
        if (IPoolV3(allPools[i]).underlyingToken() == usdc) {
            usdcPools[j++] = allPools[i];
        }
    }

    return usdcPools;
}
```

---

## Next Steps

- [Market Data](market-data.md) - Fetch complete market state with MarketCompressor
- [Credit Suite Overview](../core/credit-suite.md) - Credit Manager and Facade architecture

## Conceptual Background

For the architectural design behind contract discovery, see:

- [Core Architecture](../../new-docs-about/core-architecture/adapters-integrations.md)
