# Pool (The Liquidity Vault)

The **Liquidity Pool** is the central reservoir of capital for a Gearbox market. It is a passive smart contract where lenders deposit assets (e.g., USDC, WETH) to earn yield.

While Credit Managers define the _strategy_ (how funds are used), the Pool defines the _capacity_. It acts as a "Wholesale Bank," lending funds to various Credit Managers (Retail Branches) based on limits defined by the Curator.

## Core Aspects

### **1. The Passive Vault (ERC-4626) & Yield Mechanics**

The Pool is designed to be simple and secure. It follows the ERC-4626 standard for tokenized vaults.

* **Deposit:** Lenders deposit the underlying asset (e.g., USDC).
* **Receipt (Diesel Tokens):** The Pool issues **Diesel Tokens** (e.g., dUSDC). These represent the lender's pro-rata share of the pool.
* **Yield Accrual:** Diesel Tokens are **non-rebasing**. The quantity of tokens in the user's wallet does not change. Instead, the **Exchange Rate** increases over time as borrowers pay interest into the pool.
  * _Formula:_ `Exchange Rate = Total Assets (Principal + Interest) / Total Supply of dTokens`
* **Withdrawal:** Lenders burn Diesel Tokens to redeem their underlying asset plus the accrued interest, provided there is unborrowed liquidity available in the pool.

### **2. Risk Isolation (The "Branch" Model)**

A single Pool can fund multiple Credit Managers. This is critical for risk management.

The Pool lends to **Credit Managers**, not directly to users. The Curator sets a **Debt Ceiling** for each Manager.

* _Example:_ A $100M USDC Pool might allocate a $10M limit to a higher-risk "Emerging Asset Strategy" and $90M to a lower-risk "Blue Chip Strategy."
* _Result:_ Even if the risky strategy fails, the maximum loss for the Pool is capped at $10M (10% of the pool). The remaining capital is isolated from that specific risk

### Curator Controls — Lenders' Risk and Return

The primary role of the Market configuration is to define the risk profile for the Liquidity Providers (LPs). Since LPs cannot choose which specific borrowers they fund, they rely on the Curator to set the limits defining the aggregate exposure.

By adjusting the **Borrow Caps** for each connected Credit Manager, the Curator determines the blend of the portfolio:

* **Conservative Profile:** Allocating the majority of capital to Credit Managers with strict LTVs and blue-chip collateral. This results in lower risk but potentially lower utilization and yield.
* **Aggressive Profile:** Allocating more capital to Credit Managers allowing volatile assets or higher leverage. This increases the potential yield from borrowing fees but exposes LPs to higher risks.

For the exact list of configurable parameters and limits, refer to the specification page.

* [**See: Roles & Contract Specification**](https://www.google.com/url?sa=E\&q=roles-and-contract-level-specification.md)

### Deep Dive

#### 1. How is the total APY calculated?

Gearbox uses a composite rate model. The final cost to the borrower (and yield to the lender) is the sum of the base utilization rate plus any collateral-specific premiums.

* [**See: Interest Rate Model and Collateral-specific rates**](../economics-and-risk-controls/interest-rate-model-the-cost-engine.md)

#### 2. **What are the specific risks for Lenders?**

Lenders face distinct risks compared to borrowers, including liquidity risk (high utilization blocking withdrawals) and bad debt socialization.<br>

* See: [**Risks of Lenders**](https://www.google.com/url?sa=E\&q=risks-of-lenders.md)
