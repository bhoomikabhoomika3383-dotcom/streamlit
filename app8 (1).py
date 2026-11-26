
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import altair as alt

# -----------------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------------

st.set_page_config(
    page_title="Sales Visualization Dashboard",
    
    layout="wide"
)

st.title("Sales Data Visualization Dashboard")

# 2. CREATE DUMMY DATA
# -----------------------------------------

@st.cache_data
def create_data():

    np.random.seed(42)

    dates = pd.date_range(
        start="2025-01-01",
        periods=100,
        freq="D"
    )

    regions = ["North", "South", "East", "West"]

    states = ["Delhi", "Karnataka", "West Bengal", "Maharashtra"]

    cities = ["Delhi", "Bangalore", "Kolkata", "Mumbai"]

    products = ["Laptop", "Mobile", "Tablet", "Headphones"]

    categories = ["Electronics", "Accessories"]

    df = pd.DataFrame({
        "Date": dates,
        "Region": np.random.choice(regions, 100),
        "State": np.random.choice(states, 100),
        "City": np.random.choice(cities, 100),
        "Product": np.random.choice(products, 100),
        "Category": np.random.choice(categories, 100),
        "Sales": np.random.randint(1000, 15000, 100),
        "Profit": np.random.randint(100, 5000, 100),
        "Quantity": np.random.randint(1, 20, 100),
        "Discount": np.random.choice([5, 10, 15, 20], 100)
    })

    return df


df = create_data()

# -----------------------------------------
# 3. DISPLAY DATASET
# -----------------------------------------

st.header("1. Dummy Sales Dataset")

st.dataframe(df, use_container_width=True)

st.write("Total Records:", len(df))

# -----------------------------------------
# 4. LINE CHART
# -----------------------------------------

st.header("2. Line Chart ")

st.write("Purpose: Analyze sales trends over time.")

daily_sales = df.groupby("Date")["Sales"].sum()

st.line_chart(daily_sales)

# -----------------------------------------
# 5. BAR CHART
# -----------------------------------------

st.header("3. Bar Chart ")

st.write("Purpose: Compare sales across different regions.")

region_sales = df.groupby("Region")["Sales"].sum()

st.bar_chart(region_sales)

# -----------------------------------------
# 6. AREA CHART
# -----------------------------------------

st.header("4. Area Chart ")

st.write("Purpose: Show changes in sales over time.")

monthly_sales = (
    df.set_index("Date")
    .resample("ME")["Sales"]
    .sum()
)

st.area_chart(monthly_sales)

# -----------------------------------------
# 7. SCATTER CHART
# -----------------------------------------

st.header("5. Scatter Chart ")

st.write("Purpose: Understand the relationship between sales and profit.")

st.scatter_chart(
    df,
    x="Sales",
    y="Profit",
    color="Region",
    size="Quantity"
)


# -----------------------------------------
# 9. MATPLOTLIB CHART
# -----------------------------------------

st.header("7. Matplotlib Chart ")

st.write("Purpose: Create customized visualizations.")

product_sales = df.groupby("Product")["Sales"].sum()

fig, ax = plt.subplots()

ax.bar(
    product_sales.index,
    product_sales.values
)

ax.set_title("Product Wise Sales")
ax.set_xlabel("Products")
ax.set_ylabel("Sales Amount")

plt.xticks(rotation=20)

st.pyplot(fig)

# -----------------------------------------
# 10. PLOTLY CHART
# -----------------------------------------

st.header("8. Plotly Chart ")

st.write("Purpose: Create interactive visualizations.")

fig_plotly = px.pie(
    df,
    names="Category",
    values="Sales",
    title="Sales Distribution by Category"
)

st.plotly_chart(
    fig_plotly,
    use_container_width=True
)

# -----------------------------------------
# 11. ALTAIR CHART
# -----------------------------------------

st.header("9. Altair Chart ")

st.write("Purpose: Create interactive statistical charts.")

altair_data = df.groupby("Region", as_index=False)["Profit"].sum()

chart = alt.Chart(altair_data).mark_bar().encode(
    x=alt.X("Region:N"),
    y=alt.Y("Profit:Q"),
    color="Region",
    tooltip=["Region", "Profit"]
).properties(
    title="Region Wise Profit"
)

st.altair_chart(
    chart,
    use_container_width=True
)


st.divider()

st.success("All Streamlit Data Visualization Features Completed!")
