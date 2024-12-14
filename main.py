import streamlit as st
import yfinance as yf

st.title("Stock Price Checker")

# Stock symbol input
symbol = st.text_input("", placeholder="Enter Stock Symbol").upper()

def format_large_number(num):
    if num >= 1e12:
        return f"${num/1e12:.2f}T"
    elif num >= 1e9:
        return f"${num/1e9:.2f}B"
    elif num >= 1e6:
        return f"${num/1e6:.2f}M"
    else:
        return f"${num:,.2f}"

# Search button
if st.button("Search", type="primary"):
    if symbol:
        try:
            # Get stock data
            stock = yf.Ticker(symbol)
            info = stock.info
            
            # Display information in two columns
            for label, value in [
                ("Company Name", info.get('longName', 'N/A')),
                ("Stock Price", f"${info.get('currentPrice', 0):.2f}"),
                ("Market Cap", format_large_number(info.get('marketCap', 0)))
            ]:
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.markdown(f"**{label}**")
                with col2:
                    st.write(value)

            # Company Overview
            st.markdown("**Company Overview**")
            st.write(info.get('longBusinessSummary', 'No description available'))
            
        except Exception as e:
            st.error("Error fetching data. Please check the stock symbol and try again.")