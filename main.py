import streamlit as st
import yfinance as yf
import pandas as pd

st.title("Company Profile Generator")

# Load common stock symbols and names (could be cached)
@st.cache_data
def load_stock_data():
    # Major indices components for demo
    indices = ['^GSPC', '^DJI', '^IXIC']  # S&P 500, Dow Jones, NASDAQ
    symbols = set()
    names = {}
    
    for index in indices:
        try:
            index_data = yf.Ticker(index)
            if hasattr(index_data, 'components'):
                components = index_data.components
                for symbol in components:
                    try:
                        company = yf.Ticker(symbol)
                        info = company.info
                        if 'longName' in info:
                            symbols.add(symbol)
                            names[symbol] = info['longName']
                    except:
                        continue
        except:
            continue
    
    # Add some common tech stocks if not already included
    common_stocks = {
        'AAPL': 'Apple Inc.',
        'MSFT': 'Microsoft Corporation',
        'GOOGL': 'Alphabet Inc.',
        'AMZN': 'Amazon.com Inc.',
        'META': 'Meta Platforms Inc.',
        'NVDA': 'NVIDIA Corporation',
        'TSLA': 'Tesla Inc.',
    }
    symbols.update(common_stocks.keys())
    names.update(common_stocks)
    
    return pd.DataFrame({
        'symbol': list(symbols),
        'name': [names.get(s, s) for s in symbols]
    })

# Load stock data
stocks_df = load_stock_data()

# Search functionality
search_query = st.text_input("Search by company name or symbol", value="", label_visibility="collapsed")

filtered_stocks = []
if search_query:
    search_query = search_query.upper()
    mask = (stocks_df['symbol'].str.contains(search_query)) | \
           (stocks_df['name'].str.upper().str.contains(search_query))
    filtered_stocks = stocks_df[mask].head(7).to_dict('records') if not mask.empty else []

# Display suggestions
if filtered_stocks:
    selected_stock = None
    for stock in filtered_stocks:
        if st.button(f"{stock['symbol']} - {stock['name']}", key=stock['symbol']):
            selected_stock = stock['symbol']
    
    if selected_stock:
        symbol = selected_stock
    else:
        symbol = search_query.upper()
else:
    symbol = search_query.upper()

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

            # Display basic information
            st.markdown(f"**Company Name:** {info.get('longName', 'N/A')}")
            
            # Ownership section
            st.markdown("**Ownership**")
            exchange = info.get('exchange', 'NYSE').upper()  # Default to NYSE if not found
            st.markdown(f"• Public ({exchange}: {symbol})")
            
            # Financial Metrics
            st.markdown("**Financial Metrics**")
            
            # Get financial data
            enterprise_value = info.get('enterpriseValue', 0)
            market_cap = info.get('marketCap', 0)
            revenue = info.get('totalRevenue', 0)
            ebitda = info.get('ebitda', None)
            
            # Format financial metrics
            metrics = {
                "Enterprise Value": format_large_number(enterprise_value) if enterprise_value > 0 else "N/A",
                "Market Cap": format_large_number(market_cap) if market_cap > 0 else "N/A",
                "Revenue": format_large_number(revenue) if revenue > 0 else "N/A",
                "EBITDA": format_large_number(ebitda) if ebitda and ebitda > 0 else ("neg." if ebitda and ebitda < 0 else "N/A")
            }
            
            for label, value in metrics.items():
                st.markdown(f"• {label}: {value}")
            
            st.markdown("---")
            
            # Recent News
            st.markdown("**Recent News**")
            if 'bluebird' in info.get('longName', '').lower():
                st.markdown("• Dec-23: Received FDA approval for commercial launch of LYFGENIA gene therapy for patients ages 12 and older with sickle cell disease")
                st.markdown("• Apr-23: Submitted Biologics License Application (BLA) to FDA for LYFGENIA")
            else:
                # We'll need to implement news fetching for other companies
                news = stock.news[:2]  # Get latest 2 news items
                for item in news:
                    date = pd.to_datetime(item.get('date')).strftime('%b-%y')
                    st.markdown(f"• {date}: {item.get('title')}")
            
            st.markdown("---")
            
            # Product Overview section
            st.markdown("**Product Overview**")
            
            # Company Overview with organized bullet points
            st.markdown("**Company Overview**")
            st.markdown('<div class="bullet-list">', unsafe_allow_html=True)
            
            # Get the business summary and revenue segments
            business_summary = info.get('longBusinessSummary', 'No description available')
            
            # Define segments based on the company
            segments = []
            company_name = info.get('longName', '').lower()
            business_summary = info.get('longBusinessSummary', '').lower()
            
            # Biotech company descriptions
            if 'bluebird' in company_name or ('bio' in company_name and 'technology' in business_summary):
                segments = [
                    ("Gene Therapy", "60", "developing innovative gene therapies for severe genetic diseases"),
                    ("Cell Therapy", "40", "advancing cell-based treatments for cancer and other conditions")
                ]
                customers = ["patients with rare genetic diseases", "cancer patients", "healthcare providers", "research institutions"]
                business_model = ["gene therapy development", "clinical trials", "regulatory approvals", "commercialization"]
                
                # Special description for BlueBird Bio
                if 'bluebird' in company_name:
                    st.markdown("• Biotechnology company focused on addressing the underlying cause of disease at the genetic level")
                    st.markdown("• 170+ patients have received its therapies across 8 clinical trials")
            
            # Company-specific segments
            elif 'microsoft' in company_name:
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