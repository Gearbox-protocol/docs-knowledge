# Usecase: Direct Redemptions

## The problem: constrained instant liquidity ⇒ leverage stops working properly

Other lending protocols must treat assets with timelocked liquidity like standard tokens and rely on DEX liquidity to enable leverage. Building and maintaining deep DEX liquidity is hard, leading to thin books and low collateral limits. Furthermore, asset issuers often have to pay to seed and maintain DEX liquidity.

{% hint style="warning" %}
**This leads to fragmented UX and capital-inefficiency**, forcing users to wait for weeks or pay months worth of yield for instant liquidity
{% endhint %}

<figure><img src="../.gitbook/assets/image (5).png" alt=""><figcaption></figcaption></figure>

## Gearbox's Solution

**Zero DEX Liquidity Required:** With Gearbox, leverage can go live on day one. It eliminates the need for DEX liquidity seeding, working at any size.

**Direct Integration:** Execution is handled through direct smart-contract integration, allowing deposits and withdrawals at face value.

**Benefits for users:**

* Save time up to **8 periods** of native redemption.
* Capital requirements are reduced by **10x**.
* Save fees equal to a **month of farming yield**.

## How it works

For simplicity, we refer to the example semi-liquid asset as xVAULT, since vaults are a common example of assets with these properties. The same logic also applies to RWAs, LRTs, and other tokens with time-locked liquidity.

<figure><img src="../.gitbook/assets/image (6).png" alt=""><figcaption></figcaption></figure>

### Take leverage

* User adds USDC to Credit Account and borrows 5x more to get leveraged exposure on xVAULT yield
* Credit Account deposits 6x USDC to xVAULT issuance contract and receives the xVAULT

### Undwind position

* The Credit Account holds an xVAULT token and has an outstanding USDC debt.
* The user starts the redemption process: Credit Account sends the xVAULT token to the redemption contract.
* In return, the Credit Account receives a redemption receipt token, which represents a future claim on the underlying asset.
* The Credit Account now holds the redemption receipt token and USDC debt.

#### After the Redemption Window:

* Once the redemption window has passed, the user can finalize the redemption.
* The Credit Account burns the redemption receipt token and receives USDC to repay debt.

{% hint style="success" %}
The Credit Account always stays overcollateralized, while collateral transfroms from xRWA into redemption receipt token and eventually into liquid underlying.
{% endhint %}

