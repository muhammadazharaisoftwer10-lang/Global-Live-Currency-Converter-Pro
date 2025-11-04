import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# -------------------- PAGE SETTINGS --------------------
st.set_page_config(page_title="💱 Global Currency Converter Pro", page_icon="💵", layout="wide")

# -------------------- CSS STYLISH THEME --------------------
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #dfe9f3 0%, #ffffff 100%);
        font-family: 'Poppins', sans-serif;
        color: #1a1a1a;
    }
    .block-container {
        background: rgba(255, 255, 255, 0.85);
        border-radius: 18px;
        padding: 2rem;
        box-shadow: 0 8px 40px rgba(0, 0, 0, 0.08);
        backdrop-filter: blur(12px);
    }
    h1 {
        text-align: center;
        font-weight: 700;
        background: linear-gradient(90deg, #0072ff, #00c6ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .stButton button {
        background: linear-gradient(90deg, #0072ff 0%, #00c6ff 100%);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        padding: 0.6rem 1rem;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 12px rgba(0, 114, 255, 0.6);
    }
    .result-box {
        background: linear-gradient(90deg, #89f7fe, #66a6ff);
        padding: 1.3rem;
        border-radius: 18px;
        color: white;
        font-size: 1.4rem;
        font-weight: 600;
        text-align: center;
        box-shadow: 0 8px 30px rgba(0, 100, 255, 0.3);
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------- HEADER --------------------
st.title("💱 Global Live Currency Converter Pro")
st.markdown("### 🌍 Convert, View Live Rates & Track Your Exchange History")
st.markdown("---")

# -------------------- API CONFIG --------------------
API_URL = "https://open.er-api.com/v6/latest"

@st.cache_data(ttl=600)
def get_rates(base="USD"):
    """Fetch live exchange rates"""
    try:
        res = requests.get(f"{API_URL}/{base}", timeout=10)
        res.raise_for_status()
        data = res.json()
        if data.get("result") == "success":
            return data
        return None
    except Exception:
        return None

# -------------------- CURRENCY LIST --------------------
@st.cache_data
def get_currency_list():
    return {
        "USD": "🇺🇸 United States Dollar",
        "EUR": "🇪🇺 Euro",
        "GBP": "🇬🇧 British Pound",
        "PKR": "🇵🇰 Pakistani Rupee",
        "INR": "🇮🇳 Indian Rupee",
        "JPY": "🇯🇵 Japanese Yen",
        "CAD": "🇨🇦 Canadian Dollar",
        "AUD": "🇦🇺 Australian Dollar",
        "CNY": "🇨🇳 Chinese Yuan",
        "SAR": "🇸🇦 Saudi Riyal",
        "AED": "🇦🇪 UAE Dirham",
        "TRY": "🇹🇷 Turkish Lira",
        "CHF": "🇨🇭 Swiss Franc"
    }

currencies = get_currency_list()

# -------------------- SESSION STATE FOR HISTORY --------------------
if "history" not in st.session_state:
    st.session_state["history"] = []

# -------------------- INPUT SECTION --------------------
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    base = st.selectbox("From Currency", options=list(currencies.keys()),
                        format_func=lambda x: currencies[x], index=0)
with col2:
    target = st.selectbox("To Currency", options=list(currencies.keys()),
                          format_func=lambda x: currencies[x], index=3)
with col3:
    amount = st.number_input("Amount", min_value=0.0, value=1.0, step=0.1)

convert = st.button("🔁 Convert Now")

# -------------------- MAIN CONVERSION --------------------
if convert:
    data = get_rates(base)
    if data and "rates" in data and target in data["rates"]:
        rate = data["rates"][target]
        converted = amount * rate

        # Show result
        st.markdown(
            f"""
            <div class='result-box'>
                💰 {amount:,.2f} {base} = {converted:,.2f} {target}<br>
                <span style='font-size:0.9rem;'>1 {base} = {rate:.4f} {target}</span><br>
                <span style='font-size:0.8rem;'>Updated: {data.get('time_last_update_utc')}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Add to history
        st.session_state["history"].append({
            "Date": datetime.now().strftime("%d-%b-%Y %I:%M %p"),
            "From": base,
            "To": target,
            "Amount": amount,
            "Converted": round(converted, 2),
            "Rate": round(rate, 4)
        })
    else:
        st.error("⚠️ Could not fetch live data or currency unavailable.")

# -------------------- SHOW HISTORY --------------------
if st.session_state["history"]:
    st.markdown("### 📜 Conversion History")
    df = pd.DataFrame(st.session_state["history"])
    st.dataframe(df, use_container_width=True)

    # Chart of recent conversions
    st.markdown("### 📈 Conversion Trend (Last 5 Records)")
    if len(df) >= 2:
        chart_df = df.tail(5)
        fig, ax = plt.subplots(figsize=(8, 3))
        ax.plot(chart_df["Date"], chart_df["Rate"], marker="o", linewidth=3, color="#0072ff")
        ax.set_title(f"{chart_df.iloc[-1]['From']} → {chart_df.iloc[-1]['To']} Trend", color="#333")
        ax.grid(alpha=0.3)
        st.pyplot(fig)

st.markdown("---")
st.caption("💡 Stylish glassmorphism | Live exchange rates | Auto history record")
st.caption("Developed by MUHAMMAD AZHAR ABBASI")