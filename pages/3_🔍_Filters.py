import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Filters & Interactive",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Filters & Interactive Analysis")
st.markdown("---")

# Check if data is loaded
if st.session_state.get('df') is None:
    st.warning("⚠️ No dataset loaded. Please upload a CSV file on the main page first.")
    st.stop()

df = st.session_state.df

numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

# Initialize filtered dataframe
filtered_df = df.copy()

st.subheader("Apply Filters")

# Create filter UI in the sidebar
with st.sidebar:
    st.header("🎛️ Filter Panel")

    # Numeric Filters (Range sliders)
    if numeric_cols:
        st.subheader("Numeric Filters")

        for col in numeric_cols:
            min_val = df[col].min()
            max_val = df[col].max()

            if min_val != max_val:  # Only show if there's a range
                selected_range = st.slider(
                    f"{col} Range",
                    float(min_val),
                    float(max_val),
                    (float(min_val), float(max_val)),
                    key=f"slider_{col}"
                )

                filtered_df = filtered_df[
                    (filtered_df[col] >= selected_range[0]) &
                    (filtered_df[col] <= selected_range[1])
                ]

# Display filtered data info
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Original Records", len(df))

with col2:
    st.metric("Filtered Records", len(filtered_df))

with col3:
    percentage = (len(filtered_df) / len(df) * 100) if len(df) > 0 else 0
    st.metric("Percentage", f"{percentage:.1f}%")

st.markdown("---")

# Tabs for different views
tabs = st.tabs(["Data View", "Summary Stats", "Visualizations", "Comparisons"])

# TAB 1: Data View
with tabs[0]:
    st.subheader("Filtered Data")

    col1, col2 = st.columns([2, 1])

    with col1:
        rows_to_show = st.slider("Rows to display:", 5, 100, 10)

    with col2:
        sort_col = st.selectbox("Sort by:", df.columns, key="sort_col")

    display_df = filtered_df.sort_values(by=sort_col).head(rows_to_show)
    st.dataframe(display_df, use_container_width=True)

    # Download filtered data
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="⬇️ Download Filtered Data (CSV)",
        data=csv,
        file_name="filtered_data.csv",
        mime="text/csv"
    )

# TAB 2: Summary Stats
with tabs[1]:
    st.subheader("Summary Statistics of Filtered Data")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.write("**Numeric Summary:**")
        st.dataframe(filtered_df[numeric_cols].describe(), use_container_width=True)

    with col2:
        st.write("**Data Types:**")
        dtype_df = pd.DataFrame({
            'Column': filtered_df.columns,
            'Type': filtered_df.dtypes.astype(str)
        })
        st.dataframe(dtype_df, use_container_width=True)

    # Key metrics
    if 'price' in numeric_cols:
        st.write("---")
        st.write("**Price Summary (Filtered):**")

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric("Avg Price", f"${filtered_df['price'].mean():,.0f}")
        with col2:
            st.metric("Median Price", f"${filtered_df['price'].median():,.0f}")
        with col3:
            st.metric("Min Price", f"${filtered_df['price'].min():,.0f}")
        with col4:
            st.metric("Max Price", f"${filtered_df['price'].max():,.0f}")
        with col5:
            st.metric("Std Dev", f"${filtered_df['price'].std():,.0f}")

# TAB 3: Visualizations
with tabs[2]:
    st.subheader("Visualizations of Filtered Data")

    col1, col2 = st.columns(2)

    with col1:
        viz_type = st.selectbox("Visualization Type:",
                               ["Histogram", "Box Plot", "Scatter"],
                               key="filtered_viz")

        if viz_type == "Histogram" and numeric_cols:
            col_hist = st.selectbox("Column:", numeric_cols, key="filtered_hist")
            fig = px.histogram(filtered_df, x=col_hist, nbins=40,
                             title=f"Distribution of {col_hist} (Filtered)")
            st.plotly_chart(fig, use_container_width=True)

        elif viz_type == "Box Plot" and numeric_cols:
            col_box = st.selectbox("Column:", numeric_cols, key="filtered_box")
            fig = px.box(filtered_df, y=col_box,
                        title=f"Box Plot of {col_box} (Filtered)")
            st.plotly_chart(fig, use_container_width=True)

        elif viz_type == "Scatter" and len(numeric_cols) > 1:
            col_x = st.selectbox("X-axis:", numeric_cols, key="filtered_scatter_x")
            col_y = st.selectbox("Y-axis:", numeric_cols, key="filtered_scatter_y")

            fig = px.scatter(filtered_df, x=col_x, y=col_y,
                           title=f"{col_x} vs {col_y} (Filtered)")
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        if 'price' in numeric_cols:
            feature = st.selectbox("Compare Price with:",
                                  [col for col in numeric_cols if col != 'price'],
                                  key="price_compare")

            fig = px.scatter(filtered_df, x=feature, y='price',
                           title=f"Price vs {feature} (Filtered)",
                           trendline="ols")
            st.plotly_chart(fig, use_container_width=True)

# TAB 4: Comparisons
with tabs[3]:
    st.subheader("Comparative Analysis of Filtered Data")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Categorical Distribution**")
        if categorical_cols:
            cat_col = st.selectbox("Category:", categorical_cols, key="filtered_cat")
            value_counts = filtered_df[cat_col].value_counts()

            fig = px.bar(x=value_counts.index, y=value_counts.values,
                        title=f"{cat_col} Distribution",
                        labels={'x': cat_col, 'y': 'Count'})
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.write("**Price by Category**")
        if 'price' in numeric_cols and categorical_cols:
            cat_col = st.selectbox("Group by:", categorical_cols, key="filtered_price_cat")

            fig = px.box(filtered_df, x=cat_col, y='price',
                        title=f"Price Distribution by {cat_col}")
            st.plotly_chart(fig, use_container_width=True)

