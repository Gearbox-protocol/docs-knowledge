# Audits & Bug Bounty

{% hint style="warning" %}
Keep in mind that no number of audits can guarantee full safety. There are always high risks involved in DeFi, as many platforms are composable and depend on each other. There is no guaranteed return on Gearbox - you must **understand the risks involved**.
{% endhint %}

## Audits

<figure><img src="../.gitbook/assets/Gearbox Protocol GEAR audits ABDK Chain Security Sigma Prime MixBytes.PNG" alt=""><figcaption></figcaption></figure>

Gearbox protocol and its modules have been audited multiple times by top-tier security teams.

For the full up-to-date list of contracts and reports please refer to [Bytecode Repository](https://permissionless.gearbox.foundation/bytecode), which acts as a source of truth for verification of each deployed contract.

***

## Bug Bounty

The scope of the bug bounty refers to these contracts:

{% embed url="https://github.com/Gearbox-protocol/security/tree/main/bug-bounty" %}

Rewards are distributed according to the impact of the vulnerability. The final decision on the payout amount will be determined by the Gearbox DAO developers at their discretion.

<table><thead><tr><th>Severity</th><th>Payment in USDC / other stablecoin</th><th data-hidden></th></tr></thead><tbody><tr><td>Low</td><td>$100 - $1K</td><td></td></tr><tr><td>Medium</td><td>$1K - $5K</td><td></td></tr><tr><td>High</td><td>$5K - $20K</td><td></td></tr><tr><td>Critical</td><td>$20K - $200K (+ GEAR)</td><td></td></tr></tbody></table>

{% hint style="info" %}
For all assets labeled as “Gearbox v1” or "Gearbox v2" and deployed on the Ethereum network, only Critical and High impacts are in-scope.

If you have found a bug that you think is within the security interests of the protocol but is outside of the scope of the repository above, please do notify us then anyway. We can decide ad-hoc together with you. 1/1 payouts have been done before based on this.
{% endhint %}

Join the Bug Bounty with Immunefi! Help Gearbox stay safe and be rewarded for it.

<figure><img src="../.gitbook/assets/Screenshot 2022-10-28 at 14.59.10.png" alt=""><figcaption><p><a href="https://immunefi.com/bounty/gearbox/">https://immunefi.com/bounty/gearbox/</a></p></figcaption></figure>

If you need more information on the protocol, please check:&#x20;

* Regular protocol docs: [https://docs.gearbox.finance/ ](https://docs.gearbox.finance/)
* Developer docs: [https://docs.gearbox.fi/dev](https://docs.gearbox.fi/dev)

**NOTE**: for bugs related to the interface which are just referring to typos and non-security related issues, please feel free to report them in a community [Discord](https://discord.gg/5YuHH9tvms) pro bono - and Gearbox community can maybe send nice GIFs your way. In case a bug you found is related to the interface and is outside of the scope, but has serious security concerns, please do report it as well and a bounty can be also decided ad-hoc. Again, you can ask all your questions in [Discord](https://discord.gg/JZgvmaenwn).

### Rules

{% hint style="info" %}
Determinations of eligibility, score and all terms related to an award are at the sole and final discretion of Gearbox Protocol working DAO members. The goal is to make sure the ecosystem is safe, and that proper bug bounty work is rewarded well.
{% endhint %}

In order to be considered for a reward, all bug reports must contain the following:&#x20;

* Description of suspected vulnerability&#x20;
* Steps to reproduce the issue so we can check it&#x20;
* Your name and/or colleagues if you wish to be later recognized&#x20;
* (Optional) A patch and/or suggestions to resolve the vulnerability

The following activities are **prohibited** by bug bounty program:&#x20;

* Testing with mainnet or public testnet contracts: all testing should be done on private testnets
* Any testing with pricing oracles or third party smart contracts&#x20;
* Attempting phishing or other social engineering attacks against our employees and/or customers&#x20;
* Any testing with third party systems and applications (e.g. browser extensions) as well as websites (e.g. SSO providers, advertising networks)&#x20;
* Any denial of service attacks&#x20;
* Automated testing of services that generates significant amounts of traffic&#x20;
* Public disclosure of an unpatched vulnerability in an embargoed bounty

{% hint style="success" %}
Security is a continuous effort which must always be following protocol growth. As a DAO, it is imperative to constantly dedicate ample resources to ensure safety of funds.
{% endhint %}
