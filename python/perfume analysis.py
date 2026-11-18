
import pandas as pd
import matplotlib.pyplot as plt

# Load the cleaned perfume sales dataset
df = pd.read_csv("Perfume_Sales_Raw_Cleaned_Dataset.csv")

# Standardize column names
df.columns = df.columns.str.strip()
df.columns = df.columns.str.replace(" (?)", "", regex=False)

# Display basic information
print("Dataset loaded successfully!")
print("Number of rows and columns:", df.shape)

# Display the first five rows
print(df.head())

# Display all column names
print("\nCOLUMN NAMES:")
print(df.columns.tolist())

# Check data types and non-missing values
print("\nDATASET INFORMATION:")
df.info()

# Count missing values in each column
print("\nMISSING VALUES:")
print(df.isnull().sum())

# Count duplicate rows
print("\nDUPLICATE ROWS:")
print(df.duplicated().sum())



print(df.columns.tolist())

total_revenue = df["Revenue"].sum()
total_cost = df["Total Cost"].sum()
total_profit = df["Profit"].sum()

profit_margin = (total_profit / total_revenue) * 100

total_orders = len(df)
returned_orders = (
    df["Returned"].astype(str).str.strip().str.lower() == "yes"
).sum()

return_rate = (returned_orders / total_orders) * 100

print("\n===== PERFUME SALES KPI REPORT =====")
print(f"Total Revenue: ₦{total_revenue:,.2f}")
print(f"Total Cost: ₦{total_cost:,.2f}")
print(f"Total Profit: ₦{total_profit:,.2f}")
print(f"Profit Margin: {profit_margin:.2f}%")
print(f"Return Rate: {return_rate:.2f}%")



# ==============================
# REVENUE BY PERFUME
# ==============================

revenue_by_perfume = (
    df.groupby("Product Name")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

print("\n===== REVENUE BY PERFUME =====")
print(revenue_by_perfume)


# ==============================
# CHART: REVENUE BY PERFUME
# ==============================

plt.figure(figsize=(10, 6))

revenue_by_perfume.sort_values().plot(
    kind="barh",
    color="teal",
    title="Total Revenue by Perfume"
)

plt.xlabel("Revenue (₦)")
plt.ylabel("Perfume")
plt.tight_layout()
plt.savefig("revenue_by_perfume.png", dpi=300, bbox_inches="tight")
plt.show()
# ==============================
# PROFIT BY PERFUME
# ==============================

profit_by_perfume = (
    df.groupby("Product Name")["Profit"]
    .sum()
    .sort_values(ascending=False)
)

print("\n===== PROFIT BY PERFUME =====")
print(profit_by_perfume)

# Create a profit chart

plt.figure(figsize=(10, 6))

profit_by_perfume.sort_values().plot(
    kind="barh",
    color="seagreen",
    title="Total Profit by Perfume"
)

plt.xlabel("Profit (₦)")
plt.ylabel("Perfume")
plt.tight_layout()
plt.savefig("profit_by_perfume.png", dpi=300, bbox_inches="tight")
plt.show()


plt.figure(figsize=(10, 6))

# ==============================
# MONTHLY REVENUE ANALYSIS
# ==============================

# Make sure Order Date is recognized as a date
df["Order Date"] = pd.to_datetime(df["Order Date"])

# Extract the month and calculate revenue
df["Month"] = df["Order Date"].dt.to_period("M")

monthly_revenue = df.groupby("Month")["Revenue"].sum()

print("\n===== MONTHLY REVENUE =====")
print(monthly_revenue)

# Create a monthly revenue chart
monthly_revenue.index = monthly_revenue.index.astype(str)


plt.figure(figsize=(10, 6))

monthly_revenue.plot(
    kind="line",
    marker="o",
    title="Monthly Revenue Trend"
)

plt.xlabel("Month")
plt.ylabel("Revenue (₦)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("monthly_revenue_trend.png", dpi=300, bbox_inches="tight")
plt.show()


plt.figure(figsize=(10, 6))

# ==============================
# REVENUE BY SALES CHANNEL
# ==============================

revenue_by_channel = (
    df.groupby("Sales Channel")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

print("\n===== REVENUE BY SALES CHANNEL =====")
print(revenue_by_channel)

revenue_by_channel.sort_values().plot(
    kind="barh",
    figsize=(9, 5),
    title="Total Revenue by Sales Channel"
)

plt.xlabel("Revenue (₦)")
plt.ylabel("Sales Channel")
plt.tight_layout()
plt.show()



# ==============================
# REVENUE BY CUSTOMER TYPE
# ==============================

revenue_by_customer = (
    df.groupby("Customer Type")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

print("\n===== REVENUE BY CUSTOMER TYPE =====")
print(revenue_by_customer)

revenue_by_customer.plot(
    kind="bar",
    figsize=(8, 5),
    title="Total Revenue by Customer Type"
)

plt.xlabel("Customer Type")
plt.ylabel("Revenue (₦)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()



# ==============================
# AVERAGE RATING BY PERFUME
# ==============================

rating_by_perfume = (
    df.groupby("Product Name")["Rating"]
    .mean()
    .sort_values(ascending=False)
)

print("\n===== AVERAGE RATING BY PERFUME =====")
print(rating_by_perfume.round(2))

rating_by_perfume.sort_values().plot(
    kind="barh",
    figsize=(9, 6),
    title="Average Customer Rating by Perfume"
)

plt.xlabel("Average Rating")
plt.ylabel("Perfume")
plt.tight_layout()
plt.show()



# ==============================
# RETURN RATE BY SALES CHANNEL
# ==============================

df["Returned_Clean"] = (
    df["Returned"].astype(str).str.strip().str.lower()
)

return_analysis = df.groupby("Sales Channel").agg(
    Total_Records=("Order ID", "count"),
    Returned_Records=(
        "Returned_Clean",
        lambda x: (x == "yes").sum()
    )
)

return_analysis["Return_Rate_Percent"] = (
    return_analysis["Returned_Records"]
    / return_analysis["Total_Records"] * 100
)

return_analysis = return_analysis.sort_values(
    "Return_Rate_Percent", ascending=False
)

print("\n===== RETURN RATE BY SALES CHANNEL =====")
print(return_analysis.round(2))

return_analysis["Return_Rate_Percent"].sort_values().plot(
    kind="barh",
    figsize=(9, 5),
    title="Return Rate by Sales Channel"
)

plt.xlabel("Return Rate (%)")
plt.ylabel("Sales Channel")
plt.tight_layout()
plt.show()



# ==============================
# SALES CHANNEL PERFORMANCE
# ==============================

channel_performance = df.groupby("Sales Channel").agg(
    Total_Revenue=("Revenue", "sum"),
    Total_Records=("Order ID", "count"),
    Returned_Records=(
        "Returned_Clean",
        lambda x: (x == "yes").sum()
    )
)

channel_performance["Return_Rate_Percent"] = (
    channel_performance["Returned_Records"]
    / channel_performance["Total_Records"] * 100
)

channel_performance = channel_performance.sort_values(
    "Total_Revenue", ascending=False
)

print("\n===== SALES CHANNEL PERFORMANCE =====")
print(channel_performance.round(2))



# ==============================
# KEY BUSINESS FINDINGS
# ==============================

print("\n===== KEY BUSINESS FINDINGS =====")

print("1. Oud Royale generated the highest total revenue.")
print("2. Vanilla Mist generated the lowest total revenue.")
print("3. Instagram generated the highest revenue by sales channel.")
print("4. New customers generated the highest revenue by customer type.")
print("5. Instagram had the highest return rate among sales channels.")
print("6. The overall profit margin was approximately 46.38%.")
print("7. The overall return rate was 5.25%.")
print("8. Monthly revenue varied across the months in the dataset.")
