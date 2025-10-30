[Copy]

:

[](#why-migrate-what-you-gain-as-a-borrower)

Why migrate (what you gain as a Borrower)
:

One-time fixed reward paid in GEAR. Distributed retroactively.
:

Improved routing and support for new adapters increases capital efficiency and reduces costs.
:

Vote-based collateral-specific rate discovery is depreciated in favor of curator-controlled rates.

[](#requirements-for-allowing-a-migration-into-your-market)

Requirements for allowing a migration into your Market
:

All the collaterals of old account should be allowed in a credit manager of target Market
:

The position can be only migrated as a whole, target Market should have appropriate debt limits and capacity.
:

If the underlying token is changed during migration, new market must support swaps from new underlying to old one. E.g. you can migrate rstETH from an old wstETH pool to a new WETH pool, but WETH -\> wstETH swap must be allowed in the new pool.

[](#how-it-works)

How it works
:

New credit account is opened in a target market
:

Amount of tokens enough to repay old account is borrowed from a new account
:

Newly-borrowed tokens are swapped into underlying tokens of old account
:

Old account\'s debt is repaid and its collateral is transferred to the new account