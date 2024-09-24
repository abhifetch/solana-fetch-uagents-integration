# Solana Agent Integration with Fetch.ai's uAgents

This repository demonstrates how to integrate Solana wallet functionality into Fetch.ai’s uAgents framework, create and manage wallets, recharge them via a faucet, and use them in decentralized applications (dApps). Follow the steps below to set up the project, create a wallet, and implement the uAgents integration.

# Table of Contents


# Setup 

Before starting, ensure you have the following installed:
- [Solana CLI](https://docs.solanalabs.com/cli/install)
- [uagents python package](https://fetch.ai/docs/guides/agents/quickstart)
- [Poetry](https://python-poetry.org/docs/) for managing dependencies
- Python 3.7+ with virtualenv

## 1. Clone the repository
```
git clone git@github.com:abhifetch/solana-agent.git
cd solana-agent
```
## 2.  Install Dependencies
```
poetry install
```

## 3. Solana Wallet Setup

- Run Below commands in your terminal

```
solana-keygen new --outfile ~/path-to-your-wallet/player-wallet.json
solana-keygen new --outfile ~/path-to-your-wallet/challenger-wallet.json
solana-keygen new --outfile ~/path-to-your-wallet/escrow-wallet.json
```

```
(venv) abhimanyugangani@Abhimanyus-MacBook-Pro solana-agent % solana-keygen new --outfile player-wallet.json 

Generating a new keypair

For added security, enter a BIP39 passphrase

NOTE! This passphrase improves security of the recovery seed phrase NOT the
keypair file itself, which is stored as insecure plain text

BIP39 Passphrase (empty for none): <your_own_passphrase>
Enter same passphrase again: <your_own_passphrase>

Wrote new keypair to player-wallet.json
===============================================================================
pubkey: 3h7PuwofmA4irJ4VxyDW4DWexgmBPeGKxXSTnV4My1Y9
===============================================================================
Save this seed phrase and your BIP39 passphrase to recover your new keypair:
olympic proud tumble region monster collect adapt exist adapt truth sun trigger
===============================================================================
(venv) abhimanyugangani@Abhimanyus-MacBook-Pro solana-agent %
```
This command will generate a wallet file with a secret key. Copy the Base64-encoded secret key from the JSON file for each wallet and store it in the .env file.

Recharge your wallet on [SOLANA Devnet Faucet](https://faucet.solana.com/) using your public key. Recharge all with 5 SOL on devnet.


## 4. Storing Keypairs in Environment Variables

Create a `.env` file in your project root directory to securely store keypairs.

```
touch .env
```

Add the Base64-encoded keypairs and public keys for each agent to the `.env` file:

```
# PlayerAgent keypair
PLAYER_AGENT_KEYPAIR=<"Base64EncodedSecretKey">
PLAYER_AGENT_PUBLIC_KEY=<"PlayerAgentPublicKeyBase58">

# ChallengerAgent keypair
CHALLENGER_AGENT_KEYPAIR=<"Base64EncodedSecretKey">
CHALLENGER_AGENT_PUBLIC_KEY=<"ChallengerAgentPublicKeyBase58">

# EscrowAgent keypair
ESCROW_AGENT_KEYPAIR=<"Base64EncodedSecretKey">
ESCROW_AGENT_PUBLIC_KEY=<"EscrowAgentPublicKeyBase58">
```

Make sure to never share this .env file publicly as it contains sensitive key information.

## 5. How to Use Environment Variables for Keypair Access

The agents will retrieve the keypair and public key from the environment variables during runtime and decode them for operations like checking balances, making transfers, and placing bids.

## 6. Running the Agents

Start the three agents: `PlayerAgent`, `ChallengerAgent`, and `EscrowAgent`.

- PlayerAgent simulates a user making a bet.
- ChallengerAgent simulates an opponent making a bet.
- EscrowAgent receives and evaluates bids.

```
poetry run python player_agent.py
poetry run python challenger_agent.py
poetry run python escrow_agent.py
```
