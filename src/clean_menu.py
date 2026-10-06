import pandas as pd

file_path = "data/FruitBlend24_Intern_Case_Data.xlsx"

df = pd.read_excel(
    file_path,
    sheet_name="orders_hourly"
)


def clean_menu(x):
    x = str(x).lower().strip()

    if any(word in x for word in [
        "watermelon",
        "แตงโม"
    ]):
        return "Watermelon"

    elif any(word in x for word in [
        "pineapple",
        "สับปะรด"
    ]):
        return "Pineapple"

    elif any(word in x for word in [
        "passion",
        "passionfruit",
        "เสาวรส"
    ]):
        return "Passion Fruit"

    elif any(word in x for word in [
        "guava",
        "ฝรั่ง"
    ]):
        return "Guava"

    elif any(word in x for word in [
        "berry",
        "เบอร์รี่"
    ]):
        return "Mixed Berry"

    else:
        return "Other"



df["menu_clean"] = df["item_name_raw"].apply(clean_menu)


print(df["menu_clean"].value_counts())


# ตัด Other ออก
df_clean = df[df["menu_clean"] != "Other"]


# Export cleaned data
df_clean.to_csv(
    "output/orders_clean.csv",
    index=False
)


# Top menu
top_menu = (
    df_clean.groupby("menu_clean")
    .agg(
        units_sold=("units_sold","sum"),
        revenue=("gross_revenue_thb","sum")
    )
    .sort_values(
        "revenue",
        ascending=False
    )
)


print(top_menu)

top_menu.to_csv(
    "output/top_menu_clean.csv"
)