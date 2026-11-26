
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Superstore Sales Dashboard",
    page_icon="Sales",
    layout="wide"
)

st.title("Superstore Sales Analysis Dashboard")
st.write("Interactive dashboard for analyzing sales, profit, customers and products.")

# ==========================================
# 2. LOAD DATA
# ==========================================

@st.cache_data
def load_data(file):

    df = pd.read_excel(
        file,
        sheet_name="Orders"
    )

    # Convert date columns
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Ship Date"] = pd.to_datetime(df["Ship Date"])

    return df


# Upload Excel file
uploaded_file = st.sidebar.file_uploader(
    "Upload Superstore Excel File",
    type=["xlsx"]
)

if uploaded_file is not None:

    df = load_data(uploaded_file)

else:
    st.info("Please upload your Superstore Excel file.")
    st.stop()

# ==========================================
# 3. SIDEBAR FILTERS
# ==========================================

st.sidebar.header("Dashboard Filters")

regions = st.sidebar.multiselect(
    "Select Region",
    options=sorted(df["Region"].dropna().unique()),
    default=sorted(df["Region"].dropna().unique())
)

categories = st.sidebar.multiselect(
    "Select Category",
    options=sorted(df["Category"].dropna().unique()),
    default=sorted(df["Category"].dropna().unique())
)

segments = st.sidebar.multiselect(
    "Select Customer Segment",
    options=sorted(df["Segment"].dropna().unique()),
    default=sorted(df["Segment"].dropna().unique())
)

ship_modes = st.sidebar.multiselect(
    "Select Ship Mode",
    options=sorted(df["Ship Mode"].dropna().unique()),
    default=sorted(df["Ship Mode"].dropna().unique())
)

min_date = df["Order Date"].min().date()
max_date = df["Order Date"].max().date()

date_range = st.sidebar.date_input(
    "Select Order Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)


# ==========================================
# 4. APPLY FILTERS
# ==========================================

filtered_df = df[
    (df["Region"].isin(regions)) &
    (df["Category"].isin(categories)) &
    (df["Segment"].isin(segments)) &
    (df["Ship Mode"].isin(ship_modes))
].copy()

if len(date_range) == 2:

    start_date, end_date = date_range

    filtered_df = filtered_df[
        (filtered_df["Order Date"].dt.date >= start_date) &
        (filtered_df["Order Date"].dt.date <= end_date)
    ]


# ==========================================
# 5. KPI METRICS
# ==========================================

st.header("Business Performance Overview")
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()
total_quantity = filtered_df["Quantity"].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Sales",
    f"${total_sales:,.2f}"
)

col2.metric(
    "Total Profit",
    f"${total_profit:,.2f}"
)

col3.metric(
    "Total Orders",
    f"{total_orders:,}"
)

col4.metric(
    "Total Quantity",
    f"{total_quantity:,}"
)

st.divider()


# ==========================================
# 6. MONTHLY SALES TREND
# ==========================================

st.header("Sales Trend Analysis")

monthly_sales = (
    filtered_df
    .set_index("Order Date")
    .resample("ME")["Sales"]
    .sum()
    .reset_index()
)

fig1 = px.line(
    monthly_sales,
    x="Order Date",
    y="Sales",
    title="Monthly Sales Trend",
    markers=True,
    template="plotly_white"
)

st.plotly_chart(fig1, use_container_width=True)


# ==========================================
# 7. CATEGORY ANALYSIS
# ==========================================

st.header("Category Analysis")

col1, col2 = st.columns(2)

category_sales = (
    filtered_df.groupby("Category", as_index=False)["Sales"]
    .sum()
)

with col1:

    fig2 = px.pie(
        category_sales,
        names="Category",
        values="Sales",
        title="Sales Distribution by Category",
        hole=0.4
    )

    st.plotly_chart(fig2, use_container_width=True)


subcategory_sales = (
    filtered_df.groupby("Sub-Category", as_index=False)["Sales"]
    .sum()
    .sort_values("Sales", ascending=True)
)

with col2:

    fig3 = px.bar(
        subcategory_sales,
        x="Sales",
        y="Sub-Category",
        orientation="h",
        title="Sales by Sub-Category",
        template="plotly_white"
    )

    st.plotly_chart(fig3, use_container_width=True)


# ==========================================
# 8. REGIONAL ANALYSIS
# ==========================================

st.header("Regional Performance")

col1, col2 = st.columns(2)

region_sales = (
    filtered_df.groupby("Region", as_index=False)
    [["Sales", "Profit"]].sum()
)

with col1:

    fig4 = px.bar(
        region_sales,
        x="Region",
        y="Sales",
        title="Sales by Region",
        color="Region"
    )

    st.plotly_chart(fig4, use_container_width=True)


with col2:

    fig5 = px.bar(
        region_sales,
        x="Region",
        y="Profit",
        title="Profit by Region",
        color="Region"
    )

    st.plotly_chart(fig5, use_container_width=True)


# ==========================================
# 9. TOP 10 CUSTOMERS
# ==========================================

st.header("Customer Analysis")

top_customers = (
    filtered_df.groupby("Customer Name", as_index=False)["Sales"]
    .sum()
    .sort_values("Sales", ascending=False)
    .head(10)
)

fig6 = px.bar(
    top_customers,
    x="Sales",
    y="Customer Name",
    orientation="h",
    title="Top 10 Customers by Sales",
    color="Sales"
)

fig6.update_layout(
    yaxis={"categoryorder": "total ascending"}
)

st.plotly_chart(fig6, use_container_width=True)


# ==========================================
# 10. TOP 10 PRODUCTS
# ==========================================

st.header("Product Analysis")

top_products = (
    filtered_df.groupby("Product Name", as_index=False)["Sales"]
    .sum()
    .sort_values("Sales", ascending=False)
    .head(10)
)

fig7 = px.bar(
    top_products,
    x="Sales",
    y="Product Name",
    orientation="h",
    title="Top 10 Products by Sales",
    color="Sales"
)

fig7.update_layout(
    yaxis={"categoryorder": "total ascending"}
)

st.plotly_chart(fig7, use_container_width=True)


# ==========================================
# 11. SHIPPING ANALYSIS
# ==========================================

st.header("Shipping Analysis")

shipping = (
    filtered_df.groupby("Ship Mode", as_index=False)
    .agg(
        Sales=("Sales", "sum"),
        Orders=("Order ID", "nunique")
    )
)

col1, col2 = st.columns(2)

with col1:

    fig8 = px.bar(
        shipping,
        x="Ship Mode",
        y="Sales",
        title="Sales by Shipping Mode",
        color="Ship Mode"
    )

    st.plotly_chart(fig8, use_container_width=True)


with col2:

    fig9 = px.pie(
        shipping,
        names="Ship Mode",
        values="Orders",
        title="Orders by Shipping Mode"
    )

    st.plotly_chart(fig9, use_container_width=True)





# ==========================================
# 12. FOOTER
# ==========================================

st.divider()

st.caption(
    "Superstore Sales Dashboard | Created using Streamlit, "
    "Pandas, NumPy and Plotly"
)
