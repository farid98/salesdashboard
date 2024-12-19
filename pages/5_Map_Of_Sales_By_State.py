import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Sales by State", page_icon="🗺️", layout="wide")


@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    df["Date"] = pd.to_datetime(df["Date"])
    if "Margin %" in df.columns and df["Margin %"].dtype == object:
        df["Margin %"] = df["Margin %"].str.replace("%", "").astype(float)
    return df


# Load your data
df = load_data("dummy_sales_data.csv")

st.markdown(
    """
# 🗺️ Sales by State
This map shows sales data by state, color-coded to indicate the amount of sales.
Use the filters on the left to adjust the data displayed.
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
)

# filter data based on product category
categories = sorted(list(df["Product Category"].unique()))
selected_categories = st.sidebar.multiselect(
    "Choose Product Categories", categories, default=categories
)
filtered_df_1 = df[df["Product Category"].isin(selected_categories)]


# Filter data based on date range
filtered_df = filtered_df_1[
    (df["Date"] >= pd.to_datetime(start_date))
    & (df["Date"] <= pd.to_datetime(end_date))
]


# Aggregate sales by state
state_sales = filtered_df.groupby("State")["Total Sales"].sum().reset_index()

# Create choropleth map
fig = px.choropleth(
    state_sales,
    locations="State",
    locationmode="USA-states",
    color="Total Sales",
    color_continuous_scale="RdYlGn",
    scope="usa",
    title="Total Sales by State",
    labels={"Total Sales": "Total Sales"},
)

# Show the map
st.plotly_chart(fig)
