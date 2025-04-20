import streamlit as st
import mysql.connector as SQL
#import uuid
# Connecting to MySQL database
system = SQL.connect(host='localhost', user='abhi', password='systum', database='foodbill')
cursor = system.cursor()

# Function to clear screen (simulated in UI)
def clear():
    st.empty()

# Function to add a new food item
def Addition(item_no, item_name, item_price):
    my = "INSERT INTO item VALUES ({}, '{}', {})".format(item_no, item_name, item_price)
    cursor.execute(my)
    system.commit()
    st.success("New Item Added Successfully!")

# Function to delete an existing item
def deletion(item_no):
    my = "DELETE FROM item WHERE ItemNo = {}".format(item_no)
    cursor.execute(my)
    system.commit()
    st.success("Item Deleted Successfully!")

# Function to update an existing item
def updation(item_no, item_name, item_price):
    my = "UPDATE item SET ItemName='{}', ItemPrice={} WHERE ItemNo={}".format(item_name, item_price, item_no)
    cursor.execute(my)
    system.commit()
    st.success("Item Updated Successfully!")

# Function to search for an item
def searching(item_name):
    my = "SELECT * FROM item WHERE ItemName LIKE '%{}%'".format(item_name)
    cursor.execute(my)
    results = cursor.fetchall()
    return results

# Function for billing
def billing(items):
    total = 0
    for item_no, qty in items:
        sql = "SELECT * FROM item WHERE ItemNo ={}".format(item_no)
        cursor.execute(sql)
        result = cursor.fetchone()
        if result:
            total += qty * result[2]
    return total


# Streamlit UI
st.title("🍽️ Food Billing System")

menu = ["Add Item", "Delete Item", "Update Item", "Search Item", "Billing"]
choice = st.sidebar.radio("Menu", menu)

if choice == "Add Item":
    st.subheader("➕ Add New Food Item")
    item_no = st.text_input("Enter Item No:")
    item_name = st.text_input("Enter Item Name:")
    item_price = st.text_input("Enter Item Price:")
    if st.button("Add Item"):
        if item_no and item_name and item_price:
            Addition(item_no, item_name, item_price)
        else:
            st.warning("Please fill all fields.")

elif choice == "Delete Item":
    st.subheader("🗑️ Delete Food Item")
    item_no = st.text_input("Enter Item No:")
    if st.button("Delete Item"):
        deletion(item_no)

elif choice == "Update Item":
    st.subheader("✏️ Update Food Item")
    item_no = st.text_input("Enter Item No:")
    item_name = st.text_input("Enter New Item Name:")
    item_price = st.text_input("Enter New Item Price:")
    if st.button("Update Item"):
        updation(item_no, item_name, item_price)

elif choice == "Search Item":
    st.subheader("🔍 Search Food Item")
    item_name = st.text_input("Enter Item Name:")
    if st.button("Search"):
        results = searching(item_name)
        if results:
            for row in results:
                st.write(f"Item No: {row[0]}, Name: {row[1]}, Price: ₹{row[2]}")
        else:
            st.warning("No matching items found.")

elif choice == "Billing":
    st.subheader("🛒 Generate Bill")

    if "bill_items" not in st.session_state:
        st.session_state.bill_items = []

    if "billing_complete" not in st.session_state:
        st.session_state.billing_complete = False

    if not st.session_state.billing_complete:
        item_no = st.text_input("Enter Item No:")
        qty = st.number_input("Enter Quantity:", min_value=1, step=1)

        if st.button("Add Item to Bill"):
            if item_no:
                st.session_state.bill_items.append((item_no, qty))
                st.success("Item added to bill!")
            else:
                st.warning("Please enter an Item No.")
            st.write("### Current Bill Items:")

        if st.session_state.bill_items:
            for idx, (item_no, qty) in enumerate(st.session_state.bill_items):
                st.write(f"{idx+1}. Item No: {item_no}, Quantity: {qty}")

        if st.button("Finish Billing"):
            st.session_state.billing_complete = True

    else:
        if st.session_state.bill_items:
            total = billing(st.session_state.bill_items)
            st.success(f"✅ Total Bill: ₹{total}")
        else:
            st.warning("No items in the bill.")
