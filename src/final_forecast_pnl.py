import pandas as pd


forecast = pd.read_csv(
    "output/forecast_pnl_3_month.csv"
)


# Load overhead
monthly_profit = pd.read_csv(
    "output/monthly_profit_analysis.csv"
)


overhead = (
    monthly_profit[
        [
            "kitchen",
            "monthly_overhead"
        ]
    ]
    .drop_duplicates()
)


# Sum by month + kitchen

forecast_kitchen = (
    forecast.groupby(
        [
            "month",
            "kitchen"
        ]
    )
    .agg(
        revenue=("revenue","sum"),
        profit_before_overhead=("profit_before_overhead","sum"),
        forecast_units=("forecast_units","sum")
    )
    .reset_index()
)


# Add overhead

forecast_kitchen = forecast_kitchen.merge(
    overhead,
    on="kitchen",
    how="left"
)


# Net Profit

forecast_kitchen["net_profit"] = (
    forecast_kitchen["profit_before_overhead"]
    -
    forecast_kitchen["monthly_overhead"]
)


forecast_kitchen["net_margin_%"] = (
    forecast_kitchen["net_profit"]
    /
    forecast_kitchen["revenue"]
    *
    100
)


print("Final Forecast P&L")

print(
    forecast_kitchen.head()
)


forecast_kitchen.to_csv(
    "output/final_forecast_pnl.csv",
    index=False
)


print(
    "Export final forecast completed!"
)