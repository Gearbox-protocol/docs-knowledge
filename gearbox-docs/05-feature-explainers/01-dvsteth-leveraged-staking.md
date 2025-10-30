:

1.  [Feature explainers](/gearbox-permissionless-doc/feature-explainers)

# DVstETH leveraged staking
:
Risks and mitigations[](#risks-and-mitigations)

:

***Liquidation from price volatility*** DVstETH price in terms of ETH doesn\'t depend on DEX or CEX prices, but is computed based on underlying vaults\' internal logic. Meaning that there is no risk of price volatility

-
:

-
:

:

DVstETH/wstETH exchange rate fetched directly from [DVstETH vault contract](https://etherscan.io/address/0x5E362eb2c0706Bd1d134689eC75176018385430B)
:

wstETH/stETH exchange rate fetched directly from [wstETH vault contract](https://etherscan.io/token/0x7f39c581f595b53c5cb19bd0b3f8da6c935e2ca0)
:

[Chainlink ETH/USD](https://etherscan.io/address/0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419)

:

***Slashing*** There is no additional risk of slashing in DVstETH, as it\'s not involved in restaking activities.
:

***Collateral yield/ borrowing cost timing mismatch*** Part of the collateral yield is delayed, but borrowing costs are charged in real time --- this mismatch can cause short-term losses and even liquidations, even with long-term yield being profitable.

-
:

-
:

Investors should match leverage to how often they claim rewards: active users who claim weekly can take higher leverage (\~21× for 7 days), while passive users who claim less often should use lower leverage (\~13× for 14 days or \~8× for 30 days) to avoid losses from delayed yield and real-time borrowing costs.

[[[Previous][Testing config on forks]]](/gearbox-permissionless-doc/step-by-step-guides/testing-config-on-forks)[[[Next][Seamless LP migration]]](/gearbox-permissionless-doc/feature-explainers/seamless-lp-migration)

Last updated 3 months ago