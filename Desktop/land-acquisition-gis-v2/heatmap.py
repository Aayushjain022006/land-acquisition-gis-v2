import math
import pandas as pd
import folium
from folium.plugins import HeatMap


# ----------------------------------------
# 1. Load dataset
# ----------------------------------------

df = pd.read_csv("hybrid_data.csv")


# ----------------------------------------
# 2. State coordinates
# ----------------------------------------

STATE_COORDINATES = {
    "Andhra Pradesh": [15.9129, 79.7400],
    "Assam": [26.2006, 92.9376],
    "Bihar": [25.0961, 85.3131],
    "Chhattisgarh": [21.2787, 81.8661],
    "Gujarat": [22.2587, 71.1924],
    "Haryana": [29.0588, 76.0856],
    "Himachal Pradesh": [31.1048, 77.1734],
    "Jharkhand": [23.6102, 85.2799],
    "Karnataka": [15.3173, 75.7139],
    "Kerala": [10.8505, 76.2711],
    "Madhya Pradesh": [22.9734, 78.6569],
    "Maharashtra": [19.7515, 75.7139],
    "Odisha": [20.9517, 85.0985],
    "Punjab": [31.1471, 75.3412],
    "Rajasthan": [27.0238, 74.2179],
    "Tamil Nadu": [11.1271, 78.6569],
    "Telangana": [18.1124, 79.0193],
    "Uttar Pradesh": [26.8467, 80.9462],
    "Uttarakhand": [30.0668, 79.0193],
    "West Bengal": [22.9868, 87.8550],
    "Delhi": [28.6139, 77.2090]
}


# ----------------------------------------
# 3. Create approximate district positions
# ----------------------------------------

def create_district_coordinates(states, districts):

    coordinates = {}
    grouped = {}

    for state, district in zip(states, districts):

        grouped.setdefault(state, [])

        if district not in grouped[state]:
            grouped[state].append(district)

    for state, district_list in grouped.items():

        if state not in STATE_COORDINATES:
            continue

        base_lat = STATE_COORDINATES[state][0]
        base_lon = STATE_COORDINATES[state][1]

        total = len(district_list)

        radius = 0.6

        for i, district in enumerate(sorted(district_list)):

            angle = 2 * math.pi * i / max(total, 1)

            lat = base_lat + radius * math.sin(angle)
            lon = base_lon + radius * math.cos(angle)

            coordinates[(state, district)] = [
                lat,
                lon
            ]

    return coordinates


# ----------------------------------------
# 4. Use latest record for each project
# ----------------------------------------

latest = (
    df.sort_values(["project_id", "year"])
      .drop_duplicates("project_id", keep="last")
      .copy()
)


# ----------------------------------------
# 5. Calculate district risk
# ----------------------------------------

district_risk = (
    latest
    .groupby(["state", "district"])
    .agg(
        high_risk=(
            "delay_risk",
            lambda x: (x == "High").sum()
        ),
        total_projects=(
            "project_id",
            "nunique"
        )
    )
    .reset_index()
)


# ----------------------------------------
# 6. Create coordinates
# ----------------------------------------

coordinates = create_district_coordinates(
    latest["state"],
    latest["district"]
)


# ----------------------------------------
# 7. Create heatmap data
# ----------------------------------------

heat_data = []

for _, row in district_risk.iterrows():

    key = (
        row["state"],
        row["district"]
    )

    if key not in coordinates:
        continue

    lat, lon = coordinates[key]

    heat_data.append([
        lat,
        lon,
        float(row["high_risk"])
    ])


# ----------------------------------------
# 8. Create India map
# ----------------------------------------

m = folium.Map(
    location=[22.5, 79.0],
    zoom_start=5,
    tiles="OpenStreetMap"
)


# ----------------------------------------
# 9. Add heatmap
# ----------------------------------------

HeatMap(
    heat_data,
    radius=28,
    blur=22,
    min_opacity=0.35,
    max_zoom=7
).add_to(m)


# ----------------------------------------
# 10. Save heatmap
# ----------------------------------------

m.save(
    "risk_heatmap.html"
)


print("======================================")
print("RISK HEATMAP CREATED SUCCESSFULLY")
print("======================================")

print(
    "Districts included:",
    len(district_risk)
)

print(
    "Output:",
    "risk_heatmap.html"
)