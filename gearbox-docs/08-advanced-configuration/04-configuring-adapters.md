:

1.  [Advanced Configuration](/gearbox-permissionless-doc/advanced-configuration)

# Configuring Adapters
:
##

The Credit Account design enables active interaction with the DeFi ecosystem while borrowing --- such as swapping tokens, depositing into vaults, claiming rewards, and more. However, allowing arbitrary operations poses security risks.

> Adapters --- modular contracts that enable secure, controlled interactions with external protocols.

##

Having adapters properly configured in the market is essential for allowing collateral swaps, 1-click leverage and other UX features of Gearbox protocol.

Existing offchain infra (Front End, Liquidator) rely on router for finding paths from/to available collaterals. Router is not part of Gearbox protocol, therefore it's not present in Bytecode repository. Router is used by Gearbox SDK to provide swap paths and it doesn't interact with core contracts directly.
##

:

***Uniswap, Sushiswap, Oku Trade*** [V2](https://docs.gearbox.fi/gearbox-permissionless-doc/step-by-step-guides/configuring-adapters#uniswap-sushiswap-v2), [V3](https://docs.gearbox.fi/gearbox-permissionless-doc/step-by-step-guides/configuring-adapters#uniswap-sushiswap-pancakeswap-iguanadex-oku-trade-v3)
:

Swaps
:
:

:

***Pancakeswap, IguanaDEX*** [V3](https://docs.gearbox.fi/gearbox-permissionless-doc/step-by-step-guides/configuring-adapters#uniswap-sushiswap-pancakeswap-iguanadex-oku-trade-v3), [StableSwap](https://docs.gearbox.fi/gearbox-permissionless-doc/step-by-step-guides/configuring-adapters#pancakeswap-iguanadex-stableswap)
:

Swaps, Stableswap LP deposits
:
:

:

***Balancer*** [V2](https://docs.gearbox.fi/gearbox-permissionless-doc/step-by-step-guides/configuring-adapters#balancer-v2), [V3](https://docs.gearbox.fi/gearbox-permissionless-doc/step-by-step-guides/configuring-adapters#balancer-v3)
:

Swaps, V2 LP deposits
:
:

:

***Curve*** [Stableswap, CryptoSwap, Stable NG](https://docs.gearbox.fi/gearbox-permissionless-doc/step-by-step-guides/configuring-adapters#curve-stableswap-cryptoswap-and-stableng)
:

Swaps, LP deposits
:
:

:

[***Pendle***](https://docs.gearbox.fi/gearbox-permissionless-doc/step-by-step-guides/configuring-adapters#curve-stableswap-cryptoswap-and-stableng)
:

PT swaps
:
:

:

[***Mellow***](https://docs.gearbox.fi/gearbox-permissionless-doc/step-by-step-guides/configuring-adapters#mellow-erc4626) ERC4626 vaults, DVstETH
:

Instant deposits, Delayed withdrawals
:
:

:

***Velodrome, Aerodrome*** V3, Stableswap
:

Swaps
:
:

:

***Camelot, Thena*** *(Algebra AMM dexes)* ** V3
:

Swaps
:
:

:

***Napier***
:

PT Swaps, LP deposits
:
:

:

***Convex***
:

Staking LP, claiming rewards
:
:

:

[***Fluid DEX***](https://docs.gearbox.fi/gearbox-permissionless-doc/step-by-step-guides/configuring-adapters#fluid-dex)
:

Swaps
:
:

:

***Camelot, Thena, Quickswap*** (Algebra AMM) V3
:

Swaps
:
:

:

***Trader Joe***
:

Swaps
:
:

:

***Infrared***
:

Staking LP, claiming rewards
:
:

:

***Sky***
:

DAI - USDS conversion, Staking USDS for SKY
:
:

:

***Lido***
:

stETH - wstETH conversion
:
:

:

[***ERC4626***](https://docs.gearbox.fi/gearbox-permissionless-doc/step-by-step-guides/configuring-adapters#erc4626)
:

Instant deposits and withdrawals (whenever possible)
:
:

:

[***Kodiak Island***](https://docs.gearbox.fi/gearbox-permissionless-doc/step-by-step-guides/configuring-adapters#erc4626)
:

Deposit into Island, Swaps in pool
:
:

All the source code and audit reports of the contracts can be found in [Bytecode Repository](https://permissionless.gearbox.foundation/bytecode). Use search, click on the target contract and then **View Source** or **View Report**. All the Adapters can be found by searching for the ADAPTER domain in Bytecode Repository.

[setup example (BNB chain: USD1 pool, USDX collateral)](https://www.notion.so/Adapter-setup-example-BNB-chain-USD1-pool-USDX-collateral-208145c16224807fa1a0d318c01bc1ae?pvs=21)

[setup example (Ethereum chain: tBTC pool, uptBTC collateral)](https://www.notion.so/Adapter-setup-example-Ethereum-chain-tBTC-pool-uptBTC-collateral-20e145c1622480c886d8d43dc5e9f5bb?pvs=21)

[setup example (Ethereum chain: USDC pool, frxUSD/USDf collateral)](https://gearboxprotocol.notion.site/Adapter-setup-example-Ethereum-chain-USDC-pool-frxUSD-USDf-collateral-24c145c16224809d80d2d171e1128317?source=copy_link)

**Uniswap, Sushiswap V2**[](#uniswap-sushiswap-v2)

##

For the router on the chain to support swaps, Fluid worker should be configured.

It requires passing the following addresses:

-
:

-
:

**Add UniswapV2 adapter (requires providing router address):**

:

-
:

-
:

Before allowing pools in adapter, please ensure that tokens from a pair are added as ***Assets to Market*** and as ***Collaterals to Credit Manager***. *e.g. to add WETH/USDC pool both WETH and USDC must be added before.*
-
:

:

:

-
:

:

:
:

Sushi V2

-
:

Configuration requires specifying tokens from a pair

:

**Uniswap, Sushiswap, Pancakeswap, IguanaDEX, Oku trade V3**[](#uniswap-sushiswap-pancakeswap-iguanadex-oku-trade-v3)

[](#router-configuration-1)

Router configuration
:

SwapRouter
:

QuoterV2
:

:
:

Uni V3 deployment addresses: [https://docs.uniswap.org/contracts/v3/reference/deployments/](https://docs.uniswap.org/contracts/v3/reference/deployments/)
:

Sushi V3 deployment addresses: [https://github.com/sushiswap/v3-periphery/tree/master/deployments](https://github.com/sushiswap/v3-periphery/tree/master/deployments)
:

Oku Trade deployment addresses: [https://docs.oku.trade/home/extra-information/deployed-contracts](https://docs.oku.trade/home/extra-information/deployed-contracts)
:

PancakeSwap deployment addresses: [https://developer.pancakeswap.finance/contracts/v3/addresses](https://developer.pancakeswap.finance/contracts/v3/addresses)
:

IguanaDEX deployment addresses: [https://docs.iguanadex.com/iguanadex-on-mainnet/contract-addresses](https://docs.iguanadex.com/iguanadex-on-mainnet/contract-addresses)
:

Custom SwapRouter deployments:

-
:

:

[BNB chain](https://bscscan.com/address/0xe7aC922b9751C7aca3A46D5505F36d5BbB1456b6#code)

-
:

:

[Etherlink](https://explorer.etherlink.com/address/0x2afB54fcaECd41BE4Ecd05d7bd2e193F2F05B99d?tab=contract)
:

[Plasma](https://plasmascan.to/address/0x9Ed7DFCDE80838f9FfaF4e7fFCe5CcE4737c3e3b)

:

**Configure adapter to whitelist pools:** *Configuration requires specifying tokens and fee from a pair*

:

:

:

:
:

:
:

:
**Velodrome, Aerodrome V3 (Slipstream)**[](#velodrome-aerodrome-v3-slipstream)

:

:
:

Velodrome V3 (Slipstream) multichain deployment addresses: [https://github.com/velodrome-finance/superchain-slipstream/blob/main/deployment-addresses](https://github.com/velodrome-finance/superchain-slipstream/blob/main/deployment-addresses)
:

Aerodrome V3 (Slipstream) [https://github.com/aerodrome-finance/slipstream?tab=readme-ov-file#deployment](https://github.com/aerodrome-finance/slipstream?tab=readme-ov-file#deployment)
:

**Configure adapter to whitelist pools:** *Configuration requires specifying tokens and fee from a pair*

:

:

:

:
:

:
:

:

**Curve StableSwap, CryptoSwap and StableNG**[](#curve-stableswap-cryptoswap-and-stableng)

:

**How to understand what\'s the type of the pool of interest:**

1.
:

2.
:

3.
:

4.
:

:

:
:

:
:

***Adapter arguments:***

-
:

:

:

-
:

:

:

-
:

:

Applicable only if pool is a metapool. Example: [this](https://www.curve.finance/dex/ethereum/pools/factory-v2-251/deposit/) pool has [FRAX/USDC](https://www.curve.finance/dex/ethereum/pools/fraxusdc/deposit/) as its base pool.

-
:

:

If Type of Pool is Crypto Swap (a.k.a Twocrypto/ Tricrypto) checkout this box.

:

ETH Gateway deployments:

-
:

:

[ETH/stETH pool](https://etherscan.io/address/0xdc24316b9ae028f1497c275eb9192a3ea0f67022) Gateway: 0x0675cb2066bacae2edfd09633d5b62be3c619a35

**PancakeSwap/ IguanaDEX StableSwap**[](#pancakeswap-iguanadex-stableswap)

Before adding adapter, please ensure that tokens from a pool and pool LP token itself are added as ***Assets to Market*** and as ***Collaterals to Credit Manager***. *e.g. to add USDX/USDT adapter both USDX, USDT and pool\'s LP token itself must be added before. learn how to find pool\'s token address below.*
-
:

**Select Curve V1 2 Assets adapter:**

:

-
:

:

:

-
:

:

:

-
:

:

Not applicable to PancakeSwap. Leave untouched.

-
:

:

Checkout this checkbox.

**Pendle**[](#pendle)

[](#router-configuration-2)

Router configuration
:

routerStatic

[](#adapter-configuration)

Adapter configuration
:

:
:

Pendle deployment addresses: [https://github.com/pendle-finance/pendle-core-v2-public/blob/main/deployments](https://github.com/pendle-finance/pendle-core-v2-public/blob/main/deployments)
:

**Configure adapter to whitelist pools:** *Configuration requires specifying market address and input/output tokens*

:

:

:

***Market:***

:

:

:

:

:

***Input token:*** Select a token that is in the \"1 SY Equals To\" row on the screenshot above \^
:

***Pendle token:*** Target PT token
:

**Fluid DEX**[](#fluid-dex)

##

For the router on the chain to support swaps, Fluid worker should be configured.

It requires passing the following addresses:

-
:

Before adding pool to adapter, please ensure that pool\'s tokens are added as ***Assets to Market*** and as ***Collaterals to Credit Manager***. *e.g. to add Fluid DEX for wstUSR/USDT, both wstUSR and USDT must be added.*
-
:

**Add Fluid DEX adapter (requires providing DEX address)**

:

If the pool includes ETH token, ETH Gateway must be deployed first and then be passed as target address to Fluid DEX adapter.
-
:

DEX addresses have names in the similar format: **Dex_wstUSR_USDT.** Search the name based on required tokens above.
-
:

:

Mainnet:

-
:

[](#dex_wsteth_eth-0x9f294bf3201533b652afb6b10c0385972c28a16f)

Dex_wstETH_ETH: 0x9f294BF3201533B652aFb6B10c0385972C28a16f
-
:

[](#ezeth_eth-0xa59fc0102b7c2aee66e237ee15cb56ad58a97b2e)

ezETH_ETH: 0xa59fc0102b7c2aee66e237ee15cb56ad58a97b2e
-
:

[](#rseth_eth-0xb219ce3fa907edcb375b7375f3c50d920e244bba)

rsETH_ETH: 0xb219cE3Fa907edCb375B7375F3C50d920e244bba
-
:

[](#weeth_eth)

weETH_ETH:
**ERC4626**[](#erc4626)

:

Takes ERC4626 **Vault Address** as parameter. Target vault must be added as Asset to Market and as Collateral to Credit Manager.

Before adding adapter, please ensure that token being underlying asset of a ERC4626 vault is added as ***Assets to Market*** and as ***Collaterals to Credit Manager***. *e.g. to add sDAI ERC4626 adapter DAI itself must be added before.*
Operates using deposit, withdraw, mint and redeem functions of ERC4626 standard. Allows performing swaps from the vault's **asset** token into ERC4626 vault **share** token.

Sometimes tokens look very much like ERC4626 but with overwritten methods, like those implementing timelocked deposits and withdrawals. Note that this adapter works with vanilla standard methods only. e.g. sUSDe can be minted from USDe using ERC4626 deposit interface, but has timelocked withdrawals.
**Kodiak Island**[](#kodiak-island)

##

For the router on the chain to support swaps, Kodiak Island worker should be configured.

It requires passing:

-
:

-
:

-
:

Takes Gateway Address as parameter. On Berachain it\'s 0x8d41361d340515d1cdd8c369ca7b5c79f6b2e9c9.

:

After adding adapter, click configure to whitelist particular Islands.

Before adding Island to adapter, please ensure that Island\'s tokens and Island itself are added as ***Assets to Market*** and as ***Collaterals to Credit Manager***. *e.g. to add WBERA/iBERA Island, WBERA, iBERA and Island must be added.*
:

**Convex-staked Curve LP**[](#convex-staked-curve-lp)

:
:

***Base Reward Pool Address:***

-
:

Rewards contract address from Convex pool Info.

:

:

***Staked phantom token:***

-
:

:

:

:

**Balancer V2**[](#balancer-v2)

:
##

For the router on the chain to support swaps, Balancer V3 worker should be configured.

Configuration requires passing:

-
:

Balancer deployment addresses can be found [here](https://docs-v2.balancer.fi/reference/contracts/deployment-addresses/mainnet.html).

##

-
:

**Add BalancerV2 adapter (requires providing Vault address):**

:

-
:

Before adding adapter, please ensure that tokens from a pool and pool LP token itself are added as ***Assets to Market*** and as ***Collaterals to Credit Manager***. *e.g. to add WETH/osETH pool to adapter both WETH, osETH and WETH/osETH token itself must be added before. learn how to find pool\'s token address below.*
-
:

:

-
:

:

:

-
:

Configuration requires specifying PoolID which can be found on Balancer UI

:

:

**Balancer V3**[](#balancer-v3)

[](#router-configuration-6)

Router configuration
:

[BalancerV3MultiActionQueries](https://github.com/Van0k/balancer-queries/blob/master/src/BalancerV3MultiActionQueries.sol) (needs to be deployed manually, reach out to contributors for support)

[](#adapter-configuration-2)

Adapter configuration
:

**Add BalancerV3 adapter (requires providing Gateway address):**

:
:

Gateway deployment addresses:

-
:

-
:

:

**Finding Pool LP Token Address:**

:
:

**Configure adapter to whitelist pools:**

:

:
:

Configuration requires specifying Pool Address which can be found on Balancer UI

:
:

**Mellow ERC4626**[](#mellow-erc4626)

##

For the router on the chain to support swaps, Mellow worker should be configured. Reach out to contributors for support.

Before adding adapter, please ensure that mellow vault (LRT itself) and its Withdrawal Phantom Token are added ***Assets to Market*** and as ***Collaterals to Credit Manager***. If the phantom token is not present in PFS, ask Gearbox contributors to help you deploy a new one.
###

:

-
:

:

Select a corresponding Mellow vault (LRT itself) that was previously added as collateral.

-
:

:

A token that tracks user\'s position in withdrawal queue and allows unstaking LRT right from the Credit Account.

###

This adapter allows claiming unstaked tokens after the redemption request was processed.

:

Mellow Claimer is a contract deployed by Mellow. Deployment addresses can be found here: [https://docs.mellow.finance/multi-deployments#navigation](https://docs.mellow.finance/multi-deployments#navigation)

**Configure Mellow Claimer Adapter**

:

:

-
:

:

Mellow LRT itself

-
:

:

A token that tracks user\'s position in withdrawal queue and allows unstaking LRT right from the Credit Account.

[[[Previous][Configuring a Credit Manager]]](/gearbox-permissionless-doc/advanced-configuration/configuring-a-credit-manager)[[[Next][Creating Bundles]]](/gearbox-permissionless-doc/advanced-configuration/creating-bundles)

Last updated 6 days ago