# Chain-specific governance

Different blockchain networks have unique characteristics, especially when it comes to oracles and ecosystem-specific protocols, and these differences are critical for correct Gearbox integrations. Even when configuration processes are simple, operating at scale across hundreds of assets and price feeds increases the risk of purely technical misconfigurations.

The Instance Owner role exists to address this risk.

## Instance owner overview

Instance Owner is a business-neutral, technical safeguard.

It does not make risk, market, or business decisions and does not interfere with curator strategy. Instead, it acts as a soft-power coordination layer that ensures chain-specific parameters, particularly oracle configurations, are correct, up to date, and consistent across networks.

This role exists because even small mistakes can have outsized consequences. A well-known example occurred on Morpho, where a simple decimal misconfiguration caused a collateral asset to be priced billions of times higher than its real value. The Instance Owner is designed specifically to prevent this class of formal, mechanical errors before they reach production.

### Instance Owner Participants

The Instance Owner multisig includes curators, chain contributors, representatives from leading audit firms, partner-protocol founders, and Gearbox contributors. It is initially configured with a 4-of-12 threshold, with the long-term goal of including all relevant curators and chain contributors as signers. This structure minimizes censorship risk while preventing misconfiguration errors at scale.

For a formal definition of the Instance Owner’s scope and responsibilities, see the Instance Owner Guidelines.

To understand how this role fits into Gearbox’s broader governance model, refer to the diagram below.

<figure><img src="https://494588385-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F9n0QLqkiJru3BYkpyr8F%2Fuploads%2FHWjUfvIbazY9RydyeVFA%2Fccg.jpg?alt=media&#x26;token=441ef5e1-5cdf-47c2-9656-2c4b1dccfa36" alt=""><figcaption></figcaption></figure>
