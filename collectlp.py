import streamlit as st
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd

st.set_page_config(page_title="Pools Fermées - Krystal", layout="wide")
st.title("💧 Pools de Liquidité Fermées (Krystal)")

# URL d'entrée utilisateur
url = st.text_input("🔗 Entrez l'URL d'une stratégie Krystal :", placeholder="https://krystal.app/strategies/9700")

def scrape_krystal_positions(strategy_url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(strategy_url)

        # Clic sur l'onglet "Positions"
        try:
            page.click("text=Positions")
            page.wait_for_selector(".token-symbol", timeout=10000)  # Attente que le tableau charge
        except Exception as e:
            st.error("❌ Erreur : Impossible de charger l'onglet Positions.")
            browser.close()
            return pd.DataFrame()

        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")

    # Exemple de parsing basé sur ta capture — à adapter si besoin
    rows = soup.select("tr")  # Peut-être ".table-row" si identifiable
    data = []

    for row in rows:
        try:
            token_pair = row.select_one(".token-symbol").text.strip()
            total_value = float(row.select_one(".total-value").text.replace("$", "").replace(",", "").strip())

            if total_value == 0:
                data.append({
                    "Token Pair": token_pair,
                    "Fees Generated": row.select_one(".fees").text.strip(),
                    "Deposits": row.select_one(".deposits").text.strip(),
                    "Withdrawals": row.select_one(".withdrawals").text.strip(),
                    "PnL": row.select_one(".pnl").text.strip(),
                    "Age": row.select_one(".age").text.strip(),
                    "Price Range": row.select_one(".price-range").text.strip()
                })
        except:
            continue

    return pd.DataFrame(data)

# ⚡ Lancer l'analyse si URL valide
if url:
    with st.spinner("🔄 Chargement des données..."):
        df = scrape_krystal_positions(url)

    if not df.empty:
        st.success(f"✅ {len(df)} pool(s) fermée(s) trouvée(s)")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("Aucune pool fermée détectée ou chargement échoué.")
