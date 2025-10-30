:

1.  [Operational Standards](/gearbox-permissionless-doc/operational-standards)

# Asset integration process
:

WIP: this page is to provide exhaustive guidelines for integrating a new asset class to gearbox. It covers development and resting of adapters, price feeds and resulting market configurations.
Inputs: - asset class - are reputable external feeds available?

1.
:

:

receive request for asset come up with a scope of required contacts: adapter, phantom token, gateway, price feed, router, withdrawal subcompressor
:

codes v0 of required contracts; run unit tests
:

run complex tests in the test environment

2.
:

:

Prepare market config for testing based on template

3.
:

:

Create testnet with a functional market to test a new integration based on config from 2.

4.
:

:

Run router tests and compressor tests on that testnet until it\'s fully ready for audit

:

1.
:

:

1.
:

:
:

:

1.
:

:

1.
:

:
:

1.
:

:

Add tokens and price feeds to price feed store
:

Configure router and compressor for the instance

2.
:

:

Prepare new bundles for the target asset class

3.
:

:

Add bundles to PI

4.
:

:

Create markets using bundles and test on Staging
:

Release bundles in production

[[[Previous][Instance Activation guidlines]]](/gearbox-permissionless-doc/operational-standards/instance-activation-guidlines)[[[Next][Emergency admin]]](/gearbox-permissionless-doc/emergency-roles/emergency-admin)

Last updated 13 days ago