import sqlite3
import logging
import pandas as pd

logging.basicConfig(
    filename="app.log", level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s")

DB_NAME = "expenses.db"

def create_table():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""CREATE TABLE IF NOT EXISTS expenses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT, category TEXT, amount REAL, note TEXT)""")
    conn.commit()
    conn.close()

def add_expense(date, category, amount, note=""):
    if amount <= 0:
        logging.error("Bad amount: %s", amount)
        raise ValueError("Amount must be more than 0")
    conn = sqlite3.connect(DB_NAME)
    conn.execute(
        "INSERT INTO expenses(date, category, amount, note) VALUES (?,?,?,?)",
        (str(date), category, amount, note))
    conn.commit()
    conn.close()
    logging.info("Added %s: %s", category, amount)

def get_all_expenses():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql("SELECT * FROM expenses", conn)
    conn.close()
    return df