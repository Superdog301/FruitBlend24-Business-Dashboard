import pandas as pd


# Load data
orders = pd.read_csv(
    "output/orders_clean.csv"
)

orders["date"] = pd.to_datetime(
    orders["date"]
)


# Create month
orders["month"] = (
    orders["date"]
    .dt.to_period("M")
    .astype(str)
)


# Monthly sales
monthly_sales = (
    orders.groupby(
        ["month","kitchen","menu_clean"]
    )
    .agg(
        units_sold=("units_sold","sum"),
        revenue=("gross_revenue_thb","sum")
    )
    .reset_index()
)


# Convert month date
monthly_sales["month"] = pd.to_datetime(
    monthly_sales["month"]
)


# Last 3 months average
recent_sales = (
    monthly_sales[
        monthly_sales["month"] >= "2026-06-01"
    ]
)


forecast = (
    recent_sales.groupby(
        ["kitchen","menu_clean"]
    )
    .agg(
        forecast_units=(
            "units_sold",
            "mean"
        )
    )
    .reset_index()
)


# Create future months
future_months = pd.date_range(
    "2026-09-01",
    periods=3,
    freq="MS"
)


forecast = (
    forecast.assign(
        key=1
    )
    .merge(
        pd.DataFrame(
            {"month":future_months,
             "key":1}
        ),
        on="key"
    )
    .drop("key",axis=1)
)


# Export
forecast.to_csv(
    "output/forecast_3_month.csv",
    index=False
)


print("Forecast Example")
print(forecast.head())

print("\nExport forecast completed!")