# Tooling for curators

## Essential tooling for curators

Gearbox goes beyond providing just a protocol by offering a complete ecosystem of tools tailored for curators. These tools enable:

* **Market Configuration**: Safely set up and manage lending markets with intuitive interfaces.
* **Transaction Integrity**: Ensure the accuracy and security of transactions before they are executed onchain.
* **Pre-Deployment Testing**: Test changes in a controlled environment to validate configurations and prevent errors.
* **Multi-Chain Support**: Operate seamlessly on almost any EVM-compatible blockchain.

#### Curation Supply Chain

The curation supply chain in Gearbox is supported by a set of specialized tools designed to streamline market deployment and transaction management while prioritizing security and transparency.

**Permissionless Interface**

* **URL**: [https://permissionless.gearbox.foundation/curators](https://permissionless.gearbox.foundation/curators)
* **Purpose**: Enables curators to create transaction batches for market deployment and configuration using human-readable tables. The interface generates transaction data, which is uploaded to IPFS, with the Content Identifier (CID) signed by the GIP creator to prevent phishing.
* **Note**: This interface can't modify onchain state directly; it consists both of a frontend and backend maintained by Gearbox contributors. Therefore it shouldn't be perceived as a final source of truth for onchain state or actions.

<figure><img src="../.gitbook/assets/image (5).png" alt=""><figcaption></figcaption></figure>

**Permissionless Safe**

* **URL:** [**https://safe.gearbox.finance/**](https://safe.gearbox.finance/)
* **Repository**: [https://github.com/Gearbox-protocol/permissionless-safe](https://github.com/Gearbox-protocol/permissionless-safe)
* **Purpose**: An open-source, IPFS-hosted version of the Safe Multisig UI designed to review and sign transactions securely in a human-readable format. It eliminates backend dependencies to mitigate risks like Bybit-type attacks and performs checks of IPFS CID signature to prevent phishing.
* **Note**: The open-source nature and IPFS hosting ensure users can verify the code's integrity.

<figure><img src="../.gitbook/assets/image (3).png" alt=""><figcaption></figcaption></figure>

**Anvil Fork-Based Simulations**

* **Purpose**: A unique Gearbox service that allows curators to test market configurations and transaction changes on a fork of the blockchain before onchain execution. This ensures the correctness of state changes and supports testing of various Gearbox components, including liquidators, routers, and frontends.

<figure><img src="../.gitbook/assets/image (4).png" alt=""><figcaption></figcaption></figure>

