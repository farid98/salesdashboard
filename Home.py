import streamlit as st
import pandas as pd
import altair as alt
from datetime import date

st.set_page_config(page_title="Sales Dashboard", page_icon="💼", layout="wide")


@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    # Convert Date column to datetime
    df["Date"] = pd.to_datetime(df["Date"])
    # Convert Margin % to a numeric value (remove '%')
    df["Margin %"] = df["Margin %"].str.replace("%", "").astype(float)
    return df


df = load_data("dummy_sales_data.csv")

# Title and Intro
st.markdown(
    """
# 📊 Sales Dashboard
Welcome to the Sales Dashboard! This dashboard provides an interactive and dynamic way to explore sales, margins, and product performance across various dimensions.

Use the sidebar filters to narrow down the data and explore different views of the metrics. Use the navigation in the top-left corner to access the drill-down page for more detailed analyses.
"""
)

st.markdown("---")

# Sidebar Filters
st.sidebar.header("Filter Your View")
st.sidebar.markdown("---")
st.sidebar.write(
    "Select the date range, product categories, and customer segments to filter the data."
)


# Date Range via Slider
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

st.markdown(f"**Date Range:** {start_date} to {end_date}")
st.markdown(
    f"**Product Categories:** {', '.join(selected_categories) if selected_categories else 'None'}"
)
st.markdown(
    f"**Customer Segments:** {', '.join(selected_segments) if selected_segments else 'None'}"
)

st.markdown("---")

# High-level Metrics
total_sales = filtered_df["Total Sales"].sum() if not filtered_df.empty else 0
total_margin = filtered_df["Margin"].sum() if not filtered_df.empty else 0
avg_margin_pct = filtered_df["Margin %"].mean() if not filtered_df.empty else 0

# Use theme variables for background and text color
st.markdown(
    """
<style>
.metrics-container {
    background-color: var(--background-color);
    padding: 20px;
    border-radius: 10px;
    color: var(--text-color);
}
.metric-title {
    font-size: 16px;
    font-weight: 600;
}
.metric-value {
    font-size: 28px;
    font-weight: 700;
    margin-top: -8px;
}
</style>
""",
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        f"<div class='metrics-container'>"
        f"<div class='metric-title'>Total Sales</div>"
        f"<div class='metric-value'>${total_sales:,.2f}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        f"<div class='metrics-container'>"
        f"<div class='metric-title'>Total Margin</div>"
        f"<div class='metric-value'>${total_margin:,.2f}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        f"<div class='metrics-container'>"
        f"<div class='metric-title'>Avg Margin %</div>"
        f"<div class='metric-value'>{avg_margin_pct:,.2f}%</div>"
        f"</div>",
        unsafe_allow_html=True,
    )

st.markdown("---")

# Charts Layout
chart_col1, chart_col2 = st.columns(2)
chart_col3, chart_col4 = st.columns(2)

# Sales Over Time
if not filtered_df.empty:
    sales_over_time = filtered_df.groupby("Date", as_index=False)["Total Sales"].sum()

    line_chart = (
        alt.Chart(sales_over_time)
        .mark_line(point=True)
        .encode(
            x="Date:T",
            y="Total Sales:Q",
            tooltip=["Date", alt.Tooltip("Total Sales:Q", format="$.2f")],
        )
        .properties(title="📈 Sales Over Time", width="container", height=300)
    )

    chart_col1.altair_chart(line_chart, use_container_width=True)
else:
    chart_col1.write("No data available for the selected filters.")

# Sales by Product Category
if not filtered_df.empty:
    sales_by_category = filtered_df.groupby("Product Category", as_index=False)[
        "Total Sales"
    ].sum()
    bar_chart_category = (
        alt.Chart(sales_by_category)
        .mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5)
        .encode(
            x=alt.X("Total Sales:Q", axis=alt.Axis(format="$,.2f")),
            y=alt.Y("Product Category:N", sort="-x"),
            color=alt.Color("Product Category:N", legend=None),
            tooltip=[
                alt.Tooltip("Product Category:N"),
                alt.Tooltip("Total Sales:Q", format="$,.2f"),
            ],
        )
        .properties(title="📦 Sales by Product Category", width="container", height=300)
    )

    chart_col2.altair_chart(bar_chart_category, use_container_width=True)
else:
    chart_col2.write("No data available for the selected filters.")

# Sales by State
if not filtered_df.empty:
    sales_by_state = filtered_df.groupby("State", as_index=False)["Total Sales"].sum()
    bar_chart_state = (
        alt.Chart(sales_by_state)
        .mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5, color="teal")
        .encode(
            x="State:N",
            y=alt.Y("Total Sales:Q", axis=alt.Axis(format="$,.2f")),
            tooltip=[
                alt.Tooltip("State:N"),
                alt.Tooltip("Total Sales:Q", format="$,.2f"),
            ],
        )
        .properties(title="🏙️ Sales by State", width="container", height=300)
    )

    chart_col3.altair_chart(bar_chart_state, use_container_width=True)
else:
    chart_col3.write("No data available for the selected filters.")

# Sales by Customer Segment
if not filtered_df.empty:
    sales_by_segment = filtered_df.groupby("Customer Segment", as_index=False)[
        "Total Sales"
    ].sum()
    bar_chart_segment = (
        alt.Chart(sales_by_segment)
        .mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5, color="orange")
        .encode(
            x="Customer Segment:N",
            y=alt.Y("Total Sales:Q", axis=alt.Axis(format="$,.2f")),
            tooltip=[
                alt.Tooltip("Customer Segment:N"),
                alt.Tooltip("Total Sales:Q", format="$,.2f"),
            ],
        )
        .properties(title="🎯 Sales by Customer Segment", width="container", height=300)
    )

    chart_col4.altair_chart(bar_chart_segment, use_container_width=True)
else:
    chart_col4.write("No data available for the selected filters.")

st.markdown("---")

st.write(
    "Use the sidebar to filter the data. Navigate to the 'Drill Down' page (in the sidebar menu) to explore state and city-level details."
)
