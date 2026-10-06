import pandas as pd

file_path = "data/FruitBlend24_Intern_Case_Data.xlsx"

waste = pd.read_excel(
    file_path,
    sheet_name="waste_daily"
)


# 1. Waste by SKU
waste_by_sku = (
    waste.groupby("sku")
    .agg(
        total_units_wasted=("units_wasted","sum"),
        total_waste_cost=("est_waste_cost_thb","sum")
    )
    .reset_index()
    .sort_values(
        "total_waste_cost",
        ascending=False
    )
)


print("Waste by SKU")
print(waste_by_sku.head())


# 2. Waste by Kitchen
waste_by_kitchen = (
    waste.groupby("kitchen")
    .agg(
        total_units_wasted=("units_wasted","sum"),
        total_waste_cost=("est_waste_cost_thb","sum")
    )
    .reset_index()
    .sort_values(
        "total_waste_cost",
        ascending=False
    )
)


print("\nWaste by Kitchen")
print(waste_by_kitchen)


# Export
waste_by_sku.to_csv(
    "output/waste_analysis.csv",
    index=False
)


waste_by_kitchen.to_csv(
    "output/waste_by_kitchen.csv",
    index=False
)


print("\nExport completed!")