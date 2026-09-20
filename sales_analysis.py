# ==========================================
# SALES DATA ANALYSIS PROJECT
# ==========================================

# Import Libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------------------------------
# 1. LOAD DATA
# ------------------------------------------

# Change file name if required
df = pd.read_csv("sales_data.csv")

print("\n===== FIRST 5 ROWS =====")
print(df.head())

# ------------------------------------------
# 2. DATA INSPECTION
# ------------------------------------------

print("\n===== DATASET INFO =====")
print(df.info())

print("\n===== DATASET SHAPE =====")
print(df.shape)

print("\n===== COLUMN NAMES =====")
print(df.columns)

print("\n===== DESCRIPTIVE STATISTICS =====")
print(df.describe())

# ------------------------------------------
# 3. DATA CLEANING
# ------------------------------------------

print("\n===== MISSING VALUES =====")
print(df.isnull().sum())

# Fill numerical missing values with mean
numeric_cols = df.select_dtypes(include=['number']).columns

for col in numeric_cols:
    df[col].fillna(df[col].mean(), inplace=True)

# Remove duplicates
duplicate_count = df.duplicated().sum()
print(f"\nDuplicate Records: {duplicate_count}")

df.drop_duplicates(inplace=True)

# Convert Order Date column
if 'Order Date' in df.columns:
    df['Order Date'] = pd.to_datetime(df['Order Date'])

print("\n===== CLEANED DATA INFO =====")
print(df.info())

# ------------------------------------------
# 4. EXPLORATORY DATA ANALYSIS
# ------------------------------------------

print("\n===== SALES BY REGION =====")

if 'Region' in df.columns:
    sales_region = df.groupby('Region')['Sales'].sum()
    print(sales_region)

print("\n===== SALES BY CATEGORY =====")

if 'Category' in df.columns:
    sales_category = df.groupby('Category')['Sales'].sum()
    print(sales_category)

print("\n===== AVERAGE PROFIT BY CATEGORY =====")

if 'Profit' in df.columns:
    avg_profit = df.groupby('Category')['Profit'].mean()
    print(avg_profit)

print("\n===== REGION COUNT =====")

if 'Region' in df.columns:
    print(df['Region'].value_counts())

# ------------------------------------------
# 5. PIVOT TABLE
# ------------------------------------------

print("\n===== SALES PIVOT TABLE =====")

pivot_table = pd.pivot_table(
    df,
    values='Sales',
    index='Region',
    columns='Category',
    aggfunc='sum'
)

print(pivot_table)

# Save Pivot Table
pivot_table.to_csv("sales_pivot_table.csv")

# ------------------------------------------
# 6. VISUALIZATIONS
# ------------------------------------------

sns.set_style("whitegrid")

# Sales by Region
plt.figure(figsize=(8,5))
sales_region.plot(kind='bar', color='skyblue')
plt.title("Total Sales by Region")
plt.xlabel("Region")
plt.ylabel("Sales")
plt.tight_layout()
plt.savefig("sales_by_region.png")
plt.show()

# Category Distribution
plt.figure(figsize=(8,6))
df['Category'].value_counts().plot(
    kind='pie',
    autopct='%1.1f%%'
)
plt.ylabel("")
plt.title("Category Distribution")
plt.tight_layout()
plt.savefig("category_distribution.png")
plt.show()

# Monthly Sales Trend
if 'Order Date' in df.columns:

    df['Month'] = df['Order Date'].dt.month

    monthly_sales = (
        df.groupby('Month')['Sales']
        .sum()
        .sort_index()
    )

    plt.figure(figsize=(10,5))
    monthly_sales.plot(
        marker='o',
        linewidth=2
    )
    plt.title("Monthly Sales Trend")
    plt.xlabel("Month")
    plt.ylabel("Sales")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("monthly_sales_trend.png")
    plt.show()

# Profit by Category
if 'Profit' in df.columns:

    plt.figure(figsize=(8,5))

    sns.barplot(
        x='Category',
        y='Profit',
        data=df
    )

    plt.title("Profit by Category")
    plt.tight_layout()
    plt.savefig("profit_by_category.png")
    plt.show()

# ------------------------------------------
# 7. BUSINESS INSIGHTS
# ------------------------------------------

print("\n===== BUSINESS INSIGHTS =====")

top_region = sales_region.idxmax()
top_category = sales_category.idxmax()

print(f"Top Performing Region : {top_region}")
print(f"Top Selling Category  : {top_category}")

if 'Profit' in df.columns:
    most_profitable = avg_profit.idxmax()
    print(f"Most Profitable Category : {most_profitable}")

print("\nAnalysis Completed Successfully!")