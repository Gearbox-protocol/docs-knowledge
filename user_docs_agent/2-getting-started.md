# Getting Started

Welcome to Gearbox. This guide will help you get up and running smoothly. You'll learn how to connect your wallet, switch between networks, navigate the interface, and take the safety precautions that matter most when working with DeFi protocols.

Getting started doesn't take long—just a few minutes to connect your wallet and familiarize yourself with the interface, and then you'll be ready to explore lending pools or open your first Credit Account. Let's walk through the essentials step by step.

## Wallets & Networks

Before you dive in, you'll need a Web3 wallet and to understand which networks Gearbox supports. The good news is that Gearbox works with standard EVM-compatible wallets you probably already use.

### Supported networks

Gearbox Protocol is deployed on several EVM-compatible networks. At the time of writing, the application lists the following networks in the network selector on the **Borrow** page: **Ethereum**, **Arbitrum One**, **OP Mainnet**, **Sonic**, **BNB Smart Chain**, **Etherlink**, **Hemi**, **Lisk** and **Plasma**. New networks may be added or removed over time, so always check the network selector for the current list.

Different networks may offer different pools, assets and incentives. For example, some pools are only deployed on Ethereum while others appear on Arbitrum or other chains. You can filter pools by network on the **Earn** page using the **All Networks** dropdown to see which pools exist on each chain.

### Connect a wallet

Connecting your wallet is the first concrete step. Gearbox works with common Web3 wallets such as **MetaMask** and any wallet that uses the **WalletConnect** protocol. To connect:

1. Open the Gearbox app and look at the top-right corner of the header. If no wallet is connected, you'll see a **Connect wallet** button. Click it.  
2. The app will display a modal with supported wallets (typically **MetaMask** and **WalletConnect**). Choose the wallet you use and approve the connection in your wallet software.  
3. Once connected, the **Connect wallet** button is replaced by your truncated address (for example, `0xf39F…2266` in the dev environment) and a small network indicator. This confirms that Gearbox is connected to your wallet and shows which network you are currently using.

After connecting, verify that the address shown in the header matches your wallet and that the network indicator matches the chain you expect. If something looks wrong, disconnect in your wallet and reconnect to the correct site.

### Switch network in app

If you need to use Gearbox on a different chain—perhaps to access a pool on Arbitrum or to borrow assets on Optimism—you can switch networks directly within the app. The network selector is located on the **Borrow** page next to the **Multicollateral Loans** header. Click the **Network** dropdown and choose the desired chain from the list. Selecting a network will trigger a request in your wallet to switch to that chain. Approve the network switch in your wallet and the interface will reload showing pools and assets for the new chain.

Gearbox does not automatically convert your gas tokens, so make sure you have the native token required to pay transaction fees on the target chain (e.g. **ETH** for Ethereum, Arbitrum and OP Mainnet; **BNB** for BNB Smart Chain; **SONIC** for Sonic). You can always view your current network indicator in the top-right header next to your wallet address.

### Gas requirements

Every transaction on Gearbox requires gas fees, which are paid in the native token of whichever network you're using. Gas fees go directly to the network, not to Gearbox, and costs can vary significantly based on network congestion and the complexity of your transaction.

Before starting any transaction, check that you have sufficient gas tokens in your wallet. If you're planning multiple operations, it's wise to ensure you have enough gas for the full sequence to avoid interruptions mid-process.

### Where to see balances

Your token balances are always visible in your wallet, but the Gearbox interface also surfaces them when they're relevant. On the **Earn** page, each pool row contains a **Your Balance** column showing how many pool tokens you hold or how much you have deposited. On the **Dashboard** page, your positions in pools are listed with a **Your Balance** column summarizing your deposits and collateral. When opening a Credit Account, the **Select Collateral** table lists your **Wallet balance** for each accepted collateral asset so you can see what is available to pledge. These indicators let you confirm balances without constantly switching to your wallet.

## Interface tour

The Gearbox interface is organized into clear sections that help you navigate different functions without getting lost. Here's a tour of the key areas you'll be using.

### Pools

The **Pools** section is where passive income happens. Here you can view all available lending pools, see current APY rates, check pool utilization levels, and manage your deposits and withdrawals.

To reach the Pools page, click **Earn** in the top navigation bar. The page lists each pool along with its underlying asset, total supply, current **Supply APY**, how much has been borrowed, and a **Your Balance** column showing your position. Buttons on each row allow you to **Deposit** or **Withdraw**, and a network filter in the upper left lets you display pools by chain.

### Credit Account

The **Credit Account** section is where leverage comes to life. Here you open new Credit Accounts, view your existing accounts, monitor your Health Factor and perform all the operations that leverage enables—swapping assets, farming with borrowed funds, managing positions, and more.

To open or manage a Credit Account, choose **Borrow** from the top navigation. This takes you to the **Multicollateral Loans** page where you select the asset you want to borrow and the collateral you will provide. After opening a Credit Account, you can manage it from the same **Borrow** section: tabs such as **Swap**, **Farm** and **Manage** let you exchange assets, deploy leverage into yield farming strategies, adjust your leverage or collateral, and close the account. The account overview shows your **Health Factor** prominently so you always know where you stand relative to liquidation risk.

### History

In earlier versions of Gearbox there was a separate **History** page showing all your past transactions with status and links to block explorers. In the current permissionless interface there is no dedicated history tab. Instead, you can review your transaction history directly in your wallet or by using a block explorer such as Etherscan. When you perform operations like deposits or borrowings, the app will provide transaction hashes that you can click to open in the relevant block explorer, allowing you to verify confirmations and details on-chain.

### Settings

The **Settings** panel lets you customise your experience and manage basic preferences. To access it, click the three-dot menu in the top-right corner of the header and select **Settings**. A modal appears with controls for **Slippage Tolerance** (percentage used for swaps), **Default Quota Reserve Additive** (extra buffer for reserved credit), and toggles to **Allow Permits** (permit signatures instead of on-chain approvals) and **Allow Analytics**. A drop-down at the bottom lets you choose **Rates normalization** (how rates are displayed) such as **Total Value**.

### Key indicators on top screens

Throughout the interface you'll see indicators designed to keep you informed at a glance. In the top header, your truncated wallet address appears next to a small network icon, confirming both your connection and the current chain. On the **Borrow** page, the right-hand panel of your Credit Account shows your **Health Factor** and liquidation price; these update in real time as you adjust leverage. On the **Pools** and **Dashboard** pages, each pool row displays current **Supply APY** and pool **utilization** percentages so you can gauge yield and risk. These visual cues mean you rarely need to navigate elsewhere to check vital status information.

## Safety first

Protecting your funds starts with good security practices. The following precautions are standard for DeFi, but they're worth emphasizing because they're the foundation of safe protocol interaction.

### Hardware wallet

For the best security, consider using a hardware wallet like Ledger or Trezor connected to your Web3 wallet software. Hardware wallets keep your private keys offline and require physical confirmation for transactions, dramatically reducing the risk of compromise even if your computer or phone is compromised.

If you're using a hardware wallet, connect it to your Web3 wallet before connecting to Gearbox. Always verify transaction details on your hardware device before confirming—never approve transactions blindly. And keep your recovery phrase secure, stored offline, and never share it with anyone.

### Site verification

Always verify you're on the official Gearbox website before connecting your wallet or approving any transactions. The official domain for Gearbox is **gearbox.fi**; bookmark this URL and check for the padlock icon in your browser's address bar indicating a valid SSL certificate. If the URL looks different, do not connect your wallet. When in doubt, follow links from the official documentation or GitHub to ensure you're on the correct site.

Never enter your seed phrase or private keys anywhere, including the Gearbox interface. Legitimate protocols never ask for this information. If something asks for your seed phrase, it's a scam—disconnect immediately and verify you're on the legitimate site.

### Network checks

Before interacting with the protocol, verify you're on the correct network. Check the network name in both your wallet and the Gearbox interface (the network icon next to your address). Contract addresses should match the official deployment list published by Gearbox; you can find the current addresses in the **Deployment addresses** section of the docs. Always ensure you have enough gas on the chosen chain before initiating transactions.

If something looks wrong or addresses don't match what you expect, disconnect immediately and verify you're on the legitimate site. It's better to double-check than to risk interacting with a malicious contract.

### Basic key hygiene

Protecting your wallet comes down to basic good practices. Never share your private keys or seed phrase with anyone—ever. Use strong, unique passwords for wallet software. Enable two-factor authentication where available. Be cautious of phishing attempts through fake websites or suspicious links. Keep your wallet software updated to benefit from the latest security improvements.

Consider using separate wallets for different purposes—maybe one for testing and experimentation and another for your main funds. This way, even if something goes wrong during exploration, your primary capital remains isolated.

### Where to ask for help

If you have questions or encounter issues, there are multiple channels for support:

* **Discord** – join the Gearbox community at <https://discord.com/invite/gearbox> for general discussion and troubleshooting.  
* **Telegram** – the official Telegram channel is <https://t.me/GearboxProtocol>.  
* **Twitter/X** – follow project updates at <https://twitter.com/GearboxProtocol>.  
* **Documentation** – see the docs at <https://docs.gearbox.finance/> for FAQs and guides.  
* **GitHub** – technical issues can be reported on the GitHub repository at <https://github.com/Gearbox-protocol>.

If you suspect you've encountered a phishing site or security issue, disconnect your wallet immediately, report the issue through official channels, and verify you're on the legitimate site before reconnecting. Gearbox team members will never ask for your private keys or seed phrase—if someone does, it's a scam.

---

**Next steps:** Once you're set up and comfortable with the interface, the real fun begins. You can start by [depositing to pools](../earn-lend) to earn passive yields, or jump straight into [opening a Credit Account](../borrow-credit-accounts) to explore leverage. The choice is yours.