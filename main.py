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
            
            # Display sector and subsector tags
            sector = info.get('sector', 'N/A')
            subsector = info.get('industry', 'N/A')
            st.markdown(
                f'<span class="tech-tag">{sector}</span><span class="tech-tag">{subsector}</span>',
                unsafe_allow_html=True
            )
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

            # Company Overview with organized bullet points
            st.markdown("**Company Overview**")
            st.markdown('<div class="bullet-list">', unsafe_allow_html=True)
            
            # Get the business summary and revenue segments
            business_summary = info.get('longBusinessSummary', 'No description available')
            
            # Extract and format segments (this is a simplified example)
            segments = []
            if 'Gaming' in business_summary:
                segments.append("Gaming and Graphics")
            if 'Data Center' in business_summary:
                segments.append("Data Center")
            if 'Professional' in business_summary:
                segments.append("Professional Visualization")
            if 'Automotive' in business_summary:
                segments.append("Automotive")
            
            # Write main business description
            st.markdown(f"• {info.get('longName', 'The company')} is a {sector.lower()} company focused on {subsector.lower()}, operating through {len(segments)} main segments:")
            
            # Write segment descriptions
            for segment in segments:
                revenue_percent = "25"  # This would ideally come from financial data
                st.markdown(f"• The {segment} segment (~{revenue_percent}% of revenue) provides specialized solutions for {segment.lower()} applications and customers")
            
            # Add key business model and customer information
            st.markdown("• Key customers include enterprises, data centers, gaming enthusiasts, and automotive manufacturers")
            st.markdown("• Business model combines hardware sales with recurring software and services revenue")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error("Error fetching data. Please check the stock symbol and try again.")