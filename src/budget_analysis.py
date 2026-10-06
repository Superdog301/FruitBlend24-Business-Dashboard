import pandas as pd


# Load actual P&L
actual = pd.read_csv(
    "output/monthly_profit_analysis.csv"
)

print(actual.columns)


# Load budget
file_path = "data/FruitBlend24_Intern_Case_Data.xlsx"

budget = pd.read_excel(
    file_path,
    sheet_name="monthly_budget"
)


# แปลงเดือนให้ตรงกัน
actual["month"] = pd.to_datetime(actual["month"])
budget["month"] = pd.to_datetime(budget["month"])


# รวม actual จากทุก kitchen ต่อเดือน
actual_month = (
    actual
    .groupby("month")
    .agg(
        actual_revenue=("revenue","sum"),
        actual_gross_profit=("profit_after_platform","sum")
    )
    .reset_index()
)


print("Actual")
print(actual_month.head())


# merge กับ budget

result = actual_month.merge(
    budget,
    on="month",
    how="left"
)


# variance

result["revenue_variance"] = (
    result["actual_revenue"]
    -
    result["budget_revenue_thb"]
)


result["revenue_variance_%"] = (
    result["revenue_variance"]
    /
    result["budget_revenue_thb"]
    *100
)


result["gross_profit_variance"] = (
    result["actual_gross_profit"]
    -
    result["budget_gross_profit_thb"]
)


result["gross_profit_variance_%"] = (
    result["gross_profit_variance"]
    /
    result["budget_gross_profit_thb"]
    *100
)


print("\nBudget Comparison")
print(result.head())


result.to_csv(
    "output/budget_vs_actual.csv",
    index=False
)


print("\nExport completed!")