#!/bin/bash

# Move and rename files to appropriate folders

# 01-overview
mv protocol-overview.md 01-overview/01-protocol-overview.md
mv market.md 01-overview/02-market.md
mv multichain-architecture.md 01-overview/03-multichain-architecture.md
mv deployment-addresses.md 01-overview/04-deployment-addresses.md

# 02-permissionless-curation
mv permissionless-curation-key-concepts-and-system-overview.md 02-permissionless-curation/01-key-concepts-and-system-overview.md
mv a-day-of-a-curator.md 02-permissionless-curation/02-a-day-of-a-curator.md
mv curation-iceberg.md 02-permissionless-curation/03-curation-iceberg.md
mv fee-sharing.md 02-permissionless-curation/04-fee-sharing.md

# 03-competitive-advantages
mv competitive-advantages-collateral-specific-rates.md 03-competitive-advantages/01-collateral-specific-rates.md
mv competitive-advantages-dual-oracle-pricing.md 03-competitive-advantages/02-dual-oracle-pricing.md
mv competitive-advantages-essential-tooling-for-curators.md 03-competitive-advantages/03-essential-tooling-for-curators.md
mv direct-redemptions-for-semi-liquid-assets.md 03-competitive-advantages/04-direct-redemptions-for-semi-liquid-assets.md

# 04-step-by-step-guides
mv step-by-step-guides-creating-a-new-curator-market-configurator.md 04-step-by-step-guides/01-creating-a-new-curator-market-configurator.md
mv step-by-step-guides-adding-required-price-feeds.md 04-step-by-step-guides/02-adding-required-price-feeds.md
mv step-by-step-guides-creating-a-market.md 04-step-by-step-guides/03-creating-a-market.md
mv step-by-step-guides-allowing-strategies-for-the-market.md 04-step-by-step-guides/04-allowing-strategies-for-the-market.md
mv step-by-step-guides-claiming-fee-share.md 04-step-by-step-guides/05-claiming-fee-share.md
mv step-by-step-guides-executing-transactions.md 04-step-by-step-guides/06-executing-transactions.md
mv step-by-step-guides-testing-config-on-forks.md 04-step-by-step-guides/07-testing-config-on-forks.md

# 05-feature-explainers
mv feature-explainers-dvsteth-leveraged-staking.md 05-feature-explainers/01-dvsteth-leveraged-staking.md
mv feature-explainers-seamless-lp-migration.md 05-feature-explainers/02-seamless-lp-migration.md
mv feature-explainers-credit-account-migration.md 05-feature-explainers/03-credit-account-migration.md

# 06-operational-standards
mv operational-standards-feeds-configuration-guidlines.md 06-operational-standards/01-feeds-configuration-guidelines.md
mv operational-standards-instance-activation-guidlines.md 06-operational-standards/02-instance-activation-guidelines.md
mv operational-standards-asset-integration-process.md 06-operational-standards/03-asset-integration-process.md

# 07-emergency-roles
mv emergency-roles-emergency-admin.md 07-emergency-roles/01-emergency-admin.md
mv emergency-roles-pausable-unpausable-admin.md 07-emergency-roles/02-pausable-unpausable-admin.md

# 08-advanced-configuration
mv advanced-configuration-configuring-a-market.md 08-advanced-configuration/01-configuring-a-market.md
mv advanced-configuration-creating-a-credit-manager.md 08-advanced-configuration/02-creating-a-credit-manager.md
mv advanced-configuration-configuring-a-credit-manager.md 08-advanced-configuration/03-configuring-a-credit-manager.md
mv advanced-configuration-configuring-adapters.md 08-advanced-configuration/04-configuring-adapters.md
mv advanced-configuration-creating-bundles.md 08-advanced-configuration/05-creating-bundles.md

echo "Files organized successfully!"



