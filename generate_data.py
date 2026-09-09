"""
Generates a realistic synthetic e-commerce sales dataset for analysis.
(Synthetic data is used so the project is fully self-contained and reproducible.)
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

N = 5000

categories = {
    "Electronics": (1500, 45000, 0.18),
    "Fashion": (300, 5000, 0.30),
    "Home & Kitchen": (400, 12000, 0.22),
    "Beauty": (150, 3000, 0.15),
    "Sports": (500, 8000, 0.15),
}
cat_names = list(categories.keys())
cat_weights = [v[2] for v in categories.values()]

regions = ["North", "South", "East", "West", "Central"]
region_weights = [0.28, 0.24, 0.18, 0.20, 0.10]

payment_methods = ["UPI", "Credit Card", "Debit Card", "Net Banking", "COD"]
payment_weights = [0.42, 0.20, 0.15, 0.10, 0.13]

start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 12, 31)
date_range_days = (end_date - start_date).days

rows = []
for i in range(N):
    cat = np.random.choice(cat_names, p=cat_weights)
    low, high, return_base = categories[cat]
    price = np.round(np.random.uniform(low, high), 2)
    qty = np.random.choice([1, 1, 1, 2, 2, 3], p=[0.4, 0.25, 0.15, 0.1, 0.06, 0.04])

    # seasonal boost: Oct-Dec (festive season) gets more orders
    day_offset = np.random.randint(0, date_range_days)
    order_date = start_date + timedelta(days=day_offset)
    if order_date.month in (10, 11, 12):
        if np.random.random() < 0.4:
            day_offset = np.random.randint(
                (datetime(order_date.year, 10, 1) - start_date).days,
                (datetime(order_date.year, 12, 31) - start_date).days,
            )
            order_date = start_date + timedelta(days=day_offset)

    discount_pct = np.random.choice([0, 5, 10, 15, 20, 30], p=[0.30, 0.20, 0.20, 0.15, 0.10, 0.05])
    revenue = np.round(price * qty * (1 - discount_pct / 100), 2)

    region = np.random.choice(regions, p=region_weights)
    payment = np.random.choice(payment_methods, p=payment_weights)

    is_returned = np.random.random() < return_base * (0.6 if discount_pct > 15 else 1.0) * 0.25
    rating = np.random.choice([1, 2, 3, 4, 5], p=[0.03, 0.05, 0.12, 0.35, 0.45])

    rows.append({
        "order_id": f"ORD{100000+i}",
        "order_date": order_date.strftime("%Y-%m-%d"),
        "category": cat,
        "price": price,
        "quantity": qty,
        "discount_pct": discount_pct,
        "revenue": revenue,
        "region": region,
        "payment_method": payment,
        "is_returned": is_returned,
        "customer_rating": rating,
    })

df = pd.DataFrame(rows)
df.to_csv("/home/claude/ecommerce-sales-analysis/data/ecommerce_sales.csv", index=False)
print(f"Generated {len(df)} rows")
print(df.head())
