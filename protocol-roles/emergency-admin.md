# Emergency admin

{% hint style="success" %}
### UI for executing Emergency Admin function is located at [https://permissionless-safe.gearbox.foundation/emergency/](https://permissionless-safe.gearbox.foundation/emergency/)
{% endhint %}

### Why is it needed?

The Emergency Admin role has a very limited set of actions that can be executed immediately, without a timelock. These actions are designed to let curators respond quickly to incidents and protect the solvency of the market.

***

### How to add an emergency admin?

Only one address can have Emergency Admin role. It is set at the moment of creating a Market Configurator.&#x20;

It can be configured in Curators' UI for the existing Market Configurator:

{% embed url="https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fpcj4vgsOuQfPmnWXPHll%2Fuploads%2FyB1SGnrMeYYJMUE6GDZf%2FScreen%20Recording%202025-12-16%20at%2013.00.15.mp4?alt=media&token=21e75cd4-93fc-480a-80fd-4cd1eef6e5a9" %}

***

### What are the available functions, its scope and impact?

<table><thead><tr><th width="162.6171875">Action</th><th width="136.76171875" align="center">New positions</th><th width="96.2265625" align="center">Borrow</th><th width="110.3984375" align="center">Withdraw</th><th width="126.99609375" align="center">Adapter call</th><th width="110.375" align="center">Liquidate</th></tr></thead><tbody><tr><td>Token Limit = 0<br><br><strong>Impact:</strong> Asset (Pool)</td><td align="center">❌</td><td align="center">⚠️</td><td align="center">✅</td><td align="center">✅</td><td align="center">✅</td></tr><tr><td>Forbid Adapter<br><br><strong>Impact:</strong> Adapter (CM)</td><td align="center">⚠️</td><td align="center">✅</td><td align="center">✅</td><td align="center">❌</td><td align="center">⚠️</td></tr><tr><td>CM debt limit = 0<br><br><strong>Impact:</strong> CM</td><td align="center">❌</td><td align="center">⚠️</td><td align="center">✅</td><td align="center">✅</td><td align="center">✅</td></tr><tr><td>Forbid borrowing<br><br><strong>Impact:</strong> CM</td><td align="center">❌</td><td align="center">❌</td><td align="center">✅</td><td align="center">✅</td><td align="center">✅</td></tr><tr><td>Set Main Feed<br><br><strong>Impact:</strong> Asset (Pool)</td><td align="center">✅</td><td align="center">✅</td><td align="center">⚠️</td><td align="center">⚠️</td><td align="center">⚠️</td></tr><tr><td>Forbid Token<br><br><strong>Impact:</strong> Collateral (CM)</td><td align="center">❌</td><td align="center">❌</td><td align="center">❌</td><td align="center">❌</td><td align="center">✅</td></tr><tr><td>Pause CM<br><br><strong>Impact:</strong> CM</td><td align="center">❌</td><td align="center">❌</td><td align="center">❌</td><td align="center">❌</td><td align="center">❌</td></tr><tr><td>Pause Pool<br><br><strong>Impact:</strong> Pool</td><td align="center">❌</td><td align="center">❌</td><td align="center">❌</td><td align="center">❌</td><td align="center">❌</td></tr></tbody></table>

***

### Emergency scenarios

<details>

<summary>Collateral token incident</summary>

* <mark style="background-color:$warning;">**Low severity**</mark> _<mark style="background-color:$warning;">(incident status is unclear)</mark>_
  * **Set token limit = 0** in Pool
    * Collateral exposure can't be increased
    * Existing positions operations are not limited
* <mark style="background-color:$danger;">**Medium severity**</mark> _<mark style="background-color:$danger;">(collateral behavior is unhealthy, but no immediate bad debt risk)</mark>_
  * **Forbid token** in Credit Manager
    * Collateral exposure can't be increased
    * Existing positions operations are limited
      * Operations which decrease HF are blocked (increase debt, withdraw collateral, swap into different collateral with lower LT)
      * Operations which increase balance of forbidden token are blocked
* <mark style="background-color:red;">**High severity**</mark> _<mark style="background-color:red;">(collateral poses risk to market solvency)</mark>_
  * **Pause** all Credit Managers which have exposure
    * No user-side operations are allowed
    * Only emergency liquidators can liquidate accounts

</details>

<details>

<summary>Price feed incident</summary>

#### **Overpricing token**

* **Feed price is higher than market price enough to block liquidations**\
  In cases when price feeds deviates from market price by more than liquidation premium, liquidations become unprofitable.
  * <mark style="background-color:$warning;">**Low severity**</mark> _<mark style="background-color:$warning;">(existing positions create no insolvency risks)</mark>_
    * Set **Token Limit = 0** in Pool to limit increasing exposure to Asset.
    * Consider creating a new Credit Manager with higher liquidation premium.
  * <mark style="background-color:red;">**High severity**</mark> _<mark style="background-color:red;">(existing positions create risk to market solvency)</mark>_
    * **Set Main Feed** of token to one that is closer to market value.
      * This action will reduce Health Factor of existing positions which may result in immediate liquidations.
      * If the new Main feed is equal to current Reserve feed, reserve feed will be automatically detached from token, which will block operations relying on Safe Price (Collateral withdrawals, Usage of adapters, Partial Liquidations).
* **Feed price is higher than market price enough to drain Pool**\
  In cases when price feeds higher than market price by more than 1/LT of a token, one can buy token on secondary market and borrow more than was the cost, repeating it until "buy" liquidity or the pool is exhausted.\
  \
  \&#xNAN;_This risk is mitigated if at least one of Main and Reserve feeds returns adequate value, as the token at risk will be priced at minimal price during collateral withdrawals._
  * <mark style="background-color:red;">**High severity**</mark>
    * **Forbid token** in Credit Manager
      * Collateral exposure can't be increased
      * Existing positions operations are limited (users can only fully close accounts)

</details>

<details>

<summary>External protocol incident</summary>

**An external contract that is used through Adapter may appear to be misconfigured, hacked or is a proxy contract having its implementation replaced for an unsafe one.**

Call **Forbid Adapter** for every Credit Manager which has the adapter allowed.

</details>

#### Emergency Methods Definitions

**Token‑Specific**

**`setTokenLimit(token, 0)`**

* **Impact Scope:** Pool
* Sets the quota limit for a token to zero.
* Users cannot increase quota in that token, meaning new exposure to collateral can't be created.
* Withdrawals, debt increases, and adapter calls for existing positions remain enabled.

**`forbidToken(token)`**

* **Impact Scope:** Credit Manager
* Highly _**Restricts allowed operations**_ for accounts.
  * Operations which decrease HF are blocked (increase debt, withdraw collateral, swap into different collateral with lower LT)
  * Operations which increase balance of forbidden token are blocked
* **Liquidations** are not impacted.

**Feed‑Specific**

**`setMainPriceFeed(token, feed)`**

* Switches the main price feed of a token to another feed pre‑approved in the Price Feed Store.
* Target feed must have been added at least 1 day earlier.
* **Side effects:**
  * If the new main feed equals the current reserve feed, the reserve feed is removed (token ends up with only one feed).
  * New main price may be low enough to trigger immediate liquidations of Credit Accounts.

**Adapter‑Specific**

**`forbidAdapter(adapter)`**

* Disables calls through a specific adapter.
* Prevents swaps on DEXes, vault deposits/withdrawals, etc.
* **Side effects:**
  * If the forbidden adapter highly contributes to some tokens' liquidity, forbidding it may break liquidations, since most of Gearbox's internal liquidators rely on allowed adapters for searching tokens' swap paths. External liquidators may or may not be affected.

**Pool‑Global**

**`pausePool(pool)`**

* Pauses pool‑level operations (deposit into pool, withdraw LP tokens)
  * Designed to be combined with Credit Manager pause to prevent bank runs in the most extremal scenarios.

**`setCreditManagerDebtLimit(cm, 0)`**

* Sets the Credit Manager debt limit to zero.
* Prevents new borrowing capacity from the pool into that CM. Existing positions are not affected.

**Credit Manager‑Global**

**`pauseCreditManager(cm)`**

* Pauses all Credit Manager operations.
  * Borrowing, withdrawing collateral, opening & closing credit accounts, performing adapter calls are blocked.
* Only whitelisted **Emergency Liquidators** can liquidate accounts.

**`forbidBorrowing(cm)`**

* Forbids opening new accounts in the CM.
* Prevents increasing debt in existing accounts.

**Loss Policy**

**`setAccessMode(mode)`**

* Adjusts who can execute liquidations which result in bad debt accrual.
* Modes must be documented (TBD).

**`setChecksEnabled(flag)`**

* Enables/disables specific safety checks within loss policy.
