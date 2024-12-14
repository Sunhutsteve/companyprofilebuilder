import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Financial Terminal",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply custom CSS
with open('.streamlit/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Cache the stock data fetch
@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_stock_data(symbol):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        
        # Get historical data for the last month
        hist = stock.history(period="1mo")
        
        return {
            'info': info,
            'history': hist,
            'error': None
        }
    except Exception as e:
        return {
            'info': None,
            'history': None,
            'error': str(e)
        }

def format_large_number(num):
    if num >= 1e12:
        return f"${num/1e12:.2f}T"
    elif num >= 1e9:
        return f"${num/1e9:.2f}B"
    elif num >= 1e6:
        return f"${num/1e6:.2f}M"
    else:
        return f"${num:,.2f}"

# App header
st.markdown('<h1 class="main-header">Financial Terminal</h1>', unsafe_allow_html=True)

# Stock symbol input
col1, col2 = st.columns([2, 4])
with col1:
    symbol = st.text_input("Enter Stock Symbol", value="AAPL").upper()

# Fetch data when symbol is entered
if symbol:
    data = get_stock_data(symbol)
    
    if data['error']:
        st.error(f"Error fetching data: {data['error']}")
    else:
        info = data['info']
        history = data['history']
        
        # Company name and basic info
        st.subheader(f"{info['longName']} ({symbol})")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            price_change = info.get('regularMarketChange', 0)
            current_price = info.get('currentPrice', 0)
            if current_price > 0:
                price_change_pct = (price_change / current_price) * 100
            else:
                price_change_pct = 0
            
            st.metric(
                "Current Price",
                f"${current_price:.2f}",
                f"{price_change_pct:.2f}%"
            )
        
        with col2:
            st.metric(
                "Market Cap",
                format_large_number(info['marketCap'])
            )
            
        with col3:
            st.metric(
                "52 Week High",
                f"${info['fiftyTwoWeekHigh']:.2f}"
            )
            
        with col4:
            st.metric(
                "52 Week Low",
                f"${info['fiftyTwoWeekLow']:.2f}"
            )
        
        # Stock price chart
        fig = go.Figure()
        fig.add_trace(
            go.Candlestick(
                x=history.index,
                open=history['Open'],
                high=history['High'],
                low=history['Low'],
                close=history['Close'],
                name='Price'
            )
        )
        
        fig.update_layout(
            title='Stock Price (Last Month)',
            yaxis_title='Price',
            template='plotly_dark',
            height=500,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Company information
        st.subheader("Company Overview")
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"**Business Summary**")
            st.write(info['longBusinessSummary'])
            
        with col2:
            metrics = {
                "Sector": info.get('sector', 'N/A'),
                "Industry": info.get('industry', 'N/A'),
                "P/E Ratio": f"{info.get('trailingPE', 'N/A'):.2f}",
                "Beta": f"{info.get('beta', 'N/A'):.2f}",
                "Volume": format_large_number(info.get('volume', 0)),
                "Avg Volume": format_large_number(info.get('averageVolume', 0))
            }
            
            for key, value in metrics.items():
                st.markdown(f"**{key}:** {value}")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Data provided by Yahoo Finance | Updated: "
    f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    "</div>",
    unsafe_allow_html=True
)
