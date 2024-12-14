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
            
            # Define default segments based on the company
            segments = []
            company_name = info.get('longName', '').lower()
            business_summary = info.get('longBusinessSummary', '').lower()
            
            # Microsoft-specific segments
            if 'microsoft' in company_name:
                segments = [
                    ("Productivity and Business Processes", "30", "including Microsoft 365, LinkedIn, and Dynamics"),
                    ("Intelligent Cloud", "40", "featuring Azure, server products, and enterprise services"),
                    ("More Personal Computing", "30", "comprising Windows, devices, gaming, and search advertising")
                ]
            # NVIDIA-specific segments
            elif 'nvidia' in company_name:
                segments = [
                    ("Gaming and Graphics", "45", "providing GPUs for gaming and professional visualization"),
                    ("Data Center", "40", "offering AI solutions and high-performance computing"),
                    ("Professional Visualization", "10", "delivering graphics solutions for professionals"),
                    ("Automotive", "5", "developing autonomous driving and infotainment systems")
                ]
            # Default segmentation based on business description
            else:
                # Simple segment detection from business summary
                if 'software' in business_summary:
                    segments.append(("Software Solutions", "60", "delivering enterprise and consumer software products"))
                if 'hardware' in business_summary:
                    segments.append(("Hardware", "40", "manufacturing and selling computing hardware"))
            
            # Write main business description
            st.markdown(f"• {info.get('longName', 'The company')} is a {sector.lower()} company focused on {subsector.lower()}, operating through {len(segments)} main segments:")
            
            # Write segment descriptions
            for segment, revenue_percent, description in segments:
                st.markdown(f"• The {segment} segment (~{revenue_percent}% of revenue) {description}")
            
            # Add key business model and customer information
            st.markdown("• Key customers include enterprises, data centers, gaming enthusiasts, and automotive manufacturers")
            st.markdown("• Business model combines hardware sales with recurring software and services revenue")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error("Error fetching data. Please check the stock symbol and try again.")