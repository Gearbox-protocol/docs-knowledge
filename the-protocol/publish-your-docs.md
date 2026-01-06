---
layout:
  width: default
  title:
    visible: true
  description:
    visible: true
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: true
  metadata:
    visible: true
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/yE16Xb3IemPxJWydtPOj/getting-started/publish-your-docs
---

# Credit Accounts

> Credit Accounts are user-owned smart-contract wallets. Add collateral to unlock a credit line and use that account to trade, invest, or stake across integrated protocols while keeping ownership and portability. The protocol checks solvency on every move so risk stays controlled.

## Fragmented UX vs. Wallet-Native Credit

**Pool-based lending**

Traditional lending protocols silo users' funds in protocol-global pools, limiting capabilities to actively operate with collateral.

<figure><img src="../.gitbook/assets/legacy-lending.png" alt=""><figcaption></figcaption></figure>

**Credit Accounts**

By putting collateral, debt, and execution routes inside a single smart contract wallet, users keep ownership while moving through swaps, farming, or RWA flows without repacking positions. Solvency checks sit behind every action so convenience stays aligned with risk controls.

<figure><img src="../.gitbook/assets/ca-lending.png" alt=""><figcaption></figcaption></figure>

### What Credit Accounts enable

* **Wider reach to users for apps and institutions:** Complex multi-transaction operations gate non-professional users. Credit accounts abstract execution allowing to focus on effective use of capital.
* **Fees and time saving for investors:** Direct redemptions of semi-liquid tokens preserve months of yield, and batched transactions cut gas cost.
* **Largest set of supported collaterals:** redemption receipts or Convex-staked positions become usable in a non-custodial, programmable account instead of being limited to prime broker clients.

### Architecture & Safety

While the Credit Account provides the user experience, the safety is enforced by the underlying infrastructure.

#### 1. How is solvency enforced?

The **Credit Manager** is the "Brain" of the system. It checks every transaction against the Oracle prices and Liquidation Thresholds defined by the Curator. If an action would make the account insolvent, it reverts.

* [**Learn how Credit Managers enforce risk compliance**](../core-architecture/credit-suite-the-strategy-module.md)

#### 2. How do I interact with DeFi?

Credit Accounts cannot talk to arbitraty external protocols (like Uniswap or Lido) directly due to security reasons. They use **Adapters:** specialized connectors that translate user intent into safe, protocol-compliant transactions.

* [**Learn how Adapters enable composability**](../core-architecture/adapters-purpose-specific-execution-rules.md)

#### 3. Where does the liquidity come from?

Credit Accounts borrow funds from **Liquidity Pools**. These pools are passive reservoirs of capital (e.g., USDC, ETH) supplied by lenders. The cost of this capital is determined by the Interest Rate Model and can be adjusted for specific collateral types.

* [**Learn about Pools**](https://www.google.com/url?sa=E\&q=..%2Fgearbox-permissionless%2Fgearbox-markets%2Fpool-the-liquidity-vault.md)
