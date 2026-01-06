# Gearbox V3.1 (Permissionless) overview

After the V3.1 update, Gearbox market creation and management became permissionless. This shift is enabled by two core design choices:

### Strict role segregation

Access rights and responsibilities are programmatically enforced at the contract level. This promotes specialization among participants while limiting the power of any single role - an essential property for preserving a non-custodial user experience while still enabling flexible operations.

### Verifiable deployment

A functional Gearbox market is highly modular and consists of dozens of contracts. With V3.1, this deployment process is brought fully onchain for the first time, enabling transparent, verifiable market launches and trustless scaling across existing and future chains.

## Governance structure <a href="#strict-roles-segregation" id="strict-roles-segregation"></a>

Gearbox is modular at its core, with governance roles designed to streamline operations while keeping access tightly controlled and enabling clear specialization across participants.

<table><thead><tr><th width="238.94140625">Entity</th><th width="141.1953125">Scope</th><th width="201.203125">Allowance</th><th>Affects users?</th></tr></thead><tbody><tr><td>DAO (tokenholders) <a data-mention href="protocol-level-governance.md">protocol-level-governance.md</a></td><td>All chains</td><td>Deliver new versions<br>Configure fee split</td><td>No</td></tr><tr><td>Instance (chain) <br><a data-mention href="chain-specific-governance.md">chain-specific-governance.md</a><br></td><td>One chain</td><td>Whitelist price feeds</td><td>No</td></tr><tr><td>Risk Curators<br><a data-mention href="market-curators.md">market-curators.md</a><br></td><td>Owned markets</td><td>Change risk parameters</td><td>Yes<br>Subject to timelock</td></tr></tbody></table>
