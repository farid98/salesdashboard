import streamlit as st
import pandas as pd
import altair as alt
from datetime import date

st.set_page_config(
    page_title="Sales Over Time by Category", page_icon="📈", layout="wide"
)


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
# 📈 Sales Over Time by Category
This page shows the sales over time for all product categories on a single graph.

**Features:**
- Filter by date range, customer segments, and states.
- Toggle between daily, monthly, or quarterly aggregation.
- Toggle between showing the data as a trend (periodic) or cumulative over time.

Use the filters on the left to narrow down the data, then select how you want to view the time series.
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

# Segment Filter
segments = sorted(list(df["Customer Segment"].unique()))
selected_segments = st.sidebar.multiselect(
    "Choose Customer Segments", segments, default=segments
)
filtered_df = filtered_df[filtered_df["Customer Segment"].isin(selected_segments)]

# State Filter with "All" option
states = sorted(list(df["State"].unique()))
all_option = ["All"]  # Special option to select all states
state_options = all_option + states

selected_states = st.sidebar.multiselect(
    "Choose States", state_options, default=["All"]
)

# If "All" is selected, use all states
if "All" in selected_states:
    selected_states = states

filtered_df = filtered_df[filtered_df["State"].isin(selected_states)]

st.write(f"**Date Range:** {start_date} to {end_date}")
st.write(
    f"**Customer Segments:** {', '.join(selected_segments) if selected_segments else 'None'}"
)
st.write(f"**States:** {', '.join(selected_states) if selected_states else 'None'}")

st.markdown("---")

# View type: Trend or Cumulative
view_type = st.radio(
    "Select View Type:", ["Trend (Daily/Periodic)", "Cumulative"], index=0
)

# Frequency selection: Daily, Monthly, Quarterly
freq = st.radio("Select Frequency:", ["Daily", "Monthly", "Quarterly"], index=0)

if filtered_df.empty:
    st.write("No data available with the selected filters.")
else:
    # Depending on the frequency selected, we transform the dates
    freq_df = filtered_df.copy()

    if freq == "Daily":
        # Keep data as is, just group by day
        freq_df["Period"] = freq_df["Date"]
    elif freq == "Monthly":
        # Convert to monthly period
        freq_df["Period"] = freq_df["Date"].dt.to_period("M").dt.to_timestamp()
    else:  # Quarterly
        freq_df["Period"] = freq_df["Date"].dt.to_period("Q").dt.to_timestamp()

    # Group data by Category and Period
    grouped = (
        freq_df.groupby(["Product Category", "Period"], as_index=False)["Total Sales"]
        .sum()
        .sort_values("Period")
    )

    if view_type == "Cumulative":
        # Calculate cumulative sales per category
        grouped["Value"] = grouped.groupby("Product Category")["Total Sales"].cumsum()
        y_axis_title = "Cumulative Sales"
        chart_title = f"Cumulative Sales Over Time by Category ({freq})"
        tooltip_value = "Value"
    else:
        # Just use the periodic sum
        grouped["Value"] = grouped["Total Sales"]
        y_axis_title = "Sales"
        chart_title = f"{freq} Sales Over Time by Category"
        tooltip_value = "Value"

    # Create line chart with all categories
    line_chart = (
        alt.Chart(grouped)
        .mark_line(point=False)
        .encode(
            x="Period:T",
            y=alt.Y("Value:Q", title=y_axis_title, axis=alt.Axis(format="$.2f")),
            color="Product Category:N",
            tooltip=[
                alt.Tooltip("Period:T"),
                alt.Tooltip("Product Category:N"),
                alt.Tooltip(tooltip_value, format="$.2f"),
            ],
        )
        .properties(title=chart_title, width="container", height=400)
    )

    st.altair_chart(line_chart, use_container_width=True)

st.markdown("---")

st.write(
    "Use the filters in the sidebar to adjust the data. Use the toggles above to switch between daily, monthly, or quarterly views, and between trend or cumulative displays."
)
