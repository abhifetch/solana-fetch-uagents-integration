import base58
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.transaction import Transaction
from solders.system_program import TransferParams, transfer
from solana.rpc.api import Client
from solana.rpc.types import TxOpts
import requests

def get_keypair_details(secret_key_list):
    """
    Given a list of secret key bytes (integers), returns a dictionary with the keypair, public key,
    private key in bytes, and private key in Base58 encoding.
    """

    # Convert the list of integers into a bytes object (private key)
    secret_key_bytes = bytes(secret_key_list)

    # Restore the Keypair using the secret key
    keypair = Keypair.from_bytes(secret_key_bytes)

    # Public key (from keypair)
    public_key = keypair.pubkey()

    # Private key in Base58 encoding (for readability)
    private_key_base58 = base58.b58encode(secret_key_bytes).decode()

    # Return all necessary details in a dictionary
    return {
        "keypair": keypair,
        "public_key": public_key,  # Solders Pubkey object
        "private_key_bytes": secret_key_bytes,  # Private key in bytes
        "private_key_base58": private_key_base58  # Private key in Base58
    }

client = Client("https://api.devnet.solana.com")

# Function to check balance
def check_balance(pubkey):
    balance_resp = client.get_balance(Pubkey.from_bytes(bytes(pubkey)))
    print(f'balance_resp :{balance_resp}')
    balance = balance_resp.value  # Extract balance in lamports
    return balance / 1_000_000_000  # Convert lamports to SOL

def transfer_sol(from_keypair, to_pubkey_base58, amount_sol):
    # Convert SOL to lamports (1 SOL = 1 billion lamports)
    lamports = int(amount_sol * 1_000_000_000)

    # Convert the recipient's Base58 public key string to a Pubkey object
    to_pubkey = Pubkey.from_string(to_pubkey_base58)

    # Get latest blockhash
    blockhash_resp = client.get_latest_blockhash()
    recent_blockhash = blockhash_resp.value.blockhash

    # Create a transfer instruction
    transfer_instruction = transfer(
        TransferParams(from_pubkey=from_keypair.pubkey(), to_pubkey=to_pubkey, lamports=lamports)
    )

    # Create the transaction with the instruction directly
    transaction = Transaction.new_signed_with_payer(
        [transfer_instruction],  # Pass the list of instructions directly
        from_keypair.pubkey(),  # Fee-payer (challenger)
        [from_keypair],  # Signers (challenger)
        recent_blockhash  # Use recent blockhash directly
    )

    # Send the transaction
    result = client.send_raw_transaction(bytes(transaction), opts=TxOpts(skip_confirmation=False))
    return result

def get_latest_btc_price():
    try:
        # Binance API endpoint for fetching the latest BTC price in USDT
        url = 'https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT'
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        return float(data['price'])  # Return the latest BTC price as a float
    except requests.exceptions.RequestException as e:
        print(f"Error fetching BTC price: {e}")
        return None