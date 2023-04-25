# Crypto Application by Tushar Aggarwal

# Importing required libraries
import streamlit as st
from PIL import Image
import pandas as pd
import base64
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import json
import time




# Application layout
st.set_page_config(page_title="Crypto Price Application",
                   page_icon=":📈:",
                   layout='wide')
# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

image = Image.open('logo.jpg')

st.image(image, width=150)

# Title
st.title("Crypto Price Application")
st.markdown("### By Tushar Aggarwal")
st.markdown("""
This app retrieves cryptocurrency prices for the top 100 cryptocurrency from the **CoinMarketCap**!
""")

# About
expander_bar = st.expander("About")
expander_bar.markdown("""
* **Data source:** [CoinMarketCap](http://coinmarketcap.com).
""")

# Page divider
col1=st.sidebar

col2, col3=st.columns(2,gap="small" )

# Sidebar 
col1.header("Please choose")

# Sidebar- Currency price unit
currency_price_unit = col1.selectbox("Select currency for price", ('USD', 'BTC', 'ETH'))

# Load data
@st.cache_data(persist=True)
def load_data():
    cmc = requests.get('https://coinmarketcap.com')
    soup = BeautifulSoup(cmc.content, 'html.parser')

    data = soup.find('script', id='__NEXT_DATA__', type='application/json')
    coins = {}
    coin_data = json.loads(data.contents[0])
    listings = coin_data['props']['initialState']['cryptocurrency']['listingLatest']['data']
    for i in listings:
      coins[str(i['id'])] = i['slug']

    coin_name = []
    coin_symbol = []
    market_cap = []
    percent_change_1h = []
    percent_change_24h = []
    percent_change_7d = []
    price = []
    volume_24h = []

    for i in listings:
      coin_name.append(i['slug'])
      coin_symbol.append(i['symbol'])
      price.append(i['quote'][currency_price_unit]['price'])
      percent_change_1h.append(i['quote'][currency_price_unit]['percent_change_1h'])
      percent_change_24h.append(i['quote'][currency_price_unit]['percent_change_24h'])
      percent_change_7d.append(i['quote'][currency_price_unit]['percent_change_7d'])
      market_cap.append(i['quote'][currency_price_unit]['market_cap'])
      volume_24h.append(i['quote'][currency_price_unit]['volume_24h'])

    df = pd.DataFrame(columns=['coin_name', 'coin_symbol', 'market_cap', 'percent_change_1h', 'percent_change_24h', 'percent_change_7d', 'price', 'volume_24h'])
    df['coin_name'] = coin_name
    df['coin_symbol'] = coin_symbol
    df['price'] = price
    df['percent_change_1h'] = percent_change_1h
    df['percent_change_24h'] = percent_change_24h
    df['percent_change_7d'] = percent_change_7d
    df['market_cap'] = market_cap
    df['volume_24h'] = volume_24h
    return df

df = load_data()




































