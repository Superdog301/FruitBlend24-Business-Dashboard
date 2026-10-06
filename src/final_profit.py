import pandas as pd

# load data

orders = pd.read_csv(
    "output/orders_profit_platform.csv"
)

excel_path = "data/FruitBlend24_Intern_Case_Data.xlsx"


# load overhead

cost = pd.read_excel(
    excel_path,
    sheet_name="cost_assumptions"
)


# ==========================
# Extract kitchen overhead
# ==========================

overhead = cost[
    cost["sku"].isin(
        [
            "Pattaya_Central",
            "Pattaya_Beach",
            "BKK_Sukhumvit",
            "BKK_Ladprao"
        ]
    )
].copy()


overhead = overhead[
    [
        "sku",
        "packaging_cost_per_cup_thb"
    ]
]


overhead.columns = [
    "kitchen",
    "monthly_overhead"
]


print("\nKitchen Overhead")
print(overhead)
# ==========================
# Add month column
# ==========================

orders["date"] = pd.to_datetime(orders["date"])

orders["month"] = (
    orders["date"]
    .dt.to_period("M")
    .astype(str)
)


# ==========================
# Merge overhead
# ==========================

orders = orders.merge(
    overhead,
    on="kitchen",
    how="left"
)


print("\nAfter Overhead Merge")
print(
    orders[
        [
            "kitchen",
            "monthly_overhead"
        ]
    ].head()
)


# ==========================
# Allocate overhead by month
# ==========================

# นับจำนวนเดือนที่มีข้อมูลในแต่ละ kitchen
month_count = (
    orders
    .groupby("kitchen")["month"]
    .nunique()
    .reset_index()
)


month_count.columns = [
    "kitchen",
    "active_months"
]


orders = orders.merge(
    month_count,
    on="kitchen",
    how="left"
)





# ==========================
# Create Monthly P&L
# ==========================

monthly_profit = (
    orders
    .groupby(
        [
            "month",
            "kitchen"
        ],
        as_index=False
    )
    .agg(
        revenue=(
            "gross_revenue_thb",
            "sum"
        ),
        profit_after_platform=(
            "profit_after_platform",
            "sum"
        ),
        units_sold=(
            "units_sold",
            "sum"
        )
    )
)


monthly_profit = monthly_profit.merge(
    overhead,
    on="kitchen",
    how="left"
)


monthly_profit["net_profit"] = (
    monthly_profit["profit_after_platform"]
    -
    monthly_profit["monthly_overhead"]
)


monthly_profit["net_margin_%"] = (
    monthly_profit["net_profit"]
    /
    monthly_profit["revenue"]
    *
    100
)


print("\nMonthly P&L")
print(monthly_profit.head())


monthly_profit.to_csv(
    "output/monthly_profit_analysis.csv",
    index=False
)

print("\nExport monthly_profit_analysis.csv completed!")


print("\nExport final_profit_analysis.csv completed!")