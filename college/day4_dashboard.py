import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sales Dashboard", page_icon="📈")

st.title("Interactive Sales Dashboard")

uploaded_file = st.file_uploader("Upload Sales CSV", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        df.columns = [str(col).strip() for col in df.columns]

        st.success("File uploaded successfully!")
        st.write(df.head())

        if "Category" in df.columns and "Sales" in df.columns:
            st.subheader("Sales by Category")
            fig = px.pie(df, names='Category', values='Sales', title="Sales Distribution")
            st.plotly_chart(fig)
        else:
            st.warning("CSV must have 'Category' and 'Sales' columns for the pie chart.")

        if "Date" in df.columns and "Sales" in df.columns:
            st.subheader("Sales Over Time")
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            daily_sales = df.groupby('Date')['Sales'].sum().reset_index()
            fig2 = px.line(daily_sales, x='Date', y='Sales', title="Daily Sales Trend")
            st.plotly_chart(fig2)
        else:
            st.warning("CSV must have 'Date' and 'Sales' columns for the line chart.")

    except Exception as e:
        st.error(f"Error reading CSV: {e}")
else:
    st.info("Please upload a CSV file to see the dashboard.")

