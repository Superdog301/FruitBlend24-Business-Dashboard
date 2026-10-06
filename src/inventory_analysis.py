import pandas as pd


# Load sales
orders = pd.read_csv(
    "output/orders_clean.csv"
)

orders["date"] = pd.to_datetime(
    orders["date"]
)


# Load waste
waste = pd.read_csv(
    "output/waste_analysis.csv"
)


# Monthly demand
monthly_sales = (
    orders.groupby(
        ["kitchen","menu_clean"]
    )
    .agg(
        monthly_units=(
            "units_sold",
            "sum"
        )
    )
    .reset_index()
)


# rename for matching
monthly_sales = monthly_sales.rename(
    columns={
        "menu_clean":"sku"
    }
)


# Average daily demand
monthly_sales["daily_demand"] = (
    monthly_sales["monthly_units"] / 12 / 30
)


# Safety stock 7 days
monthly_sales["recommended_stock_7days"] = (
    monthly_sales["daily_demand"] * 7
)


print(monthly_sales.head())


monthly_sales.to_csv(
    "output/inventory_plan.csv",
    index=False
)


print("Inventory export completed!")