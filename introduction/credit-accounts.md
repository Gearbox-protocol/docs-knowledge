# Credit Accounts

A Credit Account (`CreditAccountV3`) is an isolated smart contract deployed per borrower, holding both collateral and borrowed funds in a single on-chain address. This per-borrower isolation provides asset segregation (no collateral commingling between positions), operational flexibility, and native composability — external protocols see a standard wallet address, not a protocol abstraction.

---

## Account Isolation and Operations

Each borrower operates through a dedicated Credit Account. All interactions — opening, managing, and closing — route through `CreditFacadeV3` as batched `MultiCall[]` arrays:

- **`openCreditAccount()`** deploys a new account and executes an initial set of operations in one transaction.
- **`multicall()`** executes an arbitrary batch of operations (swaps, deposits, rebalances) against the account.
- **`closeCreditAccount()`** repays debt and returns remaining assets to the borrower.

Within a single `multicall`, the borrower can interact with any protocol supported by an **Adapter** — a lightweight contract that maps operations to audited function calls on external protocols (e.g., Uniswap, Curve, Aave). The adapter constrains which functions the Credit Account may call while the external protocol processes a standard transaction from the account's address.

---

## Solvency Enforcement

Gearbox enforces solvency with a **check-on-exit** model: the protocol does not validate intermediate states within a multicall batch. After the final operation completes, the Credit Manager computes the account's **Health Factor (HF)**:

> **HF = Total Weighted Value / Total Debt**

- **Total Weighted Value (TWV):** `Σ(Balance_i × Price_i × LT_i)` across all enabled collateral tokens. Prices are sourced from `PriceOracleV3`, which supports Chainlink, Pyth, Redstone, LP price feeds, bounded, and composite oracles with staleness checks and reserve feed fallback.
- **Total Debt:** Principal + base interest (from the pool's IRM) + quota interest (managed by `PoolQuotaKeeperV3`, which enforces per-token borrowing limits) + fees.

If HF ≥ 1, the transaction commits. If HF < 1, the entire transaction reverts atomically — no state change is written. This is enforced at the EVM level.

---

## Liquidation

Between transactions, market movements or oracle price updates can cause an account's HF to drop below 1 without any borrower action. When this occurs:

- **Anyone** can call `liquidateCreditAccount()` on `CreditFacadeV3` — liquidation is permissionless.
  The liquidation call includes a `MultiCall[]` parameter, allowing the liquidator to execute swaps or other operations to efficiently convert collateral during the liquidation process.
- The liquidator receives a **liquidation premium** (defined as 1 minus the liquidation discount). The protocol treasury takes a separate fee.
- **Partial liquidation** is also available via `partiallyLiquidateCreditAccount()`, reducing debt without fully closing the position.

---

## Risk Disclosures

⚠️ **Smart contract risk.** Gearbox contracts are audited, but no audit eliminates all risk. Credit Accounts hold real assets governed by on-chain logic.

⚠️ **Oracle risk.** Price feeds may experience staleness or deviation. `PriceOracleV3` implements staleness checks with reserve feed fallback, but oracle failure or lag can result in delayed or incorrect valuations.

⚠️ **Liquidation risk.** An account's HF can decline between transactions due to market movements, oracle updates, or accruing interest — making the position liquidatable without any borrower action.

---

## Further Reading

- [Credit Suite](../core-architecture/credit-suite.md) — Health Factor calculation mechanics, liquidation threshold parameters, and Credit Manager internals.
- [Adapters & Integrations](../core-architecture/adapters-integrations.md) — Adapter security model, supported protocols, and integration architecture.
- [Pools](../core-architecture/pool.md) — Liquidity supply, interest rate models, and the quota system.
