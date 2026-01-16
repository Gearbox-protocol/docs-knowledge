# Credit Account migration

### Why migrate (what you gain as a Borrower)

**In short:** incentives, better execution and more favorable rates.

**Incentives:**

* One-time fixed reward paid in GEAR. Distributed retroactively.

**Better execution:**

* Improved routing and support for new adapters increases capital efficiency and reduces costs.

**Favorable rates:**

* Vote-based collateral-specific rate discovery is depreciated in favor of curator-controlled rates.

### Requirements for allowing a migration into your Market

1. All the collaterals of old account should be allowed in a credit manager of target Market
2. The position can be only migrated as a whole, target Market should have appropriate debt limits and capacity.
3. If the underlying token is changed during migration, new market must support swaps from new underlying to old one.\
   E.g. you can migrate rstETH from an old wstETH pool to a new WETH pool, but WETH -> wstETH swap must be allowed in the new pool.

### How it works

1. New credit account is opened in a target market
2. Amount of tokens enough to repay old account is borrowed from a new account
3. Newly-borrowed tokens are swapped into underlying tokens of old account
4. Old account's debt is repaid and its collateral is transferred to the new account
