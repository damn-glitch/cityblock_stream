import uuid

import streamlit as st
import pandas as pd
import json
import hashlib
import os
from web3 import Web3
from web3.contract import contract

# Setup web3 connection with Infura
infura_url = 'https://mainnet.infura.io/v3/cc376f7a1ea7449fa99b2bef2673529a'
web3 = Web3(Web3.HTTPProvider(infura_url))

if web3.is_connected():
    st.sidebar.success("Connected to Ethereum network")
else:
    st.sidebar.error("Failed to connect to Ethereum network")

# Contract details
contract_address = '0xd8b934580fcE35a11B58C6D73aDeE468a2833fa8'
contract_abi = json.loads('''
	[{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "demandId",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "address",
				"name": "buyer",
				"type": "address"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "energyAmount",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "maxPricePerKWh",
				"type": "uint256"
			}
		],
		"name": "DemandExpressed",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "offerId",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "address",
				"name": "seller",
				"type": "address"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "energyAmount",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "pricePerKWh",
				"type": "uint256"
			}
		],
		"name": "OfferCreated",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "tradeId",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "offerId",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "demandId",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "address",
				"name": "seller",
				"type": "address"
			},
			{
				"indexed": false,
				"internalType": "address",
				"name": "buyer",
				"type": "address"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "energyTransferred",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "pricePerKWh",
				"type": "uint256"
			}
		],
		"name": "TradeMatched",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_energyAmount",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_pricePerKWh",
				"type": "uint256"
			}
		],
		"name": "createOffer",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "demands",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "id",
				"type": "uint256"
			},
			{
				"internalType": "address",
				"name": "buyer",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "energyAmount",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "maxPricePerKWh",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_energyAmount",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_maxPricePerKWh",
				"type": "uint256"
			}
		],
		"name": "expressDemand",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "matchTrades",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "offers",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "id",
				"type": "uint256"
			},
			{
				"internalType": "address",
				"name": "seller",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "energyAmount",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "pricePerKWh",
				"type": "uint256"
			},
			{
				"internalType": "bool",
				"name": "available",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "trades",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "tradeId",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "offerId",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "demandId",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "energyTransferred",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "pricePerKWh",
				"type": "uint256"
			},
			{
				"internalType": "address",
				"name": "seller",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "buyer",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]
''')


# File paths for storing data in text files
data_files = {
    'offers': 'offers.txt',
    'demands': 'demands.txt',
    'trades': 'trades.txt',
    'blockchain': 'blockchain.txt'
}


# Function to generate a hash for blockchain linking
def generate_hash(data):
    record = json.dumps(data, sort_keys=True).encode()
    return hashlib.sha256(record).hexdigest()


# Function to generate a random hash for simulating a blockchain transaction
def generate_transaction_hash(*args):
    unique_string = ''.join(str(arg) for arg in args) + str(uuid.uuid4())
    return hashlib.sha256(unique_string.encode()).hexdigest()


# Function to load data from text files
def load_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            # Ensure 'available' key exists for all offers, defaulting to True
            for offer in data:
                if 'available' not in offer:
                    offer['available'] = True
            return data
    else:
        return []



# Function to save data to text files
def save_data(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file)


# Loading initial data
data = {key: load_data(key) for key in data_files.keys()}
offers_data = load_data('offers.txt')
demands_data = load_data('demands.txt')
trades_data = load_data('trades.txt')


def append_to_blockchain(transaction):
    prev_hash = data['blockchain'][-1]['hash'] if data['blockchain'] else '0'
    block = {
        'transaction': transaction,
        'prev_hash': prev_hash,
        'hash': generate_hash(transaction)
    }
    data['blockchain'].append(block)
    for key in data:
        save_data(data[key], key)


# Ensure the default account is set and funded appropriately
web3.eth.default_account = '0x805f70a54a2aC1bc851B4180939260A829E1894d'  # Ensure this is a valid address


def blockchain_create_offer(energy_amount, price_per_kwh):
    try:
        # Convert float to int if necessary and ensure types are correct
        energy_amount = int(energy_amount)
        price_per_kwh = int(price_per_kwh)

        # Prepare the transaction
        tx = contract.functions.createOffer(energy_amount, price_per_kwh).buildTransaction({
            'from': web3.eth.default_account,
            'nonce': web3.eth.get_transaction_count(web3.eth.default_account),
            'gas': 200000,
            'gasPrice': web3.to_wei('50', 'gwei'),
            'chainId': web3.eth.chain_id
        })

        # Send the transaction
        signed_tx = web3.eth.account.signTransaction(tx, 'your-private-key-here')
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

        return receipt.transactionHash
    except Exception as e:
        print(f"An error occurred: {e}")


def create_offer(seller, energy_amount, price_per_kwh):
    offers = load_data('offers.txt')
    new_offer = {
        'id': len(offers) + 1,
        'seller': seller,
        'energy_amount': energy_amount,
        'price_per_kwh': price_per_kwh,
        'available': True,  # Ensure this key is always included
        'transaction_hash': generate_transaction_hash(seller, energy_amount, price_per_kwh)
    }
    offers.append(new_offer)
    save_data(offers, 'offers.txt')
    return new_offer

def blockchain_express_demand(energy_amount, max_price_per_kwh):
    try:
        # Convert and ensure types are correct
        energy_amount = int(energy_amount)
        max_price_per_kwh = int(max_price_per_kwh)

        # Prepare the transaction
        tx = contract.functions.expressDemand(energy_amount, max_price_per_kwh).buildTransaction({
            'from': web3.eth.default_account,
            'nonce': web3.eth.get_transaction_count(web3.eth.default_account),
            'gas': 200000,
            'gasPrice': web3.to_wei('50', 'gwei'),
            'chainId': web3.eth.chain_id
        })

        # Send the transaction
        signed_tx = web3.eth.account.signTransaction(tx, 'your-private-key-here')
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

        return receipt.transactionHash
    except Exception as e:
        print(f"An error occurred: {e}")


def express_demand(buyer, energy_amount, price_per_kwh):
    demands = load_data('demands.txt')
    new_demand = {
        'id': len(demands) + 1,
        'buyer': buyer,
        'energy_amount': energy_amount,
        'price_per_kwh': price_per_kwh,  # Ensure this key is included
        'transaction_hash': generate_transaction_hash(buyer, energy_amount, price_per_kwh)
    }
    demands.append(new_demand)
    save_data(demands, 'demands.txt')
    return new_demand



def blockchain_match_trades():
    try:
        tx = contract.functions.matchTrades().buildTransaction({
            'from': web3.eth.default_account,
            'nonce': web3.eth.getTransactionCount(web3.eth.default_account),
            'gas': 200000,
            'gasPrice': web3.toWei('50', 'gwei'),
            'chainId': web3.eth.chain_id
        })
        signed_tx = web3.eth.account.signTransaction(tx, 'your-private-key-here')
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        receipt = web3.eth.waitForTransactionReceipt(tx_hash)
        return receipt.transactionHash
    except Exception as e:
        print(f"Error during trade matching: {str(e)}")
        return None

def match_offers_with_demands():
    offers = load_data('offers.txt')
    demands = load_data('demands.txt')
    trades = load_data('trades.txt')
    matched = False

    for demand in demands:
        for offer in offers:
            # Use .get() to safely access keys with defaults to avoid KeyError
            if offer.get('available', True) and offer['energy_amount'] >= demand['energy_amount'] and offer['price_per_kwh'] <= demand.get('price_per_kwh', float('inf')):
                # Matching logic here
                matched = True
                # Update offer status
                offer['available'] = False
                break
        if matched:
            save_data(offers, 'offers.txt')
            save_data(trades, 'trades.txt')
            return True

    return False



# Streamlit interface
# Streamlit UI to collect input and create an offer
st.title("Blockchain-Based Energy Trading System")
with st.expander("Create Offer"):
    with st.form("create_offer_form"):
        seller = st.text_input("Seller Identifier (e.g., Seller ID)")
        energy_amount = st.number_input("Energy Amount (kWh)", min_value=0)
        price_per_kwh = st.number_input("Price per kWh ($)", min_value=0.01, step=0.01)
        submit_offer = st.form_submit_button("Create Offer")

        if submit_offer:
            offer_details = create_offer(seller, energy_amount, price_per_kwh)
            if offer_details:
                st.success(f"Offer created successfully with transaction hash: {offer_details['transaction_hash']}")
                st.write(f"Seller: {offer_details['seller']}")
                st.write(f"Energy Amount: {offer_details['energy_amount']} kWh")
                st.write(f"Price per kWh: ${offer_details['price_per_kwh']}")
            else:
                st.error("Failed to create offer.")

# Express Demand
with st.expander("Express Demand"):
    with st.form("express_demand"):
        buyer = st.text_input("Buyer Identifier (e.g., Buyer ID)")
        demanded_energy = st.number_input("Demanded Energy Amount (kWh)", min_value=0)
        max_price = st.number_input("Maximum Price per kWh ($)", min_value=0.01, step=0.01, format="%.2f")
        submit_demand = st.form_submit_button("Express Demand")
        if submit_demand:
            demand_details = express_demand(buyer, demanded_energy, max_price)
            if demand_details:
                st.success(f"Demand expressed successfully on blockchain with transaction hash: {demand_details['transaction_hash']}")
                st.write(f"Buyer: {demand_details['buyer']}")
                st.write(f"Energy Amount: {demand_details['energy_amount']} kWh")
                st.write(f"Price per kWh: ${demand_details['price_per_kwh']}")
            else:
                st.error("Failed to create offer.")

# Match Offers with Demands
if st.button('Match Offers with Demands'):
    if match_offers_with_demands():
        st.success("Offers and demands matched successfully.")
        # Optionally display updated trades
        trades_df = pd.DataFrame(load_data('trades.txt'))
        st.dataframe(trades_df)
    else:
        st.error("No matches found.")

# Display existing offers
st.subheader("Current Offers")
offers_df = pd.DataFrame(load_data('offers.txt'))
st.dataframe(offers_df.style.format({'Price per kWh ($)': "{:.2f}"}))

st.subheader("Current Demands")
demands_df = pd.DataFrame(load_data('demands.txt'))
st.dataframe(demands_df.style.format({'Price per kWh ($)': "{:.2f}"}))

st.subheader("Completed Trades")
trades_df = pd.DataFrame(load_data('trades.txt'))
st.dataframe(trades_df)
