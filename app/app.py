import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# -------------------- LOAD DATA --------------------
DATA_PATH = "data/sales_data.csv"
df = pd.read_csv(DATA_PATH)

# -------------------- SIDEBAR --------------------
st.sidebar.header("🔍 Filters")

products = st.sidebar.multiselect(
    "Select Product",
    options=df["product"].unique(),
    default=df["product"].unique()
)

filtered_df = df[df["product"].isin(products)]

# -------------------- TITLE --------------------
st.title("📊 Sales Dashboard")
st.markdown("### Business Performance Overview")

# -------------------- KPIs --------------------
total_sales = filtered_df["sales"].sum()
avg_sales = filtered_df["sales"].mean()
total_orders = filtered_df["orders"].sum()

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Sales", f"{total_sales:,}")
col2.metric("📈 Avg Sales", f"{avg_sales:,.0f}")
col3.metric("📦 Total Orders", f"{total_orders:,}")

st.markdown("---")

# -------------------- CHARTS --------------------
col1, col2 = st.columns(2)

with col1:
    fig1 = px.line(
        filtered_df,
        x="month",
        y="sales",
        markers=True,
        title="📈 Sales Trend"
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.bar(
        filtered_df,
        x="product",
        y="sales",
        color="product",
        title="🛍 Sales by Product"
    )
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    fig3 = px.scatter(
        filtered_df,
        x="ad_spend",
        y="sales",
        size="orders",
        color="product",
        title="💡 Ad Spend vs Sales"
    )
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    fig4 = px.histogram(
        filtered_df,
        x="orders",
        nbins=5,
        title="📊 Order Distribution"
    )
    st.plotly_chart(fig4, use_container_width=True)

# -------------------- EDIT DATA --------------------
st.markdown("---")
st.subheader("✏️ Edit Full Dataset")

edited_df = st.data_editor(
    df,
    num_rows="dynamic",
    use_container_width=True
)

if st.button("💾 Save Changes"):
    edited_df.to_csv(DATA_PATH, index=False)
    st.success("Data saved successfully!")

# -------------------- ADD NEW DATA --------------------
st.markdown("---")
st.subheader("➕ Add New Record")

with st.form("add_data_form"):
    month = st.selectbox("Month", df["month"].unique())
    product = st.selectbox("Product", df["product"].unique())
    sales = st.number_input("Sales", min_value=0)
    ad_spend = st.number_input("Ad Spend", min_value=0)
    orders = st.number_input("Orders", min_value=0)

    submitted = st.form_submit_button("Add Data")

    if submitted:
        new_data = pd.DataFrame({
            "month": [month],
            "product": [product],
            "sales": [sales],
            "ad_spend": [ad_spend],
            "orders": [orders]
        })

        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(DATA_PATH, index=False)

        st.success("New data added successfully!")