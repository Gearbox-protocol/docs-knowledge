# Instance activation guidlines

#### TL;DR (Actionable checklist)

1. Chain's block Gas Limit ≥ 30M (it's possible to execute transaction that uses 30M gas)
2. Canonical safe proxy factory v1.4.1 (0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67) is verified
3. $GEAR address is either null or can be verified on block explorer to be $GEAR token correctly bridged from Ethereum
4. Wrapped Gas Token address is listed on Chain's docs as canonical
5. Instance Owner Safe Proxy is deployed on target chain and can be verified on block explorer
6. Financial Multisig Safe Proxy is deployed on target chain and can be verified on block explorer

⚠️ If any of these criteria aren’t met: don’t sign, ask in chat for clarification.

{% hint style="info" %}
Chain sync process involves uploading all the bytecode of used contracts to Bytecode Repository (like onchain github for secure deployment of all the modules)\
\
Here is an example of sync txs on Optimism: [https://optimistic.etherscan.io/txs?a=0xc93155e0a835cf4e17a19463fa67ed43c164d06a\\\\](https://optimistic.etherscan.io/txs?a=0xc93155e0a835cf4e17a19463fa67ed43c164d06a\\\\)\
\
The process is gas- and txs- extensive, and requires \~400M of gas and RPC with 10k blocks per getLogs request.
{% endhint %}
