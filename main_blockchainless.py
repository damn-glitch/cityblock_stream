import streamlit as st
import pandas as pd
import json
import hashlib
import os

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


# Function to load data from text files
def load_data(file_type):
    try:
        with open(data_files[file_type], 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


# Function to save data to text files
def save_data(data, file_type):
    with open(data_files[file_type], 'w') as file:
        json.dump(data, file)


# Loading initial data
data = {key: load_data(key) for key in data_files.keys()}


# Function to create an offer and save data
def create_offer(seller, energy_amount, price_per_kwh):
    new_offer = {
        'id': len(data['offers']) + 1,
        'seller': seller,
        'energy_amount': energy_amount,
        'price_per_kwh': price_per_kwh,
        'available': True
    }
    data['offers'].append(new_offer)
    append_to_blockchain(new_offer)
    return new_offer['id']


# Function to express demand and save data
def express_demand(buyer, energy_amount, max_price_per_kwh):
    new_demand = {
        'id': len(data['demands']) + 1,
        'buyer': buyer,
        'energy_amount': energy_amount,
        'max_price_per_kwh': max_price_per_kwh
    }
    data['demands'].append(new_demand)
    append_to_blockchain(new_demand)
    return new_demand['id']


# Append transaction to blockchain
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


# Function to match offers and demands and save data
def match_trades():
    matched = False
    for demand in data['demands']:
        for offer in data['offers']:
            if offer['available'] and offer['energy_amount'] >= demand['energy_amount'] and offer['price_per_kwh'] <= \
                    demand['max_price_per_kwh']:
                trade_details = {
                    'trade_id': len(data['trades']) + 1,
                    'offer_id': offer['id'],
                    'demand_id': demand['id'],
                    'energy_amount': demand['energy_amount'],
                    'price_per_kwh': offer['price_per_kwh'],
                    'seller': offer['seller'],
                    'buyer': demand['buyer']
                }
                data['trades'].append(trade_details)
                offer['available'] = False
                matched = True
                append_to_blockchain(trade_details)
                break
    if matched:
        st.success("Matching process completed!")
    else:
        st.error("No matches found!")


# Function to convert lists to pandas DataFrame for better display
def data_to_dataframe(data_list, data_type):
    if data_type == 'offers':
        df = pd.DataFrame(data_list)
        df = df[['id', 'seller', 'energy_amount', 'price_per_kwh', 'available']]
        df.columns = ['Offer ID', 'Seller', 'Energy (kWh)', 'Price per kWh ($)', 'Available']
        df['Available'] = df['Available'].map({True: 'Yes', False: 'No'})
    elif data_type == 'demands':
        df = pd.DataFrame(data_list)
        df = df[['id', 'buyer', 'energy_amount', 'max_price_per_kwh']]
        df.columns = ['Demand ID', 'Buyer', 'Energy (kWh)', 'Max Price per kWh ($)']
    else:
        df = pd.DataFrame(data_list)
        df = df[['trade_id', 'offer_id', 'demand_id', 'energy_amount', 'price_per_kwh', 'seller', 'buyer']]
        df.columns = ['Trade ID', 'Offer ID', 'Demand ID', 'Energy (kWh)', 'Price per kWh ($)', 'Seller', 'Buyer']
    return df


# Streamlit interface
st.title("Blockchain-Based Energy Trading System")

with st.expander("Create an Offer"):
    with st.form("create_offer"):
        seller = st.text_input("Seller Identifier (e.g., Seller ID)")
        energy_amount = st.number_input("Energy Amount (kWh)", min_value=0)
        price_per_kwh = st.number_input("Price per kWh ($)", min_value=0.01, step=0.01, format="%.2f")
        submit_offer = st.form_submit_button("Create Offer")
        if submit_offer:
            offer_id = create_offer(seller, energy_amount, price_per_kwh)
            st.success(f"Offer #{offer_id} created successfully!")

with st.expander("Express Demand"):
    with st.form("express_demand"):
        buyer = st.text_input("Buyer Identifier (e.g., Buyer ID)")
        demanded_energy = st.number_input("Demanded Energy Amount (kWh)", min_value=0)
        max_price = st.number_input("Maximum Price per kWh ($)", min_value=0.01, step=0.01, format="%.2f")
        submit_demand = st.form_submit_button("Express Demand")
        if submit_demand:
            demand_id = express_demand(buyer, demanded_energy, max_price)
            st.success(f"Demand #{demand_id} expressed successfully!")

if st.button('Match Offers with Demands'):
    match_trades()

# Display sections
st.subheader("Current Offers")
offers_df = data_to_dataframe(data['offers'], 'offers')
st.dataframe(offers_df.style.format({'Price per kWh ($)': "{:.2f}"}))

st.subheader("Current Demands")
demands_df = data_to_dataframe(data['demands'], 'demands')
st.dataframe(demands_df.style.format({'Max Price per kWh ($)': "{:.2f}"}))

st.subheader("Completed Trades")
trades_df = data_to_dataframe(data['trades'], 'trades')
st.dataframe(trades_df.style.format({'Price per kWh ($)': "{:.2f}"}))
