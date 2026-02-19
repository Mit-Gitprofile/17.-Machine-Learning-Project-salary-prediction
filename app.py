import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from crypto_data import fetch_crypto_data, fetch_crypto_history

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Crypto Advisor PRO",
    page_icon="💎",
    layout="wide"
)

# ---------------- PRO STYLING ---------------- #

st.markdown("""
    <style>
        .main {
            background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
            color: white;
        }

        .stButton>button {
            background: linear-gradient(90deg, #ff512f, #dd2476);
            color: white;
            border-radius: 10px;
            height: 3em;
            font-size: 16px;
            font-weight: bold;
            border: none;
        }

        .stMetric {
            background-color: rgba(255,255,255,0.05);
            padding: 10px;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------- TITLE ---------------- #

st.title("💎 Crypto Investment Advisor PRO")
st.write("Professional cryptocurrency analytics & smart investment insights.")

st.markdown("---")

# ---------------- INPUTS ---------------- #

st.subheader("💼 Investor Strategy Panel")

col1, col2, col3 = st.columns(3)

with col1:
    budget = st.number_input("💰 Budget ($)", value=1000)
    st.caption("Total capital allocated for trading/investment.")

with col2:
    risk_level = st.selectbox(
        "⚠️ Risk Appetite",
        ["Low Risk", "Medium Risk", "High Risk"]
    )
    st.caption("Controls volatility tolerance.")

with col3:
    horizon = st.selectbox(
        "⏳ Time Horizon",
        ["Short Term", "Mid Term", "Long Term"]
    )
    st.caption("Investment duration preference.")

st.markdown("---")

# ---------------- SELECTION ---------------- #

symbols = st.multiselect(
    "📊 Select Trading Assets",
    ["BTC", "ETH", "BNB", "ADA", "SOL", "XRP", "DOGE", "MATIC", "DOT"],
    default=["BTC", "ETH"]
)

fetch_button = st.button("🚀 Analyze Market")

# ---------------- MAIN ---------------- #

if fetch_button:

    df = fetch_crypto_data(symbols)

    if df.empty:
        st.error("❌ Failed to fetch market data")
        st.stop()

    # ---------------- METRICS ---------------- #

    st.subheader("📈 Market Snapshot")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("💰 Avg Price", f"${df['Price'].mean():,.2f}")
    col2.metric("📊 Avg 24h Change", f"{df['PercentChange24h'].mean():.2f}%")
    col3.metric("🔥 Top Performer", df.sort_values(by="PercentChange24h", ascending=False).iloc[0]["Symbol"])
    col4.metric("⚡ Highest Volume", df.sort_values(by="Volume24h", ascending=False).iloc[0]["Symbol"])

    # ---------------- DATA ---------------- #

    st.markdown("---")
    st.subheader("📊 Live Market Data")

    st.dataframe(df.style.format({
        "Price": "${:,.2f}",
        "MarketCap": "${:,.0f}",
        "Volume24h": "${:,.0f}",
        "PercentChange24h": "{:.2f}%"
    }))

    # ---------------- HISTORY ---------------- #

    st.markdown("---")
    st.subheader("📅 5-Day Price Analytics")

    history_df = fetch_crypto_history(symbols)

    if not history_df.empty:

        history_df["DateOnly"] = history_df["Date"].dt.date

        st.markdown("### 📊 Historical Price Table")

        st.dataframe(history_df.sort_values(by="Date").style.format({
            "Price": "${:,.2f}"
        }))

        # ---------------- LINE CHART ---------------- #

        st.markdown("### 📈 Price Trend")

        fig_line = px.line(
            history_df,
            x="Date",
            y="Price",
            color="Symbol"
        )

        fig_line.update_traces(line=dict(width=3))
        st.plotly_chart(fig_line, use_container_width=True)

        # ---------------- CANDLESTICK ---------------- #

        st.markdown("### 🕯️ Candlestick Price Action")

        ohlc_df = history_df.groupby(
            ["Symbol", "DateOnly"]
        )["Price"].agg(
            Open="first",
            High="max",
            Low="min",
            Close="last"
        ).reset_index()

        for symbol in ohlc_df["Symbol"].unique():

            coin_data = ohlc_df[ohlc_df["Symbol"] == symbol]

            fig_candle = go.Figure(data=[go.Candlestick(
                x=coin_data["DateOnly"],
                open=coin_data["Open"],
                high=coin_data["High"],
                low=coin_data["Low"],
                close=coin_data["Close"]
            )])

            fig_candle.update_layout(title=f"{symbol} Price Action")
            st.plotly_chart(fig_candle, use_container_width=True)

        # ---------------- VOLATILITY ---------------- #

        st.markdown("### 📊 Volatility Meter")

        volatility_df = history_df.groupby("Symbol")["Price"].std().reset_index()
        volatility_df.columns = ["Symbol", "Volatility"]

        fig_volatility = px.bar(
            volatility_df,
            x="Symbol",
            y="Volatility",
            color="Volatility"
        )

        st.plotly_chart(fig_volatility, use_container_width=True)

    else:
        st.warning("⚠️ No historical data available")

    ## ---------------- ADVICE ENGINE ---------------- #

    st.markdown("---")
    st.subheader("🧠 Smart Investment Advice")

    best_coin = None
    advice_msg = ""

    if risk_level == "Low Risk":
        best_coin = df.sort_values(by="MarketCap", ascending=False).iloc[0]
        advice_msg = f"""
    ✅ **{best_coin['Symbol']} Recommended**

    ✔ Strong stability & market dominance  
    ✔ Lower volatility profile  
    ✔ Suitable for long-term investment  
    ✔ Diversification recommended across top coins  
    ✔ Monitor market occasionally but focus on capital preservation  

    💡 *Tip:* Hold positions and avoid short-term speculation. Look for steady growth over months.
    """

    elif risk_level == "Medium Risk":
        best_coin = df.sort_values(by="PercentChange7d", ascending=False).iloc[0]
        advice_msg = f"""
    ✅ **{best_coin['Symbol']} Recommended**

    ✔ Balanced growth potential  
    ✔ Moderate risk-reward ratio  
    ✔ Suitable for swing trading strategies  
    ✔ Diversify across coins showing steady trends  
    ✔ Monitor daily trends and news  

    💡 *Tip:* Rebalance portfolio weekly, and track momentum for possible gains.
    """

    else:  # High Risk
        best_coin = df.sort_values(by="PercentChange24h", ascending=False).iloc[0]
        advice_msg = f"""
    ✅ **{best_coin['Symbol']} Recommended**

    ✔ High short-term momentum  
    ✔ High volatility opportunity  
    ✔ Suitable for aggressive traders  
    ✔ Diversify carefully; consider stop-loss  
    ✔ Follow market news & crypto sentiment closely  

    💡 *Tip:* Use strict risk management and watch for sudden corrections. High reward but high risk.
    """

    st.success(advice_msg)

    # ---------------- SENTIMENT ---------------- #

    st.markdown("---")
    st.subheader("📖 Market Sentiment")

    avg_change = df['PercentChange24h'].mean()

    if avg_change > 2:
        st.success("📈 Bullish Momentum Detected")
    elif avg_change > -2:
        st.info("⚖️ Sideways / Neutral Market")
    else:
        st.warning("📉 Bearish Pressure Observed")

    # ---------------- ADVANCED INSIGHTS ---------------- #

    st.markdown("---")
    st.subheader("📊 Advanced Market Insights")

    # Market Cap Distribution
    fig_marketcap = px.pie(df, names="Symbol", values="MarketCap")
    st.plotly_chart(fig_marketcap, use_container_width=True)

    # Volume vs Price
    fig_volume_price = px.scatter(
        df,
        x="Volume24h",
        y="Price",
        color="Symbol",
        size="MarketCap"
    )
    st.plotly_chart(fig_volume_price, use_container_width=True)

    if not history_df.empty:

        # Moving Average
        history_df["MA"] = history_df.groupby("Symbol")["Price"].transform(
            lambda x: x.rolling(3).mean()
        )

        fig_ma = px.line(history_df, x="Date", y="MA", color="Symbol")
        st.plotly_chart(fig_ma, use_container_width=True)

        # Cumulative Return
        history_df["Return"] = history_df.groupby("Symbol")["Price"].pct_change()
        history_df["Cumulative"] = history_df.groupby("Symbol")["Return"].transform(
            lambda x: (1 + x).cumprod()
        )

        fig_cum = px.line(history_df, x="Date", y="Cumulative", color="Symbol")
        st.plotly_chart(fig_cum, use_container_width=True)

else:
    st.write("👆 Select assets & click **Analyze Market**")
