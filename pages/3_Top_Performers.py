import streamlit as st
import pandas as pd
import altair as alt
from datetime import date

st.set_page_config(page_title="Top Performers", page_icon="⭐", layout="wide")


@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    # Convert Date column to datetime
    df["Date"] = pd.to_datetime(df["Date"])
    # Convert Margin % to numeric
    df["Margin %"] = df["Margin %"].str.replace("%", "").astype(float)
    return df


df = load_data("dummy_sales_data.csv")

st.markdown(
    """
# ⭐ Top Performers
Use this page to quickly identify the top 5 products and top 5 segments, based on total sales, within the filtered dataset.
"""
)

st.sidebar.header("Filters")

# Date Range Filter
min_date = df["Date"].min()
max_date = df["Date"].max()
start_date, end_date = st.sidebar.slider(
    "Select Date Range:",
    min_value=min_date.to_pydatetime().date(),
    max_value=max_date.to_pydatetime().date(),
    value=(min_date.to_pydatetime().date(), max_date.to_pydatetime().date()),
    format="YYYY-MM-DD",
)
filtered_df = df[
    (df["Date"] >= pd.to_datetime(start_date))
    & (df["Date"] <= pd.to_datetime(end_date))
]

# Category Filter
categories = sorted(list(df["Product Category"].unique()))
selected_categories = st.sidebar.multiselect(
    "Choose Product Categories", categories, default=categories
)
filtered_df = filtered_df[filtered_df["Product Category"].isin(selected_categories)]

# Segment Filter
segments = sorted(list(df["Customer Segment"].unique()))
selected_segments = st.sidebar.multiselect(
    "Choose Customer Segments", segments, default=segments
)
filtered_df = filtered_df[filtered_df["Customer Segment"].isin(selected_segments)]

st.write(f"**Date Range:** {start_date} to {end_date}")
st.write(
    f"**Product Categories:** {', '.join(selected_categories) if selected_categories else 'None'}"
)
st.write(
    f"**Customer Segments:** {', '.join(selected_segments) if selected_segments else 'None'}"
)

st.markdown("---")

if filtered_df.empty:
    st.write("No data available with the selected filters.")
else:
    # Top 5 Products by Total Sales
    # Group by Product Sub-Category to identify top products
    top_products = (
        filtered_df.groupby("Product Sub-Category", as_index=False)
        .agg({"Total Sales": "sum"})
        .sort_values("Total Sales", ascending=False)
        .head(5)
    )

    # Top 5 Segments by Total Sales
    top_segments = (
        filtered_df.groupby("Customer Segment", as_index=False)
        .agg({"Total Sales": "sum"})
        .sort_values("Total Sales", ascending=False)
        .head(5)
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Top 5 Products by Total Sales")
        product_chart = (
            alt.Chart(top_products)
            .mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5, color="steelblue")
            .encode(
                x=alt.X("Total Sales:Q", axis=alt.Axis(format="$,.2f")),
                y=alt.Y("Product Sub-Category:N", sort="-x"),
                tooltip=[
                    alt.Tooltip("Product Sub-Category:N"),
                    alt.Tooltip("Total Sales:Q", format="$,.2f"),
                ],
            )
            .properties(width="container", height=300)
        )
        st.altair_chart(product_chart, use_container_width=True)

    with col2:
        st.markdown("### Top 5 Segments by Total Sales")
        segment_chart = (
            alt.Chart(top_segments)
            .mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5, color="orange")
            .encode(
                x=alt.X("Total Sales:Q", axis=alt.Axis(format="$,.2f")),
                y=alt.Y("Customer Segment:N", sort="-x"),
                tooltip=[
                    alt.Tooltip("Customer Segment:N"),
                    alt.Tooltip("Total Sales:Q", format="$,.2f"),
                ],
            )
            .properties(width="container", height=300)
        )
        st.altair_chart(segment_chart, use_container_width=True)

st.markdown("---")

st.write(
    "Use the filters to adjust the dataset and see which products and segments rise to the top under different conditions."
)
