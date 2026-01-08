# Guide for Asset Issuers

Most lending protocols treat complex DeFi asset like any other ERC-20 token. While this enables basic compatibility, it prevents enforcement of issuer-defined rules such as redemption, settlement, withdrawals, and deposits.

Gearbox is built differently. Credit is extended at the asset's protocol level, not just the token level. Credit Accounts interact directly with issuer contracts, allowing purpose-specific rules to be enforced by design.

## No DEX dependency

Gearbox is built to work with asset-specific on-chain logic. Credit Accounts interact directly with issuer contracts, ensuring leverage respects the asset’s native lifecycle by design.

This direct integration allows credit users to mint and redeem assets with borrowed capital, bypassing secondary markets like DEXes altogether. This is especially important for assets with longer redemption periods, as DEX liquidity is costly and ineffective there.

**As a result:**

* **Issuers save millions of dollars** for bootstrapping and subsidizing DEX liquidity
* **Users save months of yield** by always redeeming at face value instead of selling at discount

## Launch faster, focus on distribution

Traditional looping methods don’t suit leverage for novel assets. They fragment UX with multi-step, multi-protocol transactions and become highly capital-inefficient when redemption periods are long.

Most lending protocols require 5+ transactions across the lending platform and the asset issuer to take a leverage on asset, effectively limiting access to advanced on-chain users only.

#### Gearbox's Benefits:

* **Zero DEX Liquidity Required:** With Gearbox, leverage can go live on day one. It eliminates the need for DEX liquidity seeding, working at any size.
* **Improved distribution:** User can enter leveraged position in one transaction.
* **Capital savings worth months of yield:**
  * Save time up to **8 periods** of native redemption.
  * Capital requirements are reduced by **10x**.
  * Save fees equal to a **month of farming yield**.
* **Risk Control:** Automated deleverage reduces liquidation risk, capital stays in user-owned segregated wallet minimizing indirect exposure.

## Widest collateral support & direct DeFi integration

Credit Accounts accept nearly any on-chain position as collateral: LP tokens, staked assets, vault shares, and non-tokenized positions such as redemption receipts.

This expands TVL, deepens liquidity, and unlocks leveraged versions of your asset’s native strategies.

{% hint style="success" %}
_**If you want to grow your DeFi product, whether it’s an LRT, vault, or any other productive collateral, reach out to Gearbox to power it with Distribution-focused UX and capital-efficient execution.**_
{% endhint %}

## Case studies

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-target data-type="content-ref"></th><th data-hidden data-card-cover data-type="image">Cover image</th></tr></thead><tbody><tr><td><h3>P2P vault growth</h3><p>How P2P's mellow LRT has grown from 25k to 45k restaked wstETH</p></td><td><a href="../cases/case-study-mellow-x-p2p-lrt-growth-powered-by-gearbox.md">case-study-mellow-x-p2p-lrt-growth-powered-by-gearbox.md</a></td><td><a href="../.gitbook/assets/gearboxdocsmain.png">gearboxdocsmain.png</a></td></tr></tbody></table>

## Learn in details

<table data-view="cards"><thead><tr><th></th><th data-hidden data-card-cover data-type="image">Cover image</th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><h4>Direct redemptions</h4><p>Users save months of yield; Asset issuers - millions on DEX incentives</p></td><td><a href="../.gitbook/assets/gearboxdocscurate.png">gearboxdocscurate.png</a></td><td><a href="https://app.gitbook.com/s/viVygst6ymEvrLTl74w1/reference/direct-redemptions">Usecase: Direct Redemptions</a></td></tr><tr><td><h4>User-first execution</h4><p>Integrate leverage into product offering as if it were there by design</p></td><td><a href="../.gitbook/assets/gearboxdocsborrow.png">gearboxdocsborrow.png</a></td><td><a href="https://app.gitbook.com/s/viVygst6ymEvrLTl74w1/core-architecture/adapters-integrations">Adapters &#x26; Integrations</a></td></tr></tbody></table>
