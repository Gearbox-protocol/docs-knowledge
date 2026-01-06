# Dual-oracle system

## **Why does it matter?**

Oracles are crucial for determining collateral value in lending protocols. Unlike simple exchanges (e.g., Uniswap), lending protocols rely heavily on external data. Risks include:

* **Node compromise:** Hackers could gain control of oracle nodes, submitting incorrect data. Popular oracles often rely on 4-5 nodes, selecting median values; compromising 2 or 3 of them can significantly distort reported prices.
* **Thin liquidity manipulation:** Oracles aggregate prices from various trading sources (DEXes, CEXes). In cases of low liquidity and infrequent trades, malicious actors can temporarily inflate asset prices. For example, manipulating a short-duration TWAP (e.g., 4 minutes) can lead to artificially high collateral valuations, as recently observed with Chainlink.

## How Gearbox improves collateral pricing

Gearbox operates with 2 feeds for each collateral: _**Main**_ feed and _**Reserve**_ one.\
Main feed is used for for Account Value calculation during Liquidation checks.

Reserve oracles provide an additional security layer to protect liquidity providers (LPs) from oracle manipulation risks, ensuring accurate collateral valuations.

Reserve oracle is used during collateral checks in multicalls, which is a mechanism to perform complex defi interactions from credit accounts in single transaction.

In particular, **Reserve** price feed is involved when the multicall includes **Collateral Withdrawal** or **External Calls** through adapters. The collateral check after such operations prices each collateral using the Safe Price:

$$
Safe\ Price = min(Main\ Feed\ Price, Reserve\ Feed\ Price)
$$

## Dual-oracle pricing in DeFi context

### Pricing methodologies

There are two main methodologies of pricing tokens that is used in most of the lending markets:

* **Hardcoded/ Fundamental/ Backing Value/ Exhange Rate**\
  It has multiple names, but the basic idea is to price the token based on reserves that back it
* **Secondary market price**\
  Price at which token is bought and sold on DEXes, CEXes or any other liquid market.

<table><thead><tr><th width="163.31640625">Feed type</th><th width="265.55859375" valign="top">Pros</th><th valign="top">Cons</th></tr></thead><tbody><tr><td>Hardcoded Fundamental<br>Backing Value Exhange Rate</td><td valign="top"><strong>Borrowers:</strong><br>- Minimal risks of liquidation<br>- Up-to-date reflection of staked collateral price appreciation<br><strong>Lenders:</strong><br>- Resistant to market manipulation, important for illiquid tokens</td><td valign="top"><strong>Lenders:</strong><br>- Possible overpricing during hacks and market turmoils<br>- Deposited funds can be freezed in pool due to lack of incentives for repayment or liquidation</td></tr><tr><td>Secondary market price</td><td valign="top"><strong>Lenders:</strong><br>- Pessimistic pricing (liquid tokens usually trade at discount to their backing value)<br>- Fast reaction to real market drops</td><td valign="top"><strong>Borrowers:</strong><br>- Less capital-efficient: have to maintain higher HF to avoid liquidations<br>- Can cause cascading liquidations<br><strong>Lenders:</strong><br>- Illiquid collateral markets can be manipulated to drain pool reserves at inflated price<br>- Liquidation cascades can lead to overselling and creation of bad debt on liquidations</td></tr></tbody></table>

### Dual-Oracle system: best of both worlds

Let's compare how properly configured **Main** and **Reserve** feeds can protect lenders while preserving exceptional UX and capital efficiency for borrowers by studying multiple market cases. In the table below, the case when some collateral token is used to borrow blue-chip stablecoin such as USDC.

| Scenario                                                                      | Dual-Oracle system                                                                                                                                                                                                        | Hardcoded feed                                                                                                                                                             | Market feed                                                                                                                                                                                 |
| ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| sUSDe/USD market price drops by >2.5%                                         | ✅ No liquidations of existing positions                                                                                                                                                                                   | ✅ No liquidations of existing positions                                                                                                                                    | ⚠️ Risky positions liquidated                                                                                                                                                               |
| <p>(paranoid)<br>USDe/USD market price drops by >10%</p>                      | <p>⚠️ No liquidations of existing positions<br><br>✅ Safe price = min(market, hardcoded) = $0.9<br><br>✅ Can borrow $0.915 per USDe, but can't withdraw it from credit account ⇒ liquidity doesn't exit the protocol.</p> | <p>⚠️ No liquidations of existing positions<br><br>🚨 Attack vector:<br>- buy at $0.9<br>- borrow $0.915 at max LTV (e.g. 91.5%)<br>TVL lent is used as exit liquidity</p> | 🚨Major part of positions liquidated                                                                                                                                                        |
| deUSD/USD market price pumps by >2.5%                                         | ✅ No liquidations of existing positions                                                                                                                                                                                   | ✅ No liquidations of existing positions                                                                                                                                    | ✅ No liquidations of existing positions                                                                                                                                                     |
| <p>(illiquid market manipulation)<br>deUSD/USD market price pumps by >10%</p> | <p>✅ No liquidations of existing positions<br><br>✅ Can borrow $1.02 per deUSD, but can't withdraw it from credit account ⇒ liquidity doesn't exit the protocol.</p>                                                      | ✅ No liquidations of existing positions                                                                                                                                    | <p>✅ No liquidations of existing positions</p><p>🚨 Attack vector:<br>- mint deUSD at $1<br>- borrow $1.02 at max LTV (e.g. 92.5%)</p><p><br>TVL lent drained due to inflated valuation</p> |
