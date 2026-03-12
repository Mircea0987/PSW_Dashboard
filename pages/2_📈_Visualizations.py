import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="Visualizations",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Visualizations & Charts")
st.markdown("---")

# Check if data is loaded
if st.session_state.get('df') is None:
    st.warning("⚠️ No dataset loaded. Please upload a CSV file on the main page first.")
    st.stop()

df = st.session_state.df

numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

# Create tabs for different visualizations
tabs = st.tabs(["Distribution", "Price Analysis", "Relationships", "Comparisons"])

# TAB 1: Distribution Charts
with tabs[0]:
    st.subheader("Distribution Visualizations")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Histogram - Select Column:**")
        hist_col = st.selectbox("Choose numeric column for histogram:", numeric_cols, key="hist")

        fig_hist = px.histogram(df, x=hist_col, nbins=50, title=f"Distribution of {hist_col}")
        fig_hist.update_layout(height=400, xaxis_title=hist_col, yaxis_title="Frequency")
        st.plotly_chart(fig_hist, use_container_width=True)

    with col2:
        st.write("**Box Plot - Select Column:**")
        box_col = st.selectbox("Choose numeric column for box plot:", numeric_cols, key="box")

        fig_box = px.box(df, y=box_col, title=f"Box Plot of {box_col}")
        fig_box.update_layout(height=400)
        st.plotly_chart(fig_box, use_container_width=True)

# TAB 2: Price Analysis
with tabs[1]:
    st.subheader("Price Analysis")

    if 'price' in numeric_cols:
        col1, col2, col3 = st.columns(3)

        with col1:
            st.write("**Price Distribution**")
            fig_price = px.histogram(df, x='price', nbins=50, title="House Price Distribution")
            fig_price.update_layout(height=400)
            st.plotly_chart(fig_price, use_container_width=True)

        with col2:
            st.write("**Price Box Plot**")
            fig_price_box = px.box(df, y='price', title="Price Quartiles")
            fig_price_box.update_layout(height=400)
            st.plotly_chart(fig_price_box, use_container_width=True)

        with col3:
            st.write("**Price Statistics**")
            st.metric("Mean Price", f"${df['price'].mean():,.0f}")
            st.metric("Median Price", f"${df['price'].median():,.0f}")
            st.metric("Std Dev", f"${df['price'].std():,.0f}")

        # Price vs numeric features
        st.write("---")
        st.write("**Price vs Features**")

        feature_col = st.selectbox("Select a feature to compare with price:",
                                   [col for col in numeric_cols if col != 'price'],
                                   key="scatter")

        fig_scatter = px.scatter(df, x=feature_col, y='price',
                                title=f"Price vs {feature_col}",
                                trendline="ols")
        fig_scatter.update_layout(height=500)
        st.plotly_chart(fig_scatter, use_container_width=True)

    else:
        st.warning("⚠️ 'price' column not found in dataset")

# TAB 3: Relationships
with tabs[2]:
    st.subheader("Feature Relationships")

    if len(numeric_cols) > 1:
        col1, col2 = st.columns([1, 1])

        with col1:
            x_feature = st.selectbox("Select X-axis feature:", numeric_cols, key="rel_x")

        with col2:
            y_feature = st.selectbox("Select Y-axis feature:", numeric_cols,
                                    index=min(1, len(numeric_cols)-1), key="rel_y")

        if x_feature != y_feature:
            fig_rel = px.scatter(df, x=x_feature, y=y_feature,
                                title=f"{x_feature} vs {y_feature}",
                                trendline="ols" if x_feature != 'date' else None)
            fig_rel.update_layout(height=500)
            st.plotly_chart(fig_rel, use_container_width=True)

    # Correlation heatmap
    if len(numeric_cols) > 1:
        st.write("---")
        st.write("**Correlation Heatmap**")

        corr_matrix = df[numeric_cols].corr()

        fig_heatmap = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu',
            zmid=0
        ))
        fig_heatmap.update_layout(height=600, width=800)
        st.plotly_chart(fig_heatmap, use_container_width=True)

# TAB 4: Comparisons
with tabs[3]:
    st.subheader("Comparative Analysis")

    if categorical_cols:
        st.write("**Category Comparison**")

        col1, col2 = st.columns([1, 1])

        with col1:
            category = st.selectbox("Select categorical column:", categorical_cols, key="cat_comp")

        with col2:
            if 'price' in numeric_cols:
                numeric_col = st.selectbox("Select numeric column:", numeric_cols, key="num_comp")
            else:
                numeric_col = st.selectbox("Select numeric column:", numeric_cols, key="num_comp2")

        fig_box = px.box(df, x=category, y=numeric_col,
                        title=f"{numeric_col} by {category}")
        fig_box.update_layout(height=500)
        st.plotly_chart(fig_box, use_container_width=True)

        # Bar chart for counts
        st.write("---")
        st.write("**Category Counts**")

        category_counts = df[category].value_counts()
        fig_bar = px.bar(x=category_counts.index, y=category_counts.values,
                        title=f"Count of {category}",
                        labels={'x': category, 'y': 'Count'})
        fig_bar.update_layout(height=400)
        st.plotly_chart(fig_bar, use_container_width=True)

    else:
        st.info("No categorical columns available for comparison")

# Additional visualizations
st.markdown("---")
st.subheader("Custom Visualization")

viz_type = st.selectbox("Select visualization type:",
                        ["Histogram", "Scatter Plot", "Box Plot", "Bar Chart"])

col1, col2 = st.columns([1, 1])

if viz_type == "Histogram":
    with col1:
        col = st.selectbox("Select column:", numeric_cols, key="custom_hist")
    with col2:
        bins = st.slider("Number of bins:", 10, 100, 50, key="hist_bins")

    fig = px.histogram(df, x=col, nbins=bins, title=f"Histogram of {col}")
    st.plotly_chart(fig, use_container_width=True)

elif viz_type == "Scatter Plot":
    with col1:
        x_col = st.selectbox("X-axis:", numeric_cols, key="custom_scatter_x")
    with col2:
        y_col = st.selectbox("Y-axis:", numeric_cols, key="custom_scatter_y")

    fig = px.scatter(df, x=x_col, y=y_col, title=f"{x_col} vs {y_col}")
    st.plotly_chart(fig, use_container_width=True)

elif viz_type == "Box Plot":
    with col1:
        col = st.selectbox("Select column:", numeric_cols, key="custom_box")
    with col2:
        if categorical_cols:
            cat_col = st.selectbox("Group by (optional):", ["None"] + categorical_cols, key="custom_box_group")
        else:
            cat_col = "None"

    if cat_col != "None":
        fig = px.box(df, x=cat_col, y=col, title=f"{col} grouped by {cat_col}")
    else:
        fig = px.box(df, y=col, title=f"Box Plot of {col}")

    st.plotly_chart(fig, use_container_width=True)

elif viz_type == "Bar Chart":
    with col1:
        if categorical_cols:
            col = st.selectbox("Select categorical column:", categorical_cols, key="custom_bar")
        else:
            st.warning("No categorical columns available")
            st.stop()

    with col2:
        top_n = st.slider("Show top N:", 5, 50, 10, key="bar_top_n")

    value_counts = df[col].value_counts().head(top_n)
    fig = px.bar(x=value_counts.index, y=value_counts.values,
                title=f"Top {top_n} {col}", labels={'x': col, 'y': 'Count'})
    st.plotly_chart(fig, use_container_width=True)

