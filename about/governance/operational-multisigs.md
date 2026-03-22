# Operational Multisigs

Gearbox protocol governance decisions are executed through role-specific multisigs with distinct thresholds, signer sets, and authority boundaries. Multisig roles are split between technical execution and financial treasury management. All multisigs were created prior to the deployment ceremony, and signer configurations were established through DAO voting procedures — verifiable on-chain via Etherscan contract logs.

This page documents each multisig's authority, constraints, composition, and on-chain addresses for operational due diligence.

---

## What Multisigs CANNOT Do

Every multisig operates under constraints enforced by smart contract logic, not social agreement:

- **Cannot execute without reaching quorum.** The threshold requirement is on-chain. A transaction below quorum is rejected by the contract.
- **Cannot bypass the timelock for technical changes.** All Technical Guard transactions are subject to a 2-day delay before execution.
- **The Veto role cannot propose or push transactions.** It can only block — it has no constructive authority.
- **Cannot override Curator-level market parameters.** Protocol multisigs govern protocol infrastructure, not individual market configurations.

**Implication for partners:** Multisig authority is bounded by on-chain enforcement. The trust model rests on quorum thresholds and timelocks, not solely on signer reputation.

---

## Technical Guard (6/12)

Executes proposals that have reached quorum related to technical changes and protocol improvements.

- **Threshold:** 6-of-12
- **Address:** `0xA7D5DDc1b8557914F158076b228AA91eF613f1D5`
- **Timelock:** All transactions are behind a 2-day delay, observable at the [Risk Framework dashboard](https://risk.gearbox.foundation/updates).

**Signers:**

| # | Signer | Affiliation |
|---|---|---|
| 1 | zefram.eth | 88mph, sudoswap; MetaCartel member |
| 2 | Ignacio | Co-Founder, Stakely |
| 3 | van0k | Gearbox protocol developer |
| 4 | 0xmikko | Original inventor of Gearbox (on behalf of Gearbox Protocol Limited) |
| 5 | Alex Smirnov | Co-Founder, deBridge |
| 6 | MacLane Wilkison | Co-Founder, NuCypher & Threshold |
| 7 | Simone | Developer, DegenScore |
| 8 | Lewi | OG participant, ESD summoner |
| 9 | Klim | Data analytics, YFI contributor |
| 10 | Alex | Builder, ex-Neutrino |
| 11 | Alex | CTO, Mellow Protocol |
| 12 | Lekhovitsky | Gearbox protocol developer |

---

## Veto / Unpause Role (4/12)

A multisig with the same signer set as the Technical Guard, operating at a lower threshold for faster response during emergencies.

- **Threshold:** 4-of-12
- **Address:** `0xbb803559B4D58b75E12dd74641AB955e8B0Df40E`
- **Veto capability:** Can block malicious proposals and transactions. Cannot propose or push any transaction.
- **Unpause capability:** Can restore operations after an emergency pause.

### Pause Function

The pause function is granted to 2 analytical monitoring addresses (1/1 threshold each). These addresses can only pause the protocol if their monitoring tools detect an issue — an emergency measure to halt operations before full exploitation occurs, if the on-chain time window permits.

- `0xD5C96E5c1E1C84dFD293473fC195BbE7FC8E4840`
- `0x65b384cecb12527da51d52f15b4140ed7fad7308`

---

## Treasury Guard (5/10)

Executes proposals that have reached quorum related to spending, grants, and treasury management.

- **Threshold:** 5-of-10
- **Address:** `0x7b065Fcb0760dF0CEA8CFd144e08554F3CeA73D1`

**Signers:**

| # | Signer | Affiliation |
|---|---|---|
| 1 | Stani | Founder of Aave; Venture Partner, Variant Fund |
| 2 | Amplice | lobsterdao member; core DAO contributor (marketing) |
| 3 | Pepo | Contributor, Wonderland & DeFi LATAM |
| 4 | Sergey | Founder, ICODrops |
| 5 | NDW | Castle Capital member |
| 6 | apeir99n | Original math & product, Gearbox (on behalf of Gearbox Protocol Limited) |
| 7 | Nikitakle | Core DAO contributor (marketing & community) |
| 8 | Amantay | Core DAO contributor (risk & analytics) |
| 9 | duckdegen.eth | DevRel, ex-Connext |
| 10 | Vadym | Head of Product, Kolibrio |

Spending and grants are tracked in [monthly DAO reports](https://gearboxprotocol.notion.site/Monthly-Reports-6849871a9bae44dfb903531c0a997e8f).

---

## Fee Temporary Guard (5/10)

Separates protocol fee collection from DAO development funds. Holds fees collected from the protocol until the DAO decides on a permanent allocation (e.g., staking programs or other initiatives).

- **Threshold:** 5-of-10
- **Signers:** Same set as the Treasury Guard
- **Address:** `0x3E965117A51186e41c2BB58b729A1e518A715e5F`

---

## Rewards Management Guard (2/3)

Executes rewards distribution and sets up temporary incentive campaigns, typically provided by partner protocols.

- **Threshold:** 2-of-3
- **Address:** `0x6f378f36899cEB7C6fB7D293aAE1ca86B0Edbf6D`

---

## Trust Model

- **Execution obligation:** Multisig members must execute proposals that reach winning quorum. In extreme cases, signers could voice opposition — but doing so would breach trust in the governance model and trigger immediate restructuring.
- **Accountability:** Members are semi-public with significant reputation at stake.
- **Backstop:** Permissionless market creation ensures participants can always exit to alternative Curators if governance trust deteriorates.

---

## Related Pages

- [Market Curators](market-curators.md) — Curator-level governance roles (Administrator, Emergency Admin)
- [Protocol DAO](protocol-dao.md) — What the DAO governs and the proposals these multisigs execute
- [Protocol Audits](protocol-audits.md) — Bytecode Repository and contract verification
