import pandas as pd

# file paths
excel_path = "data/FruitBlend24_Intern_Case_Data.xlsx"

# 1. Load orders
orders = pd.read_csv(
    "output/orders_clean.csv"
)

# 2. Load fruit cost
fruit_cost = pd.read_excel(
    excel_path,
    sheet_name="weekly_fruit_cost"
)

# ดูข้อมูลก่อน
print("ORDERS")
print(orders.head())

print("\nFRUIT COST")
print(fruit_cost.head())
# ==========================
# Clean SKU name
# ==========================

fruit_cost["sku"] = fruit_cost["sku"].replace({
    "PassionFruit": "Passion Fruit",
    "MixedBerryPremium": "Mixed Berry"
})


# ดูค่าเฉลี่ยต้นทุนผลไม้ต่อเมนู
fruit_cost_avg = (
    fruit_cost
    .groupby("sku")["fruit_cost_per_cup_thb"]
    .mean()
    .reset_index()
)

print("\nAverage Fruit Cost")
print(fruit_cost_avg)
# ==========================
# Merge fruit cost
# ==========================

orders_profit = orders.merge(
    fruit_cost_avg,
    left_on="menu_clean",
    right_on="sku",
    how="left"
)


print("\nAfter merge")
print(orders_profit.head())


print("\nMissing fruit cost")
print(
    orders_profit["fruit_cost_per_cup_thb"].isna().sum()
)
print("\nMissing Menu")
print(
    orders_profit[
        orders_profit["fruit_cost_per_cup_thb"].isna()
    ]["menu_clean"]
    .value_counts()
)
# ==========================
# Load cost assumptions
# ==========================

cost = pd.read_excel(
    excel_path,
    sheet_name="cost_assumptions"
)

print("\nCOST ASSUMPTIONS")
print(cost.head(10))
# ==========================
# Clean cup cost table
# ==========================

cup_cost = cost.iloc[0:5].copy()

cup_cost = cup_cost.rename(
    columns={
        "sku": "menu_clean"
    }
)

cup_cost["menu_clean"] = cup_cost["menu_clean"].replace({
    "PassionFruit": "Passion Fruit",
    "MixedBerryPremium": "Mixed Berry"
})

print("\nCUP COST")
print(cup_cost)
orders_profit = orders_profit.merge(
    cup_cost[
        [
            "menu_clean",
            "packaging_cost_per_cup_thb",
            "labor_cost_per_cup_thb"
        ]
    ],
    on="menu_clean",
    how="left"
)

print("\nAfter cost merge")
print(orders_profit.head())
# ==========================
# Calculate Profit
# ==========================

orders_profit["fruit_cost_total"] = (
    orders_profit["units_sold"] *
    orders_profit["fruit_cost_per_cup_thb"]
)

orders_profit["packaging_cost_total"] = (
    orders_profit["units_sold"] *
    orders_profit["packaging_cost_per_cup_thb"]
)

orders_profit["labor_cost_total"] = (
    orders_profit["units_sold"] *
    orders_profit["labor_cost_per_cup_thb"]
)


# Total variable cost

orders_profit["total_variable_cost"] = (
    orders_profit["fruit_cost_total"]
    +
    orders_profit["packaging_cost_total"]
    +
    orders_profit["labor_cost_total"]
)


# Profit before platform commission

orders_profit["profit_before_platform"] = (
    orders_profit["gross_revenue_thb"]
    -
    orders_profit["total_variable_cost"]
)


orders_profit["profit_margin_%"] = (
    orders_profit["profit_before_platform"]
    /
    orders_profit["gross_revenue_thb"]
    * 100
)


print("\nProfit Example")
print(
    orders_profit[
        [
            "menu_clean",
            "gross_revenue_thb",
            "total_variable_cost",
            "profit_before_platform",
            "profit_margin_%"
        ]
    ].head()
)


# Export

orders_profit.to_csv(
    "output/orders_profit.csv",
    index=False
)

print("\nExport orders_profit.csv completed!")
# ==========================
# Platform Commission
# ==========================

platform_rate = pd.read_excel(
    excel_path,
    sheet_name="platform_commission_rate"
)


# extract platform code from rate_code

orders_profit["platform_code"] = (
    orders_profit["rate_code"]
    .str.split("-")
    .str[0]
)


# merge commission

orders_profit = orders_profit.merge(
    platform_rate,
    on="platform_code",
    how="left"
)


print("\nAfter Platform Merge")
print(
    orders_profit[
        [
            "rate_code",
            "platform_name",
            "commission_rate"
        ]
    ].head()
)


# calculate commission

orders_profit["platform_fee"] = (
    orders_profit["gross_revenue_thb"]
    *
    orders_profit["commission_rate"]
)


# profit after platform

orders_profit["profit_after_platform"] = (
    orders_profit["profit_before_platform"]
    -
    orders_profit["platform_fee"]
)


orders_profit["margin_after_platform_%"] = (
    orders_profit["profit_after_platform"]
    /
    orders_profit["gross_revenue_thb"]
    *
    100
)


# save

orders_profit.to_csv(
    "output/orders_profit_platform.csv",
    index=False
)


print("\nExport completed!")