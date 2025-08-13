import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Titre de l'app
st.title("Pools de Liquidité Fermées (Krystal)")

# URL cible (à remplacer par la vraie URL Krystal ou mock HTML local)
url = "https://exemple-krystal.io/strategies"  # fictif

# Fonction de scraping simple
@st.cache_data
def fetch_data():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Parsing fictif – à adapter à la vraie structure HTML
    pools = []
    for row in soup.select(".pool-row"):
        token_pair = row.select_one(".pair").text
        total_value = float(row.select_one(".total-value").text.replace("$", "").replace(",", ""))
        fees_generated = row.select_one(".fees").text
        deposits = row.select_one(".deposits").text
        withdrawals = row.select_one(".withdrawals").text
        pnl = row.select_one(".pnl").text
        age = row.select_one(".age").text
        price_range = row.select_one(".price-range").text

        if total_value == 0:
            pools.append({
                "Token Pair": token_pair,
                "Fees Generated": fees_generated,
                "Deposits": deposits,
                "Withdrawals": withdrawals,
                "PnL": pnl,
                "Age": age,
                "Price Range": price_range
            })
    
    return pd.DataFrame(pools)

# Affichage
df = fetch_data()

if df.empty:
    st.warning("Aucune pool fermée détectée.")
else:
    st.success(f"{len(df)} pool(s) fermée(s) trouvée(s)")
    st.dataframe(df, use_container_width=True)
