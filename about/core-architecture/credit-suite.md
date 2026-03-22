# Credit Suite

The Credit Suite is the three-contract assembly that defines, executes, and governs a lending strategy in Gearbox. It consists of the **Credit Manager** (accounting and solvency), the **Credit Facade** (user entry point), and the **Credit Configurator** (administrative controls).

This page covers each component's role, integration touchpoints, and the end-to-end interaction flow — information required to evaluate integration fit, build on the Credit Suite interface, or operate a market.

---

## What a Credit Suite Is and Why It Is Three Contracts

A Credit Suite is an isolated lending strategy with unique collateral assets, borrowing limits, and liquidation thresholds. Multiple Credit Suites connect to one Pool, each with independent risk configurations.

This is the architectural implementation of "One Pool, Many Markets." The Pool supplies undifferentiated capital; each Credit Suite shapes it into a distinct credit product. Risk stays compartmentalized per Suite without fragmenting underlying liquidity.

Separating the Suite into three contracts enforces separation of concerns:

- **Configuration** is decoupled from **execution**, which is decoupled from **accounting**.
- Each contract has a defined responsibility and a restricted interface.
- Changes to risk parameters (Configurator) cannot bypass the accounting engine (Manager), and user operations (Facade) cannot bypass solvency checks (Manager).

---

## Credit Manager: Accounting and Solvency

The Credit Manager is the central state container for a lending strategy. It tracks all Credit Accounts, their debts, and their collateral values.

### What It Holds

- **Account ledger.** Every Credit Account associated with this strategy — ownership, debt amounts, enabled collateral tokens.
- **Adapter registry.** The list of approved Adapters (external protocol integrations) that accounts in this Suite can interact with.
- **Token allowlist.** The set of assets that can be held as collateral within Credit Accounts.
- **Solvency math.** The Health Factor calculation: `HF = TWV / Total Debt`, where TWV is the sum of each collateral token's balance × oracle price × Liquidation Threshold.

### Key Functions (Integrator Reference)

| Function | Purpose |
|---|---|
| `getBorrowerOrRevert(address creditAccount)` | Returns the owner address of a Credit Account |
| `enabledTokensMaskOf(address creditAccount)` | Returns a bitmask of enabled collateral tokens |
| `calcDebtAndCollateral(address creditAccount, CollateralCalcTask task)` | Full debt and collateral valuation |
| `isLiquidatable(address creditAccount, uint16 minHealthFactor)` | Health check — returns whether the account is liquidatable |
| `liquidationThresholds(address token)` | Returns the Liquidation Threshold for a specific collateral token |

The Credit Manager is the primary data source for liquidation bots, dashboards, and risk monitors.

---

## Credit Facade: User and Bot Entry Point

The Credit Facade is the single entry point for all borrower operations. Borrowers and bots never call the Credit Manager directly.

### Multicall Execution

Operations are bundled into atomic multicalls. A borrower can `borrow`, `swap`, and `deposit_into_vault` in a single transaction. The Facade processes the entire bundle, then requests a solvency check from the Credit Manager before committing.

### Check-on-Exit Solvency

The Facade implements Gearbox's optimistic execution model:

1. The borrower submits a multicall containing any sequence of whitelisted operations.
2. The Facade executes all operations without intermediate solvency checks.
3. At the end of the multicall, the Facade requests the Credit Manager to compute the Health Factor.

| Outcome | Result |
|---|---|
| HF > 1 | State changes committed on-chain |
| HF < 1 | Entire transaction reverts — no state change |

**Health Factor computation uses Total Weighted Value (TWV)**, not raw market value. TWV discounts each asset by its Liquidation Threshold (LT). Example: $100 of ETH with a 90% LT contributes $90 to the solvency calculation.

### Permissions

Only the account owner can initiate transactions affecting a specific Credit Account. Bot access is available through `botMulticall()`, which operates within safety constraints defined by the account owner.

### Key Entry Points (Integrator Reference)

| Function | Purpose |
|---|---|
| `openCreditAccount(address onBehalfOf, MultiCall[] calls, uint256 referralCode)` | Opens a new Credit Account with initial operations |
| `closeCreditAccount(address creditAccount, MultiCall[] calls)` | Closes an account after repaying debt |
| `multicall(address creditAccount, MultiCall[] calls)` | Batch operations on an existing account |
| `botMulticall(address creditAccount, MultiCall[] calls)` | Authorized bot operations within owner-defined constraints |
| `liquidateCreditAccount(address creditAccount, address to, MultiCall[] calls, bytes lossPolicyData)` | Full liquidation of an undercollateralized or expired account |
| `partiallyLiquidateCreditAccount(...)` | Partial liquidation — repay a portion of debt, seize discounted collateral |

---

## Credit Configurator: Curator Risk Management

The Credit Configurator is the administrative layer where Market Curators adjust risk parameters. Curators interact with the Configurator, never with the Credit Manager directly.

### What It Does

- **Parameter validation.** The Configurator validates inputs before applying changes to the Credit Manager. Invalid states (e.g., Liquidation Threshold > 100%) are rejected at the Configurator level.
- **Timelock enforcement.** Critical parameter changes enforce mandatory delays. Borrowers and lenders have time to evaluate changes and adjust positions before new parameters become active.
- **Interest rate model updates.** Curators can replace the Interest Rate Model via the Configurator — the old model is deauthorized and the new model authorized in a single operation.

The Configurator is the Curator's primary operational interface. It makes market management possible without exposing the accounting engine to misconfiguration.

---

## How It All Fits Together

The end-to-end interaction flow across all three contracts:

1. **Configuration.** The Curator sets risk parameters (Liquidation Thresholds, debt limits, allowed collateral, adapter permissions) via the **Credit Configurator**.
2. **Execution.** The borrower submits a multicall transaction to the **Credit Facade**.
3. **Accounting.** The Facade routes instructions to the **Credit Manager**, which updates Credit Account state and interacts with the Pool (for borrowing/repaying) or Adapters (for external protocol interactions).
4. **Verification.** The Facade requests a final solvency check from the Credit Manager before committing the transaction.

Each concern — governance, execution, accounting — has its own contract. No single contract holds all authority.

---

## Learn More

- **How do liquidations work when HF drops below 1?** → Economics & Risk: Liquidation Dynamics
- **What is the complete list of configurable risk parameters?** → Reference: Risk Configuration Dictionary
- **How do adapters connect Credit Accounts to external protocols?** → [Adapters & Integrations](adapters-integrations.md)
- **Where does the borrowed capital come from?** → [Pool](pool.md)
