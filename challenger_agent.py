import os
import ast
import base58
from uagents import Agent, Context, Model
from solders.keypair import Keypair
from functions import check_balance, transfer_sol
from uagents.setup import fund_agent_if_low

# Fetch secret key from environment variable
secret_key_str = os.getenv('CHALLENGER_SECRET_LIST')
if not secret_key_str:
    raise ValueError("CHALLENGER_SECRET_LIST not found in environment variables.")

# Convert the string back to a list of integers
secret_key_list = ast.literal_eval(secret_key_str)

# Convert the list of integers into a bytes object (private key)
secret_key_bytes = bytes(secret_key_list)

# Recreate the Keypair using the secret key
agent_keypair = Keypair.from_bytes(secret_key_bytes)
agent_pubkey_base58 = base58.b58encode(bytes(agent_keypair.pubkey())).decode('utf-8')

class escrowRequest(Model):
    amount: float
    price: float
    public_key: str

class escrowResponse(Model):
    result: str

agent = Agent(
    name="Challenger",
    port=8002,
    seed="Challenger Escrow Wallet 2",
    endpoint=["http://127.0.0.1:8002/submit"],
)


escrow_address = 'agent1qd6ts50kuy3vqq36s5yg2dkzujq60x0l0sr2acfafnp5zea749yvvvq2qm7'
escrow_pub_key = '8WMWFo13At1REkwy5t7ck6sLgCUrJ9dn66mbaccPiJ26'

fund_agent_if_low(agent.wallet.address())

@agent.on_event('startup')
async def starter_function(ctx: Context):
    # Log the initial balance
    ctx.logger.info(agent_keypair.pubkey())
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
    # Log updated account balance
    balance = check_balance(agent_keypair.pubkey())
    ctx.logger.info(f'{msg.result}. Updated account balance: {balance} SOL')

if __name__ == "__main__":
    agent.run()
