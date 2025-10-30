:

1.  [Feature explainers](/gearbox-permissionless-doc/feature-explainers)

# Seamless LP migration
:
##

**In short:** better incentives and better market coverage.

As Gearbox transitions to the permissionless curation model, rewards and activity shift to the new pools. Old pools will stop receiving rewards and become non-competitive over time. New pools are where curators focus liquidity and opportunities.
New Curator pools combine two reward streams:

-
:

-
:

In practice, the aggregate rewards allocated to the permissionless model are about 3x the legacy LM run-rate, with dilution tied more closely to real usage and protocol revenue (supporting buybacks). As a result, effective yield in new pools is expected to be higher than in legacy pools.

------------------------------------------------------------------------

##

This LP migration contract is designed to allow users migrate liquidity without monitoring the pools for available liquidity:

-
:

-
:

-
:

In other words, this contract is a safe automation tool:

-
:

-
:

-
:

------------------------------------------------------------------------

###

There are only two functions in the migration contract:

1.
:

:

You give the migration contract allowance for your LP tokens in the old pool.
:

This does not move funds immediately --- it only means:

> "Whenever possible, please take my LP tokens from the old pool and put them into the new pool."
:

After signing, you are done.

2.
:

:

Can only be called by the instance owner multisig (chain-specific). However, instance owner can\'t do anything except for migrating liquidity between the pools specified by user.
:

Once liquidity becomes available, they trigger the migration:

-
:

-
:

:

Both *old pool* and *new pool* are fixed parameters of the contract and cannot be changed.

------------------------------------------------------------------------

###

-
:

-
:

-
:

------------------------------------------------------------------------

###

1.
:

:

Approves their LP tokens to be used by migration contract.

2.
:

:

Liquidity in old pools may be fully utilized (100%).
:

Gearbox contributors monitor until withdrawals are possible.

3.
:

:

Instance owner calls the migration function at the first chance.
:

Funds are moved automatically on behalf of the user who granted the allowance.

4.
:

:

Users now hold LP tokens in the new pool.
:

Yield continues seamlessly.

------------------------------------------------------------------------

##

Gearbox is moving from V3.0 to V3.1 to solidify the permissionless governance direction. Under permissionless curation, DAO-approved curators can configure markets and parameters, and the protocol can scale across networks without slow, centralized bottlenecks.

**This migration is happening because:**

-
:

-
:

-
:

------------------------------------------------------------------------

###

To reduce multisig overhead and make the best use of liquidity windows, we process migrations in batches.

-
:

-
:

-
:

-
:

-
:

###

-
:

-
:

-
:

-
:

[[[Previous][DVstETH leveraged staking]]](/gearbox-permissionless-doc/feature-explainers/dvsteth-leveraged-staking)[[[Next][Credit Account migration]]](/gearbox-permissionless-doc/feature-explainers/credit-account-migration)

Last updated 25 days ago