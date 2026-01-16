import streamlit as st
import plotly.graph_objects as go

# --- KONFIGURACJA STRONY ---
st.set_page_config(page_title="Investment Portfolio", layout="centered")

# --- CUSTOM CSS (Dla efektu mrocznego interfejsu i kart) ---
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; }
    .holding-card {
        background-color: #161616;
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .ticker-name { font-weight: bold; font-size: 18px; color: white; }
    .sub-text { color: #808080; font-size: 14px; }
    .profit-text { color: #22c55e; font-weight: bold; }
    .total-val { color: white; font-weight: bold; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

# --- DANE (Docelowo pobierane z n8n/API) ---
portfolio_data = [
    {"ticker": "RKLB", "shares": 387, "value": 35124, "profit_pct": 260.02, "profit_abs": 25367.85, "color": "#76D7C4"},
    {"ticker": "ASTS", "shares": 291, "value": 29464, "profit_pct": 225.67, "profit_abs": 20416.56, "color": "#9B59B6"},
    {"ticker": "IREN", "shares": 400, "value": 20756, "profit_pct": 462.19, "profit_abs": 17064.00, "color": "#1ABC9C"},
]

total_value = sum(item['value'] for item in portfolio_data)
total_profit_abs = sum(item['profit_abs'] for item in portfolio_data)
total_profit_pct = (total_profit_abs / (total_value - total_profit_abs)) * 100

# --- WYKRES DONUT (CENTRALNY) ---
fig = go.Figure(data=[go.Pie(
    labels=[item['ticker'] for item in portfolio_data],
    values=[item['value'] for item in portfolio_data],
    hole=.7,
    marker_colors=[item['color'] for item in portfolio_data],
    textinfo='none'
)])

fig.update_layout(
    showlegend=False,
    margin=dict(t=0, b=0, l=0, r=0),
    height=350,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    annotations=[
        dict(text=f'${total_value:,.0f}', x=0.5, y=0.6, font_size=40, font_color="white", showarrow=False),
        dict(text=f'+${total_profit_abs:,.0f} ({total_profit_pct:.2f}%)', x=0.5, y=0.45, font_size=16, font_color="#22c55e", showarrow=False),
        dict(text='All-time ▾', x=0.5, y=0.35, font_size=14, font_color="#808080", showarrow=False)
    ]
)

st.plotly_chart(fig, use_container_width=True)

# --- LISTA HOLDINGS ---
st.markdown("### Holdings <span style='float:right; color:#808080; font-size:16px;'>Total value ▾</span>", unsafe_allow_html=True)

for item in portfolio_data:
    share_pct = (item['value'] / total_value) * 100
    st.markdown(f"""
        <div class="holding-card">
            <div>
                <span class="ticker-name">{item['ticker']}</span><br>
                <span class="sub-text">{item['shares']} shares | {share_pct:.2f}%</span>
            </div>
            <div style="text-align: right;">
                <span class="total-val">${item['value']:,.0f} USD</span><br>
                <span class="profit-text">+${item['profit_abs']:,.2f} (+{item['profit_pct']}%)</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
