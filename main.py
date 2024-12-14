import streamlit as st
import yfinance as yf

st.title("Stock Price Checker")

# Stock symbol input
symbol = st.text_input("Stock Symbol", value="", label_visibility="collapsed").upper()

def format_large_number(num):
    return f"${num:,.2f}"

# Search button
if st.button("Search", type="primary"):
    if symbol:
        try:
            # Get stock data
            stock = yf.Ticker(symbol)
            info = stock.info
            
            # Display sector and industry tags
            sector = info.get('sector', 'N/A')
            industry = info.get('industry', 'N/A')
            st.markdown(f"**Sector:** {sector} | **Industry:** {industry}")
            st.markdown("---")

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

            # Company Overview with bullet points
            st.markdown("**Company Overview**")
            business_summary = info.get('longBusinessSummary', 'No description available')
            # Split into sentences and create bullet points
            sentences = [s.strip() for s in business_summary.split('.') if s.strip()]
            for sentence in sentences:
                if sentence:  # Only create bullet point if sentence is not empty
                    st.markdown(f"• {sentence}.")
            
        except Exception as e:
            st.error("Error fetching data. Please check the stock symbol and try again.")