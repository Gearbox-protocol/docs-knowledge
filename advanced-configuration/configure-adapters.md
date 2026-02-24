# Configure Adapters

##

### What are adapters?

The Credit Account design enables active interaction with the DeFi ecosystem while borrowing — such as swapping tokens, depositing into vaults, claiming rewards, and more. However, allowing arbitrary operations poses security risks.

> Adapters — modular contracts that enable secure, controlled interactions with external protocols.

### Why do curators need to configure adapters?

Having adapters properly configured in the market is essential for allowing collateral swaps, 1-click leverage and other UX features of Gearbox protocol.

{% hint style="info" %}
Existing offchain infra (Front End, Liquidator) rely on router for finding paths from/to available collaterals. Router is not part of Gearbox protocol, therefore it’s not present in Bytecode repository. Router is used by Gearbox SDK to provide swap paths and it doesn’t interact with core contracts directly.
{% endhint %}

### What protocols are already integrated?

| Protocol                                                                                                                                                                                                                                                                                                                                                                            | Supported actions                                    |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| <p><em><strong>Uniswap, Sushiswap, Oku Trade</strong></em><br><a href="https://docs.gearbox.fi/gearbox-permissionless-doc/step-by-step-guides/configuring-adapters#uniswap-sushiswap-v2">V2</a>, <a href="https://docs.gearbox.fi/gearbox-permissionless-doc/step-by-step-guides/configuring-adapters#uniswap-sushiswap-pancakeswap-iguanadex-oku-trade-v3">V3</a></p>              | Swaps                                                |
| <p><em><strong>Pancakeswap, IguanaDEX</strong></em><br><a href="https://docs.gearbox.fi/gearbox-permissionless-doc/step-by-step-guides/configuring-adapters#uniswap-sushiswap-pancakeswap-iguanadex-oku-trade-v3">V3</a>, <a href="https://docs.gearbox.fi/gearbox-permissionless-doc/step-by-step-guides/configuring-adapters#pancakeswap-iguanadex-stableswap">StableSwap</a></p> | Swaps, Stableswap LP deposits                        |
| <p><em><strong>Balancer</strong></em><br><a href="https://docs.gearbox.fi/gearbox-permissionless-doc/step-by-step-guides/configuring-adapters#balancer-v2">V2</a>, <a href="https://docs.gearbox.fi/gearbox-permissionless-doc/step-by-step-guides/configuring-adapters#balancer-v3">V3</a></p>                                                                                     | Swaps, LP deposits                                   |
| <p><em><strong>Curve</strong></em><br><a href="https://docs.gearbox.fi/gearbox-permissionless-doc/step-by-step-guides/configuring-adapters#curve-stableswap-cryptoswap-and-stableng">Stableswap, CryptoSwap, Stable NG</a></p>                                                                                                                                                      | Swaps, LP deposits                                   |
| [_**Pendle**_](https://docs.gearbox.fi/gearbox-permissionless-doc/step-by-step-guides/configuring-adapters#curve-stableswap-cryptoswap-and-stableng)                                                                                                                                                                                                                                | PT swaps                                             |
| <p><a href="https://docs.gearbox.fi/gearbox-permissionless-doc/step-by-step-guides/configuring-adapters#mellow-erc4626"><em><strong>Mellow</strong></em></a><br>ERC4626 vaults, DVstETH</p>                                                                                                                                                                                         | Instant deposits, Delayed withdrawals                |
| <p><em><strong>Velodrome, Aerodrome</strong></em><br>V3, Stableswap</p>                                                                                                                                                                                                                                                                                                             | Swaps                                                |
| <p><em><strong>Camelot, Thena</strong> (Algebra AMM dexes)</em><br>V3</p>                                                                                                                                                                                                                                                                                                           | Swaps                                                |
| _**Napier**_                                                                                                                                                                                                                                                                                                                                                                        | PT Swaps, LP deposits                                |
| _**Convex**_                                                                                                                                                                                                                                                                                                                                                                        | Staking LP, claiming rewards                         |
| [_**Fluid DEX**_](https://docs.gearbox.fi/gearbox-permissionless-doc/step-by-step-guides/configuring-adapters#fluid-dex)                                                                                                                                                                                                                                                            | Swaps                                                |
| <p><em><strong>Camelot, Thena, Quickswap</strong></em> (Algebra AMM)<br>V3</p>                                                                                                                                                                                                                                                                                                      | Swaps                                                |
| _**Trader Joe**_                                                                                                                                                                                                                                                                                                                                                                    | Swaps                                                |
| _**Infrared**_                                                                                                                                                                                                                                                                                                                                                                      | Staking LP, claiming rewards                         |
| _**Sky**_                                                                                                                                                                                                                                                                                                                                                                           | DAI - USDS conversion, Staking USDS for SKY          |
| _**Lido**_                                                                                                                                                                                                                                                                                                                                                                          | stETH - wstETH conversion                            |
| [_**ERC4626**_](https://docs.gearbox.fi/gearbox-permissionless-doc/step-by-step-guides/configuring-adapters#erc4626)                                                                                                                                                                                                                                                                | Instant deposits and withdrawals (whenever possible) |
| [_**Kodiak Island**_](https://docs.gearbox.fi/gearbox-permissionless-doc/step-by-step-guides/configuring-adapters#erc4626)                                                                                                                                                                                                                                                          | Deposit into Island, Swaps in pool                   |
| <p>Uniswap<br>V4</p>                                                                                                                                                                                                                                                                                                                                                                | Swaps                                                |
| InfiniFi                                                                                                                                                                                                                                                                                                                                                                            | Instant deposits, Delayed withdrawals                |

All the source code and audit reports of the contracts can be found in [Bytecode Repository](https://permissionless.gearbox.foundation/bytecode). Use search, click on the target contract and then **View Source** or **View Report**. All the Adapters can be found by searching for the ADAPTER domain in Bytecode Repository.

[setup example (BNB chain: USD1 pool, USDX collateral)](https://www.notion.so/Adapter-setup-example-BNB-chain-USD1-pool-USDX-collateral-208145c16224807fa1a0d318c01bc1ae?pvs=21)

[setup example (Ethereum chain: tBTC pool, uptBTC collateral)](https://www.notion.so/Adapter-setup-example-Ethereum-chain-tBTC-pool-uptBTC-collateral-20e145c1622480c886d8d43dc5e9f5bb?pvs=21)

[setup example (Ethereum chain: USDC pool, frxUSD/USDf collateral)](https://gearboxprotocol.notion.site/Adapter-setup-example-Ethereum-chain-USDC-pool-frxUSD-USDf-collateral-24c145c16224809d80d2d171e1128317?source=copy_link)

<details>

<summary><strong>Uniswap, Sushiswap V2</strong></summary>

### Router configuration

For the router on the chain to support swaps, Uniswap V2 worker should be configured.

It requires passing the following addresses:

* SwapRouter
*   **Add UniswapV2 adapter (requires providing router address):**

    <figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FgPUvgs6W3TL9Ft5sKtxy%2Fimage.png?alt=media&#x26;token=9f153e18-b0f2-4313-b3b6-a6bc6711913f" alt=""><figcaption></figcaption></figure>

    * Uni V2 deployment addresses: [https://docs.uniswap.org/contracts/v2/reference/smart-contracts/v2-deployments](https://docs.uniswap.org/contracts/v2/reference/smart-contracts/v2-deployments)
    * Sushi V2 deployment addresses: [https://github.com/sushiswap/v2-core/tree/master/deployments](https://github.com/sushiswap/v2-core/tree/master/deployments)

{% hint style="warning" %}
Before allowing pools in adapter, please ensure that tokens from a pair are added as _**Assets to Market**_ and as _**Collaterals to Credit Manager**_.\
\
\&#xNAN;_e.g. to add WETH/USDC pool both WETH and USDC must be added before._
{% endhint %}

*   **Configure adapter to whitelist pools:**

    <figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FaoBYhRZaO2DyI1r2ol5r%2FScreenshot%202025-07-30%20at%2011.42.58.png?alt=media&#x26;token=eca49e23-f39c-4946-bc54-c7589e982e5f" alt=""><figcaption></figcaption></figure>

    <figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2F6xQ8eJtSYtt86Fre4Snn%2Fimage.png?alt=media&#x26;token=192f8408-bce9-4dd3-be6e-0d1654b273cc" alt=""><figcaption></figcaption></figure>
* Uni V2
  *   Configuration requires specifying tokens from a pair

      <figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2Fs02vv2Nl0NdxKKkGVHBB%2Fimage.png?alt=media&#x26;token=11c2ecc0-ce73-482e-9692-533da14deffb" alt=""><figcaption></figcaption></figure>
  * Sushi V2
    *   Configuration requires specifying tokens from a pair

        <figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FlwjKXetX9dIA0eXvWiNV%2Fimage.png?alt=media&#x26;token=c79c4774-b416-4cb2-a556-0ab8fdbd7182" alt=""><figcaption></figcaption></figure>

</details>

<details>

<summary><strong>Uniswap, Sushiswap, Pancakeswap, IguanaDEX, Oku trade V3</strong></summary>

### Router configuration

For the router on the chain to support swaps, Uniswap V3 worker should be configured.

It requires passing the following addresses:

* SwapRouter
* QuoterV2
*   **Add UniswapV3 adapter (requires providing SwapRouter address):**

    <figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FuraVMDpJnwa5uKGGLkb2%2Fimage.png?alt=media&#x26;token=3196b368-5b68-476e-ba0d-159f8b06f545" alt=""><figcaption></figcaption></figure>

    * Uni V3 deployment addresses: [https://docs.uniswap.org/contracts/v3/reference/deployments/](https://docs.uniswap.org/contracts/v3/reference/deployments/)
    * Sushi V3 deployment addresses: [https://github.com/sushiswap/v3-periphery/tree/master/deployments](https://github.com/sushiswap/v3-periphery/tree/master/deployments)
    * Oku Trade deployment addresses: [https://docs.oku.trade/home/extra-information/deployed-contracts](https://docs.oku.trade/home/extra-information/deployed-contracts)
    * PancakeSwap deployment addresses: [https://developer.pancakeswap.finance/contracts/v3/addresses](https://developer.pancakeswap.finance/contracts/v3/addresses)
    * IguanaDEX deployment addresses: [https://docs.iguanadex.com/iguanadex-on-mainnet/contract-addresses](https://docs.iguanadex.com/iguanadex-on-mainnet/contract-addresses)

{% hint style="info" %}
Router deployment must have bytecode of Uniswap's [SwapRouter.sol](https://github.com/Uniswap/v3-periphery/blob/v1.0.0/contracts/SwapRouter.sol) contract. Sometimes it has only [SwapRouter02](https://github.com/Uniswap/swap-router-contracts/blob/main/contracts/SwapRouter02.sol) deployment specified.\
\
On some chains that was already solved by deploying required implementation of router (see below).\
If it's not, reach out to Gearbox contributors.
{% endhint %}

* Custom SwapRouter deployments:
  * Uni V3
    * [BNB chain](https://bscscan.com/address/0xe7aC922b9751C7aca3A46D5505F36d5BbB1456b6#code)
  * Oku Trade
    * [Etherlink](https://explorer.etherlink.com/address/0x2afB54fcaECd41BE4Ecd05d7bd2e193F2F05B99d?tab=contract)
    * [Plasma](https://plasmascan.to/address/0x9Ed7DFCDE80838f9FfaF4e7fFCe5CcE4737c3e3b)
    * [Optimism](https://explorer.optimism.io/address/0xDb7D5A2146533BAE5C08A869Cb7e085d8Bee6e0F?tab=contract)

{% hint style="warning" %}
Before allowing pools in adapter, please ensure that tokens from a pair are added as _**Assets to Market**_ and as _**Collaterals to Credit Manager**_.\
\
\&#xNAN;_e.g. to add WETH/USDC pool both WETH and USDC must be added before._
{% endhint %}

*   **Configure adapter to whitelist pools:**\
    \&#xNAN;_Configuration requires specifying tokens and fee from a pair_

    <figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FoFBJtepjwKAYKKlJouh2%2FScreenshot%202025-07-30%20at%2012.23.10.png?alt=media&#x26;token=cdca39d5-3dcb-4534-a4d8-7a1e717f269a" alt=""><figcaption></figcaption></figure>

    <figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FFk1vAeE9mZYydHANXI8J%2Fimage.png?alt=media&#x26;token=8c38633f-428a-4cbf-9633-16db4d61a814" alt=""><figcaption></figcaption></figure>
*   Uni V3

    <figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FbJsE5buTT6F5PAsFLYQb%2Fimage.png?alt=media&#x26;token=21e9c43c-bb80-4b8d-8981-da2a0f4fa90f" alt=""><figcaption></figcaption></figure>
*   Sushi V3

    <figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FJD20UUZAw0vj497MivI5%2FScreenshot%202025-07-30%20at%2012.21.22.png?alt=media&#x26;token=403d92ae-9116-4032-b454-b96ed0731896" alt=""><figcaption></figcaption></figure>
* [PancakeSwap](https://pancakeswap.finance/info/v3/pairs), [IguanaDEX](https://www.iguanadex.com/info/v3?chain=etherlink)

<figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FFfDSOwZmEjzPqBAdjxg3%2FScreenshot%202025-07-30%20at%2012.28.59.png?alt=media&#x26;token=e0ad317c-cfac-422b-877a-c466b2753969" alt=""><figcaption></figcaption></figure>

</details>

<details>

<summary><strong>Velodrome, Aerodrome Concentrated Liquidity (Slipstream)</strong></summary>

For the router on the chain to support swaps, Uniswap V3 worker should be configured.

It requires passing the following addresses:

* SwapRouter
* Quoter
*   **Add UniswapV3 adapter (requires providing SwapRouter address):**

    <figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FuraVMDpJnwa5uKGGLkb2%2Fimage.png?alt=media&#x26;token=3196b368-5b68-476e-ba0d-159f8b06f545" alt=""><figcaption></figcaption></figure>

    * Velodrome V3 (Slipstream) multichain deployment addresses: [https://github.com/velodrome-finance/superchain-slipstream/blob/main/deployment-addresses](https://github.com/velodrome-finance/superchain-slipstream/blob/main/deployment-addresses)
    * Aerodrome V3 (Slipstream) [https://github.com/aerodrome-finance/slipstream?tab=readme-ov-file#deployment](https://github.com/aerodrome-finance/slipstream?tab=readme-ov-file#deployment)
*   **Configure adapter to whitelist pools:**\
    \&#xNAN;_Configuration requires specifying tokens and fee from a pair_

    <figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FoFBJtepjwKAYKKlJouh2%2FScreenshot%202025-07-30%20at%2012.23.10.png?alt=media&#x26;token=cdca39d5-3dcb-4534-a4d8-7a1e717f269a" alt=""><figcaption></figcaption></figure>

    <figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FFk1vAeE9mZYydHANXI8J%2Fimage.png?alt=media&#x26;token=8c38633f-428a-4cbf-9633-16db4d61a814" alt=""><figcaption></figcaption></figure>
*   Fee is a number specified in UI divided by 10000\
    e.g. Concentrated Volatile 100 ⇒ fee = 0.01%\
    Concentrated Stable 1 ⇒ fee = 0.0001%

    <figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2F45sMXW1mh3EDMOITumiE%2FScreenshot%202025-11-04%20at%2018.27.03.png?alt=media&#x26;token=c523a64b-21de-40fd-8b45-45853f48087d" alt=""><figcaption></figcaption></figure>

</details>

<details>

<summary><strong>Curve StableSwap, CryptoSwap and StableNG</strong></summary>

* **How to understand what's the type of the pool of interest:**
  1. Go to the block explorer page of Curve Address provider on a chain of interest:\
     [https://docs.curve.finance/deployments/integration/](https://docs.curve.finance/deployments/integration/)
  2. Call Address Provider's get\_address method with id = 7 to get address of MetaRegistry\
     On Mainnet MetaRegistry is located [here](https://etherscan.io/address/0xF98B45FA17DE75FB1aD0e7aFD971b0ca00e379fC).
  3. Call get\_registry\_handlers\_by\_pool of MetaRegistry, passing target pool address as argument.
  4. Check non-zero address from step 3. output. It usually has clues in first lines of its code.

{% hint style="warning" %}
Before adding adapter, please ensure that tokens from a pool and pool LP token itself are added as _**Assets to Market**_ and as _**Collaterals to Credit Manager**_.\
\
\&#xNAN;_e.g. to add 3Pool (USDC/USDT/DAI) adapter both USDC, USDT, DAI and 3Pool token itself must be added before._\
\
&#xNAN;_&#x6C;earn how to find pool's token address below._
{% endhint %}

*   _**If the pool is not Stable NG:**_\
    \&#xNAN;_Select Curve V1 2/3/4 Assets adapter depending on the number of different tokens in target pool:_

    <figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2Fer2qBO6Hws5WgmWfTMAU%2Fimage.png?alt=media&#x26;token=652d874e-65a6-454d-9142-347568e76411" alt=""><figcaption></figcaption></figure>
*   _**If the pool is Stable NG:**_\
    \&#xNAN;_Select Curve StableNG adapter:_

    <figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2Ff1uzTn4t0JeUurJqL3Ri%2Fimage.png?alt=media&#x26;token=1380baa9-f78e-48fe-9a7f-9468ee17bd31" alt=""><figcaption></figcaption></figure>

{% hint style="danger" %}
If the pool operates with non-erc20 ETH balance, deploy a ETH Gateway first and then pass it as target address.\
See the list of deployed gateways below and reach out to Gearbox team if the needed is not present.
{% endhint %}

* _**Adapter arguments:**_
  * **Target Address**
    *   The address of the pool

        <figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FQU3m8Ui1TQBK31vk8eZ7%2Fimage.png?alt=media&#x26;token=2e363ea8-33aa-4be3-8b15-a8baa8faea65" alt=""><figcaption></figcaption></figure>
  * **LP token**
    *   The address of the pool's LP token (may be different from pool itself)

        <figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FDNyLJqP4FiZ2ieqprrRM%2Fimage.png?alt=media&#x26;token=a94cbfe5-0096-4e51-a6a4-431cf0433eaf" alt=""><figcaption></figcaption></figure>
  * **Base Pool Address**
    * Applicable only if pool is a metapool.\
      Example: [this](https://www.curve.finance/dex/ethereum/pools/factory-v2-251/deposit/) pool has [FRAX/USDC](https://www.curve.finance/dex/ethereum/pools/fraxusdc/deposit/) as its base pool.
  * **Crypto Swap or PancakeSwap pool**
    * If Type of Pool is Crypto Swap (a.k.a Twocrypto/ Tricrypto) checkout this box.
* ETH Gateway deployments:
  * Mainnet:
    * [ETH/stETH pool](https://etherscan.io/address/0xdc24316b9ae028f1497c275eb9192a3ea0f67022) Gateway: 0x0675cb2066bacae2edfd09633d5b62be3c619a35

</details>

<details>

<summary><strong>PancakeSwap/ IguanaDEX StableSwap</strong></summary>

{% hint style="warning" %}
Before adding adapter, please ensure that tokens from a pool and pool LP token itself are added as _**Assets to Market**_ and as _**Collaterals to Credit Manager**_.\
\
\&#xNAN;_e.g. to add USDX/USDT adapter both USDX, USDT and pool's LP token itself must be added before._\
\
&#xNAN;_&#x6C;earn how to find pool's token address below._
{% endhint %}

*   **Select Curve V1 2 Assets adapter:**

    <figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2Fer2qBO6Hws5WgmWfTMAU%2Fimage.png?alt=media&#x26;token=652d874e-65a6-454d-9142-347568e76411" alt=""><figcaption></figcaption></figure>

    * **Target Address**
      *   The address of the pool

          <figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2F19Wse0ruaskhqHAzUGld%2FScreenshot%202025-07-31%20at%2018.53.41.png?alt=media&#x26;token=17f081ff-47d4-458c-8690-94f9ea9b97e6" alt=""><figcaption></figcaption></figure>
    * **LP token**
      *   The address of the pool's LP token (can be retreived by calling token() method of pool contract)

          <figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FW2gvj7zpmgsPWXEfFZdr%2FScreenshot%202025-07-31%20at%2018.54.48.png?alt=media&#x26;token=4a7bdf4c-ddc1-4379-aea7-ee5cd728f4fa" alt=""><figcaption></figcaption></figure>
    * **Base Pool Address**
      * Not applicable to PancakeSwap. Leave untouched.
    * **Crypto Swap or PancakeSwap pool**
      * Checkout this checkbox.

</details>

<details>

<summary><strong>Pendle</strong></summary>

### Router configuration

For the router on the chain to support swaps, Pendle worker should be configured.

It requires passing the following addresses:

* routerStatic

### Adapter configuration

*   **Add Pendle adapter (requires providing router address):**

    <figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FEdETjo59KTP0uc45mBu5%2Fimage.png?alt=media&#x26;token=1c2b9b0c-1095-4a7d-bd66-3cce2d25546c" alt=""><figcaption></figcaption></figure>
* Pendle deployment addresses: [https://github.com/pendle-finance/pendle-core-v2-public/blob/main/deployments](https://github.com/pendle-finance/pendle-core-v2-public/blob/main/deployments)

{% hint style="warning" %}
Before adding pool to adapter, please ensure that pool's input token and PT token are added as _**Assets to Market**_ and as _**Collaterals to Credit Manager**_.\
\
\&#xNAN;_e.g. to add Pendle pool for PT-sUSDe, both sUSDe and PT-sUSDe must be added before._
{% endhint %}

*   **Configure adapter to whitelist pools:**\
    \&#xNAN;_Configuration requires specifying market address and input/output tokens_

    <figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FxzSTHQsEiZqNxbII0d2r%2FScreenshot%202025-07-31%20at%2019.05.05.png?alt=media&#x26;token=9a383520-88f1-43b1-b431-92cabdd9f634" alt=""><figcaption></figcaption></figure>

    <figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FOTXZ7hZ3KJl84fCyNoHs%2Fimage.png?alt=media&#x26;token=edc0ac2b-3db8-48c3-ba3d-82ec4c388540" alt=""><figcaption></figcaption></figure>
*   _**Market:**_

    <figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FRDJS7RYkw9PhS9vMJZAc%2FScreenshot%202025-07-31%20at%2019.07.10.png?alt=media&#x26;token=fd9967a9-58a5-4a81-a872-9432c7626407" alt=""><figcaption></figcaption></figure>

    <figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FY900xsRdhhrPG6JDNgsn%2Fimage.png?alt=media&#x26;token=6ebae325-9377-437c-89df-f478825a8abb" alt=""><figcaption></figcaption></figure>

    <figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2F2O4sJLtbXAynhGcaJqJo%2Fimage.png?alt=media&#x26;token=10ae3170-a407-4eaf-a7b7-b1866ad512ab" alt=""><figcaption></figcaption></figure>

    <figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2F2yCVf9sGLvbJN7E9okUX%2FScreenshot%202025-07-31%20at%2019.08.20.png?alt=media&#x26;token=28e3a961-9c66-4bc4-81a1-9adb697cc208" alt=""><figcaption></figcaption></figure>
* _**Input token:**_\
  Select a token that is in the "1 SY Equals To" row on the screenshot above ^
* _**Pendle token:**_\
  Target PT token

</details>

<details>

<summary><strong>Fluid DEX</strong></summary>

### Router configuration

For the router on the chain to support swaps, Fluid worker should be configured.

It requires passing the following addresses:

* fluidDexResolver

{% hint style="warning" %}
Before adding pool to adapter, please ensure that pool's tokens are added as _**Assets to Market**_ and as _**Collaterals to Credit Manager**_.\
\
\&#xNAN;_e.g. to add Fluid DEX for wstUSR/USDT, both wstUSR and USDT must be added._
{% endhint %}

*   **Add Fluid DEX adapter (requires providing DEX address)**

    <figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2F17NXNd57pDv0baEL8S7o%2Fimage.png?alt=media&#x26;token=3f2e89b4-441e-4a56-97f4-da632f598dd5" alt=""><figcaption></figcaption></figure>

{% hint style="danger" %}
If the pool includes ETH token, ETH Gateway must be deployed first and then be passed as target address to Fluid DEX adapter.
{% endhint %}

* Fluid deployment addresses: [https://github.com/Instadapp/fluid-contracts-public/blob/main/deployments/deployments.md](https://github.com/Instadapp/fluid-contracts-public/blob/main/deployments/deployments.md)

{% hint style="info" %}
DEX addresses have names in the similar format: **Dex\_wstUSR\_USDT.**\
Search the name based on required tokens above.
{% endhint %}

* ETH Gateway deployments:
  * Mainnet:
    * **Dex\_wstETH\_ETH: 0x9f294BF3201533B652aFb6B10c0385972C28a16f**
    * **ezETH\_ETH: 0xa59fc0102b7c2aee66e237ee15cb56ad58a97b2e**
    * **rsETH\_ETH: 0xb219cE3Fa907edCb375B7375F3C50d920e244bba**
    *   **weETH\_ETH:**

        0x0A226E0efa6FCF26837441d623210A9464349200

</details>

<details>

<summary><strong>ERC4626</strong></summary>

<figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FKZ3PXJMeYwwbNlqfEhtW%2Fimage.png?alt=media&#x26;token=797ecc81-0c6f-4498-9a33-2c8763e3da58" alt=""><figcaption></figcaption></figure>

Takes ERC4626 **Vault Address** as parameter. Target vault must be added as Asset to Market and as Collateral to Credit Manager.

{% hint style="warning" %}
Before adding adapter, please ensure that token being underlying asset of a ERC4626 vault is added as _**Assets to Market**_ and as _**Collaterals to Credit Manager**_.\
\
\&#xNAN;_e.g. to add sDAI ERC4626 adapter DAI itself must be added before._
{% endhint %}

Operates using deposit, withdraw, mint and redeem functions of ERC4626 standard. Allows performing swaps from the vault’s **asset** token into ERC4626 vault **share** token.

{% hint style="info" %}
Sometimes tokens look very much like ERC4626 but with overwritten methods, like those implementing timelocked deposits and withdrawals.\
Note that this adapter works with vanilla standard methods only.\
\
e.g. sUSDe can be minted from USDe using ERC4626 deposit interface, but has timelocked withdrawals.
{% endhint %}

</details>

<details>

<summary><strong>Kodiak Island</strong></summary>

### Router configuration

For the router on the chain to support swaps, Kodiak Island worker should be configured.

It requires passing:

* \_kodiakIslandRouter - 0x679a7C63FC83b6A4D9C1F931891d705483d4791F
* \_kodiakSwapRouter - 0xEd158C4b336A6FCb5B193A5570e3a571f6cbe690
* \_kodiakQuoter - 0x644C8D6E501f7C994B74F5ceA96abe65d0BA662B

Takes Gateway Address as parameter. On Berachain it's 0x8d41361d340515d1cdd8c369ca7b5c79f6b2e9c9.

<figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FHwTMmN6z9RGbS67tdvWr%2Fimage.png?alt=media&#x26;token=c0747fbd-5750-4da1-92aa-70ca9ad56c14" alt=""><figcaption></figcaption></figure>

After adding adapter, click configure to whitelist particular Islands.

{% hint style="warning" %}
Before adding Island to adapter, please ensure that Island's tokens and Island itself are added as _**Assets to Market**_ and as _**Collaterals to Credit Manager**_.\
\
\&#xNAN;_e.g. to add WBERA/iBERA Island, WBERA, iBERA and Island must be added._
{% endhint %}

<figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FQulvfrSABEtd0kfmsTYz%2FScreenshot%202025-08-06%20at%2023.21.42.png?alt=media&#x26;token=4de8aff4-bb3c-433f-9702-f3305dc0c788" alt=""><figcaption></figcaption></figure>

</details>

<details>

<summary><strong>Convex-staked Curve LP</strong></summary>

{% hint style="warning" %}
Before adding and configuring Convex pool adapters, ensure that **Curve LP token**, **Convex Deposit Token**, **Staked Phantom Token**, **CRV** and **CVX** are added as collaterals to Market and Credit Manager (everything except **Staked Phantom Token** can have zero limit, LT and feed).\
\
\
**Convex Deposit Token** can be found by its symbol. If the Curve LP token has symbol frxUSDUSDf, then Convex deposit token will have symbol cvxfrxUSDUSDf.

**Staked Phantom Token** can be found by its symbol. If the Curve LP token has symbol frxUSDUSDf, then Convex deposit token will have symbol stkcvxfrxUSDUSDf.
{% endhint %}

**Add Convex Base Reward Pool adapter.**

<figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FGWJihi6v4HXYTBzXwTHn%2Fimage.png?alt=media&#x26;token=de47cb2e-30d1-4ae7-acef-5c30cf873268" alt=""><figcaption></figcaption></figure>

* _**Base Reward Pool Address:**_
  *   Rewards contract address from Convex pool Info.

      <figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2F5G25SD5feSPFgxqEHf88%2FScreenshot%202025-08-11%20at%2018.25.08.png?alt=media&#x26;token=9c5a5e22-cd32-4bca-96a0-756b8c4b7c04" alt=""><figcaption></figcaption></figure>
* _**Staked phantom token:**_
  * **Staked Phantom Token** can be found by its symbol. If the Curve LP token has symbol frxUSDUSDf, then Convex deposit token will have symbol stkcvxfrxUSDUSDf.

**Add Convex Booster adapter**

{% hint style="success" %}
If the Credit Manager already includes the Convex Booster adapter, skip it and proceed to the next step (Update Convex booster Pool IDs).
{% endhint %}

{% hint style="info" %}
Booster address is single across all chains and is suggested as default option.
{% endhint %}

<figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FLUreGlKhUL1JIBttyUAx%2Fimage.png?alt=media&#x26;token=a5e429f9-362a-4e55-8a94-947d17e88c58" alt=""><figcaption></figcaption></figure>

**Update Convex booster Pool IDs**

{% hint style="info" %}
After each new Convex pool is added, Booster pool ids should be updated.
{% endhint %}

<figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FksbowXgQmglpu63apbiq%2FScreenshot%202025-08-11%20at%2018.49.58.png?alt=media&#x26;token=918b3854-3249-46f3-8b70-deff6b9e7df8" alt=""><figcaption></figcaption></figure>

<figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FZiz7jeL4kFrjc0zcF4bG%2FScreenshot%202025-08-11%20at%2018.51.39.png?alt=media&#x26;token=68bef310-b551-4f91-8f86-a03bac5459fe" alt=""><figcaption></figcaption></figure>

<br>

</details>

<details>

<summary><strong>Balancer V2</strong></summary>

### Router configuration

For the router on the chain to support swaps, Balancer V2 worker should be configured.

Configuration requires passing:

* BalancerQueries

Balancer deployment addresses can be found [here](https://docs-v2.balancer.fi/reference/contracts/deployment-addresses/mainnet.html).

### Adapter configuration

*   **Add BalancerV2 adapter (requires providing Vault address):**

    <figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FlnwiyFpcKYePevVDrWUX%2Fimage.png?alt=media&#x26;token=c45ab5d4-9d73-4f25-9e37-e093d9fb1992" alt=""><figcaption></figcaption></figure>

    * Deployment addresses:\
      [https://docs-v2.balancer.fi/reference/contracts/deployment-addresses/mainnet.html](https://docs-v2.balancer.fi/reference/contracts/deployment-addresses/mainnet.html)

{% hint style="warning" %}
Before adding adapter, please ensure that tokens from a pool and pool LP token itself are added as _**Assets to Market**_ and as _**Collaterals to Credit Manager**_.\
\
\&#xNAN;_e.g. to add WETH/osETH pool to adapter both WETH, osETH and WETH/osETH token itself must be added before._\
\
&#xNAN;_&#x6C;earn how to find pool's token address below._
{% endhint %}

* **Finding Pool LP Token Address:**

<figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FzsulT91DhQ06LhW4TYMG%2FScreenshot%202025-09-08%20at%2013.58.46.png?alt=media&#x26;token=e9b944df-68bf-4d09-8575-c06f61a36825" alt=""><figcaption></figcaption></figure>

* **Configure adapter to whitelist pools:**

<figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FROwzCJShVrloEqj4A7WU%2FScreenshot%202025-09-08%20at%2013.55.44.png?alt=media&#x26;token=1bf21836-5e5d-42e3-a4ea-bb5389db7a31" alt=""><figcaption></figcaption></figure>

<figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FHwV0fQxznBwHni5G1J0r%2Fimage.png?alt=media&#x26;token=d6d15d54-508d-4112-b28b-afef428a7196" alt=""><figcaption></figcaption></figure>

*   Configuration requires specifying PoolID which can be found on Balancer UI<br>

    <figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FxicEIVIbkd8cKRAGI3Pc%2FScreenshot%202025-09-08%20at%2013.53.56.png?alt=media&#x26;token=1b7c3e84-f208-4204-b8bb-d191d9e38f5f" alt=""><figcaption></figcaption></figure>

</details>

<details>

<summary><strong>Balancer V3</strong></summary>

### Router configuration

For the router on the chain to support swaps, Balancer V3 worker should be configured.

Configuration requires passing:

* [BalancerV3MultiActionQueries](https://github.com/Van0k/balancer-queries/blob/master/src/BalancerV3MultiActionQueries.sol) (needs to be deployed manually, reach out to contributors for support)

Balancer deployment addresses can be found [here](https://docs.balancer.fi/developer-reference/contracts/deployment-addresses/plasma.html#core-contracts).

BalancerV3MultiActionQueries deployments:

* Plasma
  * 0x1a9B1bfD35fA3932493b5f4F20Cb16b2B88Cc0C8
* Mainnet
  * 0x0BA8417d19D87b7b5C9dA8762ba505d61D1bF1E7
* Optimism
  * 0x1b8a4BA520C7789D7bE7476960B8Cdd42e57d928

### Adapter configuration

* **Add BalancerV3 adapter (requires providing Gateway address):**

<figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2Fmls6oiCcKLriwKhEPdSt%2Fimage.png?alt=media&#x26;token=5efed6c7-0ff5-4c1c-94c4-92e801eb2acd" alt=""><figcaption></figcaption></figure>

* Gateway deployment addresses:
  * Ethereum:
    * v3.10 (outdated) 0x21f55223de449224e8bdf4f59452e072bdf7af57
    * v3.11 (up to date) 0x8A57c21234ddc225499843F6A073dd374c952560
  * Plasma:
    * v3.10 (outdated) 0xd5c89297ad23e12d7f0ff24112418dbe9ebeae56
    * v3.11 (up to date) 0x55109bA88c396008cfBe9F27Ad97A7e1e4394f6F
  * Optimism:
    * v3.11 (up to date) 0x77b2dfc344072fa242f2d03893ccbdbb0ef47b7c

{% hint style="warning" %}
Before adding adapter, please ensure that tokens from a pool are added as _**Assets to Market**_ and as _**Collaterals to Credit Manager**_.\
\
\&#xNAN;_e.g. to add_ waEthLidowstET&#x48;_/rstETH pool to adapter both_ waEthLidowstET&#x48;_, rstETH and_ waEthLidowstET&#x48;_/rstETH token itself must be added before._\
\
&#xNAN;_&#x6C;earn how to find pool's token address below._
{% endhint %}

{% hint style="info" %}
What are _wa_-tokens?\
It's erc4626 vaults representing positions staked in Aave pools.\
To support swaps from wstETH through waEthLidowstET&#x48;_/rstETH_ boosted Balancer pool, you need to include wa-token as collateral and add erc4626 adapter with wa-token address as vault which will process swaps from wstETH to waEthLidowstETH.
{% endhint %}

* **Finding Pool LP Token Address:**

<figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FmYO13gfzXpxs0joceoTZ%2FScreenshot%202025-09-08%20at%2015.27.47.png?alt=media&#x26;token=bfbeed19-6a9e-466f-8c27-60428196e3ea" alt=""><figcaption></figcaption></figure>

* **Configure adapter to whitelist pools:**

<figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FROwzCJShVrloEqj4A7WU%2FScreenshot%202025-09-08%20at%2013.55.44.png?alt=media&#x26;token=1bf21836-5e5d-42e3-a4ea-bb5389db7a31" alt=""><figcaption></figcaption></figure>

<figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FIEx3xUoAQLYQdD6Fk5F3%2Fimage.png?alt=media&#x26;token=c6723aa2-3b46-4ada-b7d1-22b0b6e13b02" alt=""><figcaption></figcaption></figure>

* Configuration requires specifying Pool Address which can be found on Balancer UI

<figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2Fxy74glIyKmeVOWolJYqI%2FScreenshot%202025-09-08%20at%2015.27.47.png?alt=media&#x26;token=9ef6875f-0a94-4893-a9dc-edbb12c262b4" alt=""><figcaption></figcaption></figure>

</details>

<details>

<summary><strong>Mellow ERC4626</strong></summary>

### Router configuration

For the router on the chain to support swaps, Mellow worker should be configured. Reach out to contributors for support.

{% hint style="warning" %}
Before adding adapter, please ensure that mellow vault (LRT itself) and its Withdrawal Phantom Token are added _**Assets to Market**_ and as _**Collaterals to Credit Manager**_.\
\
If the phantom token is not present in PFS, ask Gearbox contributors to help you deploy a new one.
{% endhint %}

#### **Add Mellow ERC4626 adapter:**

<figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2Fhhyy1ezj4oAIMF2bFJRj%2Fimage.png?alt=media&#x26;token=837d9d8d-c803-4d3e-bbe2-3f7167892e7a" alt=""><figcaption></figcaption></figure>

* Vault address
  * Select a corresponding Mellow vault (LRT itself) that was previously added as collateral.
* Phantom Token
  * A token that tracks user's position in withdrawal queue and allows unstaking LRT right from the Credit Account.

#### **Add Mellow claimer adapter:**

This adapter allows claiming unstaked tokens after the redemption request was processed.

<figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FuV4fPeYu6we7yG4d069v%2Fimage.png?alt=media&#x26;token=61fc8213-cd22-4213-90ec-f4b0ca33308f" alt=""><figcaption></figcaption></figure>

Mellow Claimer is a contract deployed by Mellow. Deployment addresses can be found here: [https://docs.mellow.finance/multi-deployments#navigation](https://docs.mellow.finance/multi-deployments#navigation)

**Configure Mellow Claimer Adapter**

<figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FbGkErmaEZ3tylx2KZGEd%2FScreenshot%202025-09-08%20at%2017.13.56.png?alt=media&#x26;token=fa0bdac7-b038-4a95-a824-d72e0a9492b9" alt=""><figcaption></figcaption></figure>

<figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2Fw2q163xn91fhnUikuYiV%2Fimage.png?alt=media&#x26;token=8ba56bc2-3559-4bb5-8b49-a24f5331aa56" alt=""><figcaption></figcaption></figure>

* Multi vault
  * Mellow LRT itself
* Phantom token
  * A token that tracks user's position in withdrawal queue and allows unstaking LRT right from the Credit Account.

</details>

<details>

<summary><strong>Midas (direct deposits &#x26; redemptions)</strong></summary>

Midas risks:

\- If Midas rejects a withdrawal request, a credit account that has the request rejected will have its phantom token balance locked and non-claimable. This means that de-facto the account has bad debt (that cannot be liquidated) until the situation is resolved manually

\- A gateway has a function to manually process a cancelled request by paying an amount of at least pendingTokenOutAmount for the respective credit account (the function can be called by anyone). This will allow the credit account to claim a withdrawal as if it was normally processed

\- It's best to forbid the withdrawal phantom token if there is a rejected request to Gearbox CA, since Midas might accidentally refund the withdrawal to the CA itself, leading to double counting. Forbidding the token will prevent the user to borrow and withdraw more against their collateral in this case.

{% hint style="warning" %}
For safety, each curator on each chain must have its own gateway and phantom token for each vault.
{% endhint %}

Gateway addresses:

* Plasma
  * Hyperithm Curator: 0xB375DF6a1D7a1c172e65D4FBDA2d3caa144Bf8e7

Phantom token addresses:

* Plasma
  * Hyperithm Curator: 0x0835e60e9A56734cEE76e3953c3BE0635Fcb71d5

</details>

<details>

<summary><strong>Velodrome, Aerodrome V1 &#x26; V2 (Basic volatile and Basic stable)</strong></summary>

For the router on the chain to support swaps, Velodrome worker should be configured.

It requires passing the following addresses:

* Router
* **Add Velodrome V2 adapter (requires providing Router address):**

<figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FJy5Z2T1W9XpkR1Yqyro6%2Fimage.png?alt=media&#x26;token=ef71c35d-1e47-4f24-b0f3-3522e7dd9a71" alt=""><figcaption></figcaption></figure>

* Velodrome v2 optimism deployment addresses: [https://github.com/velodrome-finance/contracts/tree/main/deployment-addresses](https://github.com/velodrome-finance/contracts/tree/main/deployment-addresses)
*   **Configure adapter to whitelist pools:**\
    \&#xNAN;_Configuration requires specifying tokens and fee from a pair_\
    &#xNAN;_&#x4C;ook for Pool Factory in deployment addresses_

    <figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FX1mHADL2rTEmesSiyBKg%2Fimage.png?alt=media&#x26;token=f8877bbc-4cec-4121-9b5f-03dc5d51f9f4" alt=""><figcaption></figcaption></figure>
* Is Stable?\
  Basic stable ⇒ Stable\
  Basic volatile ⇒ not Stable

</details>

<details>

<summary><strong>Uniswap V4</strong></summary>

### Router configuration

For the router on the chain to support swaps, Uniswap V3 worker should be configured.

It requires passing the following addresses:

* [Universal Router](https://github.com/Uniswap/universal-router/blob/dev/contracts/UniversalRouter.sol)
* [Quoter](https://github.com/Uniswap/v4-periphery/blob/main/src/lens/V4Quoter.sol)
*   **Add UniswapV4 adapter (requires providing Gateway address):**

    <figure><img src="../.gitbook/assets/image (1).png" alt=""><figcaption></figcaption></figure>

    * Uni V4 deployment addresses: [https://docs.uniswap.org/contracts/v4/deployments](https://docs.uniswap.org/contracts/v4/deployments)
    * Gateway deployment addresses:
      * Monad: 0xCC7944C237DC540585935F19Bc9aeA0003BC4224
      * Ethereum: 0x3b74c70283b291e875da84d58176a63dac5d1824

{% hint style="warning" %}
Before allowing pools in adapter, please ensure that tokens from a pair are added as _**Assets to Market**_ and as _**Collaterals to Credit Manager**_.\
\
&#xNAN;_&#x65;.g. to add WETH/USDC pool both WETH and USDC must be added before._
{% endhint %}

{% hint style="success" %}
To fetch fee, tick spacing and hook list, go to **Position Manager** contract and call _**poolKeys**_ method passing first 52 symbols of pool identifier from Uniswap UI as PoolID.\
\
E.g. if uniswap link has 0x9b25899648292dce5f8805823aebd0d025bf2625be3162a2f1199e13d8d300c8, then 0x9b25899648292dce5f8805823aebd0d025bf2625be3162a2f1 should be passed as poolID to Position Manager. \
\
Position Manager addresses on different chains can be found [here](https://docs.uniswap.org/contracts/v4/deployments).
{% endhint %}

<figure><img src="../.gitbook/assets/Screenshot 2026-02-24 at 18.27.33.png" alt=""><figcaption></figcaption></figure>

* **Configure adapter to whitelist** \
  &#xNAN;_&#x43;onfiguration requires specifying tokens and fee from a pair_



</details>

