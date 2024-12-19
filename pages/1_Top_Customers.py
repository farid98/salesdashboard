import pandas as pd
import plotly.express as px
import streamlit as st

# Load your data
df = pd.read_csv("dummy_sales_data.csv")

# Top 5 customers by Total Sales
top_customers_sales = df.nlargest(5, "Total Sales").sort_values(
    by="Total Sales", ascending=True
)

# Top 5 customers by Margin
top_customers_profit = df.nlargest(5, "Margin").sort_values(by="Margin", ascending=True)

# Streamlit app content
st.markdown("# 🏆 Top Customers")
st.markdown("## Top 5 Customers by Total Sales")
fig_sales = px.bar(
    top_customers_sales,
    x="Total Sales",
    y="Customer Name",
    title="Top 5 Customers by Total Sales",
    orientation="h",
)
st.plotly_chart(fig_sales)

st.markdown("## Top 5 Customers by Margin")
fig_profit = px.bar(
    top_customers_profit,
    x="Margin",
    y="Customer Name",
    title="Top 5 Customers by Margin",
    orientation="h",
)
st.plotly_chart(fig_profit)
