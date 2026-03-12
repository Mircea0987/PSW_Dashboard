import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

# Configure page layout
st.set_page_config(
    page_title="House Price Dashboard",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for storing the dataframe
if 'df' not in st.session_state:
    st.session_state.df = None

st.title("🏠 House Price Dashboard")
st.markdown("---")

# Main page content
st.header("Welcome to the House Price Dashboard")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    This dashboard allows you to explore and analyze house pricing data.
    
    **Features:**
    - 📊 Upload your CSV file with house data
    - 📈 View comprehensive statistics
    - 📉 Explore interactive visualizations
    - 🔍 Filter and search the data
    """)

with col2:
    st.info("**Dataset Status**\n\n" +
            ("✅ Dataset loaded" if st.session_state.df is not None else "❌ No dataset loaded"))

# CSV Upload Section
st.markdown("---")
st.subheader("📁 Upload Your Data")

uploaded_file = st.file_uploader(
    "Upload a CSV file with house price data",
    type=['csv'],
    help="Make sure your CSV contains columns like: date, price, bedrooms, bathrooms, sqft_living, etc."
)

# 1. DATA LOADING PHASE
df = None

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("✅ File uploaded successfully!")
    except Exception as e:
        st.error(f"❌ Error reading file: {str(e)}")
else:
    # Fallback to the default file
    try:
        df = pd.read_csv("./data/data.csv")
        st.info("ℹ️ No file uploaded. Using the default house price dataset.")
    except FileNotFoundError:
        st.warning("⚠️ Awaiting file upload... (Default file not found on server)")

# 2. DATA DISPLAY & STORAGE PHASE
if df is not None:
    # Save to session state so it persists across interactions
    st.session_state.df = df

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Records", len(df))
    with col2:
        st.metric("Total Columns", len(df.columns))

    # Show data preview
    st.subheader("Data Preview")
    st.dataframe(df.head(10))

    # Show column information
    st.subheader("Column Information")
    col1, col2 = st.columns(2)

    with col1:
        st.write("**Column Names:**")
        st.code("\n".join(df.columns.tolist()))

    with col2:
        st.write("**Data Types:**")
        dtype_info = df.dtypes.astype(str).to_dict()
        st.json(dtype_info)


# Navigation info
st.markdown("---")
st.info("""
👈 **Navigation:** Use the sidebar to navigate to different pages:
- **📊 Statistics** - View key metrics and summaries
- **📈 Visualizations** - Explore charts and graphs
- **🔍 Filters** - Interact with the data using filters
""")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>"
    "House Price Dashboard | Created with Streamlit"
    "</p>",
    unsafe_allow_html=True
)

