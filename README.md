# Gearbox Protocol – Monad LP Opportunity

### Overview

Gearbox is a composable leverage protocol enabling undercollateralized on-chain borrowing through Credit Accounts. Current focus:  yield strategies via Midas-issued collateral.

**Two ways to participate:**

|         | Lending                                      | Leverage                                    |
| ------- | -------------------------------------------- | ------------------------------------------- |
| APY     | 6-9%                                         | Up to 20%                                   |
| Role    | Passive liquidity provider                   | Active carry trade                          |
| Risk    | Indirect exposure, protected by liquidations | Direct collateral exposure                  |
| Lock-up | None                                         | None (subject to Midas redemption schedule) |

***

### Lending Side (Passive)

**How it works:** Deposit USDC into the Gearbox pool. Earn yield from borrowers who use Credit Accounts to execute carry trades, borrowing at pool rates to deploy into higher-yielding RWA collateral. Gearbox solvency guardrails protect against borrower default.

**Deposit here:** [Gearbox USDC Pool](https://app.gearbox.finance/pools/143/0x6b343f7b797f1488aa48c49d540690f2b2c89751)

***

### Leverage Side (Active)

**How it works:** Open a Credit Account, borrow USDC, and deploy into Midas collaterals. Capture the full carry trade spread with leverage.

**Yield source:** Direct exposure to mEDGE yield minus borrow cost. Net APY can reach 20% at max leverage (\~7x).

**Zero slippage execution:** Gearbox direct integration allows entry/exit without DEX slippage. Redemptions execute at NAV.

→ [How Direct Redemptions Work](https://docs.gearbox.finance/about-gearbox/reference/direct-redemptions)

**Open position here:** [mEDGE Leverage Strategy](https://app.gearbox.finance/strategies/open/143/0x1c8ee940b654bfced403f2a44c1603d5be0f50fa)

***

### Risk Framework

#### Collateral Exposure: mEDGE

Both sides have exposure to mEDGE (Midas EDGE vault). Current composition:

→ [View mEDGE Holdings](https://midas.app/medge)

#### What happens if mEDGE depegs?

| Scenario          | Lending Side                                            | Leverage Side               |
| ----------------- | ------------------------------------------------------- | --------------------------- |
| Depeg <13%        | Protected: liquidations trigger, borrowers absorb loss. | Position may be liquidated. |
| Orderly wind-down | Redemptions via direct integration at NAV               | Exit at NAV, no slippage    |

#### Gearbox Solvency Guardrails

* **LTV limits:** Credit Accounts enforce max leverage
* **Liquidation threshold:** Positions liquidated before insolvency
* **Price feeds:** Oracle-based with sanity checks
* **Audits:** [Security repo](https://github.com/Gearbox-protocol/security/tree/main/audits)

***

### Summary

|           | Lending                                                                                  | Leverage                                                                                               |
| --------- | ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| Target LP | Passive yield seekers                                                                    | Active DeFi users                                                                                      |
| APY       | 6-9%                                                                                     | Up to 20%                                                                                              |
| Risk      | Lower (liquidation buffer)                                                               | Higher (direct exposure)                                                                               |
| Effort    | Deposit & forget                                                                         | Manage position                                                                                        |
| Deposit   | [Pool](https://app.gearbox.finance/pools/143/0x6b343f7b797f1488aa48c49d540690f2b2c89751) | [Strategy](https://app.gearbox.finance/strategies/open/143/0x1c8ee940b654bfced403f2a44c1603d5be0f50fa) |

***

## Gearbox LP Demo Day – Blurb

**Project:** Gearbox Protocol

**Project Description:** Composable leverage protocol with Credit Accounts enabling undercollateralized on-chain borrowing. Two LP opportunities on RWA yield strategies:

* **Lending side:** Passive yield from borrower demand (6-9% APY)
* **Leverage side:** Active carry trade via Credit Accounts (up to 20% APY)

**Max TVL capacity:** 50M USDC in mid-term (nearest month) until considerable yield dilution.\
Further expansion driven by new collaterals addition.

**Yield APY:** 6-9% (lending) / up to 20% (leverage)

**Source of yield:** Carry trade between Gearbox borrow rates and Midas RWA collateral (mEDGE). Lenders earn borrow interest + MON incentives; leverage users capture full carry.

**Duration of deal:** No lock-up

**Audit link:** https://github.com/Gearbox-protocol/security/tree/main/audits

**Your contact:** Telegram - @OxIlya
