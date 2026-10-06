import pandas as pd

orders = pd.read_csv(
    "output/orders_clean.csv"
)

orders["date"] = pd.to_datetime(
    orders["date"]
)

print(
    orders["date"].min()
)

print(
    orders["date"].max()
)

print(
    orders.columns
)