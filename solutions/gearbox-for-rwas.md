[MODE=PRODUCT]

# Gearbox for RWAs

## Gearbox: The Premier Prime Brokerage for RWA Leverage

Gearbox is the definitive platform for leveraging Real-World Assets (RWA). Fully live since December 2021 , Gearbox offers a seamless, all-in-one prime brokerage experience, right from your favorite wallet. It is easy to manage and easy to track.

## Addressing Core Inefficiencies in RWA Leverage

Traditional looping methods are inefficient for leverage. Gearbox solves critical issues faced by both asset issuers and users.

## For Asset Issuers: Eliminate Costly DEX Dependence

Other lending protocols must treat Real-World Assets (RWA) like standard tokens and rely on DEX liquidity to enable looping. Building and maintaining deep DEX liquidity is slow and expensive, leading to thin books, low collateral limits, and unhappy users. Furthermore, asset issuers often have to pay to seed and maintain DEX liquidity.

### Gearbox's Solution:

- **Zero DEX Liquidity Required:** With Gearbox, leverage can go live on day one. It eliminates the need for DEX liquidity seeding, working at any size.  
- **Direct Integration:** Leverage works via direct smart contract integration, allowing 1:1 deposits and withdrawals at face value.  
- **Compliance Enforcement:** It is almost impossible to enforce transfer-agent/compliance obligations on-chain in traditional pools-based lendings. Gearbox is designed for compliant, credit-account access.

## For Users: Superior UX and Performance

Users typically suffer slippage every time they open or close a leveraged position. Adjusting leverage is a trade-off between committing more capital and waiting longer. Additionally, funds are often mixed up in pools , which is problematic from a regulatory standpoint.

### Gearbox's Benefits:

- **Zero Slippage:** Enjoy direct interaction with contracts and 1:1 assets, resulting in zero slippage.  
- **Best-in-Class UX:** Offers one-click opening and closing of leveraged positions.  
- **Risk Control:** Features flexible deleveraging settings to reduce liquidation risk , plus built-in automation and risk controls - no external bots or tooling needed.

## Compliant Credit Accounts by Design

Gearbox provides a robust framework for compliance and regulatory clarity:

- **Position Isolation:** Each user's position is fully isolated, preventing the mixing of assets or risk between accounts.  
- **Access Control:** Supports KYC- and rules-based access control, including per-account whitelists, jurisdiction filters, and configurable limits.  
- **On-Chain Enforcement:** Built-in position freezing and granular operation controls (what can be traded, where, and when) allows curator to enforce regulatory obligations on-chain.

## Direct Redemptions for Semi-Liquid Assets

Direct redemptions address the challenge of low instant liquidity for collateral tokens by utilizing Gearbox's unique Credit Account structure to bypass expensive, time-locked, or low-liquidity secondary markets.

### Benefits of Direct Redemption:

- Save time up to 8 periods of native redemption in comparison with manual unwinding looped positions  
- Capital requirements are reduced by 10x.  
- User saves fees equal to a month (or even more) of farming yield.

## How It Works

- The Credit Account holds an xRWA token and has an outstanding USDT debt.  
- The user starts the redemption process.  
- The Credit Account sends the xRWA token to the redemption contract.  
- In return, the Credit Account receives a redemption receipt token, which represents a future claim on the underlying asset.  
- The Credit Account now holds the redemption receipt token and still has the USDT debt.  

### After the Redemption Window:

- Once the redemption window has passed, the user can finalize the redemption.  
- The Credit Account burns the redemption receipt token.  
- The Credit Account receives the underlying asset.  
- The Credit Account always stays overcollateralized, it's just the collateral which transfrom from xRWA into redemption receipt token and eventually into liquid underlying.
