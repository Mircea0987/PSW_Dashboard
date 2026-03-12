import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Statistics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Statistics & Summary")
st.markdown("---")

# Check if data is loaded
if st.session_state.get('df') is None:
    st.warning("⚠️ No dataset loaded. Please upload a CSV file on the main page first.")
    st.stop()

df = st.session_state.df

# Key Metrics Section
st.subheader("Key Metrics")

col1, col2, col3, col4, col5 = st.columns(5)

numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

if 'price' in numeric_cols:
    with col1:
        st.metric("Average Price", f"${df['price'].mean():,.0f}")
    with col2:
        st.metric("Median Price", f"${df['price'].median():,.0f}")
    with col3:
        st.metric("Min Price", f"${df['price'].min():,.0f}")
    with col4:
        st.metric("Max Price", f"${df['price'].max():,.0f}")
    with col5:
        st.metric("Std Dev", f"${df['price'].std():,.0f}")

# Detailed Statistics
st.subheader("Detailed Statistics")

tabs = st.tabs(["Summary Stats", "Numeric Columns", "Missing Values", "Correlations"])

with tabs[0]:
    st.dataframe(df.describe(), use_container_width=True)

with tabs[1]:
    if numeric_cols:
        selected_col = st.selectbox("Select a column to analyze:", numeric_cols)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Mean", f"{df[selected_col].mean():.2f}")
        with col2:
            st.metric("Median", f"{df[selected_col].median():.2f}")
        with col3:
            st.metric("Std Dev", f"{df[selected_col].std():.2f}")
        with col4:
            st.metric("Variance", f"{df[selected_col].var():.2f}")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("25th Percentile", f"{df[selected_col].quantile(0.25):.2f}")
        with col2:
            st.metric("50th Percentile", f"{df[selected_col].quantile(0.50):.2f}")
        with col3:
            st.metric("75th Percentile", f"{df[selected_col].quantile(0.75):.2f}")
        with col4:
            st.metric("IQR", f"{df[selected_col].quantile(0.75) - df[selected_col].quantile(0.25):.2f}")

with tabs[2]:
    missing_data = pd.DataFrame({
        'Column': df.columns,
        'Missing Count': df.isnull().sum().values,
        'Missing %': (df.isnull().sum().values / len(df) * 100).round(2)
    })
    st.dataframe(missing_data, use_container_width=True)

    if missing_data['Missing Count'].sum() == 0:
        st.success("✅ No missing values found!")

with tabs[3]:
    if len(numeric_cols) > 1:
        corr_matrix = df[numeric_cols].corr()
        st.dataframe(corr_matrix, use_container_width=True)
    else:
        st.info("Need at least 2 numeric columns for correlation analysis")

# Distribution Analysis
st.subheader("Distribution Analysis")

if numeric_cols:
    col_to_analyze = st.selectbox("Select a numeric column to analyze distribution:", numeric_cols, key="dist")

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Skewness:** {df[col_to_analyze].skew():.4f}")
        st.write(f"**Kurtosis:** {df[col_to_analyze].kurtosis():.4f}")

    with col2:
        st.write(f"**Range:** {df[col_to_analyze].max() - df[col_to_analyze].min():.2f}")
        st.write(f"**Coefficient of Variation:** {(df[col_to_analyze].std() / df[col_to_analyze].mean()):.4f}")

