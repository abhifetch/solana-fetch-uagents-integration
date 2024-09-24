# Solana Agent Integration with Fetch.ai's uAgents

This repository demonstrates how to integrate Solana wallet functionality into Fetch.ai’s uAgents framework, create and manage wallets, recharge them via a faucet, and use them in decentralized applications (dApps). Follow the steps below to set up the project, create a wallet, and implement the uAgents integration.

# Table of Contents

- [Setup](#setup)
- [Cloning the Repository](#cloning-the-repository)
- [Installing Dependencies](#installing-dependencies)
- [Solana Wallet Setup](#solana-wallet-setup)
- [Storing Keypairs in Environment Variables](#storing-keypairs-in-environment-variables)
- [Running the Agents](#running-the-agents)

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
### Output
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
export CHALLENGER_SECRET_LIST="[134,53,148,91,88,30,254,53,171,183,219,91,33,67,24,9,65,70,128,231,136,243,156,242,28,154,86,57,52,74,95,78,17,144,169,154,136,6,134,127,249,191,120,216,68,210,15,4,143,224,8,93,96,31,109,175,98,167,196,18,140,79,159,33]"
```

### Note : These wallets are just for educational purpose

## 5. How to Use Environment Variables for Keypair Access

The agents will retrieve the keypair and public key from the environment variables during runtime and decode them for operations like checking balances, making transfers, and placing bids.

## 6. Running the Agents

Start the three agents: `PlayerAgent`, `ChallengerAgent`, and `EscrowAgent`.



- EscrowAgent receives and evaluates bids. (First Run this one)
- PlayerAgent simulates a user making a bet. (then run this and let it execute fully)
- ChallengerAgent simulates an opponent making a bet. (once player agent is executed then run this one)
   
```
poetry run python player_agent.py
poetry run python challenger_agent.py
poetry run python escrow_agent.py
```
### Output at escrow
```
(venv) abhimanyugangani@Abhimanyus-MacBook-Pro agents % python3 escrow_agent.py
INFO:     [EscrowAgent]: Registration on Almanac API successful
INFO:     [EscrowAgent]: Almanac contract registration is up to date!
INFO:     [EscrowAgent]: Escrow agent initialized, ready for bids.
INFO:     [EscrowAgent]: Escrow agent address: agent1qd6ts50kuy3vqq36s5yg2dkzujq60x0l0sr2acfafnp5zea749yvvvq2qm7
INFO:     [EscrowAgent]: Starting server on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     [EscrowAgent]: Received escrowRequest message
INFO:     [EscrowAgent]: Current bid count: 0
INFO:     [EscrowAgent]: Storing first request with amount: 0.5, price: 65000.0, sender: agent1qwahxahxaryt234ewwumy2d3uzuwgazfz7ng6m7mun00raqxa4gavzz37nj
INFO:     [EscrowAgent]: Received escrowRequest message
INFO:     [EscrowAgent]: Current bid count: 1
INFO:     [EscrowAgent]: Storing second request with amount: 0.5, price: 650000.0, sender: agent1qdm4753vsgfdrlk7l6g77vqtglv3uq8fqw9jfucm50zs3khuuff95szvtyh
INFO:     [EscrowAgent]: Processing bids to determine the winner.
INFO:     [EscrowAgent]: First request details: {'amount': 0.5, 'price': 65000.0, 'public_key': 'GnmWZeouyoqqae5HUTcCMJpgfoYG9J1umtdG391ZEBg5', 'sender': 'agent1qwahxahxaryt234ewwumy2d3uzuwgazfz7ng6m7mun00raqxa4gavzz37nj'}
INFO:     [EscrowAgent]: Second request details: {'amount': 0.5, 'price': 650000.0, 'public_key': '2BZsXTXMCcPbcHEM6LVM5BoxCKfRZS1qcuuNw7AB54dn', 'sender': 'agent1qdm4753vsgfdrlk7l6g77vqtglv3uq8fqw9jfucm50zs3khuuff95szvtyh'}
INFO:     [EscrowAgent]: Latest BTC price: 63180.0
INFO:     [EscrowAgent]: First bid difference: 1820.0, Second bid difference: 586820.0
INFO:     [EscrowAgent]: Total amount: 1.0, Amount to send to winner: 0.9
INFO:     [EscrowAgent]: Transferring 0.9 SOL to winner with public key: GnmWZeouyoqqae5HUTcCMJpgfoYG9J1umtdG391ZEBg5
INFO:httpx:HTTP Request: POST https://api.devnet.solana.com "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.devnet.solana.com "HTTP/1.1 200 OK"
INFO:solanaweb3.rpc.httprpc.HTTPClient:Transaction sent to https://api.devnet.solana.com. Signature 5cv66DLBSNTKtEPd1KmnMgy5vamn7AGBjLCjEjRii5q1bjjdR282CDxXhUSS6GJwVTKJbpRRDdykzb9YJaLw3W87: 
INFO:httpx:HTTP Request: POST https://api.devnet.solana.com "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.devnet.solana.com "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.devnet.solana.com "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.devnet.solana.com "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.devnet.solana.com "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.devnet.solana.com "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.devnet.solana.com "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.devnet.solana.com "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.devnet.solana.com "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.devnet.solana.com "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.devnet.solana.com "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.devnet.solana.com "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.devnet.solana.com "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.devnet.solana.com "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.devnet.solana.com "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.devnet.solana.com "HTTP/1.1 200 OK"
INFO:     [EscrowAgent]: Notifying winner and loser.
INFO:     [EscrowAgent]: Resetting bids count and clearing stored bid details.
```

### Output at sample agent

```
(venv) abhimanyugangani@Abhimanyus-MacBook-Pro solana_uagents % python3 agents/player_agent.py
INFO:     [PlayerAgent]: Registration on Almanac API successful
INFO:     [PlayerAgent]: Almanac contract registration is up to date!
INFO:httpx:HTTP Request: POST https://api.devnet.solana.com "HTTP/1.1 200 OK"
balance_resp :GetBalanceResp { context: RpcResponseContext { slot: 328266494, api_version: Some("2.0.8") }, value: 4819985000 }
INFO:     [PlayerAgent]: GnmWZeouyoqqae5HUTcCMJpgfoYG9J1umtdG391ZEBg5
INFO:     [PlayerAgent]: Initial agent balance: 4.819985 SOL
What is the amount of SOL you want to deposit? 0.5
What is the price of Bitcoin you want to bid at? 65000
INFO:     [PlayerAgent]: Placing bet of 0.5 SOL on Bitcoin at 65000.0$ with wallet address: GnmWZeouyoqqae5HUTcCMJpgfoYG9J1umtdG391ZEBg5
INFO:     [PlayerAgent]: Transferring 0.5 SOL to 8WMWFo13At1REkwy5t7ck6sLgCUrJ9dn66mbaccPiJ26
INFO:httpx:HTTP Request: POST https://api.devnet.solana.com "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.devnet.solana.com "HTTP/1.1 200 OK"
INFO:solanaweb3.rpc.httprpc.HTTPClient:Transaction sent to https://api.devnet.solana.com. Signature 4VGbzh1N6QX3DnfLXXhcbiU78FR4v3aLphEQqbxjBaqEthsoABMDeKFdTPKEwPzsY2muC7jRNziZJKX7e2wAfhsD: 
INFO:httpx:HTTP Request: POST https://api.devnet.solana.com "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.devnet.solana.com "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.devnet.solana.com "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.devnet.solana.com "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.devnet.solana.com "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.devnet.solana.com "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.devnet.solana.com "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.devnet.solana.com "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.devnet.solana.com "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.devnet.solana.com "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.devnet.solana.com "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.devnet.solana.com "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.devnet.solana.com "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: POST https://api.devnet.solana.com "HTTP/1.1 200 OK"
INFO:     [PlayerAgent]: Transfer result: SendTransactionResp(Signature(4VGbzh1N6QX3DnfLXXhcbiU78FR4v3aLphEQqbxjBaqEthsoABMDeKFdTPKEwPzsY2muC7jRNziZJKX7e2wAfhsD))
INFO:httpx:HTTP Request: POST https://api.devnet.solana.com "HTTP/1.1 200 OK"
balance_resp :GetBalanceResp { context: RpcResponseContext { slot: 328266551, api_version: Some("2.0.8") }, value: 4319980000 }
INFO:     [PlayerAgent]: Final agent balance: 4.31998 SOL
INFO:     [PlayerAgent]: Starting server on http://0.0.0.0:8001 (Press CTRL+C to quit)
INFO:httpx:HTTP Request: POST https://api.devnet.solana.com "HTTP/1.1 200 OK"
balance_resp :GetBalanceResp { context: RpcResponseContext { slot: 328266695, api_version: Some("2.0.8") }, value: 5219980000 }
INFO:     [PlayerAgent]: You Won. Updated account balance: 5.21998 SOL
```
