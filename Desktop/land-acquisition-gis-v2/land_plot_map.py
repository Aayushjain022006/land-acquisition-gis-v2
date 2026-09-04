import pandas as pd
import folium
from folium.features import DivIcon


# =========================================================
# LOAD MERGED DATASET
# =========================================================

df = pd.read_csv("final_data.csv")


# =========================================================
# SELECT ONE PROJECT FOR PARCEL DEMO
# =========================================================

project_id = "LA-REF-0001"

project_df = df[
    df["project_id"].astype(str) == project_id
].copy()


# Show only records having plot IDs
project_df = project_df[
    project_df["plot_id"].notna()
].head(5)


# =========================================================
# FALLBACK
# =========================================================

if project_df.empty:

    print("No plot records found.")

    raise SystemExit


# =========================================================
# MAP LOCATION
# =========================================================

center_lat = 19.2500
center_lon = 73.0200


m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=13,
    control_scale=True
)


# =========================================================
# TITLE
# =========================================================

title_html = f"""
<div style="
    position: fixed;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 9999;
    background: white;
    padding: 18px 35px;
    border-radius: 14px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.25);
    text-align: center;
    min-width: 520px;
">

    <div style="
        font-size: 26px;
        font-weight: 800;
        color: #222;
    ">
        LAND PARCEL STATUS VIEWER
    </div>

    <div style="
        margin-top: 8px;
        font-size: 15px;
        color: #444;
    ">
        Mumbai-Ahmedabad High Speed Rail
        (Bullet Train) - Package 1
    </div>

    <div style="
        margin-top: 4px;
        font-size: 14px;
        color: #666;
    ">
        Palghar, Maharashtra
    </div>

</div>
"""

m.get_root().html.add_child(
    folium.Element(title_html)
)


# =========================================================
# LEGEND
# =========================================================

legend_html = """
<div style="
    position: fixed;
    bottom: 35px;
    left: 35px;
    z-index: 9999;
    background: white;
    padding: 18px 20px;
    border-radius: 14px;
    box-shadow: 0 3px 15px rgba(0,0,0,0.25);
    width: 260px;
">

    <div style="
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 15px;
    ">
        LAND POSSESSION STATUS
    </div>

    <div style="margin: 10px 0;">
        <span style="
            display:inline-block;
            width:14px;
            height:14px;
            background:#168a16;
            margin-right:8px;
        "></span>
        Not in Possession
    </div>

    <div style="margin: 10px 0;">
        <span style="
            display:inline-block;
            width:14px;
            height:14px;
            background:#ff9f0a;
            margin-right:8px;
        "></span>
        Partially Possessed
    </div>

    <div style="margin: 10px 0;">
        <span style="
            display:inline-block;
            width:14px;
            height:14px;
            background:#ff1f1f;
            margin-right:8px;
        "></span>
        Fully Possessed
    </div>

    <hr>

    <div style="
        font-size: 13px;
        color: #777;
    ">
        Prototype parcel boundaries
    </div>

</div>
"""

m.get_root().html.add_child(
    folium.Element(legend_html)
)


# =========================================================
# PLOT COLORS
# =========================================================

def get_color(status):

    status = str(status).upper().strip()

    if status == "FULLY POSSESSED":
        return "#ff1f1f"

    elif status == "PARTIALLY POSSESSED":
        return "#ffb347"

    else:
        return "#6aaa5a"


# =========================================================
# CREATE 5 PARCELS
# =========================================================

base_lat = 19.255
base_lon = 73.020


plot_positions = [

    [(base_lat, base_lon),
     (base_lat + 0.002, base_lon + 0.001),
     (base_lat + 0.001, base_lon + 0.004),
     (base_lat - 0.001, base_lon + 0.004)],

    [(base_lat + 0.002, base_lon + 0.004),
     (base_lat + 0.004, base_lon + 0.0045),
     (base_lat + 0.004, base_lon + 0.0075),
     (base_lat + 0.002, base_lon + 0.007)],

    [(base_lat - 0.001, base_lon + 0.004),
     (base_lat + 0.001, base_lon + 0.004),
     (base_lat + 0.001, base_lon + 0.007),
     (base_lat - 0.001, base_lon + 0.007)],

    [(base_lat + 0.004, base_lon + 0.0005),
     (base_lat + 0.006, base_lon + 0.001),
     (base_lat + 0.006, base_lon + 0.004),
     (base_lat + 0.004, base_lon + 0.0045)],

    [(base_lat + 0.004, base_lon + 0.0075),
     (base_lat + 0.006, base_lon + 0.007),
     (base_lat + 0.006, base_lon + 0.0095),
     (base_lat + 0.003, base_lon + 0.0095)]
]


# =========================================================
# DRAW PARCELS
# =========================================================

for index, (_, row) in enumerate(
    project_df.iterrows()
):

    if index >= len(plot_positions):
        break


    plot_id = str(
        row["plot_id"]
    )

    parcel_id = str(
        row["parcel_id"]
    )

    possession_status = str(
        row["possession_status"]
    )


    possession_percent = row[
        "possession_percent"
    ]


    land_acquired = row[
        "land_acquired_percent"
    ]


    delay_days = row[
        "delay_days"
    ]


    delay_risk = str(
        row["delay_risk"]
    )


    compensation_status = str(
        row["compensation_status"]
    )


    color = get_color(
        possession_status
    )


    # -----------------------------------------------------
    # POPUP
    # -----------------------------------------------------

    popup_html = f"""
    <div style="
        width: 350px;
        font-family: Arial;
        line-height: 1.6;
    ">

        <h3 style="
            margin-top:0;
            color:#16325c;
        ">
            LAND PLOT DETAILS
        </h3>

        <hr>

        <b>Plot ID:</b>
        {plot_id}

        <br>

        <b>Parcel ID:</b>
        {parcel_id}

        <br>

        <b>Project ID:</b>
        {project_id}

        <br><br>

        <b>District:</b>
        {row["district"]}

        <br>

        <b>State:</b>
        {row["state"]}

        <br><br>

        <hr>

        <b>Possession:</b>
        {possession_percent}%

        <br>

        <b>Possession Status:</b>
        {possession_status}

        <br>

        <b>Land Acquired:</b>
        {land_acquired}%

        <br>

        <b>Delay:</b>
        {delay_days} days

        <br>

        <b>Delay Risk:</b>
        {delay_risk}

        <br>

        <b>Compensation:</b>
        {compensation_status}

        <br>

        <b>Legal Cases:</b>
        {row["legal_cases"]}

    </div>
    """


    popup = folium.Popup(
        popup_html,
        max_width=420
    )


    # -----------------------------------------------------
    # POLYGON
    # -----------------------------------------------------

    folium.Polygon(
        locations=plot_positions[index],
        color="white",
        weight=3,
        fill=True,
        fill_color=color,
        fill_opacity=0.75,
        popup=popup,
        tooltip=f"{plot_id} | {possession_status}"
    ).add_to(m)


    # -----------------------------------------------------
    # LABEL
    # -----------------------------------------------------

    center_point = [
        sum(
            point[0]
            for point in plot_positions[index]
        ) / len(plot_positions[index]),

        sum(
            point[1]
            for point in plot_positions[index]
        ) / len(plot_positions[index])
    ]


    folium.map.Marker(
        center_point,
        icon=DivIcon(
            html=f"""
            <div style="
                font-size: 13px;
                font-weight: 700;
                color: white;
                background: rgba(0,0,0,0.55);
                padding: 5px 8px;
                border-radius: 6px;
                text-align: center;
                white-space: nowrap;
            ">
                {plot_id}
            </div>
            """
        )
    ).add_to(m)


# =========================================================
# LAYER CONTROL
# =========================================================

folium.LayerControl().add_to(m)


# =========================================================
# SAVE MAP
# =========================================================

output_file = "land_plot_map.html"

m.save(output_file)


# =========================================================
# SUCCESS MESSAGE
# =========================================================

print()
print("=" * 50)
print("LAND PARCEL MAP CREATED SUCCESSFULLY")
print("=" * 50)

print(
    "Project:",
    project_id
)

print(
    "Plots shown:",
    len(project_df)
)

print(
    "Output:",
    output_file
)

print("=" * 50)