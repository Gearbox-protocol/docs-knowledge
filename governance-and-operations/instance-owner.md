# Instance Owner

## Instance Owner

The Instance Owner is a chain-specific technical multisig responsible for maintaining the integrity of the local Gearbox deployment. It acts as a **technical gatekeeper**, ensuring that critical infrastructure, specifically the Price Feed Store, remains secure, verified, and consistent across networks.

Unlike Market Curators, who manage financial risk parameters, the Instance Owner operates under a strict mandate of **business neutrality**. It does not assess the economic viability of assets or strategies but ensures the underlying data feeds function correctly.

### The Neutrality Principle

Gearbox enforces a strict separation between **Technical Maintenance** and **Financial Risk Management**.

* **Market Curators (Financial Layer):** Responsible for setting LTVs, interest rates, and supply caps. They bear the economic risk of their decisions.
* **Instance Owner (Infrastructure Layer):** Responsible for verifying that a price feed contract is technically sound, correctly configured, and secure.

The Instance Owner does not gatekeep assets based on quality or volatility. If a Curator wishes to list a volatile asset, the Instance Owner’s sole responsibility is to ensure the requested price feed (e.g., Chainlink, Redstone, or TWAP) is implemented correctly and added to the registry. This prevents technical misconfigurations—such as decimal errors or stale feed pointers—without interfering in the free market of credit strategies.

### Core Responsibilities

#### Price Feed Store Management

The primary function of the Instance Owner is the management of the **Price Feed Store**, the onchain registry of allowed price sources for a specific network.

Before a Curator can list an asset in a Credit Manager, the asset and its corresponding price feed must be whitelisted in the Price Feed Store. The Instance Owner verifies:

1. **Contract Verification:** The feed contract is verified on the block explorer.
2. **Source Integrity:** The feed points to the correct aggregator address (e.g., the official Chainlink or Pyth contract for that chain).
3. **Technical Specification:** The feed returns data in the format required by the Credit Manager (typically 8 decimals).

Once verified, the Instance Owner adds the feed to the store, making it available for any Curator to use.

* [**See: Price Oracle Architecture**](https://www.google.com/url?sa=E\&q=..%2Feconomics-and-risk%2Fprice-oracle.md)

#### Protocol Upgrades & Maintenance

While the Protocol DAO votes on global upgrades and new contract versions, the Instance Owner executes the specific transactions required to apply these updates to the local chain instance. This ensures that upgrades are applied atomically and correctly within the context of the specific network environment.

### Multisig Composition

To maintain neutrality and prevent censorship, the Instance Owner multisig is composed of a diverse set of ecosystem participants. This structure ensures that no single entity can block a valid technical integration.

**Typical Composition:**

* **Threshold:** 4-of-12 (Subject to chain-specific configuration)
* **Signers:**
  * Active Market Curators
  * Chain Foundation Contributors
  * Security Auditors
  * Partner Protocol Founders
  * Gearbox Core Contributors

This broad distribution prevents the Instance Owner from becoming a point of centralization while maintaining a high bar for technical competence among signers.

<figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FHWjUfvIbazY9RydyeVFA%2Fccg.jpg?alt=media&#x26;token=441ef5e1-5cdf-47c2-9656-2c4b1dccfa36" alt=""><figcaption></figcaption></figure>
