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
            
            # Display company info
            st.write("Company Name")
            st.write(info.get('longName', 'N/A'))
            
            # Display stock price
            st.write("Stock Price")
            st.write(f"${info.get('currentPrice', 0):.2f}")
            
            # Display market cap
            st.write("Market Cap")
            st.write(format_large_number(info.get('marketCap', 0)))
            
        except Exception as e:
            st.error("Error fetching data. Please check the stock symbol and try again.")