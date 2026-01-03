# Protocol-level governance

### Cross Chain Multisig (Cross-chain governance) <a href="#cross-chain-multisig-cross-chain-governance" id="cross-chain-multisig-cross-chain-governance"></a>

**Permissionless Curation Contracts** are designed to enable the Gearbox Protocol to function fully without active DAO involvement, with DAO influence restricted at the smart-contract level. The design follows these key principles:

* **Non-Interference with Decisions**: The DAO cannot influence or override decisions made by Curators or Instance Managers.
* **No Control Over Market Contracts**: Market contracts' parameters allow flexible modification by Curators, but the DAO cannot alter them.
* **Exclusive Control Over System Contract Versions**: Only the DAO can authorize new versions of system contracts (core protocol logic) for use. Adding adapters, price feeds, bots, or other components remains permissionless.
* **Chain Expansion Oversight**: Only the DAO can activate Gearbox on new chains, ensuring the correct Treasury address and Instance Owner multisig are set.
