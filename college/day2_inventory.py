import streamlit as st
import mysql.connector
import pandas as pd

# --- STREAMLIT PAGE CONFIG ---
st.set_page_config(page_title="Inventory Manager", page_icon="📦", layout="centered")

# --- DB CONNECTION FUNCTION ---
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="streamlit_user",   # Change as per your DB
        password="mypassword",   # Change as per your DB
        database="testdb"
    )

# --- CREATE TABLE ---
conn = get_connection()
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS inventory (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100),
    quantity INT,
    price FLOAT
)
""")
conn.commit()
cursor.close()
conn.close()

st.title("📦 Inventory Management System")

# --- SIDEBAR MENU ---
menu = ["Add Product", "View Inventory", "Update Product", "Delete Product"]
choice = st.sidebar.selectbox("Menu", menu)

# --- ADD PRODUCT ---
if choice == "Add Product":
    st.subheader("Add a New Product")
    product_name = st.text_input("Product Name")
    quantity = st.number_input("Quantity", min_value=1, step=1)
    price = st.number_input("Price", min_value=0.0, step=0.5)

    if st.button("Add Product"):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO inventory (product_name, quantity, price) VALUES (%s, %s, %s)",
                       (product_name, quantity, price))
        conn.commit()
        cursor.close()
        conn.close()
        st.success(f"Product '{product_name}' Added!")

# --- VIEW INVENTORY ---
elif choice == "View Inventory":
    st.subheader("Inventory List")
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM inventory", conn)
    conn.close()
    st.dataframe(df)

# --- UPDATE PRODUCT ---
elif choice == "Update Product":
    st.subheader("Update Product Details")
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM inventory", conn)
    conn.close()

    product_ids = df['id'].tolist()
    selected_id = st.selectbox("Select Product ID to Update", product_ids)

    if selected_id:
        selected_product = df[df['id'] == selected_id].iloc[0]
        new_name = st.text_input("Product Name", selected_product['product_name'])
        new_quantity = st.number_input("Quantity", min_value=1, value=int(selected_product['quantity']))
        new_price = st.number_input("Price", min_value=0.0, value=float(selected_product['price']), step=0.5)

        if st.button("Update Product"):
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE inventory
                SET product_name=%s, quantity=%s, price=%s
                WHERE id=%s
            """, (new_name, new_quantity, new_price, selected_id))
            conn.commit()
            cursor.close()
            conn.close()
            st.success("Product Updated Successfully!")

# --- DELETE PRODUCT ---
elif choice == "Delete Product":
    st.subheader("Delete a Product")
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM inventory", conn)
    conn.close()

    product_ids = df['id'].tolist()
    selected_id = st.selectbox("Select Product ID to Delete", product_ids)

    if st.button("Delete Product"):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM inventory WHERE id=%s", (selected_id,))
        conn.commit()
        cursor.close()
        conn.close()
        st.warning(f"🗑️ Product ID {selected_id} Deleted!")


