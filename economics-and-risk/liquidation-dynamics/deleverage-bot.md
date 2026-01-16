# Deleverage bot

### Deleverage - protection against liquidations

The deleverage bot is designed to protect Gearbox users from full liquidations by automatically reducing leverage when an account’s health factor (HF) falls below a safe threshold.

It acts as an early warning mechanism selling a small portion of collateral to restore safety before liquidation conditions are met.

By doing so, the bot helps maintain protocol stability, safeguards user positions, and ensures smooth, market-driven deleveraging without requiring manual intervention or external subsidies.

### How to connect a bot

Any user can connect a bot directly through the UI.

From a technical standpoint, bot deployment is fully permissionless, users do not need approval from the DAO or a curator to deploy or connect a bot.

However, for a bot to appear and be connectable via the UI, it must first be whitelisted there.

### Bot fees

When a deleveraging event occurs, two types of fees are distributed:

* **Premium:** Paid to the liquidator (deleverager) who executes the deleverage transaction. This serves as the direct incentive for running a bot and maintaining system safety.
* **Fee:** Sent to the protocol treasury as the protocol’s share from the operation.

### Bot parameters

| minHF        | The threshold at which the bot starts deleveraging. When a user’s HF falls below this value, the bot begins selling part of their collateral to restore stability.                                                                                                                       |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| maxHF        | The upper limit to which the bot is allowed to increase a user’s HF during a deleveraging operation. The bot will not push the HF above this value. The target HF for each operation lies somewhere between minHF and maxHF, depending on market conditions and the available liquidity. |
| PremiumScale | Defines how much of the Credit Manager’s liquidation premium is taken as the deleverage premium. A value of 100% means the bot receives the same premium as a liquidator would.                                                                                                          |
| FeeScale     | Specifies the fraction of the protocol fee applied to deleveraging. Typically set to 100%, aligning it with the standard liquidation fee.                                                                                                                                                |

### **Rationale Behind Selecting Bot Parameters**

#### **1. Primary Goal – Prevent Full Liquidations**

The main purpose of the deleverage bot is to **protect users from full liquidations**.

* The `minHF` (health factor at which deleverage is triggered) should be high enough so that a sudden drop in collateral value doesn’t make an account liquidatable immediately.
* This gives the bot a time window to act and deleverage before liquidation occurs.
*   **Example:** If **WETH** is the collateral and we want to protect users from a **10% short-term price drop**, then:

    ```
    minHF = 1 + 0.10 = 1.1
    ```

***

#### **2. Avoid Triggering Under Normal Conditions**

Deleveraging should **not** happen during ordinary market fluctuations.

* Therefore, `minHF` should be **as low as possible**, ensuring that minor price deviations do not trigger unnecessary deleveraging.

***

#### **3. Minimize Collateral Sold Per Event**

The amount of collateral sold in a single deleveraging event should be minimized.

* To achieve this, `maxHF` should be set **as close as possible to `minHF`**, limiting the size of each operation.

***

#### **4. Ensure Organic Profitability**

Deleveraging operations should be **naturally profitable** to encourage participation from external bots without requiring subsidies.

* Set `PremiumScale` and `FeeScale` to **100%**, meaning the **deleverage premium = liquidation premium**.
* The scale defines how much of the Credit Manager’s liquidation premium is allocated to deleveraging.
* `maxHF` should be high enough so that both the **liquidation size** and **premium** are meaningful in dollar terms.

***

#### **5. Keep Minimal Position Size Reasonable**

The minimum position size (Credit Manager’s minimum debt) should not be too large.

* The target for the **minimum position size** is around **$10,000**.
