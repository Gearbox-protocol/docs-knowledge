# Solidity Guide

Integrate directly with Gearbox contracts from your Solidity code. This guide covers on-chain integration patterns for smart contract developers.

## Prerequisites

- Solidity 0.8.x experience
- Familiarity with interface-based contract interaction
- Understanding of ERC-20 and common DeFi patterns

## What You'll Learn

| Topic | Description |
|-------|-------------|
| Contract Discovery | Find any protocol address via AddressProvider |
| Credit Operations | Interact with CreditFacade and CreditManager |
| Multicall Encoding | Build and execute multicalls in Solidity |
| Pool Operations | Deposit, withdraw, and read pool state |

## Guide Structure

1. **[Contract Discovery](discovery.md)** - AddressProvider, ContractsRegister, navigation patterns
2. **[Credit Operations](credit-operations.md)** - ICreditFacadeV3, ICreditManagerV3 interfaces
3. **[Multicalls](multicalls.md)** - MultiCall struct encoding, adapter calls
4. **[Pool Operations](pool-operations.md)** - IPoolV3 deposit/withdraw, ERC-4626 functions

## Key Interfaces

```solidity
// Core interfaces you'll use
import {IAddressProviderV3} from "@gearbox-protocol/core-v3/contracts/interfaces/IAddressProviderV3.sol";
import {ICreditFacadeV3} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditFacadeV3.sol";
import {ICreditManagerV3} from "@gearbox-protocol/core-v3/contracts/interfaces/ICreditManagerV3.sol";
import {IPoolV3} from "@gearbox-protocol/core-v3/contracts/interfaces/IPoolV3.sol";
```

## When to Use Solidity Integration

| Use Case | Recommended |
|----------|-------------|
| On-chain protocol integration | Yes |
| Building adapters | Yes |
| Composable strategies | Yes |
| Backend services | No (use SDK Guide) |
| Frontend applications | No (use SDK Guide) |

For TypeScript/JavaScript applications, see the [SDK Guide](../sdk-guide/README.md).

## Architecture Understanding

For conceptual background on how Gearbox works:

- [Credit Suite Architecture](../concepts/credit-suite.md) - How Credit Managers, Facades, and Configurators work together
- [Pool Architecture](../concepts/pools.md) - Lending pools and ERC-4626 compliance
- [Multicall System](../concepts/multicall-system.md) - How multicalls execute and validate
