import pandas as pd
import numpy as np

# =========================
# 1. LOAD DATA
# =========================
df = pd.read_csv("cafe_sales_dataset.csv")

# =========================
# 2. CLEAN DATA
# =========================
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

df.dropna(inplace=True)

df['order_date'] = pd.to_datetime(df['order_date'])
df['order_time'] = pd.to_datetime(df['order_time'], format='%H:%M:%S')

# =========================
# 3. FEATURE ENGINEERING
# =========================
df['hour'] = df['order_time'].dt.hour
df['day'] = df['order_date'].dt.day_name()

if 'total_sales' not in df.columns:
    df['total_sales'] = df['quantity'] * df['price']

# =========================
# 4. KPI CALCULATIONS
# =========================
kpi_df = pd.DataFrame([{
    "total_revenue": df['total_sales'].sum(),
    "total_orders": df['order_id'].nunique(),
    "avg_order_value": df.groupby('order_id')['total_sales'].sum().mean(),
    "avg_items_per_order": df['quantity'].sum() / df['order_id'].nunique()
}])

# =========================
# 5. CATEGORY SUMMARY
# =========================
category_summary = (
    df.groupby('category')['total_sales']
    .sum()
    .reset_index()
    .sort_values(by='total_sales', ascending=False)
)

# =========================
# 6. PRODUCT SUMMARY
# =========================
product_summary = (
    df.groupby('product_name')['total_sales']
    .sum()
    .reset_index()
    .sort_values(by='total_sales', ascending=False)
)

# =========================
# 7. HOURLY SALES
# =========================
hourly_summary = (
    df.groupby('hour')['total_sales']
    .sum()
    .reset_index()
    .sort_values('hour')
)

# =========================
# 8. DAILY SALES
# =========================
daily_summary = (
    df.groupby('order_date')['total_sales']
    .sum()
    .reset_index()
)

# =========================
# 9. PAYMENT METHOD SUMMARY
# =========================
payment_summary = (
    df.groupby('payment_method')['total_sales']
    .sum()
    .reset_index()
    .sort_values(by='total_sales', ascending=False)
)

# =========================
# 10. EXPORT FOR EXCEL
# =========================
kpi_df.to_csv("kpi_summary.csv", index=False)
category_summary.to_csv("category_summary.csv", index=False)
product_summary.to_csv("product_summary.csv", index=False)
hourly_summary.to_csv("hourly_summary.csv", index=False)
daily_summary.to_csv("daily_summary.csv", index=False)
payment_summary.to_csv("payment_summary.csv", index=False)

print("✅ All summary files created successfully!")
