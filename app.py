import streamlit as st
from utils import *
from datetime import datetime
import os

st.set_page_config(page_title="Sales Commission System", layout="wide")
os.makedirs("uploads", exist_ok=True)

if "user" not in st.session_state:
    st.session_state.user = None

def login_screen():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "admin" and password == "admin123":
            st.session_state.user = {"role": "admin", "username": "admin"}
        else:
            user = validate_login(username, password)
            if user:
                st.session_state.user = {**user, "role": "agent"}
            else:
                st.error("Invalid login")

def logout_button():
    if st.button("Logout"):
        st.session_state.user = None
        st.rerun()

def display_sales(sales):
    for i, s in enumerate(sales):
        with st.expander(f"{s['customer_name']} | {s['product']} | Rs {s['price']}"):
            st.write(f"Order #: {s['order_number']}")
            st.write(f"Platform: {s['platform']}")
            st.write(f"IMEA: {s['imea']}")
            st.write(f"Commission: Rs {s['commission']:.2f}")
            st.write(f"Date: {s['datetime']}")
            if st.button(f"View Image - {i}"):
                st.image(s["proof_image"], use_container_width=True)

def agent_dashboard(agent):
    st.sidebar.image("salamtec_logo.webp", use_container_width=150)
    st.sidebar.title("Agent Menu")
    st.sidebar.write(f"Welcome, {agent['name']}")
    page = st.sidebar.radio("Go to", ["Home", "Add Sale", "Sales History"])

    if page == "Home":
        sales = [s for s in load_data(SALES_FILE) if s["agent_username"] == agent["username"]]
        st.title("Agent Home")
        st.metric("Total Sales", len(sales))
        st.metric("Total Commission", f"Rs {sum(s['commission'] for s in sales):.2f}")

    elif page == "Add Sale":
        st.title("Add Sale")
        customer_name = st.text_input("Customer Name")
        order_number = st.text_input("Order Number")
        platform = st.selectbox("Platform", ["Alfamall", "Digimall", "Website"])
        product = st.text_input("Product Detail")
        imea = st.text_input("IMEA")
        price = st.number_input("Price", min_value=0.0)
        category = st.selectbox("Category", ["Mobile", "Chromebook", "Accessory"])
        proof_image = st.file_uploader("Upload Sale Proof (Image)", type=["jpg", "jpeg", "png"])

        if st.button("Submit"):
            if proof_image is None:
                st.error("Please upload an image as proof of sale.")
            else:
                commission = calculate_commission(price)
        # Clean filename (no spaces or special chars)
                safe_customer = customer_name.replace(" ", "_").replace("/", "_")
                safe_order = order_number.replace(" ", "_").replace("/", "_")
                ext = proof_image.name.split('.')[-1]
                image_path = f"{safe_order}_{safe_customer}.{ext}"
                with open(image_path, "wb") as f:
                    f.write(proof_image.getbuffer())

                sale_entry = {
                    "agent_username": agent["username"],
                    "customer_name": customer_name,
                    "order_number": order_number,
                    "platform": platform,
                    "product": product,
                    "imea": imea,
                    "price": price,
                    "commission": commission,
                    "proof_image": image_path,
                    "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                data = load_data(SALES_FILE)
                data.append(sale_entry)
                save_data(SALES_FILE, data)
                st.success("Sale recorded successfully with proof image!")

    elif page == "Sales History":

        st.title("Sales History")
        sales = [s for s in load_data(SALES_FILE) if s["agent_username"] == agent["username"]]
        for s in sales:
            s["dt"] = datetime.strptime(s["datetime"], "%Y-%m-%d %H:%M:%S")

        st.subheader("Filters")
        col1, col2 = st.columns(2)
        with col1:
            from_date = st.date_input("From Date")
        with col2:
            to_date = st.date_input("To Date")
        customer_filter = st.text_input("Customer Name Filter")
        product_filter = st.text_input("Product Filter")

        filtered = []
        for s in sales:
            if from_date and s["dt"].date() < from_date:
                continue
            if to_date and s["dt"].date() > to_date:
                continue
            if customer_filter and customer_filter.lower() not in s["customer_name"].lower():
                continue
            if product_filter and product_filter.lower() not in s["product"].lower():
                continue
            filtered.append(s)

        total_products = len(filtered)
        total_commission = sum(s["commission"] for s in filtered)

        st.subheader("Summary")
        col1, col2 = st.columns(2)
        col1.metric("Products Sold", total_products)
        col2.metric("Total Commission", f"Rs {total_commission:.2f}")

        if filtered:
            display_sales(filtered)
        else:
            st.info("No records match the filters.")

def admin_dashboard():
    st.sidebar.image("salamtec_logo.webp", use_container_width=False, width=150)
    st.sidebar.title("Admin Menu")
    page = st.sidebar.radio("Go to", ["Home", "Add Agent", "Agents Data", "Sales History"])

    if page == "Home":
        sales = load_data(SALES_FILE)
        st.title("Admin Home")
        st.metric("Total Sales", len(sales))
        st.metric("Total Commission", f"Rs {sum(s['commission'] for s in sales):.2f}")


    elif page == "Add Agent":
        st.title("Add Agent")
        name = st.text_input("Full Name")
        number = st.text_input("Contact Number")
        email = st.text_input("Email")
        address = st.text_input("Address")
        joining_date = st.date_input("Joining Date")
        salary = st.number_input("Salary")
        username = st.text_input("Username")
        password = st.text_input("Password")
        if st.button("Add Agent"):
            agents = load_data(AGENTS_FILE)
            agents.append({
                "name": name, "number": number, "email": email,
                "address": address, "joining_date": str(joining_date),
                "salary": salary, "username": username, "password": password
            })
            save_data(AGENTS_FILE, agents)
            st.success("Agent added successfully!")


    elif page == "Agents Data":
        st.title("All Agents")
        agents = load_data(AGENTS_FILE)
        st.dataframe(agents)

    elif page == "Sales History":
        st.title("All Sales History")
        sales = load_data(SALES_FILE)
        agents = load_data(AGENTS_FILE)  # Load the agent data as well
        agent_dict = {agent['username']: agent['name'] for agent in agents}  # Create a dictionary mapping username to name

        for s in sales:
            s["dt"] = datetime.strptime(s["datetime"], "%Y-%m-%d %H:%M:%S")
            s["agent_name"] = agent_dict.get(s["agent_username"], "Unknown")  # Add the agent's name to the sales entry

        st.subheader("Filters")
        col1, col2 = st.columns(2)
        with col1:
            from_date = st.date_input("From Date")
        with col2:
            to_date = st.date_input("To Date")
        agent_name_filter = st.text_input("Agent Username Filter")

        filtered = []
        for s in sales:
            if from_date and s["dt"].date() < from_date:
                continue
            if to_date and s["dt"].date() > to_date:
                continue
            if agent_name_filter and agent_name_filter.lower() not in s["agent_username"].lower():
                continue
            filtered.append(s)

        total_products = len(filtered)
        total_commission = sum(s["commission"] for s in filtered)

        st.subheader("Summary")
        col1, col2 = st.columns(2)
        col1.metric("Products Sold", total_products)
        col2.metric("Total Commission", f"Rs {total_commission:.2f}")

        # Display the sales data along with the agent's name
        if filtered:
            display_sales(filtered)
        else:
            st.info("No sales match the filters.")


def main():
    if not st.session_state.user:
        login_screen()
    else:
        logout_button()
        if st.session_state.user["role"] == "admin":
            admin_dashboard()
        else:
            agent_dashboard(st.session_state.user)

if __name__ == "__main__":
    main()
