import os
import base64
import ast
import base58
from uagents import Agent, Context, Model
from solders.keypair import Keypair
from functions import get_latest_btc_price, transfer_sol
import time

# Fetch secret key from environment variable
escrow_secret_key_str = os.getenv('ESCROW_SECRET_LIST')
if not escrow_secret_key_str:
    raise ValueError("ESCROW_SECRET_LIST not found in environment variables.")

# Convert the string back to a list of integers
escrow_secret_key_list = ast.literal_eval(escrow_secret_key_str)

# Convert the list of integers into a bytes object (private key)
escrow_secret_key_bytes = bytes(escrow_secret_key_list)

# Recreate the Keypair using the secret key
escrow_keypair = Keypair.from_bytes(escrow_secret_key_bytes)
escrow_pubkey_base58 = base58.b58encode(bytes(escrow_keypair.pubkey())).decode('utf-8')

class escrowRequest(Model):
    amount: float
    price: float
    public_key: str

class escrowResponse(Model):
    result: str

agent = Agent(
    name="EscrowAgent",
    port=8000,
    seed="Escrow Wallet",
    endpoint=["http://127.0.0.1:8000/submit"],
)

@agent.on_event('startup')
async def saf(ctx: Context):
    ctx.logger.info("Escrow agent initialized, ready for bids.")
    ctx.logger.info(f"Escrow agent address: {agent.address}")
    # Initialize the bid count in storage if it doesn't exist
    ctx.storage.set("bids_count", 0)

@agent.on_message(model=escrowRequest, replies={escrowResponse})
async def escrow_request_handler(ctx: Context, sender: str, msg: escrowRequest):
    ctx.logger.info('Received escrowRequest message')

    # Get the current bid count from storage
    current_count = ctx.storage.get("bids_count") or 0
    ctx.logger.info(f'Current bid count: {current_count}')
    
    # Store the first bid if count is 0
    if current_count == 0:
        ctx.logger.info(f"Storing first request with amount: {msg.amount}, price: {msg.price}, sender: {sender}")
        ctx.storage.set("request_details_1", {
            'amount': msg.amount, 
            'price': msg.price, 
            'public_key': msg.public_key, 
            'sender': sender
        })
        ctx.storage.set("bids_count", current_count + 1)
    
    # Store the second bid and determine the winner
    elif current_count == 1:
        time.sleep(10)
        ctx.logger.info(f"Storing second request with amount: {msg.amount}, price: {msg.price}, sender: {sender}")
        ctx.storage.set("request_details_2", {
            'amount': msg.amount, 
            'price': msg.price, 
            'public_key': msg.public_key, 
            'sender': sender
        })
        ctx.storage.set("bids_count", current_count + 1)

        ctx.logger.info("Processing bids to determine the winner.")
        
        # Retrieve the bids from storage
        first_request_details = ctx.storage.get("request_details_1")
        second_request_details = ctx.storage.get("request_details_2")
        
        ctx.logger.info(f"First request details: {first_request_details}")
        ctx.logger.info(f"Second request details: {second_request_details}")
        
        # Extract data for the first and second bids
        first_amount = first_request_details['amount']
        first_price = first_request_details['price']
        first_public_key = first_request_details['public_key']
        first_sender = first_request_details['sender']

        second_amount = second_request_details['amount']
        second_price = second_request_details['price']
        second_public_key = second_request_details['public_key']
        second_sender = second_request_details['sender']

        # Get the latest BTC price
        latest_btc_price = get_latest_btc_price()
        ctx.logger.info(f"Latest BTC price: {latest_btc_price}")

        if latest_btc_price is None:
            ctx.logger.error("Failed to get the latest BTC price.")
            return

        # Calculate which bid is closer to the latest BTC price
        first_difference = abs(latest_btc_price - first_price)
        second_difference = abs(latest_btc_price - second_price)

        ctx.logger.info(f"First bid difference: {first_difference}, Second bid difference: {second_difference}")

        if first_difference < second_difference:
            winner_public_key = first_public_key
            winner_sender = first_sender
            loser_sender = second_sender
        else:
            winner_public_key = second_public_key
            winner_sender = second_sender
            loser_sender = first_sender

        # Calculate total and 90% amount to send
        total_amount = first_amount + second_amount
        amount_to_send = total_amount * 0.90
        ctx.logger.info(f"Total amount: {total_amount}, Amount to send to winner: {amount_to_send}")

        try:
            # Transfer 90% of the total amount to the winner
            ctx.logger.info(f"Transferring {amount_to_send} SOL to winner with public key: {winner_public_key}")
            transfer_sol(escrow_keypair, winner_public_key, amount_to_send)
        except Exception as e:
            ctx.logger.error(f"Error during SOL transfer: {e}")
            return

        # Notify the winner and loser
        ctx.logger.info("Notifying winner and loser.")
        await ctx.send(winner_sender, escrowResponse(result='You Won'))
        await ctx.send(loser_sender, escrowResponse(result='You Lost'))

        # Clear bids from storage and reset bids count
        ctx.logger.info("Resetting bids count and clearing stored bid details.")
        ctx.storage.set("request_details_1", '')
        ctx.storage.set("request_details_2", '')
        ctx.storage.set("bids_count", 0)

if __name__ == "__main__":
    agent.run()
