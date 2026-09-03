import pandas as pd

# Load the new hybrid dataset
df = pd.read_csv("hybrid_data.csv")

print("====================================")
print("HYBRID DATASET LOADED SUCCESSFULLY")
print("====================================")

print()

print("Total Records:", len(df))
print("Total Columns:", len(df.columns))

print()

print("Unique Projects:", df["project_id"].nunique())

print("States:", df["state"].nunique())

print("Districts:", df["district"].nunique())

print(
    "Year Range:",
    int(df["year"].min()),
    "to",
    int(df["year"].max())
)

print()

print("Risk Distribution:")
print(df["delay_risk"].value_counts())

print()

print("Column Names:")
print(df.columns.tolist())

print()

print("First 5 Records:")
print(df.head())