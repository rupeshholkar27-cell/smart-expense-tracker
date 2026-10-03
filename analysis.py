import pandas as pd

def summary(df):
    return {
        "total": df["amount"].sum(),
        "average": df["amount"].mean(),
        "median": df["amount"].median(),
        "std_dev": df["amount"].std(),
        "biggest": df["amount"].max(),
    }

def by_category(df):
    return df.groupby("category")["amount"].sum().sort_values(ascending=False)

def by_month(df):
    df = df.copy()
    df["month"] = pd.to_datetime(df["date"]).dt.to_period("M").astype(str)
    return df.groupby("month")["amount"].sum()

def find_unusual(df):
    # z-score: how far is each expense from normal?
    z = (df["amount"] - df["amount"].mean()) / df["amount"].std()
    return df[z.abs() > 2]   # more than 2 std devs away = unusual