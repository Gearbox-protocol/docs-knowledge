---
title: Balancer V3 LP Price Feed
---

# Balancer V3 LP Price Feed

The Balancer V3 LP price feed returns the USD price for a single Balancer V3 LP token (BPT). It is designed to safely price BPTs so they can be used as collateral in Gearbox.

## How it works

Balancer V3 pool tokens (BPTs) are not directly ERC-20 transferable in the same way as V2 — they live inside the Vault. To use them as collateral, two steps are required:

1. **Wrap the BPT** using `WrappedBalancerPoolTokenFactory` — this creates a standard ERC-20 wrapper around the Vault-managed BPT.
2. **Deploy an oracle** using `StableLPOracleFactory` — this creates a Chainlink-compatible price feed for the wrapped token.

## Step 1: Deploy Wrapped LP Token

Use the `WrappedBalancerPoolTokenFactory` to create an ERC-20 wrapper for the target Balancer V3 pool token.

```solidity
WrappedBalancerPoolTokenFactory.createWrappedToken(address balancerPoolToken)
```

This deploys a `WrappedBalancerPoolToken` contract that wraps the BPT into a standard ERC-20 token with name "Wrapped {pool name}" and symbol "w{pool symbol}".

## Step 2: Deploy Price Oracle

Use the `StableLPOracleFactory` to deploy a price oracle for the pool. The oracle requires Chainlink price feeds for each underlying token in the pool.

The `StableLPOracle` computes the LP token price by:
- Fetching live balances from the Vault
- Computing the pool invariant
- Calculating the TVL using Chainlink prices for underlying assets
- Dividing by total supply to get per-token price

The oracle implements the `AggregatorV3Interface` (Chainlink-compatible), so it can be plugged directly into Gearbox's price oracle system.

## Contract Addresses

### Ethereum Mainnet

| Contract | Address |
|---|---|
| WrappedBalancerPoolTokenFactory | `0xA3d11a39dEA14d245659816d35456B89FfBfB744` |
| StableLPOracleFactory | `0x83bf399FA3DC49Af8fb5c34031a50c7C93F56129` |

For other chains, see the [Balancer V3 deployment addresses](https://docs.balancer.fi/developer-reference/contracts/deployment-addresses/mainnet.html).

## Source Code

- [StableLPOracle.sol](https://github.com/balancer/balancer-v3-monorepo/blob/main/pkg/oracles/contracts/StableLPOracle.sol)
- [StableLPOracleFactory.sol](https://etherscan.io/address/0x83bf399FA3DC49Af8fb5c34031a50c7C93F56129#code)
- [WrappedBalancerPoolTokenFactory.sol](https://etherscan.io/address/0xA3d11a39dEA14d245659816d35456B89FfBfB744#code)
