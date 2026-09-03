import pandas as pd

# Load the new dataset
df = pd.read_csv("hybrid_data.csv")

print("\n======================================")
print("LAND ACQUISITION DATA ANALYSIS")
print("======================================")

# ----------------------------------------
# Basic Information
# ----------------------------------------

print("\nTotal Records:", len(df))

print(
    "Unique Projects:",
    df["project_id"].nunique()
)

print(
    "States:",
    df["state"].nunique()
)

print(
    "Districts:",
    df["district"].nunique()
)

print(
    "Year Range:",
    int(df["year"].min()),
    "to",
    int(df["year"].max())
)

# ----------------------------------------
# Risk Distribution
# ----------------------------------------

print("\nRisk Distribution:")

print(
    df["delay_risk"].value_counts()
)

# ----------------------------------------
# Project Status
# ----------------------------------------

print("\nProject Status:")

print(
    df["project_status"].value_counts()
)

# ----------------------------------------
# Completion Status
# ----------------------------------------

print("\nCompletion Status:")

print(
    df["project_completion_status"].value_counts()
)

# ----------------------------------------
# Projects by State
# ----------------------------------------

print("\nProjects by State:")

print(
    df.groupby("state")["project_id"]
    .nunique()
    .sort_values(ascending=False)
)

# ----------------------------------------
# Projects by District
# ----------------------------------------

print("\nTop 15 Districts:")

print(
    df.groupby("district")["project_id"]
    .nunique()
    .sort_values(ascending=False)
    .head(15)
)

# ----------------------------------------
# Average Delay
# ----------------------------------------

print("\nAverage Delay:")

print(
    round(df["delay_days"].mean(), 2),
    "days"
)

# ----------------------------------------
# Maximum Delay
# ----------------------------------------

print("\nMaximum Delay:")

print(
    df["delay_days"].max(),
    "days"
)

# ----------------------------------------
# Minimum Delay
# ----------------------------------------

print("\nMinimum Delay:")

print(
    df["delay_days"].min(),
    "days"
)

# ----------------------------------------
# High Risk Districts
# ----------------------------------------

print("\nHigh Risk Districts:")

high_risk = (
    df[df["delay_risk"] == "High"]
    .groupby("district")["project_id"]
    .nunique()
    .sort_values(ascending=False)
    .head(15)
)

print(high_risk)

# ----------------------------------------
# Average Delay by Year
# ----------------------------------------

print("\nAverage Delay by Year:")

year_delay = (
    df.groupby("year")["delay_days"]
    .mean()
    .round(2)
)

print(year_delay)

print("\n======================================")
print("ANALYSIS COMPLETED SUCCESSFULLY")
print("======================================")