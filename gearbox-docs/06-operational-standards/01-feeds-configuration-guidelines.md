[Copy]

:

:
###

1.
:

:

Review allowPriceFeed transactions.
:

Grab the token address and verify its price on a DEX aggregator (https://meta.matcha.xyz/)
:

If not tradable on aggregators, ask the proposer for the correct reference (e.g. Pendle UI for PTs, Curve UI for LP tokens, or the issuer's app for derivatives/vaults)
:

Zero price feed (always returns \$0) can be safely added to any token for compatibility.

2.
:

:

Pull feeds → 4 min staleness
:

Push feeds → Heartbeat + 15 min (Ethereum) / Heartbeat + 2 min (L2s & faster chains).

3.
:

:

Confirm verification on the chain's block explorer.

4.
:

:

Stablecoin feeds are capped by \$1.04 from above
:

PT feeds for dollar-pegged vaults are capped by \$1 from above

⚠️ If any of these criteria aren't met: don't sign, ask in chat for clarification.

------------------------------------------------------------------------

###

These Terms & Conditions define the minimum due‑diligence and neutral‑gatekeeping standards for IO signers when **adding, configuring, or allowing** price feeds in the **Price Feed Store (PFS)** on any supported EVM chain. The sole goal is to ensure that, **at the moment of signing**, every configured feed **returns an adequate market price for the intended token, normalized to 8 decimals**, and satisfies staleness / quality constraints.

> Scope explicitly excludes any market‑risk, business, or curation decisions. IO signers act only as neutral technical gatekeepers.

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

-
:

-
:

-
:

-
:

------------------------------------------------------------------------

###

**Signers must complete all checks below before approving the transaction.** If any check fails, **do not sign.**

####

1.
:

2.
:

####

1.
:

:

**CoinGecko** (or equivalent public index),
:

**Trusted DEX/aggregators** (Uniswap/Curve/Balancer; 1inch/Cow/Odos),
:

**Designated platforms** when public indexes are unavailable (e.g., **Pendle markets** for PTs; **Pyth Insights**; **Redstone App**; protocol UIs for ERC4626 vault exchange rate).

2.
:

####

1.
:

:

**Pull‑type feeds (e.g., Pyth/Redstone pull):** *recommended* `240s` (4 min) unless documented otherwise.
:

**External Aggregator feeds (push/heartbeat):** heartbeat **+ 15 min** (slower chains, e.g. Ethereum) or **+ 2 min** (faster chains, e.g. L2s).

####

1.
:

2.
:

------------------------------------------------------------------------

###

If **any** requirement in fails or is inconclusive, **do not sign any transactions**. Examples:

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

------------------------------------------------------------------------

##

Asset class is a pair of (token-specific features, price feed methodology) which defines the behavior of collateral in different market scenarios. The same token can have different risks for LPs/Borrowers if priced differently.

All of the tokens can be borrow-only or used as collaterals.

Consider cases of

-
:

-
:

Describe the policy of setting reserve feeds and aliased loss policy.

Take into account that pull feeds providers (pyth and especially redstone) can be less reliable than push

Some of the used feeds can be provided by token issuer itself (for example Resolv PoR, midas feeds etc.) and have no strict update frequency (we\'ve seen Resolv update PoR feeds 2 hours later than was initially stated)

1.
:

2.
:

:

stETH, tBTC etc

3.
:

:

Priced using ERC4626 feeds
:

Priced using composite feeds (prices can be market-based, exchange rate or PoR)

4.
:

:

TWAP-based pricing or deterministic feeds

5.
:

:

For the tokens having rate oracle or erc4626 vault attached in Curve or Balancer pools, oracle price appreciation is automatically displayed in virtual_price

6.
:

:

TWAP-based pricing or deterministic feeds

7.
:

:

Since delayed withdrawal tokens are not liquidatable, the most favorable setting is when the position\'s HF is high enough not to fall below 1 due to accrued debt while redemption is being processed. One of the ways to achieve it is to set reserve feed of withdrawal token to be lower than its Main feed by some percentage. This percentage will effectively enforce the minimal health factor for user to have to initiate delayed withdrawal. Reserve to main price discount of 2% will mean that user has to maintain HF above \~1.02 to initiate full withdrawal of his collateral.

: