import pandas as pd

file_path = "data/FruitBlend24_Intern_Case_Data.xlsx"

df = pd.read_excel(
    file_path,
    sheet_name="orders_hourly"
)

print(df["item_name_raw"].value_counts())