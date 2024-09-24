import base64
import base58
from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
from solders.keypair import Keypair
from functions import check_balance, transfer_sol


class escrowRequest(Model):
    amount: float
    price: float
    public_key: str

class escrowResponse(Model):
    result: str

agent = Agent(
    name="AbhiAgent",
    port=8001,
    seed="Abhi Escrow Wallet 1",
    endpoint=["http://127.0.0.1:8001/submit"],
)

escrow_address = 'agent1qd6ts50kuy3vqq36s5yg2dkzujq60x0l0sr2acfafnp5zea749yvvvq2qm7'
escrow_pub_key = '6jPaZ3md3UjBaKDeXUg6NgGTg79SWB2F4b7Nxodov54f'

fund_agent_if_low(agent.wallet.address())

@agent.on_event('startup')
async def starter_function(ctx: Context):
    # Retrieve the stored Base64-encoded secret key from storage
    stored_secret_key_base64 = ctx.storage.get('agent_keypair')
    
    if stored_secret_key_base64:
        # Decode the Base64 secret key back into bytes
        secret_key_bytes = base64.b64decode(stored_secret_key_base64)
        # Recreate the Keypair from the decoded secret key
        agent_keypair = Keypair.from_bytes(secret_key_bytes)
        # Retrieve the stored Base58-encoded public key from storage
        stored_pubkey_base58 = ctx.storage.get('agent_pubkey')
        agent_pubkey_base58 = stored_pubkey_base58 if stored_pubkey_base58 else base58.b58encode(bytes(agent_keypair.pubkey())).decode('utf-8')
    else:
        ctx.logger.error("Secret key not found in storage.")
        return

    # Log the initial balance
    initial_balance = check_balance(agent_keypair.pubkey())
    ctx.logger.info(f"Initial agent balance: {initial_balance} SOL")

    # Ask the user for the amount and price, and convert them to float
    amount = float(input('What is the amount of SOL you want to deposit? '))
    price = float(input('What is the price of Bitcoin you want to bid at? '))

    # Log the bet details
    ctx.logger.info(f'Placing bet of {amount} SOL on Bitcoin at {price}$ with wallet address: {agent_pubkey_base58}')

    # Send the bet to the escrow address
    await ctx.send(escrow_address, escrowRequest(amount=amount, price=price, public_key=agent_pubkey_base58))
    
    # Transfer the amount provided by the user
    ctx.logger.info(f"Transferring {amount} SOL to {escrow_pub_key}")

    # Perform the transfer using the stored agent_keypair
    transfer_result = transfer_sol(agent_keypair, escrow_pub_key, amount)
    ctx.logger.info(f"Transfer result: {transfer_result}")

    # Log the final balance after transfer
    final_balance = check_balance(agent_keypair.pubkey())
    ctx.logger.info(f"Final agent balance: {final_balance} SOL")


@agent.on_message(model=escrowResponse)
async def escrow_request_handler(ctx: Context, sender: str, msg: escrowResponse):
    # Retrieve the secret key and check balance
    stored_secret_key_base64 = ctx.storage.get('agent_keypair')
    secret_key_bytes = base64.b64decode(stored_secret_key_base64)
    agent_keypair = Keypair.from_bytes(secret_key_bytes)
    agent_pubkey = agent_keypair.pubkey()

    # Log updated account balance
    balance = check_balance(agent_pubkey)
    ctx.logger.info(f'{msg.result}. Updated account balance: {balance} SOL')

if __name__ == "__main__":
    agent.run()
