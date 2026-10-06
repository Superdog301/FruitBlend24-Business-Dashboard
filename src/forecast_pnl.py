import pandas as pd


# =========================
# Load Forecast
# =========================

forecast = pd.read_csv(
    "output/forecast_3_month.csv"
)


# =========================
# Load Cost Data
# =========================

cost = pd.read_csv(
    "output/orders_profit_platform.csv"
)


print("Cost Columns")
print(cost.columns)


# =========================
# Calculate Average Cost per Menu
# =========================

menu_cost = (
    cost.groupby("menu_clean")
    .agg(
        fruit_cost=(
            "fruit_cost_per_cup_thb",
            "mean"
        ),
        packaging_cost=(
            "packaging_cost_per_cup_thb",
            "mean"
        ),
        labor_cost=(
            "labor_cost_per_cup_thb",
            "mean"
        ),
        commission_rate=(
            "commission_rate",
            "mean"
        )
    )
    .reset_index()
)


# =========================
# Selling Price
# =========================

orders = pd.read_csv(
    "output/orders_clean.csv"
)


menu_price = (
    orders.groupby("menu_clean")
    .agg(
        price_thb=(
            "price_thb",
            "mean"
        )
    )
    .reset_index()
)


# =========================
# Merge
# =========================

forecast = forecast.merge(
    menu_cost,
    on="menu_clean",
    how="left"
)


forecast = forecast.merge(
    menu_price,
    on="menu_clean",
    how="left"
)


print("\nAfter Merge")
print(forecast.head())


# =========================
# Revenue
# =========================

forecast["revenue"] = (
    forecast["forecast_units"]
    *
    forecast["price_thb"]
)


# =========================
# Variable Cost
# =========================

forecast["variable_cost"] = (
    forecast["forecast_units"]
    *
    (
        forecast["fruit_cost"]
        +
        forecast["packaging_cost"]
        +
        forecast["labor_cost"]
    )
)


# =========================
# Platform Fee
# =========================

forecast["platform_fee"] = (
    forecast["revenue"]
    *
    forecast["commission_rate"]
)


# =========================
# Profit Before Overhead
# =========================

forecast["profit_before_overhead"] = (
    forecast["revenue"]
    -
    forecast["variable_cost"]
    -
    forecast["platform_fee"]
)


# =========================
# Export
# =========================

forecast.to_csv(
    "output/forecast_pnl_3_month.csv",
    index=False
)


print("\nForecast P&L Example")
print(
    forecast.head()
)


print(
    "\nExport forecast P&L completed!"
)