# Supply Information

GEAR token specifications, current circulation, distribution breakdown, and vesting status — for partner due diligence on tokenomics and governance power concentration.

---

## Token Specifications

| Property | Value |
|---|---|
| **Contract** | `0xba3335588d9403515223f109edc4eb7269a9ab5d` |
| **Standard** | ERC-20 |
| **Decimals** | 18 |
| **Symbol** | GEAR |
| **Hard cap** | 10,000,000,000 (10 billion) |
| **Cap enforcement** | Immutable in source code — cannot be changed by any governance action |
| **Circulating supply** | Approximately 50% of total supply |

---

## Buyback Program

Per GIP-219, 25% of DAO revenue is directed to purchasing GEAR/WETH LP tokens on Uniswap V2. Buyback activity is publicly trackable via the [Dune analytics query](https://dune.com/queries/6372284).

---

## Initial Distribution

Nearly all vestings completed by mid-2024. There is no significant upcoming token supply overhang.

### Community DAO Portion: ~58% (No Vesting)

| Allocation | Share | Vesting |
|---|---|---|
| DAO Treasury Multisig | Originally 51.00% | No vesting. Managed by DAO-enacted treasury multisig. |
| Credit Account Mining | 5.00% | No vesting. Mined by 5,000 participants in the launch ceremony. |
| Community Testers | ~1.085% | No vesting. |
| Early Discord Members | ~0.348% | No vesting. |
| Retroactive Rewards (2021) | ~0.5% | No vesting. |

The DAO Treasury also funded two DAO rounds:
- DAO Round Part 1 (2.766% of supply): 1-year lockup + 1-year linear vesting, ended July 2024.
- DAO Round Part 2 (1.057% of supply): 1-year lockup + 1-year linear vesting, ended September 2024.

### Initial External Contributors: 1.28%

Contributors to technical development who were not committing capital.
- **Lockup:** 12 months from token deployment
- **Vesting:** 18 months linear after lockup
- **Status:** Ended June 2024

### Early Backers: 9.20%

Early contributors who participated in pre-DAO development.
- **Lockup:** 12 months from token deployment
- **Vesting:** 12 months linear after lockup
- **Status:** Ended December 2023

### Initial Core Contributors: 20%

Original core development team.
- **Lockup:** 12 months from token deployment
- **Vesting:** 18 months linear after lockup
- **Status:** Ended June 2024

### Company Wallet: 11.52%

Entity that kickstarted initial protocol development pre-DAO launch. Outside the scope of DAO governance. Used for discretionary activities including onboarding contributors, auditor engagements, and external work performed before the DAO was established.
- **Lockup:** 12 months from token deployment
- **Vesting:** 18 months linear after lockup
- **Status:** Ended June 2024
- **Address:** `0xa8b1d00b1d224e83760963e361b7f676581a622d`

---

## Verification

All vesting schedules are verifiable on-chain. The `TokenDistributor` contract provides:
- `contributorsList` — list of all contributor addresses
- `contributorVestingContracts` — the corresponding vesting contract for each address

No trust required. Community retains the largest share in both distribution and voting weight.

---

## Related Pages

- [Protocol DAO](../governance/protocol-dao.md) — DAO governance scope and GEAR token role
- [Operational Multisigs](../governance/operational-multisigs.md) — Treasury Guard and fee management multisigs
