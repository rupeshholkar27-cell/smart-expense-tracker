import streamlit as st
from datetime import date
import database as db
import analysis as an

db.create_table()
st.title("💰 Smart Expense Tracker")

# Part 1: add an expense
st.sidebar.header("Add expense")
d = st.sidebar.date_input("Date", date.today())
cat = st.sidebar.selectbox("Category", ["Food", "Travel", "Shopping", "Bills", "Fun", "Other"])
amt = st.sidebar.number_input("Amount", min_value=0.0, step=10.0)
note = st.sidebar.text_input("Note")

if st.sidebar.button("Save"):
    try:
        db.add_expense(d, cat, amt, note)
        st.sidebar.success("Saved!")
    except ValueError as e:
        st.sidebar.error(str(e))

# Part 2: show results
df = db.get_all_expenses()
if df.empty:
    st.info("No expenses yet. Add one from the left!")
else:
    s = an.summary(df)
    c1, c2, c3 = st.columns(3)
    c1.metric("Total", f"{s['total']:.0f}")
    c2.metric("Average", f"{s['average']:.0f}")
    c3.metric("Biggest", f"{s['biggest']:.0f}")

    st.subheader("Spending by category")
    st.bar_chart(an.by_category(df))

    st.subheader("Spending by month")
    st.line_chart(an.by_month(df))

    st.subheader("Unusual expenses ⚠️")
    st.dataframe(an.find_unusual(df))

    st.subheader("All expenses")
    st.dataframe(df)