# Business Model

Gearbox Protocol generates revenue through two channels: interest fees on borrowing activity and liquidation fees during risk events. The fee model is additive — protocol fees are charged on top of lender yield, not extracted from it. Curator economics are predictable, transparent, and enforced at the contract level.

## Interest Fee: Revenue from Borrowing

The Interest Fee is a percentage markup applied on top of the base borrowing rate. Lenders earn the full base rate plus quota rate; the fee is an additional cost borne by borrowers only.

### Formula

$$
Rate_{\text{Borrower}} = (Rate_{\text{Base}} + Rate_{\text{Collateral-specific}}) \times (1 + Fee_{\text{Interest}})
$$

### Example

With a 5% base rate (including any collateral-specific quota rate) and a 20% Interest Fee:

| Component | Rate | Recipient |
|-----------|------|-----------|
| Base + Quota Rate | 5.00% | Liquidity Providers |
| Interest Fee (5% × 20%) | 1.00% | Curator & DAO |
| **Total borrower cost** | **6.00%** | — |

The fee does not reduce lender yield. Liquidity providers earn 5.00% regardless of the fee level. The 1.00% markup is extracted entirely from the borrower.

## Revenue Split

All collected Interest Fees are split at the `TreasurySplitter` contract:

| Recipient | Default Share |
|-----------|--------------|
| Market Curator | 50% |
| Gearbox DAO | 50% |

This split is enforced on-chain. It is not discretionary — distribution follows the contract logic on every fee collection event.

**Implication for partners:** Curator revenue is a deterministic function of pool activity. Partners operating as curators can model revenue directly from pool utilization and fee parameters.

## Liquidation Economics

When a Credit Account becomes undercollateralized and is liquidated, two fee components are extracted from the borrower's remaining collateral:

| Component | Recipient | Purpose |
|-----------|-----------|---------|
| **Liquidation Premium** | Liquidator | Execution incentive — the "bounty" for calling `liquidateCreditAccount()` |
| **Liquidation Fee** | DAO & Curator | Protocol revenue from the liquidation event |

Separate (typically lower) fee and discount parameters apply to expired account liquidations versus undercollateralized liquidations.

**Revenue alignment:** The protocol earns more during periods of market stress (when liquidations are more frequent). This creates structural alignment — the protocol accumulates reserves precisely when solvency risk is highest.

---

**Related pages:**

- [Interest Rate Model](interest-rate-model.md) — How base rates are determined by pool utilization
- [Collateral Limits & Specific Rates](quota-controls.md) — How quota rates price asset-specific risk
- [Insurance & Solvency Reserves](insurance-and-solvency.md) — How revenue is retained as solvency buffer before distribution
- [Liquidation Process](liquidation-dynamics.md) — Full liquidation mechanics and fee flows
