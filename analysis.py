"""
E-Commerce Sales Data Analysis
--------------------------------
Performs exploratory data analysis on 2 years of e-commerce order data,
generates key business insights, and saves visualizations.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette="viridis")
plt.rcParams["figure.dpi"] = 130

DATA_PATH = "/home/claude/ecommerce-sales-analysis/data/ecommerce_sales.csv"
VIS_DIR = "/home/claude/ecommerce-sales-analysis/visuals"

df = pd.read_csv(DATA_PATH, parse_dates=["order_date"])
df["month"] = df["order_date"].dt.to_period("M").astype(str)
df["month_num"] = df["order_date"].dt.month
df["year"] = df["order_date"].dt.year

# ---------------------------------------------------------------
# 1. Monthly revenue trend
# ---------------------------------------------------------------
monthly = df.groupby("month")["revenue"].sum().reset_index()
plt.figure(figsize=(11, 5))
plt.plot(monthly["month"], monthly["revenue"], marker="o", linewidth=2, color="#3b6ea5")
plt.fill_between(range(len(monthly)), monthly["revenue"], alpha=0.15, color="#3b6ea5")
plt.xticks(rotation=60, fontsize=8)
plt.title("Monthly Revenue Trend (2024–2025)", fontsize=13, fontweight="bold")
plt.ylabel("Revenue (₹)")
plt.xlabel("")
plt.tight_layout()
plt.savefig(f"{VIS_DIR}/01_monthly_revenue_trend.png")
plt.close()

# ---------------------------------------------------------------
# 2. Revenue by category
# ---------------------------------------------------------------
cat_rev = df.groupby("category")["revenue"].sum().sort_values(ascending=False)
plt.figure(figsize=(8, 5))
sns.barplot(x=cat_rev.values, y=cat_rev.index, hue=cat_rev.index, legend=False, palette="crest")
plt.title("Total Revenue by Category", fontsize=13, fontweight="bold")
plt.xlabel("Revenue (₹)")
plt.ylabel("")
for i, v in enumerate(cat_rev.values):
    plt.text(v, i, f" ₹{v:,.0f}", va="center", fontsize=9)
plt.tight_layout()
plt.savefig(f"{VIS_DIR}/02_revenue_by_category.png")
plt.close()

# ---------------------------------------------------------------
# 3. Regional performance
# ---------------------------------------------------------------
region_rev = df.groupby("region")["revenue"].sum().sort_values(ascending=False)
plt.figure(figsize=(7, 6))
colors = sns.color_palette("crest", len(region_rev))
plt.pie(region_rev.values, labels=region_rev.index, autopct="%1.1f%%",
        startangle=90, colors=colors, wedgeprops={"edgecolor": "white", "linewidth": 1.5})
plt.title("Revenue Share by Region", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig(f"{VIS_DIR}/03_revenue_by_region.png")
plt.close()

# ---------------------------------------------------------------
# 4. Payment method popularity vs avg order value
# ---------------------------------------------------------------
pay_stats = df.groupby("payment_method").agg(orders=("order_id", "count"),
                                              avg_value=("revenue", "mean")).sort_values("orders", ascending=False)
fig, ax1 = plt.subplots(figsize=(9, 5))
ax2 = ax1.twinx()
ax1.bar(pay_stats.index, pay_stats["orders"], color="#3b6ea5", alpha=0.85, label="Order Count")
ax2.plot(pay_stats.index, pay_stats["avg_value"], color="#e8871e", marker="o", linewidth=2.5, label="Avg Order Value")
ax1.set_ylabel("Number of Orders")
ax2.set_ylabel("Average Order Value (₹)")
ax1.set_title("Payment Method: Popularity vs Average Order Value", fontsize=13, fontweight="bold")
fig.legend(loc="upper right", bbox_to_anchor=(0.9, 0.88))
plt.tight_layout()
plt.savefig(f"{VIS_DIR}/04_payment_methods.png")
plt.close()

# ---------------------------------------------------------------
# 5. Discount % vs Return rate (does discounting hurt quality perception?)
# ---------------------------------------------------------------
discount_return = df.groupby("discount_pct")["is_returned"].mean().reset_index()
discount_return["is_returned"] *= 100
plt.figure(figsize=(8, 5))
sns.barplot(x="discount_pct", y="is_returned", data=discount_return, hue="discount_pct",
            legend=False, palette="rocket")
plt.title("Return Rate by Discount Level", fontsize=13, fontweight="bold")
plt.xlabel("Discount (%)")
plt.ylabel("Return Rate (%)")
plt.tight_layout()
plt.savefig(f"{VIS_DIR}/05_discount_vs_returns.png")
plt.close()

# ---------------------------------------------------------------
# 6. Customer rating distribution
# ---------------------------------------------------------------
plt.figure(figsize=(7, 5))
sns.countplot(x="customer_rating", data=df, hue="customer_rating", legend=False, palette="crest")
plt.title("Customer Rating Distribution", fontsize=13, fontweight="bold")
plt.xlabel("Rating (1–5 stars)")
plt.ylabel("Number of Orders")
plt.tight_layout()
plt.savefig(f"{VIS_DIR}/06_rating_distribution.png")
plt.close()

# ---------------------------------------------------------------
# Key insights (printed + saved to text file for README)
# ---------------------------------------------------------------
total_revenue = df["revenue"].sum()
total_orders = len(df)
avg_order_value = df["revenue"].mean()
return_rate = df["is_returned"].mean() * 100
top_category = cat_rev.idxmax()
top_region = region_rev.idxmax()
best_month = monthly.loc[monthly["revenue"].idxmax(), "month"]
top_payment = pay_stats["orders"].idxmax()
high_discount_return = discount_return.iloc[-1]["is_returned"]
low_discount_return = discount_return.iloc[0]["is_returned"]

insights = f"""KEY INSIGHTS
============
- Total Revenue: ₹{total_revenue:,.0f} across {total_orders:,} orders
- Average Order Value: ₹{avg_order_value:,.0f}
- Overall Return Rate: {return_rate:.1f}%
- Top Category by Revenue: {top_category} (₹{cat_rev.max():,.0f})
- Top Performing Region: {top_region} ({region_rev.max()/total_revenue*100:.1f}% of revenue)
- Peak Sales Month: {best_month}
- Most Used Payment Method: {top_payment} ({pay_stats.loc[top_payment,'orders']} orders)
- Return rate does not increase steadily with discount depth — it ranges narrowly between {discount_return['is_returned'].min():.1f}% and {discount_return['is_returned'].max():.1f}% across all discount tiers, suggesting discounting alone isn't a strong driver of returns
- Festive season (Oct-Dec) shows a visible revenue spike in the monthly trend chart
"""

with open("/home/claude/ecommerce-sales-analysis/insights.txt", "w") as f:
    f.write(insights)

print(insights)
print("All visualizations saved to:", VIS_DIR)
