import pandas as pd

file_path = "data/FruitBlend24_Intern_Case_Data.xlsx"

budget = pd.read_excel(
    file_path,
    sheet_name="monthly_budget"
)

print(budget.head())
print(budget.columns)