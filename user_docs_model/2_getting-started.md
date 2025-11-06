# Getting Started

Welcome to Gearbox. This guide will help you get up and running smoothly. You'll learn how to connect your wallet, switch between networks, navigate the interface, and take the safety precautions that matter most when working with DeFi protocols.

Getting started doesn't take long—just a few minutes to connect your wallet and familiarize yourself with the interface, and then you'll be ready to explore lending pools or open your first Credit Account. Let's walk through the essentials step by step.

## Wallets & Networks

Before you dive in, you'll need a Web3 wallet and to understand which networks Gearbox supports. The good news is that Gearbox works with standard EVM-compatible wallets you probably already use.

### Supported networks

Gearbox Protocol is deployed on multiple EVM-compatible networks, and the exact list may change over time.

Keep in mind that different networks may have different pools, assets, and features available. The interface makes it easy to switch between networks, and you'll see which networks support which functionality as you explore.

VERIFY: confirm supported networks in current app

### Connect a wallet

Connecting your wallet is the first concrete step. Gearbox works with any compatible Web3 wallet—MetaMask, WalletConnect, or other EVM-compatible options you might prefer.

Once you click connect and approve the connection, you should see your wallet address displayed in the interface, along with the network you're currently on and your token balances for that network. Everything should be visible in the top-right area of the interface, so you always know your connection status at a glance.

TODO: Add exact steps for connecting wallet in current UI, including button location and supported wallet types

After connecting, take a moment to verify everything looks correct. Your address should match what you see in your wallet software, and the network should match where you intend to operate. If anything seems off, disconnect and reconnect to ensure you're connecting to the legitimate Gearbox interface.

VERIFY: After connecting, your address and network are visible in the top-right area of the interface

### Switch network in app

If you need to use Gearbox on a different network—maybe you want to trade on Arbitrum for lower fees or access a specific asset on Optimism—you can switch networks directly in the app interface.

TODO: Add exact location and steps for switching networks in the current UI

When you select a different network, the app will typically prompt your wallet to switch as well. Make sure you have enough native gas token for the selected network. Gas requirements and the exact token vary by network.
VERIFY: confirm gas token requirements per network in the current app

### Gas requirements

Every transaction on Gearbox requires gas fees, which are paid in the native token of whichever network you're using. Gas fees go directly to the network, not to Gearbox, and costs can vary significantly based on network congestion and the complexity of your transaction.

Before starting any transaction, check that you have sufficient gas tokens in your wallet. If you're planning multiple operations, it's wise to ensure you have enough gas for the full sequence to avoid interruptions mid-process.

### Where to see balances

Your token balances are always visible in your wallet, but the Gearbox interface also shows relevant balances when they matter. When you're depositing to pools, you'll see your available balance. When opening Credit Accounts, you'll see your collateral balance. When performing swaps, you'll see balances for the tokens involved.

TODO: Add exact locations in UI where balances are displayed

The interface makes it easy to see what you have available without constantly switching to your wallet software. If you need more detail, your wallet interface remains the source of truth for your complete balance information.

VERIFY: Token balances are shown in transaction forms and account overview screens

## Interface tour

The Gearbox interface is organized into clear sections that help you navigate different functions without getting lost. Here's a tour of the key areas you'll be using.

### Pools

The Pools section is where passive income happens. This is where you can view all available lending pools, see current APY rates, check pool utilization levels, and manage your deposits and withdrawals.

When you navigate to Pools, you'll see a clear overview of what's available—which assets you can deposit, what kind of yields are being offered, and how much of each pool is currently being used by borrowers. This information helps you make informed decisions about where to allocate your capital.

TODO: Add exact navigation path to Pools section (e.g., top menu, sidebar, main dashboard)

SCREENSHOT: Pools page showing available pools, APY rates, and deposit/withdraw options

### Credit Account

The Credit Account section is where leverage comes to life. This is where you open new Credit Accounts, view your existing accounts, monitor your Health Factor, and perform all the operations that leverage enables—swapping assets, farming with borrowed funds, managing positions, and more.

The Credit Account interface typically organizes actions into clear tabs: Swap for exchanging assets within your account, Farm for deploying leverage into yield farming strategies, and Manage for adjusting leverage, adding collateral, or closing accounts when you're ready to exit.

Everything you need to manage your leveraged positions lives in this section, with your Health Factor prominently displayed so you always know where you stand relative to liquidation risk.

TODO: Add exact navigation path to Credit Account section

SCREENSHOT: Credit Account dashboard showing account overview, Health Factor, and available actions

### History

The History section gives you a clear record of everything you've done. You can see your deposits and withdrawals from pools, all your Credit Account operations, swaps, and other actions, along with transaction status and confirmation details.

This transparency is valuable when you're managing multiple positions or simply want to review your activity. Each transaction should be linkable to block explorers, so you can verify everything on-chain if you need deeper detail.

TODO: Add exact navigation path to History section

VERIFY: History shows transactions with status (pending, confirmed, failed) and links to block explorers

### Settings

The Settings section typically includes wallet connection status, network selection options, app preferences, and links to documentation and support channels. It's where you manage the fundamentals of your Gearbox experience.

TODO: Add exact navigation path to Settings and what options are available

### Key indicators on top screens

Throughout the interface, you'll see important indicators that keep you informed at a glance. Your connected wallet address shows which wallet is active. The network indicator shows which blockchain you're operating on. For Credit Accounts, your Health Factor is prominently displayed so you can monitor account health easily. APY displays show current yield rates for pools, and pool utilization metrics show how much of each pool is being borrowed.

These indicators are designed to give you the information you need without requiring you to dig through multiple screens.

TODO: Add exact locations and appearance of these indicators in the current UI

SCREENSHOT: Top bar or header showing wallet address, network, and key indicators

## Safety first

Protecting your funds starts with good security practices. The following precautions are standard for DeFi, but they're worth emphasizing because they're the foundation of safe protocol interaction.

### Hardware wallet

For the best security, consider using a hardware wallet like Ledger or Trezor connected to your Web3 wallet software. Hardware wallets keep your private keys offline and require physical confirmation for transactions, dramatically reducing the risk of compromise even if your computer or phone is compromised.

If you're using a hardware wallet, connect it to your Web3 wallet before connecting to Gearbox. Always verify transaction details on your hardware device before confirming—never approve transactions blindly. And keep your recovery phrase secure, stored offline, and never share it with anyone.

### Site verification

Always verify you're on the official Gearbox website before connecting your wallet or approving any transactions. Check that the URL matches the official domain, look for SSL certificate indicators like the padlock icon in your browser, and bookmark the official site to avoid phishing attempts.

TODO: Add official Gearbox website URL and how to verify (SSL certificate, domain verification, etc.)

Never enter your seed phrase or private keys anywhere, including the Gearbox interface. Legitimate protocols never ask for this information. If something asks for your seed phrase, it's a scam—disconnect immediately and verify you're on the legitimate site.

### Network checks

Before interacting with the protocol, verify you're on the correct network. Check the network name in both your wallet and the app interface. Confirm that contract addresses match the official deployments list. Double-check that you have enough gas for the network you're using.

TODO: add link to official deployments list

If something looks wrong or addresses don't match what you expect, disconnect immediately and verify you're on the legitimate site. It's better to take a moment to double-check than to risk interacting with a malicious contract.

### Basic key hygiene

Protecting your wallet comes down to basic good practices. Never share your private keys or seed phrase with anyone—ever. Use strong, unique passwords for wallet software. Enable two-factor authentication where available. Be cautious of phishing attempts through fake websites or suspicious links. Keep your wallet software updated to benefit from the latest security improvements.

Consider using separate wallets for different purposes—maybe one for testing and experimentation and another for your main funds. This way, even if something goes wrong during exploration, your primary capital remains isolated.

### Where to ask for help

If you have questions or encounter issues, there are multiple channels for support. The Discord community is active and helpful for general discussions and troubleshooting. Telegram provides another way to connect with other users. The documentation includes FAQ and troubleshooting sections that cover common issues. And for technical problems, GitHub is the place to report bugs.

TODO: Add actual links to Discord, Telegram, and other support channels

If you suspect you've encountered a phishing site or security issue, disconnect your wallet immediately, report the issue through official channels, and verify you're on the legitimate site before reconnecting. Remember: Gearbox team members will never ask for your private keys or seed phrase. If someone asks for this information, it's a scam.

---

**Next steps:** Once you're set up and comfortable with the interface, the real fun begins. You can start by [depositing to pools](../earn-lend) to earn passive yields, or jump straight into [opening a Credit Account](../borrow-credit-accounts) to explore leverage. The choice is yours.
