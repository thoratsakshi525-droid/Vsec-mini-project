
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Create vegetable price dataset (sample prices in Rs/kg)

data = {
    "Vegetable": [
        "Tomato", "Onion", "Potato", "Cauliflower",
        "Cabbage", "Carrot", "Brinjal", "Green Chilli"
    ],
    "January":  [25, 30, 20, 35, 25, 40, 30, 60],
    "February": [30, 28, 22, 30, 28, 35, 32, 55],
    "March":    [22, 32, 24, 28, 30, 38, 28, 70],
    "April":    [40, 35, 25, 32, 27, 45, 35, 65],
    "May":      [35, 38, 28, 40, 32, 50, 38, 80],
    "June":     [50, 42, 30, 45, 35, 55, 40, 90]
}

df = pd.DataFrame(data)

months = [
    "January", "February", "March",
    "April", "May", "June"
]

# 2. Clean the data
df = df.drop_duplicates(subset="Vegetable")
df[months] = df[months].apply(
    pd.to_numeric, errors="coerce"
)
df[months] = df[months].fillna(df[months].median())

# 3. Calculate statistics
df["Average Price"] = df[months].mean(axis=1)
df["Price Change (%)"] = (
    (df["June"] - df["January"]) /
    df["January"].replace(0, np.nan) * 100
)

highest = df.loc[df["Average Price"].idxmax()]
biggest_rise = df.loc[df["Price Change (%)"].idxmax()]

print("\nVEGETABLE PRICE ANALYZER")
print("=" * 35)
print("Average prices (Rs/kg):")
print(df[["Vegetable", "Average Price"]].round(2).to_string(index=False))

print("\nMost expensive on average:",
      highest["Vegetable"])
print("Average price: Rs.",
      round(highest["Average Price"], 2), "per kg")

print("\nHighest percentage increase:",
      biggest_rise["Vegetable"])
print("Price increase:",
      round(biggest_rise["Price Change (%)"], 2), "%")

# 4. Create one clean dashboard
sns.set_theme(style="whitegrid")

fig = plt.figure(figsize=(14, 9))
fig.suptitle(
    "VEGETABLE PRICE FLUCTUATION ANALYZER",
    fontsize=19, fontweight="bold"
)

# Chart 1: Average price comparison
ax1 = fig.add_subplot(2, 2, 1)

sns.barplot(
    data=df.sort_values("Average Price", ascending=False),
    x="Average Price",
    y="Vegetable",
    color="seagreen",
    ax=ax1
)

ax1.set_title("Average Price of Vegetables")
ax1.set_xlabel("Price (Rs/kg)")
ax1.set_ylabel("")

# Chart 2: Simple tomato price trend
ax2 = fig.add_subplot(2, 2, 2)

ax2.plot(
    months,
    df.loc[df["Vegetable"] == "Tomato", months].iloc[0],
    marker="o",
    linewidth=3,
    color="tomato"
)

ax2.set_title("Tomato Price Trend")
ax2.set_ylabel("Price (Rs/kg)")
ax2.set_xlabel("Month")
ax2.tick_params(axis="x", rotation=25)

# Chart 3: Heatmap for all vegetables
ax3 = fig.add_subplot(2, 1, 2)

sns.heatmap(
    df.set_index("Vegetable")[months],
    annot=True,
    fmt=".0f",
    cmap="YlOrRd",
    linewidths=0.5,
    cbar_kws={"label": "Price (Rs/kg)"},
    ax=ax3
)

ax3.set_title("Monthly Price Comparison")
ax3.set_xlabel("Month")
ax3.set_ylabel("Vegetable")

plt.tight_layout(rect=[0, 0, 1, 0.95])

# 5. Save results
df.to_csv("vegetable_price_analysis.csv", index=False)
plt.savefig("vegetable_price_dashboard.png", dpi=200,
            bbox_inches="tight")

plt.show()

print("\nDashboard saved successfully!")
print("CSV report saved successfully!")
