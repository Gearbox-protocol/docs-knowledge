# Audits and Bug Bounty

{% hint style="warning" %}
Keep in mind that no number of audits can guarantee full safety. There are always high risks involved in DeFi, as many platforms are composable and depend on each other. There is no guaranteed return on Gearbox - you must **understand the risks involved**.
{% endhint %}

### Audits

<figure><img src="https://2617978714-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FviVygst6ymEvrLTl74w1%2Fuploads%2F09JAlRjpp85Kb1CJ2hNQ%2FGearbox%20Protocol%20GEAR%20audits%20ABDK%20Chain%20Security%20Sigma%20Prime%20MixBytes.PNG?alt=media&#x26;token=cc7a03ed-6f16-4d90-b7dd-301acc70eebf" alt=""><figcaption></figcaption></figure>

Gearbox protocol and its modules have been audited multiple times by top-tier security teams.

For the full up-to-date list of contracts and reports please refer to [Bytecode Repository](https://permissionless.gearbox.foundation/bytecode), which acts as a source of truth for verification of each deployed contract.

***

### Bug Bounty

The scope of the bug bounty refers to these contracts:

Rewards are distributed according to the impact of the vulnerability. The final decision on the payout amount will be determined by the Gearbox DAO developers at their discretion.

<table><thead><tr><th>Severity</th><th>Payment in USDC / other stablecoin</th><th data-hidden></th></tr></thead><tbody><tr><td>Low</td><td>$100 - $1K</td><td></td></tr><tr><td>Medium</td><td>$1K - $5K</td><td></td></tr><tr><td>High</td><td>$5K - $20K</td><td></td></tr><tr><td>Critical</td><td>$20K - $200K (+ GEAR)</td><td></td></tr></tbody></table>

{% hint style="info" %}
For all assets labeled as “Gearbox v1” or "Gearbox v2" and deployed on the Ethereum network, only Critical and High impacts are in-scope.

If you have found a bug that you think is within the security interests of the protocol but is outside of the scope of the repository above, please do notify us then anyway. We can decide ad-hoc together with you. 1/1 payouts have been done before based on this.
{% endhint %}

Join the Bug Bounty with Immunefi! Help Gearbox stay safe and be rewarded for it.

<figure><img src="https://2617978714-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FviVygst6ymEvrLTl74w1%2Fuploads%2FCfi4VtNk7f6oNM5D88yd%2FScreenshot%202022-10-28%20at%2014.59.10.png?alt=media&#x26;token=3dbf03fc-c041-4c4f-846f-373a6d6f49b9" alt=""><figcaption><p><a href="https://immunefi.com/bounty/gearbox/">https://immunefi.com/bounty/gearbox/</a></p></figcaption></figure>

If you need more information on the protocol, please check:

* Regular protocol docs: [https://docs.gearbox.finance/](https://docs.gearbox.finance/)
* Developer docs: [https://docs.gearbox.fi/dev](https://docs.gearbox.fi/dev)

**NOTE**: for bugs related to the interface which are just referring to typos and non-security related issues, please feel free to report them in a community [Discord](https://discord.gg/5YuHH9tvms) pro bono - and Gearbox community can maybe send nice GIFs your way. In case a bug you found is related to the interface and is outside of the scope, but has serious security concerns, please do report it as well and a bounty can be also decided ad-hoc. Again, you can ask all your questions in [Discord](https://discord.gg/JZgvmaenwn).

#### Rules

{% hint style="info" %}
Determinations of eligibility, score and all terms related to an award are at the sole and final discretion of Gearbox Protocol working DAO members. The goal is to make sure the ecosystem is safe, and that proper bug bounty work is rewarded well.
{% endhint %}

In order to be considered for a reward, all bug reports must contain the following:

* Description of suspected vulnerability
* Steps to reproduce the issue so we can check it
* Your name and/or colleagues if you wish to be later recognized
* (Optional) A patch and/or suggestions to resolve the vulnerability

The following activities are **prohibited** by bug bounty program:

* Testing with mainnet or public testnet contracts: all testing should be done on private testnets
* Any testing with pricing oracles or third party smart contracts
* Attempting phishing or other social engineering attacks against our employees and/or customers
* Any testing with third party systems and applications (e.g. browser extensions) as well as websites (e.g. SSO providers, advertising networks)
* Any denial of service attacks
* Automated testing of services that generates significant amounts of traffic
* Public disclosure of an unpatched vulnerability in an embargoed bounty

{% hint style="success" %}
Security is a continuous effort which must always be following protocol growth. As a DAO, it is imperative to constantly dedicate ample resources to ensure safety of funds.
{% endhint %}

***

## Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://docs.gearbox.finance/about-gearbox/economics-and-risk/audits-and-bug-bounty.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language. The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
