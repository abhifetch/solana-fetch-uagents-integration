import base64
import base58
from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
from solders.keypair import Keypair
from functions import get_latest_btc_price, transfer_sol
import time

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

fund_agent_if_low(agent.wallet.address())

@agent.on_event('startup')
async def saf(ctx:Context):
    ctx.storage.set("bids_count",0)

@agent.on_message(model=escrowRequest, replies={escrowResponse})
async def escrow_request_handler(ctx: Context, sender: str, msg: escrowRequest):
    ctx.logger.info('Received escrowRequest message')
    current_count = ctx.storage.get("bids_count") or 0
    ctx.logger.info(f'Current bid count: {current_count}')
    
    # Store the bid as a dictionary for easier retrieval
    if current_count == 0:
        ctx.logger.info(f"Storing first request with amount: {msg.amount}, price: {msg.price}, sender: {sender}")
        ctx.storage.set("request_details_1", {'amount': msg.amount, 'price': msg.price, 'public_key': msg.public_key, 'sender': sender})
        ctx.storage.set("bids_count", current_count + 1)
    elif current_count == 1:
        time.sleep(15)
        ctx.logger.info(f"Storing second request with amount: {msg.amount}, price: {msg.price}, sender: {sender}")
        ctx.storage.set("request_details_2", {'amount': msg.amount, 'price': msg.price, 'public_key': msg.public_key, 'sender': sender})
        ctx.storage.set("bids_count", current_count + 1)
        ctx.logger.info("Processing bids to determine the winner.")
        
        # Retrieve the bids in a structured way
        first_request_details = ctx.storage.get("request_details_1")
        second_request_details = ctx.storage.get("request_details_2")
        
        ctx.logger.info(f"First request details: {first_request_details}")
        ctx.logger.info(f"Second request details: {second_request_details}")
        
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

        # Retrieve agent keypair from storage for transferring SOL
        stored_secret_key_base64 = ctx.storage.get('agent_keypair')
        stored_pubkey_base58 = ctx.storage.get('agent_pubkey')

        if stored_secret_key_base64 and stored_pubkey_base58:
            ctx.logger.info("Agent keypair and public key found in storage.")
            secret_key_bytes = base64.b64decode(stored_secret_key_base64)
            agent_keypair = Keypair.from_bytes(secret_key_bytes)
            ctx.logger.info(f"Agent keypair successfully recreated from storage.")
        else:
            ctx.logger.error("Agent keypair or public key not found in storage.")
            return

        try:
            # Transfer 90% of the total amount to the winner
            ctx.logger.info(f"Transferring {amount_to_send} SOL to winner with public key: {winner_public_key}")
            transfer_sol(agent_keypair, winner_public_key, amount_to_send)
        except Exception as e:
            ctx.logger.error(f"Error during SOL transfer: {e}")
            return

        # Notify winner and loser
        ctx.logger.info("Notifying winner and loser.")
        await ctx.send(winner_sender, escrowResponse(result='You Won'))
        await ctx.send(loser_sender, escrowResponse(result='You Lost'))

        # Reset the bids count and clear bid details after transfer
        ctx.logger.info("Resetting bids count and clearing stored bid details.")
        ctx.storage.set("request_details_1",'')
        ctx.storage.set("request_details_2",'')
        ctx.storage.set("bids_count", 0)


if __name__ == "__main__":
    agent.run()
