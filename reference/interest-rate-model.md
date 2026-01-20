# Interest Rate Model

The Interest Rate Model (IRM) is a critical component of the Gearbox Protocol that determines the cost of borrowing for Credit Accounts. In Gearbox V3, the protocol primarily utilizes a **Two-Point Linear Interest Rate Model** (`IRM::LINEAR`), designed to provide more stable rates and prevent sudden interest spikes during large liquidity fluctuations.



### Pool and IRM Interaction

The `PoolV3` contract acts as the primary consumer of the IRM. It does not store interest rate logic internally but instead queries the IRM whenever the pool's state changes.

#### Triggering Rate Updates

The pool triggers a rate recalculation via the IRM's `calcBorrowRate` function during any operation that affects the pool's utilization:

* **Lending Operations**: `deposit`, `mint`, `withdraw`, and `redeem`.
* **Borrowing Operations**: `lendCreditAccount` (when a user opens or increases debt) and `repayCreditAccount` (when debt is repaid or an account is liquidated).

#### Optimal Borrowing Check

A unique feature of the V3 IRM is the `checkOptimalBorrowing` flag.&#x20;

When a Credit Manager attempts to borrow funds via `lendCreditAccount`, it passes `true` to this flag.&#x20;

If the IRM is configured with `isBorrowingMoreU2Forbidden = true`, the call will revert if the new borrowing would push the pool's utilization beyond the U\_2 (steep region) threshold. This ensures a liquidity buffer remains available for lenders to withdraw.

### The Two-Point Linear Model

Unlike traditional models that use a single "kink," Gearbox V3 introduces an intermediate region to smooth the transition between low utilization and the "liquidity crunch" (steep) region.

| Region           | Range           | Slope         | Description                                                           |
| ---------------- | --------------- | ------------- | --------------------------------------------------------------------- |
| **Obtuse**       | $0 \to U\_1$    | $R\_{slope1}$ | Low utilization; rates grow slowly.                                   |
| **Intermediate** | $U\_1 \to U\_2$ | $R\_{slope2}$ | Normal operation; provides a buffer before the steep curve.           |
| **Steep**        | $U\_2 \to 100%$ | $R\_{slope3}$ | Emergency region; rates increase aggressively to encourage repayment. |

### Fetching Core Parameters

Users and integrators can fetch the parameters influencing their interest rates through multiple layers.

#### 1. Direct Contract Queries

You can call the IRM contract directly using the `ILinearInterestRateModelV3` interface:

* **`getModelParameters()`**: Returns the fixed configuration ($U\_1, U\_2, R\_{base}, R\_{slope1}, R\_{slope2}, R\_{slope3}$) in basis points (1/100th of a percent).
* **`isBorrowingMoreU2Forbidden()`**: Returns whether the pool blocks borrowing above $U\_2$.
* **`calcBorrowRate(expected, available, check)`**: Returns the current borrow rate in **RAY** ($10^{27}$) based on hypothetical liquidity levels.

#### 2. High-Level Pool State

The `PoolV3` provides the results of the IRM's calculation:

* **`baseInterestRate()`**: Returns the current annual interest rate (in RAY) currently applied to all borrowers.
* **`supplyRate()`**: Returns the annual rate earned by LPs, which is the `baseInterestRate` scaled by utilization, plus quota revenue.

```typescript
// TypeScript: Reading interest rates from pool
const borrowRate = await pool.read.baseInterestRate();
const supplyRate = await pool.read.supplyRate();

// Convert from RAY (27 decimals) to percentage
const RAY = 10n ** 27n;
const borrowAPR = Number(borrowRate * 10000n / RAY) / 100; // e.g., 5.25%
const supplyAPY = Number(supplyRate * 10000n / RAY) / 100;

// Reading IRM parameters directly
const irm = getContract({
  address: irmAddress,
  abi: linearInterestRateModelAbi,
  client: publicClient,
});

const params = await irm.read.getModelParameters();
// Returns: [U1, U2, Rbase, Rslope1, Rslope2, Rslope3] in basis points
```

### Security and Risk Considerations

* **Utilization Manipulation**: Because the rate is calculated based on `availableLiquidity`, large atomic withdrawals can spike the interest rate. The $U\_1 \to U\_2$ intermediate slope is specifically designed to mitigate the impact of these "jumps."
* **Immutable Parameters**: In the standard deployment, IRM parameters are set at construction. However, the `PoolV3` allows the `CONFIGURATOR` to swap the entire IRM contract via `setInterestRateModel` if market conditions shift significantly.

<details>

<summary>Sources</summary>

* [contracts/interfaces/ILinearInterestRateModelV3.sol](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/interfaces/ILinearInterestRateModelV3.sol)
* [contracts/pool/LinearInterestRateModelV3.sol](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/pool/LinearInterestRateModelV3.sol)
* [contracts/pool/PoolV3.sol](https://github.com/Gearbox-protocol/core-v3/blob/main/contracts/pool/PoolV3.sol)
* [contracts/compressors/MarketCompressor.sol](https://github.com/Gearbox-protocol/periphery-v3/blob/main/contracts/compressors/MarketCompressor.sol)
* [contracts/types/MarketData.sol](https://github.com/Gearbox-protocol/periphery-v3/blob/main/contracts/types/MarketData.sol)

</details>
