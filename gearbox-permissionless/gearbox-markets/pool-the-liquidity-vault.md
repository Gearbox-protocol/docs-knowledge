# Pool (The Liquidity Vault)

## Pool (The Liquidity Vault)

The Pool serves as the secure reservoir for the market's liquidity. It is a passive contract where lenders deposit assets to earn yield without managing individual loan risks.

#### Core Functions:

* Capital Container: It holds the underlying assets and issues "Diesel Tokens" (lpTokens) to lenders as a receipt of their deposit.
* Risk Isolation: It enforces strict debt ceilings for each connected Credit Manager. Think of the Pool as a wholesale bank and the Credit Managers as retail branches that handle specific loan strategies.\
  This ensures that a single high-risk strategy cannot drain all the market's available liquidity.
* Integration Ready: It adheres to the ERC-4626 standard, making it fully composable for other protocols to build yield products on top of it.

#### Curator Controls

* Global Borrow Cap: Sets the absolute maximum amount of assets that can be borrowed from the pool across _all_ strategies combined. Curators use this to cap the total protocol exposure to the underlying asset.
* Strategy Allocations: Defines the maximum credit line for each specific Credit Manager. Curators use this to throttle growth for riskier strategies while allowing more capital for safer ones.
* Withdrawal Fee: Configures a fee charged when lenders remove liquidity. While typically set to 0%, Curators can increase this during periods of high volatility to discourage mercenary capital rotation.
