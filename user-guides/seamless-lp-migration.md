# Seamless LP migration

### Why migrate (what you gain as an LP)

**In short:** better incentives and better market coverage.

{% hint style="info" %}
As Gearbox transitions to the permissionless curation model, rewards and activity shift to the new pools. Old pools will stop receiving rewards and become non-competitive over time. New pools are where curators focus liquidity and opportunities.
{% endhint %}

New Curator pools combine two reward streams:

* baseline, time-weighted TVL incentives to bootstrap passive liquidity
* performance-based rewards proportional to the Curator’s revenue share.

In practice, the aggregate rewards allocated to the permissionless model are about 3x the legacy LM run-rate, with dilution tied more closely to real usage and protocol revenue (supporting buybacks). As a result, effective yield in new pools is expected to be higher than in legacy pools.

***

### Purpose

This LP migration contract is designed to allow users migrate liquidity without monitoring the pools for available liquidity:

* Designed for the case where immediate migration is not possible due to liquidity constraints.
* Users can pre-sign their intention to migrate by granting allowance to the migration contract.
* The migration will be executed by the instance owner multisig as soon as liquidity becomes available.

In other words, this contract is a safe automation tool:

* You lock in your intent to move from the old pool to the new one.
* You don’t have to monitor liquidity or time the transaction yourself.
* The migration will happen at the first opportunity.

***

#### How it Works

There are only two functions in the migration contract:

1. User function (allowance setup)
   * You give the migration contract allowance for your LP tokens in the old pool.
   *   This does not move funds immediately — it only means:

       > “Whenever possible, please take my LP tokens from the old pool and put them into the new pool.”
   * After signing, you are done.
2. Instance owner function (execute migration)
   * Can only be called by the instance owner multisig (chain-specific). However, instance owner can't do anything except for migrating liquidity between the pools specified by user.
   * Once liquidity becomes available, they trigger the migration:
     * LP tokens are redeemed from the old pool.
     * Assets are deposited into the new pool on behalf of the user.
   * Both _old pool_ and _new pool_ are fixed parameters of the contract and cannot be changed.

***

#### Safety of Allowance

* **Immutable destination:** your funds can only move old pool → new pool.
* **No arbitrary spending:** allowance is strictly limited to the old pool LP tokens.
* **Controlled execution:** the migration logic is minimalistic and fixed in contract. Even if instance owner multisig goes malicious, its actions can't result in user losing money.

***

#### Migration Lifecycle

1. User grants allowance
   * Approves their LP tokens to be used by migration contract.
2. Monitoring phase
   * Liquidity in old pools may be fully utilized (100%).
   * Gearbox contributors monitor until withdrawals are possible.
3. Execution phase
   * Instance owner calls the migration function at the first chance.
   * Funds are moved automatically on behalf of the user who granted the allowance.
4. Completion
   * Users now hold LP tokens in the new pool.
   * Yield continues seamlessly.

***

### Why now (governance & versions)

Gearbox is moving from V3.0 to V3.1 to solidify the permissionless governance direction. Under permissionless curation, DAO-approved curators can configure markets and parameters, and the protocol can scale across networks without slow, centralized bottlenecks.

**This migration is happening because:**

* Maintaining two versions is technically **complex and fragments liquidity.**\
  Supporting both legacy pools and new permissionless pools in parallel would complicate operations and potentially reduce yields for everyone. Consolidating liquidity in the new system is safer and more efficient.
* Legacy pools had the **DAO as the sole curator - this is changing.**\
  In the permissionless model, curators manage markets directly within clear, on-chain constraints. So legacy pools either need to be turned off or migrated to preserve TVL in the ecosystem.
* It’s **better for LPs.**\
  Rewards and curator attention move to the new pools. Old pools will become non-competitive over time. Specialized curators are expected to maintain attractive rates more consistently than DAO-only governance, because they operate faster and stay deeper in the market.

***

#### Batching and timelines

To reduce multisig overhead and make the best use of liquidity windows, we process migrations in batches.

* **Positions up to $1,000,000.**\
  Migrated in full within the nearest suitable batch.
* **Positions above $1,000,000.**\
  Moved in several chunks. This is normal and helps keep utilization healthy while your position transitions.
* **Target batch size.**\
  We aim to group requests into roughly $1,000,000 batches to execute efficiently when liquidity allows.
* **FIFO queueing.**\
  LP requests are processed in chronological order. This keeps the process transparent and predictable.
* **Timing.**\
  Your migration may wait while a batch fills. The maximum wait time will not exceed 14 days.

#### FAQ

* **Can the migration contract move my funds anywhere else?**\
  No. It can only move LP from the specific old pool to the specific new pool you selected.
* **Why would APY be higher in the new pools?**\
  New pools stack baseline TVL incentives with performance-based rewards linked to real fee generation. The overall incentive budget for the permissionless phase is roughly 3x legacy LM, with dilution aligned to revenue (supports buybacks), so effective yields are expected to be superior versus legacy pools.
* **What if utilization in the old pool is 100% for a while?**\
  We keep your request in the FIFO queue and execute at the first safe window. Batching helps reduce delays.
* **Do I keep earning yield?**\
  Yes. After migration you hold LP in the new pool and continue earning according to its parameters and incentives.
