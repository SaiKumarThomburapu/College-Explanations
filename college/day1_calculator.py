import streamlit as st

st.set_page_config(page_title="GST & Discount Calculator", page_icon="💰")

st.title("GST & Discount Calculator")

price = st.number_input("Enter Original Price (₹):", min_value=0.0, step=0.5)
discount = st.slider("Discount (%)", 0, 100, 10)
gst = st.slider("GST (%)", 0, 28, 18)

discount_amount = price * (discount / 100)
price_after_discount = price - discount_amount
gst_amount = price_after_discount * (gst / 100)
final_price = price_after_discount + gst_amount

st.write(f"**Price after Discount:** ₹{price_after_discount:,.2f}")
st.write(f"**GST Amount:** ₹{gst_amount:,.2f}")
st.success(f"**Final Price:** ₹{final_price:,.2f}")

