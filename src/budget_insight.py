import pandas as pd


df = pd.read_csv(
    "output/budget_vs_actual.csv"
)


print("Worst Revenue Month")
print(
    df.sort_values(
        "revenue_variance"
    ).head(5)
)


print("\nWorst Gross Profit Month")
print(
    df.sort_values(
        "gross_profit_variance"
    ).head(5)
)


print("\nBest Gross Profit Recovery")
print(
    df.sort_values(
        "gross_profit_variance_%",
        ascending=False
    ).head(5)
)