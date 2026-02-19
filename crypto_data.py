import requests
import pandas as pd
from datetime import datetime

API_KEY = "7731952695a94da18d2d8ec0316eb5dc"


# ---------------- LIVE MARKET DATA ---------------- #

def fetch_crypto_data(symbols):

    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"

    headers = {
        "X-CMC_PRO_API_KEY": API_KEY,
        "Accepts": "application/json"
    }

    params = {
        "symbol": ",".join(symbols),
        "convert": "USD"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        if "data" not in data:
            return pd.DataFrame()

        crypto_list = []

        for symbol in symbols:

            coin = data["data"][symbol]

            crypto_list.append({
                "Symbol": symbol,
                "Name": coin["name"],
                "Price": coin["quote"]["USD"]["price"],
                "MarketCap": coin["quote"]["USD"]["market_cap"],
                "Volume24h": coin["quote"]["USD"]["volume_24h"],
                "PercentChange24h": coin["quote"]["USD"]["percent_change_24h"],
                "PercentChange7d": coin["quote"]["USD"]["percent_change_7d"]
            })

        return pd.DataFrame(crypto_list)

    except:
        return pd.DataFrame()


# ---------------- HISTORICAL DATA ---------------- #

def fetch_crypto_history(symbols):

    history_data = []

    id_map = {
        "BTC": "bitcoin",
        "ETH": "ethereum",
        "BNB": "binancecoin",
        "ADA": "cardano",
        "SOL": "solana",
        "XRP": "ripple",
        "DOGE": "dogecoin",
        "MATIC": "matic-network",
        "DOT": "polkadot"
    }

    try:

        for symbol in symbols:

            if symbol not in id_map:
                continue

            coin_id = id_map[symbol]

            url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"

            params = {
                "vs_currency": "usd",
                "days": "5"
            }

            response = requests.get(url, params=params)
            data = response.json()

            if "prices" not in data:
                continue

            for timestamp, price in data["prices"]:

                history_data.append({
                    "Date": datetime.fromtimestamp(timestamp / 1000),
                    "Symbol": symbol,   # ✅ ALWAYS INCLUDED
                    "Price": price
                })

        df = pd.DataFrame(history_data)

        # ✅ GUARANTEE columns exist
        if df.empty:
            return pd.DataFrame(columns=["Date", "Symbol", "Price"])

        return df

    except:
        return pd.DataFrame(columns=["Date", "Symbol", "Price"])


