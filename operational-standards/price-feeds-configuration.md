# Price feeds' configuration

The feeds configurations are reviewed at [https://safe.gearbox.finance/](https://safe.gearbox.finance/). It requires CID of txs file uploaded to IPFS.

<figure><img src="../.gitbook/assets/image (4).png" alt=""><figcaption></figcaption></figure>

#### TL;DR (Actionable checklist)

1. Txs simulation must pass. Click on Simulate button next to each batch to check.
2. Check the displayed price in the multisig UI to adequatly match current market values
   1. Review allowPriceFeed transactions.
   2. Grab the token address and verify its price on a DEX aggregator ([https://meta.matcha.xyz/](https://meta.matcha.xyz/))
   3. If not tradable on aggregators, ask the proposer for the correct reference (e.g. Pendle UI for PTs, Curve UI for LP tokens, or the issuer’s app for derivatives/vaults)
   4. Zero price feed (always returns $0) can be safely added to any token for compatibility.
3. Check staleness period of the feed
   1. Pull feeds → 4 min staleness
   2. Push feeds → Heartbeat + 15 min (Ethereum) / Heartbeat + 2 min (L2s & faster chains).
4. Check that the feed contract is verified
   1. Confirm verification on the chain’s block explorer.
5. Check that feeds are adequately capped from above:
   1. Stablecoin feeds are capped by $1.04 from above
   2. PT feeds for dollar-pegged vaults are capped by $1 from above
6. If the feed is deployed from external factory, it should use no Pull feeds as underlying feeds of factory deployment.

⚠️ If any of these criteria aren’t met: don’t sign, ask in chat for clarification.

✅ For a setLimiter transactions it's enough to check that simulation passes. This action updates exchange rate bounds of LP price feeds, and its correctness is checked on a contract level.

***

#### 1) Purpose & Scope

These Terms & Conditions define the minimum due‑diligence and neutral‑gatekeeping standards for IO signers when **adding, configuring, or allowing** price feeds in the **Price Feed Store (PFS)** on any supported EVM chain. The sole goal is to ensure that, **at the moment of signing**, every configured feed **returns an adequate market price for the intended token, normalized to 8 decimals**, and satisfies staleness / quality constraints.

> Scope explicitly excludes any market‑risk, business, or curation decisions. IO signers act only as neutral technical gatekeepers.

***

#### 2) Authority, Membership & Neutrality (summary)

* **Authority (PFS):** IO may add/remove feeds; set staleness period; attach/detach feeds to tokens; and run feed configuration calls required by integrated providers.
* **Neutrality:** IO remains **business-neutral**. Decisions must be based **only on objective technical criteria** below. All valid, safe requests should be processed in a reasonable timeframe.
* **Non‑interference with markets:** PFS changes **do not alter behavior of existing Markets by themselves** and **are not auto‑applied** to them.

***

#### 3) Definitions & Expectations

* **Price Feed Store (PFS):** Chain‑specific registry of tokens and feeds. A token can be used as collateral only after its token entry and at least one allowed feed are present.
* **8‑decimal normalization:** All effective Gearbox price feeds **must return USD‑denominated prices with 8 decimals** (`1e8` scale). Signers should verify output scale when checking a feed.
* **Staleness Period:** Maximum allowed time since last update before a feed is considered stale and reverts/invalidates.
* **Adequate market price:** A price reasonably close to reputable sources at the time of signing.

***

#### 4) Pre‑Signing Due‑Diligence (hard requirements)

**Signers must complete all checks below before approving the transaction.** If any check fails, **do not sign.**

**4.1 Contract & Deployment**

1. **Feed contract is verified** on a reputable explorer (Etherscan/chain explorer).
2. If the feed is not external, it must be deployed from Bytecode Repository.

**4.2 Price Output & Decimals**

1. **Price sanity:** Read the feed (via explorer read panel, provider dashboard, or PFS UI). The value must be **within a reasonable range** of one or more of:
   1. **CoinGecko** (or equivalent public index),
   2. **Trusted DEX/aggregators** (Uniswap/Curve/Balancer; 1inch/Cow/Odos),
   3. **Designated platforms** when public indexes are unavailable (e.g., **Pendle markets** for PTs; **Pyth Insights**; **Redstone App**; protocol UIs for ERC4626 vault exchange rate).
2. **Decimals:** Confirm that the effective price value is **normalized to 8 decimals**.

**4.3 Staleness**

1. **Staleness period** must be reasonable for the source and chain:
   1. **Pull‑type feeds (e.g., Pyth/Redstone pull):** _recommended_ `240s` (4 min) unless documented otherwise.
   2. **External Aggregator feeds (push/heartbeat):** heartbeat **+ 15 min** (slower chains, e.g. Ethereum) or **+ 2 min** (faster chains, e.g. L2s).

**4.4 Asset‑Specific Parameters (when applicable)**

1. **Stablecoin‑to‑USD feeds:** The observed price should be **bounded from above at 1.04**.
2. **Pegged assets feeds (LST-to-ETH, LRT-to-BTC, cbBTC-to-BTC etc.):** The observed ratio should be **bounded from above at 1.04**.

***

#### 5) Refusal Policy

If **any** requirement in fails or is inconclusive, **do not sign any transactions**. Examples:

* Contract not verified;
* Output not 8‑decimals normalized;
* Price materially diverges from reputable venues;
* Staleness period unreasonable for the source/chain;
* Asset‑specific parameters missing/incorrect.

***

### Asset classes

Asset class is a pair of (token-specific features, price feed methodology) which defines the behavior of collateral in different market scenarios. The same token can have different risks for LPs/Borrowers if priced differently.

All of the tokens can be borrow-only or used as collaterals.

\
Consider cases of

* Correlated debt/collateral pairs
* Volatile debt/collateral pairs

Describe the policy of setting reserve feeds and aliased loss policy.

Take into account that pull feeds providers (pyth and especially redstone) can be less reliable than push

Some of the used feeds can be provided by token issuer itself (for example Resolv PoR, midas feeds etc.) and have no strict update frequency (we've seen Resolv update PoR feeds 2 hours later than was initially stated)

1. Stablecoins/ synthetic dollars\
   USDT, USDe, USDai, DAI, USDf etc.
2. ETH or BTC equivalents
   1. stETH, tBTC etc
3. Yield-bearing vaults\
   Stream.finance xUSD, Midas vaults, tETH, LRTs etc.
   1. Priced using ERC4626 feeds
   2. Priced using composite feeds (prices can be market-based, exchange rate or PoR)
4. Pendle PT tokens
   1. TWAP-based pricing or deterministic feeds
5. Curve, Balancer LP tokens
   1. For the tokens having rate oracle or erc4626 vault attached in Curve or Balancer pools, oracle price appreciation is automatically displayed in virtual\_price
6. Pendle LP tokens
   1. TWAP-based pricing or deterministic feeds
7. Delayed withdrawal phantom tokens
   1. Since delayed withdrawal tokens are not liquidatable, the most favorable setting is when the position's HF is high enough not to fall below 1 due to accrued debt while redemption is being processed.\
      \
      One of the ways to achieve it is to set reserve feed of withdrawal token to be lower than its Main feed by some percentage. This percentage will effectively enforce the minimal health factor for user to have to initiate delayed withdrawal.\
      \
      Reserve to main price discount of 2% will mean that user has to maintain HF above \~1.02 to initiate full withdrawal of his collateral.
