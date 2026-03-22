# Deleverage Bot

Deleverage bots perform partial liquidations — selling just enough collateral to restore a Credit Account's Health Factor before full liquidation conditions are met. This early intervention preserves most of the borrower's position and reduces bad debt exposure for liquidity providers.

## Mechanism

The bot monitors Health Factor across Credit Accounts. When HF drops below the configured `minHF` threshold but remains above 1 (the full liquidation trigger), the bot executes a partial liquidation via `botMulticall()`:

1. Calculates the minimum collateral sale required to restore HF to the target (`maxHF`)
2. Calls `partiallyLiquidateCreditAccount()`, specifying the token, repayment amount, and minimum collateral to seize
3. The sold collateral repays a portion of the account's debt; the bot operator receives a premium

The borrower retains the remainder of the position. Only the fraction necessary to restore solvency is sold.

## Bot Authorization

Two distinct layers govern bot access:

**On-chain permissions:** The Credit Account owner grants specific operation rights to a bot address. Permissions are stored as a `uint192` bitmask — each bit corresponds to a specific operation type (e.g., decrease debt, withdraw collateral). The bot can only perform operations the owner has explicitly authorized. No DAO or curator approval is required; the owner controls which bots can act on the account.

**Interface whitelisting:** For a bot to appear in the protocol UI, it must be whitelisted at the interface level. This is a frontend filter, not a protocol-level restriction. On-chain, any address with granted permissions can call `botMulticall()` regardless of UI listing.

The bot executes all operations through `botMulticall(address creditAccount, MultiCall[] calldata calls)`, which enforces the granted permission bitmask. If a bot attempts an operation not authorized by the account owner, the transaction reverts.

⚠️ **Compliant account restriction:** Bot permissions are blocked for accounts under compliance frameworks (e.g., Securitize-gated on-demand pools). Automated control of KYC-bound accounts is not permitted.

## Bot Economics

Each deleverage event generates two fee components:

| Component | Recipient | Purpose |
|-----------|-----------|---------|
| **Premium** | Bot operator | Execution incentive for the deleverage transaction |
| **Fee** | Protocol treasury | Protocol share, split between Curator and DAO |

The premium structure derives from the full liquidation premium, scaled by the `PremiumScale` parameter. At 100% PremiumScale, the deleverage premium equals the liquidation premium. Bot profitability depends on the premium earned minus gas costs — smaller positions yield lower absolute premiums, which may not cover transaction costs on high-gas networks.

## Pool Protection

Deleveraging reduces bad debt risk for liquidity providers through two effects:

1. **Pre-emptive intervention** — Positions are partially unwound while still overcollateralized (HF > 1), before any shortfall can develop. Most minor market dips result in partial deleverage rather than full liquidation.

2. **Reduced liquidation severity** — When full liquidation does occur, the remaining position is smaller and has a higher Health Factor baseline, lowering the probability that collateral value falls below total debt.

If the insurance fund (Treasury LP shares) is insufficient to cover bad debt, losses are socialized across all liquidity providers. Deleveraging reduces the frequency and magnitude of that scenario.

## Parameters

| Parameter | Purpose | Design Rationale |
|-----------|---------|-----------------|
| `minHF` | Trigger threshold for deleverage | High enough to buffer against sudden price drops; low enough to avoid triggering on normal volatility |
| `maxHF` | Target HF after deleverage | Set close to `minHF` to minimize the collateral sold per event |
| `PremiumScale` | Fraction of liquidation premium applied | 100% aligns deleverage economics with full liquidation profitability |
| `FeeScale` | Fraction of protocol fee applied | Typically 100%, aligning with the standard liquidation fee |

### Example

For WETH collateral with a 10% short-term price drop protection target:

```
minHF = 1 + 0.10 = 1.10
```

When the WETH price drops 8%, the bot intervenes by selling a small portion of collateral and repaying debt. If the price drops beyond the buffer instantly (e.g., 12%), the account may proceed to full liquidation.

---

**Related pages:**

- [Liquidation Process](liquidation-dynamics.md) — Full liquidation mechanics and bad debt handling
- [Business Model](business-model.md) — How liquidation fees are distributed
- [Insurance & Solvency Reserves](insurance-and-solvency.md) — How the reserve fund absorbs losses before LP dilution
