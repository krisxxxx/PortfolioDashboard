import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --- KONFIGURACJA STRONY ---
st.set_page_config(page_title="Portfolio Dashboard", layout="wide")
st.title("📈 Moje Centrum Inwestycyjne")

# --- FUNKCJA POBIERANIA DANYCH (MOCK API) ---
# Tutaj docelowo wstawisz logikę swojego brokera (np. requests.get(...))
@st.cache_data
def get_portfolio_data():
    portfolios = ['IKE', 'IKZE', 'Obligacje', 'ETF']
    data = []
    for p in portfolios:
        # Symulacja danych: Nazwa, Wartość, Zysk/Strata, Sektor
        data.append({"Portfolio": p, "Value": np.random.randint(10000, 50000), "Change": np.random.uniform(-5, 5)})
    return pd.DataFrame(data)

def get_historical_data():
    # Symulacja historii wartości portfela z ostatnich 30 dni
    dates = pd.date_range(start='2025-12-17', periods=30)
    df = pd.DataFrame({
        'Data': dates,
        'Wartość': np.cumsum(np.random.normal(100, 50, 30)) + 100000
    })
    return df

# --- POBIERANIE DANYCH ---
df_portfolios = get_portfolio_data()
df_history = get_historical_data()
total_value = df_portfolios['Value'].sum()

# --- SIDEBAR (FILTRY) ---
st.sidebar.header("Ustawienia")
selected_p = st.sidebar.multiselect("Wybierz portfele:", df_portfolios['Portfolio'].unique(), default=df_portfolios['Portfolio'].unique())

# --- SEKCA 1: KPI (GŁÓWNE WSKAŹNIKI) ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Całkowita Wartość", f"{total_value:,.2f} PLN")
col2.metric("Zmiana 24h", "+1.2%", "0.5%")
col3.metric("Liczba Aktywów", "24")
col4.metric("Dywersyfikacja (HHI)", "Niska")

st.divider()

# --- SEKCJA 2: WYKRESY ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Alokacja Kapitału")
    fig_pie = px.pie(df_portfolios, values='Value', names='Portfolio', hole=0.4,
                     color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig_pie, width='stretch')

with col_right:
    st.subheader("Historia Wyników (Łącznie)")
    fig_line = px.line(df_history, x='Data', y='Wartość', template="plotly_white")
    st.plotly_chart(fig_line, width=True)

# --- SEKCJA 3: TABELA SZCZEGÓŁOWA ---
st.subheader("Szczegóły Portfeli")
st.dataframe(df_portfolios, width='stretch')
