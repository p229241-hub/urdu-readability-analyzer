"""
Preprocessing script for input_to_linear_regression2.xlsx
- Drops Unnamed: 8 column (100% empty)
- Removes rows with null/NA values
- Keeps duplicate rows (as required for project)
"""

import pandas as pd

print("Loading dataset...")
df = pd.read_excel("input_to_linear_regression2.xlsx")
print(f"Original shape: {df.shape[0]} rows x {df.shape[1]} columns")

# 1. Drop Unnamed: 8 column (100% empty)
if "Unnamed: 8" in df.columns:
    df = df.drop(columns=["Unnamed: 8"])
    print("Dropped column: Unnamed: 8")

# 2. Remove rows with any null/NA values (keep duplicates)
df_cleaned = df.dropna()
rows_removed = len(df) - len(df_cleaned)
print(f"Removed {rows_removed} rows with null values")

print(f"Cleaned shape: {df_cleaned.shape[0]} rows x {df_cleaned.shape[1]} columns")
print(f"Remaining duplicates: {df_cleaned.duplicated().sum()}")

# Save to new file (CSV is faster for large datasets; use to_excel if you need .xlsx)
output_csv = "input_to_linear_regression2_cleaned.csv"
df_cleaned.to_csv(output_csv, index=False)
print(f"\nSaved cleaned data to: {output_csv}")

# Optional: save as Excel (slower, uncomment if needed)
# df_cleaned.to_excel("input_to_linear_regression2_cleaned.xlsx", index=False)
