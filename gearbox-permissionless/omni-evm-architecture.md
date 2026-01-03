# Omni-EVM Architecture

## Scalable by design

Gearbox Permissionless stack is built to minimize dependencies, allowing to launch distribution-ready lending products without waiting oracles, aggregators and multisig UIs to deploy:

* **Day-0 oracles:** Most push oracle providers are supported (Chainlink, Redstone, DIA, EO and more) + On-Demand feeds' support (Pyth, Redstone pull) + smart-contract-based price feeds tailored for ERC4626, Curve, Convex, Balancer LP positions and more.\
  &#xNAN;_&#x55;sage of Redstone Pull oracle is permissionless and free._
* **Built-in aggregator:** Custom fully-onchain router supporting 20+ DeFi protocols.
* **No AMM Depth Requirement:** There is also no need to wait for AMMs or DEXes liquidity to be deep if the integrations are based on withdraw-deposit operations (e.g. ERC4626 vaults). Unlike other lending protocols that rely only on DEX liquidity to add collaterals, Gearbox can support such integrations.
* **Self-hosted operational tooling:** Open-source multisig UI for secure market management.
* **Battle-tested & scalable:** Gearbox Permissionless is already technically live on 27 different networks, enabling Curators to launch markets across various Layer 2 and Layer 1 EVMs.

## Strict roles segregation

Gearbox is modular at its core, with governance roles designed to streamline operations while keeping access tightly controlled and enabling clear specialization across participants.

<table><thead><tr><th width="238.94140625">Entity</th><th width="141.1953125">Scope</th><th width="201.203125">Allowance</th><th>Affects users?</th></tr></thead><tbody><tr><td>DAO (tokenholders)<br><a data-mention href="gearbox-v3.1-permissionless-overview/protocol-level-governance.md">protocol-level-governance.md</a></td><td>All chains</td><td>Deliver new versions<br>Configure fee split</td><td>No</td></tr><tr><td>Instance (chain)<br><a data-mention href="gearbox-v3.1-permissionless-overview/chain-specific-governance.md">chain-specific-governance.md</a></td><td>One chain</td><td>Whitelist price feeds</td><td>No</td></tr><tr><td>Risk Curators<br><a data-mention href="gearbox-v3.1-permissionless-overview/market-curators.md">market-curators.md</a></td><td>Owned markets</td><td>Change risk parameters</td><td>Yes<br>Subject to timelock</td></tr></tbody></table>

## Verifiable contract deployment

The Bytecode Repository acts as an “on-chain GitHub,” storing contract bytecode, managing contract versions, and proving audit coverage by recording auditors’ signatures on-chain.

## Multi-level protection from misconfigurations

The chain-specific Instance Manager role is governed by a diverse multisig comprising curators, chain contributors, representatives from leading audit firms, partner-protocol founders, and Gearbox contributors. This role is responsible for whitelisting price feeds for use by curators.
