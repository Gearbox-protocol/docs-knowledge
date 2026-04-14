# Use Cases

Practical guides for common Solidity integration patterns with Gearbox.

## Available Guides

| Use Case             | Description                                                 | Guide                                           |
| -------------------- | ----------------------------------------------------------- | ----------------------------------------------- |
| Adapter Development  | Build adapters to integrate new DeFi protocols with Gearbox | [Adapter Development](adapter-development.md)   |
| Protocol Integration | Build protocols that compose with Gearbox Credit Accounts   | [Protocol Integration](protocol-integration.md) |
| Core Extension       | Extend Gearbox core contracts (advanced)                    | [Core Extension](core-extension.md)             |
| Liquidation Bots     | Build on-chain liquidation contracts with keeper automation | [Liquidation Bots](liquidation-bots.md)         |

## Choosing Your Path

### Adapter Development

Choose this path if you want to:

* Add a new DeFi protocol (DEX, lending, yield) to Gearbox
* Enable Credit Accounts to interact with your protocol
* Become part of the Gearbox ecosystem

Adapters are the bridge between Credit Accounts and external protocols. They enforce security constraints while translating calls to protocol-specific interfaces.

### Protocol Integration

Choose this path if you want to:

* Build a smart contract that uses Gearbox Credit Accounts
* Create automated strategies on top of Gearbox
* Compose Gearbox with your own protocol logic

Protocol integrations call Gearbox from the outside, building multicalls and executing operations programmatically.

### Core Extension

Choose this path if you want to:

* Extend Gearbox core functionality (CreditManager, Pool, etc.)
* Build custom contract logic that inherits from core contracts
* Implement advanced customizations requiring deep protocol knowledge

This is an advanced path requiring thorough understanding of Gearbox internals, security considerations, and upgrade patterns.

## Prerequisites

All paths require:

* Solidity 0.8.x experience
* Understanding of the [Multicall System](../../concepts/multicall-system.md)
* Familiarity with [Credit Accounts](../credit-accounts.md)

## Related

* [Multicalls](../multicalls/) - Core encoding patterns
* [Multicall Operations](../multicalls/multicalls/) - Individual operation guides
* [Credit Accounts](../credit-accounts.md) - Contract discovery and core interfaces
