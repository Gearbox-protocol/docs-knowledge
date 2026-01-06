# Pool (The Liquidity Vault)

The **Liquidity Pool** is the liquidity vault of the Gearbox market. It is a passive reservoir of capital (e.g., USDC, WETH) supplied by lenders.

While Credit Managers define _strategy_, the Pool defines _capacity_. It acts as a "Wholesale Bank," lending funds to various Credit Managers (Retail Branches) based on limits defined by the Curator.

### Core Architecture

#### 1. The Passive Vault (ERC-4626)

The Pool is designed to be simple and secure.

* **Deposit:** Lenders deposit the underlying asset (e.g., USDC).
* **Receipt:** The Pool issues **Diesel Tokens** (e.g., dUSDC). These are standard ERC-4626 vault shares that represent the lender's claim on the principal plus accrued interest.
* **Withdrawal:** Lenders can burn Diesel Tokens to redeem their underlying asset, provided there is unborrowed liquidity available.

#### 2. Risk Isolation (The "Branch" Model)

A single Pool can fund multiple Credit Managers. This is critical for risk management.

The Pool lends to **Credit Managers**, not users. The Curator sets a **Debt Ceiling** for each Manager.

* _Example:_ A $100M USDC Pool might allocate $10M limit for borrowing against an emerging and $90M to the liquid cash-like assets.
* _Result:_ Even if the risky strategy fails, the maximum loss is capped at $10M (10% of the pool).

### Curator Controls

As a Curator, you manage the Pool to balance **Yield** (for lenders) against **Risk** (from borrowers).

#### 1. Global Capacity

* **Total Borrow Cap:** The absolute maximum amount of assets that can be borrowed from the pool across all strategies combined.
* **Strategy Allocations:** You can throttle specific Credit Managers. If a new strategy is experimental, you can give it a small "Credit Line" (e.g., $1M) to test it before opening the floodgates.

#### 2. Interest Rate Model (IRM)

The Pool does not set a fixed rate. Instead, it uses an algorithmic **Interest Rate Model** based on utilization.

* **Low Utilization:** Low rates to encourage borrowing.
* **High Utilization:** High rates to incentivize repayments and attract new deposits.
* **The "Kink":** Curators configure an optimal utilization point (e.g., 85%) where the rate curve steepens sharply.

#### 3. Withdrawal Fees

* **Purpose:** To prevent "Mercenary Capital" from entering and exiting the pool rapidly to farm short-term incentives, destabilizing the utilization rate.
* **Configuration:** Typically set to 0%, but can be increased during periods of high volatility.

### Deep Dive

Now that you understand the source of capital, learn how the system prices that capital and manages risk.

#### 1. How is the Interest Rate calculated?

The cost of borrowing is dynamic. Learn about the "Kink," the "Base Rate," and how utilization drives the APY.

* [**See: Interest Rate Mechanics**](https://www.google.com/url?sa=E\&q=..%2F04-risk-and-economics%2Finterest-rate-mechanics.md)

#### 2. How does the system prevent bad debt?

The Pool is protected by the liquidation logic enforced by the Credit Managers.

* [**See: Liquidation Dynamics**](https://www.google.com/url?sa=E\&q=..%2F04-risk-and-economics%2Fliquidation-dynamics.md)

#### 3. How do I configure a Pool?

Ready to launch? Follow the step-by-step guide to deploying your own lending market.

* [**See: Create a Market**](https://www.google.com/url?sa=E\&q=..%2Fcuration-step-by-step%2Fcreate-a-market.md)
