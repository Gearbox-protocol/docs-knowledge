# Instance Owner

The Instance Owner is a chain-specific technical multisig responsible for maintaining the integrity of the local Gearbox deployment. It manages the Price Feed Store — the on-chain registry of allowed price sources for a given network — and executes DAO-authorized upgrades on that chain.

This page establishes what the Instance Owner is prevented from doing before describing its responsibilities, so that partners can confirm this role operates as neutral infrastructure, not a business gatekeeper.

---

## What the Instance Owner CANNOT Do

The Instance Owner operates under a strict mandate of business neutrality. The following constraints are enforced by the protocol's design and governance structure:

- **Cannot gatekeep assets based on quality, volatility, or business judgment.** If a Curator requests a price feed for a volatile or unconventional asset, the Instance Owner's sole function is to verify the feed is technically sound. It does not assess economic viability.
- **Cannot interfere in the free market of credit strategies.** The Instance Owner has no authority over which assets a Curator lists, what LTVs are set, or how markets are configured.
- **Cannot initiate protocol upgrades autonomously.** The Instance Owner executes only changes that have been authorized through DAO governance. It is an executor, not a decision-maker.
- **Cannot censor a market or prevent a valid technical integration.** The multisig composition (see below) ensures no single entity can block a legitimate request.

**Implication for partners:** The Instance Owner cannot prevent a Curator from listing an asset or operating a market. Technical verification is the only gate.

---

## What the Instance Owner Does

### Price Feed Store Management

The primary function: maintaining the on-chain registry of allowed price sources for the specific network.

Before a Curator can list an asset in a Credit Manager, the asset's price feed must be whitelisted in the Price Feed Store. The Instance Owner verifies three criteria:

1. **Contract verification:** The feed contract is verified on the block explorer.
2. **Source integrity:** The feed points to the correct aggregator address (e.g., the official Chainlink or Pyth contract for that chain).
3. **Technical specification:** The feed returns data in the required 8-decimal format.

Once verified and added, the feed is available for any Curator to use. The Instance Owner does not decide which Curators may access it.

### Protocol Upgrade Execution

The Protocol DAO votes on global upgrades and new contract versions. The Instance Owner executes the specific transactions required to apply these updates to the local chain instance, ensuring upgrades are applied atomically and correctly within that network's environment.

---

## Separation: Technical vs. Financial

Gearbox enforces a strict separation between technical maintenance and financial risk management:

| Responsibility | Role | Scope |
|---|---|---|
| Price feed technical soundness | Instance Owner | Verifies correct aggregator, decimals, contract verification |
| Asset listing, LTVs, interest rates | Market Curator | Decides which assets to list and at what risk parameters |

This separation prevents technical misconfigurations — decimal errors, stale feed pointers, incorrect aggregator addresses — without interfering in Curators' financial decisions.

**Implication for partners:** Listing a new asset requires two independent approvals: technical verification (Instance Owner) and financial risk acceptance (Curator). Neither role can substitute for the other.

---

## Multisig Composition

The Instance Owner multisig is composed of a diverse set of ecosystem participants. This structure prevents any single entity from blocking a valid technical integration.

- **Typical threshold:** 4-of-12 (subject to chain-specific configuration)
- **Signer categories:**
  - Active Market Curators
  - Chain Foundation Contributors
  - Security Auditors
  - Partner Protocol Founders
  - Gearbox Core Contributors

The broad distribution creates a low censorship risk. Signers are reputation-backed participants from across the ecosystem — no single category holds a blocking majority.

---

## Related Pages

- [Market Curators](market-curators.md) — Financial risk management role (parameters, collateral, fees)
- [Protocol DAO](protocol-dao.md) — Governance scope: upgrades, chain activation, fee splits
- [Operational Multisigs](operational-multisigs.md) — Protocol-level multisig details and signer lists
