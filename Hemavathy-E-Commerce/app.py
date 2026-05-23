
import streamlit as st
import sqlite3
import pandas as pd
import random

st.set_page_config(page_title="Modern E-Commerce", layout="wide")

# ---------------- DATABASE ----------------
conn = sqlite3.connect("ecommerce.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    category TEXT,
    price INTEGER,
    rating REAL,
    image TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    password TEXT
)
""")

conn.commit()

# ---------------- SAMPLE DATA ----------------
sample_products = [
    ("Gaming Laptop", "Electronics", 85000, 4.8, "https://images.unsplash.com/photo-1517336714739-489689fd1ca8"),
    ("Smart Watch", "Accessories", 6000, 4.5, "https://images.unsplash.com/photo-1523275335684-37898b6baf30"),
    ("Wireless Headphones", "Electronics", 3500, 4.6, "https://images.unsplash.com/photo-1505740420928-5e560c06d30e"),
    ("Sneakers", "Fashion", 2500, 4.2, "https://images.unsplash.com/photo-1542291026-7eec264c27ff"),
    ("Backpack", "Travel", 1800, 4.4, "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee"),
]

cursor.execute("SELECT COUNT(*) FROM products")
if cursor.fetchone()[0] == 0:
    cursor.executemany(
        "INSERT INTO products (name, category, price, rating, image) VALUES (?, ?, ?, ?, ?)",
        sample_products
    )
    conn.commit()

# ---------------- SESSION ----------------
if "cart" not in st.session_state:
    st.session_state.cart = {}

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# ---------------- STYLES ----------------
bg = "#111827" if st.session_state.dark_mode else "#f4f7ff"
text = "white" if st.session_state.dark_mode else "#111827"

st.markdown(f"""
<style>
body {{
    background: {bg};
}}
.main {{
    background-color: {bg};
    color: {text};
}}
.product-card {{
    border-radius: 20px;
    padding: 15px;
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    transition: 0.3s;
}}
.product-card:hover {{
    transform: translateY(-5px);
}}
.banner {{
    padding: 40px;
    border-radius: 25px;
    background: linear-gradient(135deg, #7c3aed, #06b6d4);
    color: white;
    text-align: center;
}}
</style>
""", unsafe_allow_html=True)

# ---------------- NAVBAR ----------------
col1, col2, col3 = st.columns([4,2,1])

with col1:
    st.title("🛍️ NeoShop")

with col2:
    search = st.text_input("Search Products")

with col3:
    if st.button("🌙 Mode"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# ---------------- HERO ----------------
st.markdown("""
<div class='banner'>
<h1>Modern E-Commerce Store</h1>
<p>Premium shopping experience with stylish UI</p>
</div>
""", unsafe_allow_html=True)

st.write("")

# ---------------- SIDEBAR ----------------
st.sidebar.header("Filters")

category = st.sidebar.selectbox(
    "Category",
    ["All", "Electronics", "Accessories", "Fashion", "Travel"]
)

sort_option = st.sidebar.selectbox(
    "Sort By",
    ["Popularity", "Low to High", "High to Low"]
)

max_price = st.sidebar.slider("Max Price", 1000, 100000, 100000)

# ---------------- FETCH PRODUCTS ----------------
df = pd.read_sql_query("SELECT * FROM products", conn)

if search:
    df = df[df["name"].str.contains(search, case=False)]

if category != "All":
    df = df[df["category"] == category]

df = df[df["price"] <= max_price]

if sort_option == "Low to High":
    df = df.sort_values("price")
elif sort_option == "High to Low":
    df = df.sort_values("price", ascending=False)
else:
    df = df.sort_values("rating", ascending=False)

# ---------------- PRODUCTS ----------------
st.subheader("🔥 Featured Products")

cols = st.columns(3)

for index, row in df.iterrows():
    with cols[index % 3]:
        st.markdown("<div class='product-card'>", unsafe_allow_html=True)
        st.image(row["image"], use_container_width=True)
        st.markdown(f"### {row['name']}")
        st.write(f"Category: {row['category']}")
        st.write(f"⭐ {row['rating']}")
        st.write(f"💰 ₹{row['price']}")

        if st.button(f"Add to Cart {row['id']}"):
            if row["id"] not in st.session_state.cart:
                st.session_state.cart[row["id"]] = 1
            else:
                st.session_state.cart[row["id"]] += 1
            st.success("Added to cart!")

        st.button(f"View Details {row['id']}")
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------- CART ----------------
st.divider()
st.header("🛒 Shopping Cart")

total = 0

if st.session_state.cart:
    for product_id, quantity in st.session_state.cart.items():
        product = df[df["id"] == product_id]

        if not product.empty:
            name = product.iloc[0]["name"]
            price = product.iloc[0]["price"]

            col1, col2, col3 = st.columns([4,2,1])

            with col1:
                st.write(f"{name}")

            with col2:
                qty = st.number_input(
                    f"Qty {product_id}",
                    min_value=1,
                    value=quantity,
                    key=f"qty_{product_id}"
                )
                st.session_state.cart[product_id] = qty

            with col3:
                if st.button(f"Remove {product_id}"):
                    del st.session_state.cart[product_id]
                    st.rerun()

            total += price * qty

    tax = total * 0.05
    final_total = total + tax

    st.write(f"Subtotal: ₹{total}")
    st.write(f"Tax: ₹{tax:.2f}")
    st.success(f"Total: ₹{final_total:.2f}")

    if st.button("Proceed to Checkout"):
        st.balloons()
        st.success("Order Confirmed Successfully!")

else:
    st.info("Your cart is empty.")

# ---------------- AUTH ----------------
st.divider()
st.header("🔐 User Authentication")

auth_tab1, auth_tab2 = st.tabs(["Login", "Signup"])

with auth_tab1:
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    remember = st.checkbox("Remember me")

    if st.button("Login"):
        st.success("Login successful!")

with auth_tab2:
    new_email = st.text_input("New Email")
    new_password = st.text_input("New Password", type="password")

    if st.button("Create Account"):
        cursor.execute(
            "INSERT INTO users (email, password) VALUES (?, ?)",
            (new_email, new_password)
        )
        conn.commit()
        st.success("Account created!")

# ---------------- ADMIN DASHBOARD ----------------
st.divider()
st.header("📊 Admin Dashboard")

tab1, tab2, tab3 = st.tabs(["Add Product", "Analytics", "Orders"])

with tab1:
    pname = st.text_input("Product Name")
    pcat = st.text_input("Category")
    pprice = st.number_input("Price", 100)
    prating = st.slider("Rating", 1.0, 5.0, 4.0)
    pimage = st.text_input("Image URL")

    if st.button("Add Product"):
        cursor.execute(
            "INSERT INTO products (name, category, price, rating, image) VALUES (?, ?, ?, ?, ?)",
            (pname, pcat, pprice, prating, pimage)
        )
        conn.commit()
        st.success("Product Added!")

with tab2:
    chart_data = pd.DataFrame({
        "Sales": [random.randint(10, 100) for _ in range(7)]
    })
    st.line_chart(chart_data)

with tab3:
    st.write("Total Orders: 25")
    st.write("Active Users: 12")

