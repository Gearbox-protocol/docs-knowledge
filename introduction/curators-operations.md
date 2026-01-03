# Curator's operations

Morpho has pioneered the concept of curated lending markets in DeFi, but its approach differs significantly from Gearbox's model. Below is a clear comparison of how curators function in each protocol:

#### Morpho: Active Capital Allocation

In Morpho, curators are active capital allocators. They:

* Distribute depositors' funds across various yield-generating markets.
* Operate within markets defined by immutable parameters, such as Loan-to-Value (LTV) ratios and oracles.

#### Gearbox: Risk Parameter Management

In Gearbox, curators have a more limited role, focusing solely on risk management. They:

* Set risk parameters for markets, such as LTV ratios or liquidation thresholds.
* Have no authority to move or allocate depositors' funds, which remain under user or protocol control.

| Action                                            | Gearbox                                                                                                                                      | Morpho                                                                                                                                                                                                                                                  |
| ------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Add exposure to new collateral                    | <ol><li>Set collateral limit, LTV and oracle for a new token in Market</li><li>Borrowers can now use pool's liquidity</li></ol>              | <ol><li>Add nonzero supply cap for existing market (LTV and oracle are pre-configured)</li><li>Deposit vault's funds to the new market</li><li>Borrowers can now use vault's liquidity</li></ol>                                                        |
| Modify collateral LTV or Price Feed               | <ol><li>Set new price feed</li><li>Start ramp of LTV to target value</li><li>Feed &#x26; LTV for old and new borrowers are changed</li></ol> | <ol><li>Deploy a market with needed LTV and oracle and set nonzero supply cap for it</li><li>Feed &#x26; LTV are changed only for new borrowers</li><li>Start withdrawing liquidity from old market &#x26; push borrowers out by raising rate</li></ol> |
| Increase/decrease collateral-specific borrow rate | <ol><li>Set a new collateral-specific rate in addition to IRM utilization rate</li></ol>                                                     | <ol><li>Move vault's allocation in/out of the Market to move dynamic IRM</li></ol>                                                                                                                                                                      |
| Enable 1-click leverage for a collateral          | <ol><li>Allow the list of needed adapters in the Market</li></ol>                                                                            | <ol><li>Contact contango or another strategy provider to integrate your collateral</li></ol>                                                                                                                                                            |
