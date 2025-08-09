import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Business Insights Tool", page_icon="📊")

st.title("Business Insights Tool")

uploaded_file = st.file_uploader("Upload CSV (Sales Data)", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        df.columns = [str(col).strip() for col in df.columns]

        if "Category" in df.columns and "Sales" in df.columns:
            st.sidebar.header("Filters")
            category_filter = st.sidebar.multiselect("Select Categories", df['Category'].unique())
            if category_filter:
                df = df[df['Category'].isin(category_filter)]

        st.subheader("Key Metrics")
        if "Sales" in df.columns:
            st.metric("Total Sales", f"₹{df['Sales'].sum():,.2f}")
        if "Quantity" in df.columns:
            st.metric("Total Quantity", int(df['Quantity'].sum()))

        if "Category" in df.columns and "Sales" in df.columns:
            st.subheader("Category-wise Sales")
            fig = px.bar(df, x='Category', y='Sales', color='Category', title="Sales by Category")
            st.plotly_chart(fig)

        if "Date" in df.columns and "Sales" in df.columns:
            st.subheader("Sales Trend")
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            trend = df.groupby('Date')['Sales'].sum().reset_index()
            fig2 = px.line(trend, x='Date', y='Sales', title="Sales Trend Over Time")
            st.plotly_chart(fig2)

    except Exception as e:
        st.error(f"Error reading CSV: {e}")
else:
    st.info("Please upload a CSV file to get started.")

