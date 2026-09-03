import math
import pandas as pd
import folium
from folium.plugins import MarkerCluster


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

            angle = (
                2 * math.pi * i / max(total, 1)
            )

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
      .drop_duplicates(
          "project_id",
          keep="last"
      )
      .copy()
)


# ----------------------------------------
# 5. District-level summary
# ----------------------------------------

district_summary = (
    latest
    .groupby(["state", "district"])
    .agg(
        total_projects=("project_id", "nunique"),

        high_risk=(
            "delay_risk",
            lambda x: (x == "High").sum()
        ),

        medium_risk=(
            "delay_risk",
            lambda x: (x == "Medium").sum()
        ),

        low_risk=(
            "delay_risk",
            lambda x: (x == "Low").sum()
        ),

        average_delay=(
            "delay_days",
            "mean"
        ),

        average_objections=(
            "objection_count",
            "mean"
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
# 7. Create India map
# ----------------------------------------

m = folium.Map(
    location=[22.5, 79.0],
    zoom_start=5,
    tiles="OpenStreetMap"
)


# ----------------------------------------
# 8. Marker cluster
# ----------------------------------------

marker_cluster = MarkerCluster(
    name="District Risk Markers"
).add_to(m)


# ----------------------------------------
# 9. Add district markers
# ----------------------------------------

for _, row in district_summary.iterrows():

    state = row["state"]
    district = row["district"]

    key = (state, district)

    if key not in coordinates:
        continue


    # Determine dominant risk
    if (
        row["high_risk"]
        >= row["medium_risk"]
        and
        row["high_risk"]
        >= row["low_risk"]
    ):

        marker_color = "red"
        risk = "HIGH"

    elif row["medium_risk"] >= row["low_risk"]:

        marker_color = "orange"
        risk = "MEDIUM"

    else:

        marker_color = "green"
        risk = "LOW"


    lat, lon = coordinates[key]


    popup_html = f"""

    <div style="font-size:14px;">

        <b>District:</b>
        {district}
        <br><br>

        <b>State:</b>
        {state}
        <br><br>

        <b>Total Projects:</b>
        {int(row['total_projects'])}
        <br>

        <b>High Risk:</b>
        {int(row['high_risk'])}
        <br>

        <b>Medium Risk:</b>
        {int(row['medium_risk'])}
        <br>

        <b>Low Risk:</b>
        {int(row['low_risk'])}
        <br>

        <b>Average Delay:</b>
        {row['average_delay']:.1f}
        days
        <br>

        <b>Average Objections:</b>
        {row['average_objections']:.1f}
        <br>

        <b>Dominant Risk:</b>
        {risk}

    </div>

    """


    folium.CircleMarker(

        location=[
            lat,
            lon
        ],

        radius=9,

        color=marker_color,

        fill=True,

        fill_opacity=0.75,

        popup=folium.Popup(
            popup_html,
            max_width=320
        ),

        tooltip=(
            f"{district}, "
            f"{state} - {risk}"
        )

    ).add_to(marker_cluster)


# ----------------------------------------
# 10. Add note
# ----------------------------------------

folium.map.Marker(

    [9.0, 68.0],

    icon=folium.DivIcon(

        html="""
        <div style="
            background:white;
            padding:6px;
            border:1px solid #888;
            font-size:11px;">
            Prototype positions are approximate.
            Replace with official district/project
            coordinates for production.
        </div>
        """

    )

).add_to(m)


# ----------------------------------------
# 11. Layer control
# ----------------------------------------

folium.LayerControl().add_to(m)


# ----------------------------------------
# 12. Save map
# ----------------------------------------

m.save(
    "land_acquisition_map.html"
)


print("======================================")
print("DISTRICT GIS MAP CREATED SUCCESSFULLY")
print("======================================")

print(
    "Districts mapped:",
    len(district_summary)
)

print(
    "Output:",
    "land_acquisition_map.html"
)