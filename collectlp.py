import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import requests

st.set_page_config(page_title="Pools Fermées - Krystal", layout="wide")
st.title("🔍 Pools de Liquidité Fermées (Krystal)")

# --- Entrée de l'URL à scanner ---
url = st.text_input("🔗 Entrez l'URL de la page Krystal à analyser :", placeholder="https://krystal.app/strategies")

use_local_file = st.checkbox("Utiliser un fichier HTML local (`mock.html`) pour tester sans connexion")

@st.cache_data
def fetch_html_from_url(target_url):
    try:
        response = requests.get(target_url, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement de l'URL : {e}")
        return None

@st.cache_data
def fetch_html_from_local_file():
    try:
        with open("mock.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        st.error("❌ Le fichier `mock.html` est introuvable.")
        return None

def extract_closed_pools(html):
    soup = BeautifulSoup(html, "html.parser")

    # 🧪 Simule les sélecteurs CSS de chaque ligne (à adapter à ta vraie page)
    rows = soup.select(".pool-row")  # Exemple fictif
    data = []

    for row in rows:
        try:
            total_value = float(row.select_one(".total-value").text.replace("$", "").replace(",", "").strip())

            if total_value == 0:
                data.append({
                    "Token Pair": row.select_one(".pair").text.strip(),
                    "Fees Generated": row.select_one(".fees").text.strip(),
                    "Deposits": row.select_one(".deposits").text.strip(),
                    "Withdrawals": row.select_one(".withdrawals").text.strip(),
                    "PnL": row.select_one(".pnl").text.strip(),
                    "Age": row.select_one(".age").text.strip(),
                    "Price Range": row.select_one(".price-range").text.strip()
                })
        except Exception as err:
            continue  # Ignore les lignes mal formées

    return pd.DataFrame(data)

# --- Lancer l'analyse ---
if (url and not use_local_file) or use_local_file:
    html = fetch_html_from_local_file() if use_local_file else fetch_html_from_url(url)

    if html:
        df = extract_closed_pools(html)

        if not df.empty:
            st.success(f"✅ {len(df)} pool(s) fermée(s) trouvée(s)")
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("Aucune pool fermée détectée ou structure HTML non reconnue.")
