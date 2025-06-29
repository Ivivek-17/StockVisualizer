# app.py
import streamlit as st
import yfinance as yf
import mplfinance as mpf
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Stock Visualizer", layout="centered")

st.title("📈 Stock Market Visualizer")

# 1. Sidebar Inputs
st.sidebar.header("Input Parameters")
ticker = st.sidebar.text_input("Stock Ticker (e.g., AAPL, TSLA)", "AAPL").upper()
start = st.sidebar.date_input("Start Date", datetime(2023, 1, 1))
end = st.sidebar.date_input("End Date", datetime.today())

# 2. Fetch Data
@st.cache_data
def fetch_data(ticker, start, end):
    return yf.download(ticker, start=start, end=end)

# 3. Generate Plots
def plot_candlestick(data, ticker):
    mpf.plot(data, type='candle', volume=True, style='yahoo',
             mav=(5, 20), title=f"{ticker} Candlestick Chart",
             savefig='chart.png')

# 4. Display Data and Charts
if st.sidebar.button("Fetch & Visualize"):
    with st.spinner("Fetching data..."):
        data = fetch_data(ticker, start, end)

    if not data.empty:
        st.success(f"Fetched {len(data)} data points for {ticker}")
        st.write(data.tail())

        # Line chart
        st.subheader("🔹 Closing Price Trend")
        st.line_chart(data["Close"])

                # Candlestick chart
        st.subheader("🕯 Candlestick Chart (with Volume & MA)")
        
        # Clean data for mplfinance
        data = data.dropna()
        data = data.astype({
            'Open': 'float',
            'High': 'float',
            'Low': 'float',
            'Close': 'float',
            'Volume': 'float'
        })

        plot_candlestick(data, ticker)
        # Download Option
        with open("chart.png", "rb") as f:
            st.download_button("📥 Download Chart", f, file_name=f"{ticker}_chart.png")
    else:
        st.error("No data found. Please check the inputs.")