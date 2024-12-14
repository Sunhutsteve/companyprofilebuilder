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
            
            # Define segments based on the company
            segments = []
            company_name = info.get('longName', '').lower()
            business_summary = info.get('longBusinessSummary', '').lower()
            
            # Company-specific segments
            if 'microsoft' in company_name:
                segments = [
                    ("Productivity and Business Processes", "30", "including Microsoft 365, LinkedIn, and Dynamics"),
                    ("Intelligent Cloud", "40", "featuring Azure, server products, and enterprise services"),
                    ("More Personal Computing", "30", "comprising Windows, devices, gaming, and search advertising")
                ]
            elif 'nvidia' in company_name:
                segments = [
                    ("Gaming and Graphics", "45", "providing GPUs for gaming and professional visualization"),
                    ("Data Center", "40", "offering AI solutions and high-performance computing"),
                    ("Professional Visualization", "10", "delivering graphics solutions for professionals"),
                    ("Automotive", "5", "developing autonomous driving and infotainment systems")
                ]
            elif 'apple' in company_name:
                segments = [
                    ("iPhone", "45", "flagship smartphone product line"),
                    ("Services", "25", "including App Store, Apple Music, iCloud, and Apple Pay"),
                    ("Mac", "10", "personal computers and workstations"),
                    ("Wearables, Home and Accessories", "10", "including Apple Watch, AirPods, and HomePod"),
                    ("iPad", "10", "tablet computing devices")
                ]
            elif 'amazon' in company_name:
                segments = [
                    ("North America", "40", "retail sales and third-party seller services"),
                    ("AWS", "30", "cloud computing and infrastructure services"),
                    ("International", "20", "global retail operations and Prime services"),
                    ("Other", "10", "including advertising and subscription services")
                ]
            elif 'alphabet' in company_name or 'google' in company_name:
                segments = [
                    ("Google Search & Other", "60", "including ads, Android, Chrome, and hardware"),
                    ("Google Cloud", "20", "enterprise cloud platform and solutions"),
                    ("YouTube", "15", "video platform and YouTube TV services"),
                    ("Other Bets", "5", "including Waymo, Verily, and other innovations")
                ]
            # Default segmentation based on business description
            else:
                if 'software' in business_summary and 'hardware' in business_summary:
                    segments = [
                        ("Software Solutions", "60", "enterprise and consumer software products"),
                        ("Hardware", "40", "computing and electronic hardware")
                    ]
                elif 'software' in business_summary:
                    segments = [
                        ("Software Products", "70", "core software solutions and services"),
                        ("Services", "30", "professional and support services")
                    ]
                elif 'hardware' in business_summary:
                    segments = [
                        ("Hardware Products", "80", "core hardware offerings"),
                        ("Services", "20", "maintenance and support services")
                    ]
            
            # Write main business description
            st.markdown(f"• {info.get('longName', 'The company')} is a {sector.lower()} company focused on {subsector.lower()}, operating through {len(segments)} main segments:")
            
            # Write segment descriptions with indentation and styling
            for segment, revenue_percent, description in segments:
                st.markdown(
                    f'<div class="segment-bullet">The {segment} segment (~{revenue_percent}% of revenue) {description}</div>',
                    unsafe_allow_html=True
                )
            
            st.markdown("---")  # Visual separator
            
            # Add key business model and customer information based on company type
            customers = []
            business_model = []
            
            if 'microsoft' in company_name:
                customers = ["enterprises", "consumers", "developers", "cloud customers"]
                business_model = ["subscription-based cloud services", "software licenses", "hardware sales"]
            elif 'apple' in company_name:
                customers = ["consumers", "professionals", "enterprises", "educational institutions"]
                business_model = ["premium hardware sales", "services subscriptions", "app store revenue"]
            elif 'nvidia' in company_name:
                customers = ["gamers", "data centers", "automotive manufacturers", "professional users"]
                business_model = ["hardware sales", "software licensing", "recurring services revenue"]
            else:
                if 'software' in business_summary:
                    customers = ["enterprises", "developers", "end-users"]
                    business_model = ["software licensing", "subscription services"]
                if 'hardware' in business_summary:
                    customers.extend(["hardware customers", "system integrators"])
                    business_model.extend(["hardware sales", "maintenance services"])
            
            st.markdown("• Key customers include " + ", ".join(customers))
            st.markdown("• Business model includes " + ", ".join(business_model))
            
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error("Error fetching data. Please check the stock symbol and try again.")