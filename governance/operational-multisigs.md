# Operational Multisigs

Gearbox protocol governance executes through role-specific multisigs, each with defined thresholds, signer sets, and authority boundaries. Two functional domains exist: technical execution (contract upgrades, emergency response) and financial management (treasury spending, fee custody, rewards). The DAO created all multisigs prior to the deployment ceremony, and signer configurations were ratified through on-chain DAO votes — verifiable via Etherscan contract logs.

**Scope:** Multisig addresses, thresholds, signer identities, authority boundaries, and the trust model governing execution obligations.
**Anti-scope:** Individual market risk parameters — those belong to [Market Curators](market-curators.md). DAO proposal mechanics and voting procedures — see [Protocol DAO](protocol-dao.md). Contract bytecode verification — see [Protocol Audits](protocol-audits.md).

---

## What Multisigs CANNOT Do

Every multisig operates under constraints enforced by smart contract logic, not social agreement:

- **Cannot execute without reaching quorum.** The threshold is on-chain. The Safe contract rejects any transaction that lacks sufficient signatures.
- **Cannot bypass the timelock for technical changes.** All Technical Guard transactions pass through a 2-day delay before execution. No signer combination can skip this delay.
- **The Veto multisig cannot propose or push transactions.** It holds blocking authority only — no constructive power exists.
- **Cannot override Curator-level market parameters.** Protocol multisigs govern protocol infrastructure. Individual market configurations (LTVs, debt limits, collateral lists) remain under exclusive Curator control via `MarketConfigurator`.

---

## Technical Guard (6/12)

The Technical Guard executes DAO-approved proposals related to contract upgrades, chain deployments, and protocol parameter changes. A proposal must reach winning quorum in the DAO vote before the Technical Guard signers execute it.

- **Threshold:** 6-of-12 — six signers must approve every transaction
- **Address:** [`0xA7D5DDc1b8557914F158076b228AA91eF613f1D5`](https://etherscan.io/address/0xA7D5DDc1b8557914F158076b228AA91eF613f1D5)
- **Timelock:** Every transaction enters a 2-day delay before execution. Pending transactions are observable on the [Risk Framework dashboard](https://risk.gearbox.foundation/updates). Any participant can audit queued changes during this window.

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

The Veto multisig shares the same 12 signers as the Technical Guard but operates at a lower threshold for faster emergency response. Four signers can block a malicious proposal or restore operations after a pause.

- **Threshold:** 4-of-12 — four signers must approve
- **Address:** [`0xbb803559B4D58b75E12dd74641AB955e8B0Df40E`](https://etherscan.io/address/0xbb803559B4D58b75E12dd74641AB955e8B0Df40E)
- **Veto capability:** Signers can block malicious proposals and transactions queued in the timelock. The Veto multisig cannot propose, queue, or push any transaction — it holds blocking authority only.
- **Unpause capability:** After an emergency pause halts protocol operations, this multisig can restore normal operation by calling the unpause function.

### Pause Function

Two analytical monitoring addresses hold independent 1/1 pause authority. Each address can trigger an emergency pause if its monitoring tools detect an exploit or anomaly — halting protocol operations before full exploitation occurs, if the on-chain time window permits.

- [`0xD5C96E5c1E1C84dFD293473fC195BbE7FC8E4840`](https://etherscan.io/address/0xD5C96E5c1E1C84dFD293473fC195BbE7FC8E4840)
- [`0x65b384cecb12527da51d52f15b4140ed7fad7308`](https://etherscan.io/address/0x65b384cecb12527da51d52f15b4140ed7fad7308)

The pause function is a unilateral emergency measure. Only the 4/12 Veto multisig can unpause — a single monitoring address cannot both pause and restore operations.

---

## Treasury Guard (5/10)

The Treasury Guard executes DAO-approved proposals related to spending, grants, and treasury management. A separate signer set from the Technical Guard ensures that entities controlling protocol upgrades do not also control funds.

- **Threshold:** 5-of-10 — five signers must approve every disbursement
- **Address:** [`0x7b065Fcb0760dF0CEA8CFd144e08554F3CeA73D1`](https://etherscan.io/address/0x7b065Fcb0760dF0CEA8CFd144e08554F3CeA73D1)

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

The DAO tracks spending and grants in [monthly DAO reports](https://gearboxprotocol.notion.site/Monthly-Reports-6849871a9bae44dfb903531c0a997e8f).

---

## Fee Temporary Guard (5/10)

The Fee Temporary Guard holds protocol fees collected from markets until the DAO votes on a permanent allocation strategy (e.g., staking programs, buybacks, or other initiatives). Separating fee custody from the Treasury Guard prevents commingling of development funds with earned protocol revenue.

- **Threshold:** 5-of-10
- **Signers:** Same 10 signers as the Treasury Guard
- **Address:** [DEBT — verify on-chain; address not confirmed in canon]

---

## Rewards Management Guard (2/3)

The Rewards Management Guard distributes incentive rewards and configures temporary reward campaigns, typically funded by partner protocols. The low 2/3 threshold reflects the operational nature of this role — reward distribution follows pre-approved campaign terms, not discretionary spending.

- **Threshold:** 2-of-3 — two signers must approve each distribution
- **Address:** [`0x6f378f36899cEB7C6fB7D293aAE1ca86B0Edbf6D`](https://etherscan.io/address/0x6f378f36899cEB7C6fB7D293aAE1ca86B0Edbf6D)

---

## Risk Factors

⚠️ **Signer compromise:** If an attacker gains control of enough signer keys to meet the quorum threshold (e.g., 6-of-12 for the Technical Guard), the attacker could execute unauthorized transactions — subject to the 2-day timelock. The timelock provides a detection window: monitoring systems and the Veto multisig (4/12) can block malicious transactions before execution. Treasury Guard compromise (5/10) carries higher immediate risk because treasury disbursements are not behind the same timelock.

⚠️ **Quorum failure:** If enough signers become permanently unavailable (e.g., lost keys, incapacitation) such that the remaining signers cannot meet the threshold, the multisig becomes inoperable. For the Technical Guard, this would block protocol upgrades. For the Treasury Guard, this would freeze DAO funds. The DAO would need to deploy replacement multisigs through an alternative governance path.

⚠️ **Collusion risk:** The trust model assumes signers act independently. If a majority of signers collude, they can execute any transaction within the multisig's authority scope — but still cannot exceed the on-chain authority boundaries (e.g., cannot override Curator market parameters or extract funds from pools).

---

## Trust Model

- **Execution obligation:** Multisig signers must execute proposals that reach winning quorum in DAO governance. Refusing to execute a valid proposal breaches the governance mandate and triggers immediate signer restructuring via DAO vote.
- **Accountability:** Signer identities are semi-public. Each signer has significant ecosystem reputation at stake — reputational damage from misconduct extends beyond Gearbox to their primary affiliations.
- **Structural safeguards:** The 2-day timelock on Technical Guard transactions, the Veto multisig's blocking authority, and the separation between technical and treasury signers create layered defense against single points of failure.
- **Exit option:** Permissionless market creation (via `MarketConfigurator.createMarket()`) ensures that lenders and borrowers can migrate to alternative Curator markets if governance trust deteriorates. No participant depends on a single multisig for continued protocol access.

---

## Related Pages

- [Market Curators](market-curators.md) — How Curators govern individual market parameters (Administrator, Emergency Admin roles) independently of protocol multisigs
- [Protocol DAO](protocol-dao.md) — What the DAO governs and the proposal lifecycle that these multisigs execute
- [Protocol Audits](protocol-audits.md) — Bytecode Repository verification: how deployed contracts are validated against audited source
- [Instance Owner](instance-owner.md) — Chain-specific technical multisig for price feed verification and upgrade execution
