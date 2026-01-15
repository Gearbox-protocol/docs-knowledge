# Insurance & Solvency Reserves

The Gearbox Protocol employs an automated, on-chain reserve system designed to absorb bad debt and protect Passive Lenders. This mechanism functions not as an external insurance policy, but as a **retention buffer** on protocol revenue.

Its primary objective is to ensure that the Liquidity Pool remains solvent even if a borrower's position is liquidated below the value of their debt.

### Conceptual Overview

In traditional finance, this is analogous to a "First-Loss Capital" tranche.

The protocol generates revenue through interest rates and liquidation fees. Rather than distributing 100% of this revenue to the DAO or Market Curators immediately, the system enforces a **mandatory savings threshold**.

1. **Revenue Accumulation:** All protocol fees flow into a specific contract (`TreasurySplitter`).
2. **The Safety Floor:** A target insurance amount is defined (e.g., 100,000 USDC).
3. **Conditional Distribution:**
   * **Below Target:** If reserves are below the target, **100% of revenue is retained**. No profit is distributed.
   * **Above Target:** Only the _excess_ revenue (surplus) is distributed to the DAO and Curators.

This ensures the protocol prioritizes solvency over profit extraction.

***

### Architecture: The Treasury Splitter

The core component governing this logic is the `TreasurySplitter` contract. It acts as a gatekeeper between protocol fees and profit recipients.

#### The Distribution Logic

The `TreasurySplitter` holds assets (typically LP tokens of the pool it protects). When a distribution is attempted, the contract performs a logic check against the `tokenInsuranceAmount`.

```mermaid

flowchart TD
subgraph Inflow
Fees[Protocol Fees & Interest] -->|Accumulate| Splitter[TreasurySplitter Contract]
end
subgraph Logic Gate
Splitter --> Check{Is Balance > Insurance Target?}
Check -- No --> Retain[RETAIN FUNDS: Build Buffer]
Check -- Yes --> Distribute[DISTRIBUTE SURPLUS: Pay DAO/Curator]
end

subgraph Solvency Event
Retain -.->|Absorb Loss| Pool[Liquidity Pool]
end
```

#### The Asset Composition

The Insurance Fund does not sit idle. It is typically held in **LP Shares** (Diesel Tokens) of the pool it insures. This aligns the Treasury's interests with the Lenders' interests and allows the insurance capital to earn yield while waiting to be used.

***

### Bad Debt Coverage Mechanism

"Bad Debt" occurs when a Credit Account is liquidated, but the collateral value is insufficient to repay the debt to the pool. Without insurance, this loss would be socialized among all Lenders (reducing the value of their LP tokens).

The Insurance mechanism intervenes to prevent this socialization.

#### The Coverage Flow

1. **Liquidation Event:** A liquidator closes a non-solvent Credit Account. The remaining collateral is sold, but a deficit remains (e.g., Debt: 100k, Collateral Value: 98k, Deficit: 2k).
2. **Loss Recognition:** The Credit Manager reports the loss to the Pool.
3. **Treasury Absorption:** The Pool burns **LP Shares held by the Treasury** equal to the value of the loss.

By burning the Treasury's shares, the total supply of LP shares decreases, while the underlying assets in the pool remain (mostly) constant relative to the remaining Lenders. The Treasury effectively "pays" for the loss by giving up its claim on the pool's liquidity.

***

### On-Chain Verification

Market participants can verify the solvency health of a pool by querying the `TreasurySplitter` contract directly.

#### 1. Verify the Insurance Target (The Floor)

To determine the minimum safety buffer the protocol enforces:

* **Function:** `tokenInsuranceAmount(address token)`
* **Interpretation:** This is the "water level." The protocol will not allow profit-taking if reserves drop below this value.

#### 2. Verify Current Reserves (The Buffer)

To determine the actual capital available to absorb losses:

* **Function:** `IERC20(token).balanceOf(address treasurySplitter)`
* **Interpretation:**
  * If `Balance > InsuranceAmount`: The pool is fully insured and generating surplus.
  * If `Balance < InsuranceAmount`: The pool is building reserves; all fees are currently being retained to increase safety.

#### 3. Monitor Governance Changes

Changes to insurance parameters require a dual-signature process (Curator + DAO).

* **Function:** `activeProposals()`
* **Interpretation:** Returns pending changes to the insurance floor or distribution logic. This allows Lenders to see if a Curator is attempting to lower safety parameters.

***

### Related Resources

* [**Liquidation Dynamics**](https://www.google.com/url?sa=E\&q=%2Feconomics%2Fliquidation): How the protocol prevents bad debt before it happens.
* [**Pool Architecture**](https://www.google.com/url?sa=E\&q=%2Fcore-architecture%2Fpool): Understanding the Liquidity Vault and Diesel Tokens.
* [**Market Curators**](https://www.google.com/url?sa=E\&q=%2Fgovernance%2Fmarket-curators): The entities responsible for configuring insurance parameters.
