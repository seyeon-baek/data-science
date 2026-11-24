import pandas as pd

df = pd.read_csv("data/raw/super_store_sales.csv")
df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True)
df["Order Month"] = df["Order Date"].dt.to_period("M").astype(str)

cols = ["Order Month", "Region", "Category", "Sub-Category", "Order ID", "Sales"]
cols += [c for c in ["Profit", "Quantity"] if c in df.columns]
df[cols].to_csv("data/superstore_clean.csv", index=False)
print(df[cols].shape)