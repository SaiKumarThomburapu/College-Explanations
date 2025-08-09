import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sales Data Analysis", page_icon="📊")

st.title("Sales Data Analysis")

uploaded_file = st.file_uploader("Upload Sales CSV", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        # Clean column names (remove spaces, NaN headers, etc.)
        df.columns = [str(col).strip() for col in df.columns if str(col).strip() != '']

        if df.empty:
            st.error("The uploaded CSV is empty. Please upload a valid sales dataset.")
        else:
            st.subheader("Data Preview")
            st.dataframe(df.head())

            if all(col in df.columns for col in ['Quantity', 'Price']):
                df['Revenue'] = df['Quantity'] * df['Price']

                st.subheader("Basic Stats")
                st.write(df.describe())

                st.metric("Total Revenue", f"₹{df['Revenue'].sum():,.2f}")

                min_price = st.slider(
                    "Filter by Minimum Price",
                    int(df['Price'].min()),
                    int(df['Price'].max()),
                    int(df['Price'].min())
                )
                st.dataframe(df[df['Price'] >= min_price])
            else:
                st.error("CSV must contain 'Quantity' and 'Price' columns.")
    except Exception as e:
        st.error(f"Error reading file: {e}")
else:
    st.info("Please upload a CSV file to start analysis.")

