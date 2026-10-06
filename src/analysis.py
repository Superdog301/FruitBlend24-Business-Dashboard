import pandas as pd

file_path = "data/FruitBlend24_Intern_Case_Data.xlsx"

df = pd.read_csv(
    "output/orders_clean.csv"
)

# ดูภาพรวม
print("Shape:", df.shape)

print("\nColumn:")
print(df.columns)

print("\nSummary:")
print(df.describe())

print("\nKitchen:")
print(df["kitchen"].value_counts())

print("\nTop Menu:")
print(
    df.groupby("item_name_raw")["units_sold"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nRevenue by Kitchen:")
print(
    df.groupby("kitchen")["gross_revenue_thb"]
    .sum()
    .sort_values(ascending=False)
)
# Revenue by Kitchen

revenue_by_kitchen = (
    df.groupby("kitchen")
    .agg(
        total_revenue=("gross_revenue_thb", "sum"),
        total_units=("units_sold", "sum")
    )
    .sort_values(
        by="total_revenue",
        ascending=False
    )
)


print(revenue_by_kitchen)


# Export CSV
kitchen_summary = (
    df.groupby("kitchen")
    .agg(
        total_revenue=("gross_revenue_thb", "sum"),
        total_units=("units_sold", "sum")
    )
    .sort_values(
        "total_revenue",
        ascending=False
    )
)

print(kitchen_summary)

kitchen_summary.to_csv(
    "output/revenue_by_kitchen_clean.csv"
)