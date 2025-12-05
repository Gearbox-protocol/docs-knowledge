[MODE=BALANCED]

# Gearbox concepts
## Credit Accounts
Credit Accounts are user-owned smart wallets that combine personal capital with borrowed liquidity while keeping positions liquid.

**How they differ from pool-based lending**
- **Control:** users manage a dedicated account, not a pro-rata share of a pooled vault, so assets and actions remain directly-owned.

- **Execution:** accounts call external protocols through adapters that fence interactions and preserve composability across DeFi.

- **Risk:** solvency is evaluated on every action, keeping each account overcollateralized and liquidating at the account level when needed.


## Pools
Single-asset ERC4626 vaults serving as a source of liquidity for overcollateralized loans.

- **Exposure:** curator-set collateral lists and limits shape a defined portfolio of loans for each pool.

- **Risk controls:** overcollateralization is maintained through pricing safeguards, liquidations, and bad-debt protection.

- **Liquidity:** withdrawals have no timelocks can be limited by unborrowed liquidity, with utilization caps preserving buffers for depositors.

## Markets & Curators
Markets are modular contract sets that connect pools to borrowers under a defined configuration.
A curator deploys and governs each market, with timelocked configuration for critical changes and separate pause/emergency roles for rapid responses to changing market conditions.

- **Pool-level controls:** caps on collateral exposure, choice of price sources, and policies to prevent bad debt.

- **Position-level controls:** whitelisting rules (KYC),limits on position size and leverage, allowed external contracts, and fee schedules for curator and DAO.

- **Roles:** designated addresses adjust parameters at timelock of min 24h, while emergency roles can pause contracts or cut exposure without timelock to protect markets when conditions shift.



## Oracles
Oracles are system modules that keep collateral pricing safe for borrowing and liquidations.

- **Providers and modules:** supports major feeds (Chainlink, Redstone, Pyth) plus 10+ custom modules to price complex DeFi positions.

- **Security-first:** critical actions reference 2 different price sources to resist manipulation and sudden swings.

- **Coverage:** modules audited 20+ times price exotic and pegged assets (Curve, Balancer, Pendle) within curated risk bounds.

## Liquidations
Liquidations are the backstop that keeps loans overcollateralized. When collateralization falls below a minimal allowed threshold, liquidator can step in, repay the full loan, and buy the account’s assets at a preset discount. The discount is defined by the market’s liquidation premium.

- **Mechanism:** a liquidator repays the full debt and purchases the account’s collateral at a defined discount when solvency drops.

- **Bad-debt protection:** policies check collateral backing to avoid cascading liquidations that would create losses for pools, reverting if liquidation would push the market into bad debt.

- **Preventive mode:** optional partial liquidations can trim risk early by selling only part of the collateral when buffers thin, reducing user loss while restoring health.