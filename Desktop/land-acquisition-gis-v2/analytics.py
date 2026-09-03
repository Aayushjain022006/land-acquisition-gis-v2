import pandas as pd
import plotly.express as px


# ========================================
# 1. Load Dataset
# ========================================

df = pd.read_csv("hybrid_data.csv")


# ========================================
# 2. Use latest record for each project
# ========================================

latest = (
    df.sort_values(["project_id", "year"])
      .drop_duplicates("project_id", keep="last")
      .copy()
)


print("======================================")
print("LAND ACQUISITION ANALYTICS")
print("======================================")


# ========================================
# 3. Risk Distribution
# ========================================

risk_counts = (
    latest["delay_risk"]
    .value_counts()
    .rename_axis("Risk Level")
    .reset_index(name="Projects")
)


fig1 = px.bar(
    risk_counts,
    x="Risk Level",
    y="Projects",
    title="Land Acquisition Risk Distribution"
)


fig1.write_html(
    "risk_distribution.html"
)


print("Risk distribution chart created.")


# ========================================
# 4. Projects by State
# ========================================

state_counts = (
    latest.groupby("state")["project_id"]
    .nunique()
    .sort_values(ascending=False)
    .reset_index()
)


state_counts.columns = [
    "State",
    "Projects"
]


fig2 = px.bar(
    state_counts,
    x="State",
    y="Projects",
    title="Unique Projects by State"
)


fig2.update_layout(
    xaxis_tickangle=-45
)


fig2.write_html(
    "projects_by_state.html"
)


print("State-wise chart created.")


# ========================================
# 5. Projects by District
# ========================================

district_counts = (
    latest.groupby("district")["project_id"]
    .nunique()
    .sort_values(ascending=False)
    .head(20)
    .reset_index()
)


district_counts.columns = [
    "District",
    "Projects"
]


fig3 = px.bar(
    district_counts,
    x="District",
    y="Projects",
    title="Top 20 Districts by Projects"
)


fig3.update_layout(
    xaxis_tickangle=-45
)


fig3.write_html(
    "projects_by_district.html"
)


print("District-wise chart created.")


# ========================================
# 6. Average Delay by State
# ========================================

average_delay_state = (
    latest.groupby("state")["delay_days"]
    .mean()
    .round(2)
    .sort_values(ascending=False)
    .reset_index()
)


average_delay_state.columns = [
    "State",
    "Average Delay"
]


fig4 = px.bar(
    average_delay_state,
    x="State",
    y="Average Delay",
    title="Average Land Acquisition Delay by State"
)


fig4.update_layout(
    xaxis_tickangle=-45
)


fig4.write_html(
    "average_delay_by_state.html"
)


print("Average delay chart created.")


# ========================================
# 7. High-Risk Projects by District
# ========================================

high_risk_district = (
    latest[latest["delay_risk"] == "High"]
    .groupby("district")["project_id"]
    .nunique()
    .sort_values(ascending=False)
    .head(20)
    .reset_index()
)


high_risk_district.columns = [
    "District",
    "High Risk Projects"
]


fig5 = px.bar(
    high_risk_district,
    x="District",
    y="High Risk Projects",
    title="Top 20 Districts by High-Risk Projects"
)


fig5.update_layout(
    xaxis_tickangle=-45
)


fig5.write_html(
    "high_risk_by_district.html"
)


print("High-risk district chart created.")


# ========================================
# 8. Average Delay by Year
# ========================================

year_delay = (
    df.groupby("year")["delay_days"]
    .mean()
    .round(2)
    .reset_index()
)


fig6 = px.line(
    year_delay,
    x="year",
    y="delay_days",
    markers=True,
    title="Average Delay Trend by Year"
)


fig6.write_html(
    "average_delay_by_year.html"
)


print("Year-wise delay chart created.")


# ========================================
# 9. Compensation Status
# ========================================

compensation = (
    latest["compensation_status"]
    .value_counts()
    .rename_axis("Compensation Status")
    .reset_index(name="Projects")
)


fig7 = px.pie(
    compensation,
    names="Compensation Status",
    values="Projects",
    title="Compensation Status"
)


fig7.write_html(
    "compensation_status.html"
)


print("Compensation chart created.")


# ========================================
# 10. Final Message
# ========================================

print()
print("======================================")
print("ALL ANALYTICS CREATED SUCCESSFULLY")
print("======================================")