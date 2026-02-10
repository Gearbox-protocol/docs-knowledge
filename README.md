# Developer Documentation

Build on Gearbox Protocol. Choose your path based on how you'll integrate.

## Choose Your Path

### [SDK Guide (TypeScript)](sdk-guide/README.md)

**Best for:** Frontend developers, bot builders, analytics dashboards

The SDK provides typed access to Gearbox protocol state and operations. It wraps contract calls, handles encoding, and provides cached market data.

- Read market state via `marketRegister`
- Query credit accounts via services
- Build multicalls with helpers
- No Solidity knowledge required

### [Solidity Guide](solidity-guide/README.md)

**Best for:** Smart contract developers, on-chain integrators, adapter builders

Integrate directly with Gearbox contracts from your Solidity code.

- Discover contracts via AddressProvider
- Call CreditFacade operations
- Build multicalls in Solidity
- Build custom adapters

## Reference

- [Concepts](concepts/) - Architecture explanations (no code)
- [Compressors](reference/compressors.md) - Data aggregation contracts
- [Automated Insurance](reference/automated-insurance.md) - Protocol safety mechanisms
- [Interest Rate Model](reference/interest-rate-model.md) - Utilization curves and rates
- [Quota Keeper](reference/quota-keeper.md) - Collateral exposure limits

## Quick Links

| Need | Go to |
|------|-------|
| Install SDK | [SDK Setup](sdk-guide/setup.md) |
| Find contract addresses | [Credit Accounts](solidity-guide/credit-accounts.md) |
| Understand Credit Suite | [Credit Suite Concepts](concepts/credit-suite.md) |
| Build multicalls | [SDK Multicalls](sdk-guide/multicalls.md) or [Solidity Multicalls](solidity-guide/multicalls.md) |
| Query credit accounts | [SDK Credit Accounts](sdk-guide/credit-accounts.md) |
| Pool deposit/withdraw | [Pool Operations](solidity-guide/pool-operations.md) |
