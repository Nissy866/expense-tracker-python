"""Web version of the Expense Tracker (deploy free on Streamlit Community Cloud).
Run locally:  streamlit run streamlit_app.py"""
from datetime import date

import pandas as pd
import streamlit as st

import database
import services

st.set_page_config(page_title="Expense Tracker", page_icon="💸")
st.title("💸 Expense Tracker")

try:
    database.create_table()
except database.DatabaseError as err:
    st.error(str(err))
    st.stop()

with st.form("add_expense", clear_on_submit=True):
    st.subheader("Add expense")
    col1, col2 = st.columns(2)
    amount = col1.text_input("Amount (₹)")
    category = col2.text_input("Category", placeholder="Food, Travel...")
    description = st.text_input("Description (optional)")
    when = st.date_input("Date", value=date.today())
    submitted = st.form_submit_button("Add", type="primary")

if submitted:
    try:
        database.add_expense(
            services.validate_amount(amount),
            services.validate_category(category),
            description.strip(),
            str(when),
        )
        st.success("Expense added!")
    except ValueError as err:
        st.error(str(err))
    except database.DatabaseError as err:
        st.error(str(err))

expenses = database.get_all_expenses()
st.subheader("All expenses")
if not expenses:
    st.info("No expenses yet. Add your first one above.")
else:
    df = pd.DataFrame(expenses)
    st.dataframe(df, hide_index=True, use_container_width=True)
    st.metric("Total spent", services.format_money(df["amount"].sum()))

    left, right = st.columns(2)
    with left:
        st.subheader("By category")
        cat = pd.DataFrame(database.totals_by_category()).set_index("category")
        st.bar_chart(cat)
    with right:
        st.subheader("By month")
        mon = pd.DataFrame(database.totals_by_month()).set_index("month")
        st.bar_chart(mon)

    st.subheader("Delete an expense")
    delete_id = st.selectbox("Choose expense ID", df["id"].tolist())
    if st.button("Delete"):
        database.delete_expense(int(delete_id))
        st.rerun()
