from web3 import Web3

# Replace with your Ganache RPC URL
ganache_url = "HTTP://127.0.0.1:7545"

# Connect to the Ganache network
web3 = Web3(Web3.HTTPProvider(ganache_url))

def get_balance(account):
    return web3.from_wei(web3.eth.get_balance(account),'ether')

def transfer_eth(sender_address,receiver_address,private_key_sender,amount):
    # Convert Ether amount to Wei (1 Ether = 10^18 Wei)
    amount_in_wei = web3.to_wei(amount, "ether")

    # Check the sender's balance before the transfer
    sender_balance_before = web3.eth.get_balance(sender_address)

    # Create a transaction
    transaction = {
        "to": receiver_address,
        "value": amount_in_wei,
        "gas": 21000,  # Gas limit for a simple transaction
        "gasPrice": web3.to_wei("20", "gwei"),  # Adjust gas price as needed
        "nonce": web3.eth.get_transaction_count(sender_address),
    }

    # Sign the transaction
    signed_transaction = web3.eth.account.sign_transaction(transaction, private_key_sender)

    # Send the transaction
    transaction_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)

    # Wait for the transaction to be mined
    web3.eth.wait_for_transaction_receipt(transaction_hash)

    # Check the sender's balance after the transfer
    sender_balance_after = web3.eth.get_balance(sender_address)

    print(f"Transferred {amount} Ether from {sender_address} to {receiver_address}")
    print(f"Sender's balance before: {web3.from_wei(sender_balance_before, 'ether')} Ether")
    print(f"Sender's balance after: {web3.from_wei(sender_balance_after, 'ether')} Ether")

if __name__ == "__main__":
    transfer_eth()
