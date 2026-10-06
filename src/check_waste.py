import pandas as pd

file_path = "data/FruitBlend24_Intern_Case_Data.xlsx"

waste = pd.read_excel(
    file_path,
    sheet_name="waste_daily"
)

print(waste.head())
print(waste.columns)