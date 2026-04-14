# Pools

PoolV3 is the central vault for a specific underlying asset (e.g., USDC, WETH). It follows the ERC-4626 tokenized vault standard, allowing users to deposit assets and receive Diesel Tokens (LP tokens) representing their share.

## Core Design Principles

Unlike standard lending protocols, users do not borrow directly from the pool. Instead, whitelisted Credit Managers borrow liquidity on behalf of Credit Accounts to execute leveraged strategies.

This separation ensures:

* All borrowed funds flow through Credit Accounts with proper collateral checks
* Lenders earn passive yield without exposure to leverage decisions
* Risk is isolated at the Credit Manager level

## ERC-4626 Compliance

PoolV3 implements the full ERC-4626 tokenized vault standard. Any tooling built for ERC-4626 vaults works with Gearbox pools.

**Standard Functions:**

| Function                            | Purpose                                    |
| ----------------------------------- | ------------------------------------------ |
| `deposit(assets, receiver)`         | Deposit underlying, receive shares         |
| `mint(shares, receiver)`            | Mint exact shares, deposit required assets |
| `withdraw(assets, receiver, owner)` | Withdraw exact assets, burn shares         |
| `redeem(shares, receiver, owner)`   | Burn exact shares, receive assets          |
| `convertToShares(assets)`           | Preview shares for asset amount            |
| `convertToAssets(shares)`           | Preview assets for share amount            |

**Gearbox Extensions:**

| Function              | Purpose                          |
| --------------------- | -------------------------------- |
| `depositWithReferral` | On-chain referral tracking       |
| `lendCreditAccount`   | Credit Manager-only borrowing    |
| `repayCreditAccount`  | Credit Manager-only repayment    |
| `dieselRate()`        | Share price in RAY (27 decimals) |

## Diesel Rate (Share Price)

The diesel rate represents how many underlying tokens each diesel token (share) is worth. It starts at 1 RAY (10^27) and increases as interest accrues.

**Calculation:**

* 1 diesel token = dieselRate / 10^27 underlying tokens
* The rate grows over time as borrowers pay interest
* Lenders profit as their shares become worth more underlying

## Yield Sources

Lenders provide liquidity to earn passive yield from two sources:

1. **Base Interest:** Paid by borrowers on the principal debt
2. **Quota Revenue:** Paid by borrowers for the right to hold specific collateral tokens

The combined yield is reflected in the `supplyRate()` function.

## Withdrawal Mechanics

Withdrawals in Gearbox V3 are subject to a withdrawal fee. This fee is taken from the interest earned, keeping the capital principal intact when possible.

**Key considerations:**

* Withdrawals revert if the pool is paused
* Available liquidity limits maximum withdrawal
* Fee calculation happens automatically during redeem/withdraw

## Credit Manager Interaction

Only whitelisted Credit Managers can borrow from the pool:

| Function                                   | Access  | Purpose          |
| ------------------------------------------ | ------- | ---------------- |
| `lendCreditAccount(amount, creditAccount)` | CM only | Borrow from pool |
| `repayCreditAccount(repaid, profit, loss)` | CM only | Repay to pool    |

Regular users cannot call these functions. All borrowing flows through the Credit Suite.

## Pool State

Key state variables for monitoring pool health:

| Field                | Description               |
| -------------------- | ------------------------- |
| `totalAssets`        | Total value held by pool  |
| `availableLiquidity` | Borrowable amount         |
| `dieselRate`         | Current share price (RAY) |
| `supplyRate`         | Lender APY (RAY)          |
| `baseInterestRate`   | Borrower APR (RAY)        |

## Interest Rate Determination

The pool does not store interest rate logic. It queries the Interest Rate Model (IRM) whenever state changes. See the Interest Rate Model reference for the utilization curve mechanics.

## Implementation

For implementation details, see:

* **TypeScript/SDK:** [Reading Data](../sdk-guide-typescript/reading-data.md)
* **Solidity:** [Pool Operations](../solidity-guide/pool-operations.md)
