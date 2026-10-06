import pandas as pd

file_path = "data/FruitBlend24_Intern_Case_Data.xlsx"

df = pd.read_excel(
    file_path,
    sheet_name="platform_commission_rate"
)

print(df.head())
print(df.columns)