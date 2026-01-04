# Listing a new asset in the main App

Once the market contracts are deployed onchain, the Gearbox Interface (`app.gearbox.fi`) must be updated to display them.

The official interface is maintained by Gearbox Contributors. To accelerate the listing process, Curators can submit a **Pull Request (PR)** to the configuration repositories. This provides the development team with the necessary data (icons, addresses, APY sources) in a ready-to-merge format.

## Prerequisites

1. **GitHub Account:** Required to submit changes.
2. **Asset Icons:** High-quality `.svg` files for the underlying token and any reward tokens.
3. **Contract Addresses:** The addresses of the deployed Credit Managers.
4. **APY Data Sources:** Links to DefiLlama or Merkl pools (if applicable).

{% stepper %}
{% step %}
## Upload Asset Icons

**Repository Location:** [https://github.com/Gearbox-protocol/static/tree/main/public/tokens](https://github.com/Gearbox-protocol/static/tree/main/public/tokens)

**Instructions:**

* Format: `.svg` (Strict requirement).
* Naming: **Lowercase symbol** (e.g., `susde.svg`, `wsteth.svg`).

<details>

<summary>Asset display example</summary>

<figure><img src="../.gitbook/assets/image (5).png" alt=""><figcaption></figcaption></figure>

</details>

{% hint style="warning" %}
**Merkl Campaigns:** If the strategy earns rewards via Merkl, the reward token icon must also be uploaded, or the APR tooltip will break.
{% endhint %}

<details>

<summary>Merkl display example</summary>

<figure><img src="../.gitbook/assets/Screenshot 2025-12-16 at 12.31.53.png" alt=""><figcaption></figcaption></figure>

</details>
{% endstep %}

{% step %}
### Configure Lending Pools (Earn Page)

If a new Liquidity Pool was deployed, it must be added to the "Earn" page configuration.

**Repository Location:** [https://github.com/Gearbox-protocol/static/blob/main/src/pools/index.ts](https://github.com/Gearbox-protocol/static/blob/main/src/pools/index.ts)

**Fill in the following fields:**

* `name`: The displayed name (e.g., "Edge UltraYield USDC").
* `address`: The contract address of the Liquidity Pool.
* `chainId`: The integer ID of the network (e.g., `1` for Mainnet, `42161` for Arbitrum).
* `network`: The string name of the network (e.g., "Mainnet", "Arbitrum").
* `curator`: The entity managing the pool.
  * _Constraint:_ This must match a valid `Curator` type defined in the [Gearbox SDK](https://github.com/Gearbox-protocol/sdk/blob/master/src/sdk/chain/chains.ts).
* `poolType`: The category tag (e.g., `["stable"]`, `["eth"]`).
  * _Constraint:_ This must match a valid pool type defined in the [Pools type list](https://github.com/Gearbox-protocol/static/blob/main/src/core/pools.ts).
{% endstep %}

{% step %}
### Configure Strategies (Farm Page)

If new Credit Managers (Strategies) were deployed, they must be added to the "Farm" page configuration.

**Repository Location:** [https://github.com/Gearbox-protocol/static/blob/main/src/strategies/index.ts](https://github.com/Gearbox-protocol/static/blob/main/src/strategies/index.ts)

**Fill in the following fields:**

* `name`: The display name (e.g., "Lido staked ETH").
* `id`: The token symbol (e.g., "susde"). This serves as the unique key.
* `tokenOutAddress`: The address of the collateral token.
* `creditManagers`: An array containing the addresses of all Credit Managers that support this strategy.
  * _Example:_ `["0xCM_Address_1", "0xCM_Address_2"]`
* `strategyType`: The category tag (e.g., `["stable"]`, `["eth"]`).
  * _Constraint:_ This must match a valid strategy type defined in the [Strategy types list.](https://github.com/Gearbox-protocol/static/blob/main/src/core/strategy.ts)
* `issuesOnClose`: Set to `true` if the asset has delayed redemptions or requires extra capital to close (prevents users from getting stuck).
{% endstep %}

{% step %}
## Connect Yield Data (APY)

#### Option A: DefiLlama Integration

If the underlying protocol is tracked on DefiLlama.

**Repository Location:** [https://github.com/Gearbox-protocol/apy-server/blob/main/src/tokens/apy/llama/constants.ts](https://github.com/Gearbox-protocol/apy-server/blob/main/src/tokens/apy/llama/constants.ts)

* **Action:** Add the DefiLlama Pool ID to the configuration map.

#### Option B: Merkl Integration

If the strategy earns incentives via Merkl.

**Repository Location:** [https://github.com/Gearbox-protocol/apy-server/blob/main/src/tokens/apy/merkle/constants.ts](https://github.com/Gearbox-protocol/apy-server/blob/main/src/tokens/apy/merkle/constants.ts)

* **Action:** Add the Merkl Campaign parameters to the relevant Network object (e.g., `Plasma`, `Monad`).
  * **Key:** The token address (e.g., `"0x2d84..."`).
  * **Value Object:**
    * `id`: The token address(repeated).
    * `symbol`: Token symbol (e.g., `"USDT0USDe"`).
    * `type`: Usually `"common"`.

#### Option C: Points Campaigns

If the strategy or pool earns points (e.g., Ethena Sats, EigenLayer Points), the configuration is split into three parts.

**1. Register the Point Type**\
If this is a new point system, define it in the base configuration.

* [**Path**](https://github.com/Gearbox-protocol/apy-server/blob/92bf265744b95ecf7ce85da67278b27a71229691/src/tokens/points/constants.ts#L58)
*   **Action:** Add a new entry to `REWARDS_BASE_INFO`.

    ```typescript
    somnia: (multiplier: PointsReward["multiplier"]): PointsReward => ({
      name: "Somnia",
      units: "points multiplier",
      multiplier,
      type: "somnia",
    }),
    ```

**2. Apply to Strategies (Farm Page)**\
If the points are earned by holding collateral (e.g., weETH).

* [**Path**](https://github.com/Gearbox-protocol/apy-server/blob/92bf265744b95ecf7ce85da67278b27a71229691/src/tokens/points/constants.ts#L276C14-L285C7)
*   **Action:** Add the collateral address to `POINTS_INFO_BY_NETWORK`.

    ```typescript
    {
      address: "0xCollateralAddress...",
      symbol: "weETH",
      rewards: [REWARDS_BASE_INFO.etherfi(200n)], // 200n = 2x Multiplier
    },
    ```

**3. Apply to Pools (Earn Page)**\
If the points are earned by depositing into a lending pool.

* **File:** [https://github.com/Gearbox-protocol/apy-server/blob/main/src/pools/points/constants.ts](https://github.com/Gearbox-protocol/apy-server/blob/main/src/pools/points/constants.ts)
* **Action:**
  1. Add the Pool Address to `const POOLS`.
  2. Add the Token Address to `const TOKENS`.
  3.  Add the Reward Logic to the Network array.

      ```typescript
      {
        pool: POOLS.USDC_E_V3_SOMNIA,
        token: TOKENS.USDC_E_SOMNIA,
        symbol: "USDC.e",
        amount: 12n * 1000n, // 12n * 1000n = 1.2x Multiplier
        duration: "day",
        name: `${REWARDS_BASE_INFO.somnia(1n).name} ${REWARDS_BASE_INFO.somnia(1n).units}`,
        type: REWARDS_BASE_INFO.somnia(1n).type,
        estimation: "absolute",
        condition: "holding",
      },
      ```
{% endstep %}
{% endstepper %}
