# Pool Quota Keeper

In Gearbox V3, "Quotas" are the primary mechanism for managing risk associated with collateral exposure. While a lending pool provides the capital (underlying), the **PoolQuotaKeeper** regulates how much of that capital can be exposed to specific collateral types and at what cost.

## Pool and PoolQuotaKeeper Interaction

The **Pool** (`PoolV3`) and the **PoolQuotaKeeper** (`PoolQuotaKeeperV3`) form a tight loop for financial accounting and revenue distribution.

> For the economic rationale behind quotas and how they affect borrowing strategy, see [Quota Controls](../../new-docs-about/economics-and-risk/quota-controls.md).

**Architecture and Data Flow**

The Pool manages the actual ERC-20 assets, while the QuotaKeeper tracks the borrowing capacity for the collaterals.

* **Additive Interest**: Unlike the base debt which compounds, quota interest is additive (linear). The QuotaKeeper tracks a `cumulativeIndex` for each token that grows based on the rate set by the Gauge.

***

## Quota Limits and Risk Management

Quota limits represent the protocol's "risk appetite" for specific assets. They are enforced globally per pool.

**What are Quota Limits?**

A **Quota Limit** is the maximum aggregate amount of debt backed a specific collateral token that all Credit Accounts combined can hold.

* **Preventing Tail Risk**: Limits ensure that the protocol is never over-exposed to a single asset that might suffer from a liquidity crunch or oracle failure.
* **Capacity Control**: If a token's `totalQuoted` reaches its `limit`, any transaction attempting to increase that quota in a Credit Account will revert with `QuotaIsOutOfBoundsException`.

**Mechanism for Setting Limits**

Limits are managed directly on the `PoolQuotaKeeperV3` contract:

* **Function**: `setTokenLimit(address token, uint96 limit)`
* **Access Control**: Only the `CONFIGURATOR` (typically a Risk Curator or the DAO) can call this.
* **Validation**: In the **Permissionless** framework, the `PoolFactory` ensures that limits cannot be set for tokens that do not have a valid price feed.

***

## Gauge Model: Gauge vs. Tumbler

Every QuotaKeeper relies on an external contract implementing `IRateKeeper` to provide interest rates.

**GaugeV3 (Voting Model)**

Used in the core protocol where GEAR stakers vote to move interest rates between a `minRate` and `maxRate`. This reflects decentralized market sentiment regarding the risk/reward of specific strategies.

**TumblerV3 (Curator Model)**

The **Tumbler** is a simplified, non-voting implementation of the Gauge. It is the standard choice for curators in the Gearbox Permissionless ecosystem.

* **Direct Control**: Curators set exact rates using `setRate(address token, uint16 rate)`.
* **Epoch-Based Updates**: Rates are set in basis points but only take effect when `updateRates()` is called. The Tumbler enforces an `epochLength` to prevent frequent rate manipulation and provide predictability for borrowers.

***

## Data Retrieval and Observability

To monitor the state of quotas and limits, several view functions are provided.

**Global Quota Data**

To see the status of a specific token within a pool, call `PoolQuotaKeeperV3.getTokenQuotaParams(address token)`. This returns:

* `rate`: The current annual interest rate in basis points.
* `totalQuoted`: Total amount of this token currently held as quota across all accounts.
* `limit`: The maximum allowed `totalQuoted`.
* `isActive`: Whether the token is currently quoted in this keeper.

**User-Specific Data**

To see how much quota an individual Credit Account is consuming, call `PoolQuotaKeeperV3.getQuotaAndOutstandingInterest(address creditAccount, address token)`.

* `quoted`: The amount of token quota held by the account.
* `outstandingInterest`: The interest accrued by this quota that hasn't been added to the account's debt yet.

```typescript
// TypeScript: Reading quota data
import { getContract } from 'viem';

const quotaKeeper = getContract({
  address: quotaKeeperAddress,
  abi: poolQuotaKeeperV3Abi,
  client: publicClient,
});

// Get global quota parameters for a token
const tokenParams = await quotaKeeper.read.getTokenQuotaParams([tokenAddress]);
// Returns: { rate, cumulativeIndex, quotaIncreaseFee, totalQuoted, limit, isActive }

// Get account-specific quota and accrued interest
const [quoted, outstandingInterest] = await quotaKeeper.read.getQuotaAndOutstandingInterest([
  creditAccountAddress,
  tokenAddress,
]);

// Check if quota is available (not at limit)
const availableQuota = tokenParams.limit - tokenParams.totalQuoted;
```

<details>

<summary>Sources</summary>

* [contracts/pool/PoolQuotaKeeperV3.sol](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/pool/PoolQuotaKeeperV3.sol)
* [contracts/pool/PoolV3.sol](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/pool/PoolV3.sol)
* [contracts/pool/TumblerV3.sol](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/pool/TumblerV3.sol)
* [contracts/interfaces/IPoolQuotaKeeperV3.sol](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/interfaces/IPoolQuotaKeeperV3.sol)
* [contracts/factories/PoolFactory.sol](https://github.com/Gearbox-protocol/permissionless/blob/master/contracts/factories/PoolFactory.sol)
* [contracts/types/MarketData.sol](https://github.com/Gearbox-protocol/periphery-v3/blob/main/contracts/types/MarketData.sol)

</details>
