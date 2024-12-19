import streamlit as st
import pandas as pd
import altair as alt
from datetime import date

st.set_page_config(page_title="Compare States", page_icon="🔀", layout="wide")


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
# 🔀 Compare Sales Between Two States
Use the filters on the left to narrow down your view. Then select two states below to compare their sales side-by-side. This can help you identify regional differences in sales performance.
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

states_available = sorted(filtered_df["State"].unique().tolist())
col_select1, col_select2 = st.columns(2)
with col_select1:
    selected_state_1 = st.selectbox(
        "Choose the First State:", ["(None)"] + states_available
    )
with col_select2:
    selected_state_2 = st.selectbox(
        "Choose the Second State:", ["(None)"] + states_available
    )

if selected_state_1 != "(None)" and selected_state_2 != "(None)":
    state1_df = filtered_df[filtered_df["State"] == selected_state_1]
    state2_df = filtered_df[filtered_df["State"] == selected_state_2]

    # Ensure there is data for both states
    if state1_df.empty or state2_df.empty:
        st.write("No data available for one or both of the selected states.")
    else:
        # Compute metrics for both states
        total_sales_1 = state1_df["Total Sales"].sum()
        total_margin_1 = state1_df["Margin"].sum()
        avg_margin_pct_1 = state1_df["Margin %"].mean() if not state1_df.empty else 0

        total_sales_2 = state2_df["Total Sales"].sum()
        total_margin_2 = state2_df["Margin"].sum()
        avg_margin_pct_2 = state2_df["Margin %"].mean() if not state2_df.empty else 0

        # Display metrics side by side
        st.markdown(
            """
        <style>
        .metrics-container {
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 10px;
        }
        .metric-title {
            font-size: 16px;
            font-weight: 600;
            color: #555;
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

        st.markdown("## Key Metrics Comparison")

        colA, colB = st.columns(2)
        with colA:
            st.markdown(f"### {selected_state_1}")
            st.markdown(
                "<div class='metrics-container'><div class='metric-title'>Total Sales</div><div class='metric-value'>${:,.2f}</div></div>".format(
                    total_sales_1
                ),
                unsafe_allow_html=True,
            )
            st.markdown(
                "<div class='metrics-container'><div class='metric-title'>Total Margin</div><div class='metric-value'>${:,.2f}</div></div>".format(
                    total_margin_1
                ),
                unsafe_allow_html=True,
            )
            st.markdown(
                "<div class='metrics-container'><div class='metric-title'>Avg Margin %</div><div class='metric-value'>{:,.2f}%</div></div>".format(
                    avg_margin_pct_1
                ),
                unsafe_allow_html=True,
            )

        with colB:
            st.markdown(f"### {selected_state_2}")
            st.markdown(
                "<div class='metrics-container'><div class='metric-title'>Total Sales</div><div class='metric-value'>${:,.2f}</div></div>".format(
                    total_sales_2
                ),
                unsafe_allow_html=True,
            )
            st.markdown(
                "<div class='metrics-container'><div class='metric-title'>Total Margin</div><div class='metric-value'>${:,.2f}</div></div>".format(
                    total_margin_2
                ),
                unsafe_allow_html=True,
            )
            st.markdown(
                "<div class='metrics-container'><div class='metric-title'>Avg Margin %</div><div class='metric-value'>{:,.2f}%</div></div>".format(
                    avg_margin_pct_2
                ),
                unsafe_allow_html=True,
            )

        st.markdown("---")

        st.markdown("## Sales Over Time Comparison")

        # Sales Over Time for both states
        sales_time_state1 = state1_df.groupby("Date", as_index=False)[
            "Total Sales"
        ].sum()
        sales_time_state2 = state2_df.groupby("Date", as_index=False)[
            "Total Sales"
        ].sum()

        line_chart1 = (
            alt.Chart(sales_time_state1)
            .mark_line(point=True)
            .encode(
                x="Date:T",
                y="Total Sales:Q",
                tooltip=["Date", alt.Tooltip("Total Sales:Q", format="$.2f")],
                color=alt.value("steelblue"),
            )
            .properties(
                title=f"{selected_state_1}: Sales Over Time",
                width="container",
                height=300,
            )
        )

        line_chart2 = (
            alt.Chart(sales_time_state2)
            .mark_line(point=True)
            .encode(
                x="Date:T",
                y="Total Sales:Q",
                tooltip=["Date", alt.Tooltip("Total Sales:Q", format="$.2f")],
                color=alt.value("orange"),
            )
            .properties(
                title=f"{selected_state_2}: Sales Over Time",
                width="container",
                height=300,
            )
        )

        colC, colD = st.columns(2)
        colC.altair_chart(line_chart1, use_container_width=True)
        colD.altair_chart(line_chart2, use_container_width=True)

        st.markdown("---")

        st.markdown("## Product Category Breakdown Comparison")

        # Product Category Breakdown
        cat_state1 = state1_df.groupby("Product Category", as_index=False)[
            "Total Sales"
        ].sum()
        cat_state2 = state2_df.groupby("Product Category", as_index=False)[
            "Total Sales"
        ].sum()

        bar_chart_cat1 = (
            alt.Chart(cat_state1)
            .mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5)
            .encode(
                x=alt.X("Total Sales:Q", axis=alt.Axis(format="$,.2f")),
                y=alt.Y("Product Category:N", sort="-x"),
                tooltip=[
                    alt.Tooltip("Product Category:N"),
                    alt.Tooltip("Total Sales:Q", format="$,.2f"),
                ],
                color=alt.value("steelblue"),
            )
            .properties(
                title=f"{selected_state_1}: Sales by Product Category",
                width="container",
                height=300,
            )
        )

        bar_chart_cat2 = (
            alt.Chart(cat_state2)
            .mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5)
            .encode(
                x=alt.X("Total Sales:Q", axis=alt.Axis(format="$,.2f")),
                y=alt.Y("Product Category:N", sort="-x"),
                tooltip=[
                    alt.Tooltip("Product Category:N"),
                    alt.Tooltip("Total Sales:Q", format="$,.2f"),
                ],
                color=alt.value("orange"),
            )
            .properties(
                title=f"{selected_state_2}: Sales by Product Category",
                width="container",
                height=300,
            )
        )

        colE, colF = st.columns(2)
        colE.altair_chart(bar_chart_cat1, use_container_width=True)
        colF.altair_chart(bar_chart_cat2, use_container_width=True)

else:
    st.write("Select two different states above to start the comparison.")
