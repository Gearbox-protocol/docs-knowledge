# Insurance & Solvency Reserves

An automated on-chain reserve system absorbs bad debt before it affects lenders. The mechanism functions as a revenue retention buffer — the protocol withholds all fee revenue until the reserve reaches a defined safety floor. This page covers how the reserve accumulates, how it absorbs losses, how to verify its health on-chain, and what it does not cover.

## Revenue Retention Model

All protocol fees flow into the `TreasurySplitter` contract, which gates distribution against a target insurance amount.

1. **Revenue accumulates** — Interest fees and liquidation fees are collected in the TreasurySplitter
2. **Safety floor is checked** — A target insurance amount is defined per token (e.g., 100,000 USDC)
3. **Distribution is conditional:**
   - **Below target:** 100% of revenue is retained. No profits are distributed to DAO or Curators.
   - **Above target:** Only the surplus (amount exceeding the target) is distributed.

The protocol prioritizes solvency reserves over profit extraction. Revenue distribution resumes only after the insurance floor is fully funded.

### Asset Composition

The reserve is held in **LP shares** (Diesel Tokens) of the pool it insures, not in idle capital. This means:

- The insurance fund earns yield alongside other liquidity providers
- The Treasury's interests are aligned with lender interests
- Reserve value fluctuates with pool performance

## How Bad Debt Is Absorbed

Bad debt occurs when a liquidated Credit Account's collateral is insufficient to repay the pool. Without the reserve, this loss would reduce the LP token exchange rate (socializing the loss among all lenders).

### Coverage Flow

1. **Deficit identified** — A liquidation completes with a shortfall (e.g., Debt: 100k, Collateral: 98k, Deficit: 2k)
2. **Credit Manager reports loss** to the Pool
3. **Pool burns Treasury LP shares** equal to the deficit value

By burning the Treasury's shares, total LP share supply decreases while the underlying assets in the pool remain proportional to remaining lender claims. The Treasury "pays" by giving up its claim on pool liquidity — lenders are protected first.

## On-Chain Verification

Partners and market participants can audit the reserve health directly on-chain:

### Verify the Insurance Target (Safety Floor)

```
tokenInsuranceAmount(address token) → uint256
```

Returns the minimum reserve the protocol enforces before allowing profit distribution. This is the "water level."

### Verify Current Reserves (Actual Buffer)

```
IERC20(token).balanceOf(address treasurySplitter) → uint256
```

- `Balance > InsuranceAmount` — Pool is fully insured and generating distributable surplus
- `Balance < InsuranceAmount` — Pool is building reserves; all fees are currently retained

### Monitor Governance Changes

```
activeProposals() → Proposal[]
```

Returns pending changes to insurance parameters. Changes require dual-signature (Curator + DAO), and lenders can observe any attempt to modify safety floors before execution.

## Scope Limitations

The reserve fund covers **under-collateralization during liquidations only**. It does not cover:

- ⚠️ **Software exploits or hacks** — The reserve is not a general-purpose insurance fund. Smart contract vulnerabilities, exploits, or security breaches are outside its scope.
- ⚠️ **Oracle manipulation beyond dual-oracle protections** — If both oracle feeds report incorrect data simultaneously, the reserve may be insufficient.

The DAO can manage its exposure by unwrapping Diesel Tokens (converting LP shares to underlying assets). Only assets held as Diesel Tokens count toward the insurance fund. Non-dToken assets in the Treasury are not part of the reserve.

**Implication for partners:** This is bad-debt insurance, not protocol-wide coverage. Partners should communicate to lenders that the reserve absorbs liquidation deficits but does not protect against all categories of loss.

---

**Related pages:**

- [Liquidation Process](liquidation-dynamics.md) — How bad debt occurs and the full liquidation sequence
- [Business Model](business-model.md) — How revenue flows into the TreasurySplitter
- [Audits & Bug Bounty](audits-and-bug-bounty.md) — Security measures for smart contract risk
