import pandas as pd
import folium
from folium.plugins import Fullscreen


# =========================================================
# 1. LOAD DATASET
# =========================================================

df = pd.read_csv("final_data.csv")


# =========================================================
# 2. CREATE POSSESSION STATUS
# =========================================================

def get_possession_status(value):

    if value == 0:
        return "NOT IN POSSESSION"

    elif value < 100:
        return "PARTIALLY POSSESSED"

    else:
        return "FULLY POSSESSED"


df["possession_status"] = (
    df["possession_percent"]
    .apply(get_possession_status)
)


# =========================================================
# 3. TAKE ONE PROJECT FOR DETAILED PARCEL VIEW
# =========================================================

project_id = df["project_id"].iloc[0]

project_df = (
    df[df["project_id"] == project_id]
    .copy()
    .reset_index(drop=True)
)


# =========================================================
# 4. PROJECT INFORMATION
# =========================================================

project_name = project_df["project_name"].iloc[0]
district = project_df["district"].iloc[0]
state = project_df["state"].iloc[0]


# =========================================================
# 5. DEMO SITE CENTER
# =========================================================

# Approximate center only.
# It is NOT the actual project GPS location.

site_lat = 19.7515
site_lon = 75.7139


# =========================================================
# 6. CREATE LARGE PLOT LAYOUT
# =========================================================

plot_shapes = [

    [
        (0.0000, 0.0000),
        (0.0015, 0.0002),
        (0.0013, 0.0028),
        (0.0000, 0.0025)
    ],

    [
        (0.0017, 0.0002),
        (0.0032, 0.0000),
        (0.0031, 0.0027),
        (0.0015, 0.0028)
    ],

    [
        (0.0034, 0.0000),
        (0.0050, 0.0002),
        (0.0051, 0.0026),
        (0.0032, 0.0027)
    ],

    [
        (0.0001, 0.0027),
        (0.0016, 0.0029),
        (0.0014, 0.0056),
        (0.0000, 0.0054)
    ],

    [
        (0.0017, 0.0029),
        (0.0032, 0.0028),
        (0.0033, 0.0055),
        (0.0014, 0.0056)
    ],

    [
        (0.0034, 0.0028),
        (0.0051, 0.0027),
        (0.0050, 0.0054),
        (0.0033, 0.0055)
    ],

    [
        (0.0000, 0.0056),
        (0.0014, 0.0057),
        (0.0013, 0.0083),
        (0.0000, 0.0081)
    ],

    [
        (0.0015, 0.0057),
        (0.0033, 0.0056),
        (0.0032, 0.0082),
        (0.0013, 0.0083)
    ],

    [
        (0.0034, 0.0056),
        (0.0050, 0.0055),
        (0.0051, 0.0081),
        (0.0032, 0.0082)
    ],

    [
        (0.0000, 0.0083),
        (0.0013, 0.0084),
        (0.0015, 0.0110),
        (0.0000, 0.0108)
    ],

    [
        (0.0015, 0.0084),
        (0.0032, 0.0083),
        (0.0033, 0.0109),
        (0.0015, 0.0110)
    ],

    [
        (0.0034, 0.0083),
        (0.0051, 0.0082),
        (0.0050, 0.0108),
        (0.0033, 0.0109)
    ]
]


# =========================================================
# 7. CREATE SATELLITE MAP
# =========================================================

m = folium.Map(

    location=[
        site_lat,
        site_lon
    ],

    zoom_start=15,

    tiles=None

)


# =========================================================
# 8. SATELLITE LAYER
# =========================================================

folium.TileLayer(

    tiles=(
        "https://server.arcgisonline.com/"
        "ArcGIS/rest/services/World_Imagery/"
        "MapServer/tile/{z}/{y}/{x}"
    ),

    attr="Esri World Imagery",

    name="Satellite",

    overlay=False,

    control=True

).add_to(m)


# =========================================================
# 9. OPENSTREETMAP LAYER
# =========================================================

folium.TileLayer(

    "OpenStreetMap",

    name="Street Map",

    overlay=False,

    control=True

).add_to(m)


# =========================================================
# 10. ADD ROAD
# =========================================================

road = [

    [
        site_lat - 0.0008,
        site_lon - 0.0020
    ],

    [
        site_lat - 0.0008,
        site_lon + 0.0080
    ]

]


folium.PolyLine(

    road,

    color="white",

    weight=20,

    opacity=0.9

).add_to(m)


# =========================================================
# 11. ADD PLOTS
# =========================================================

for i, (_, row) in enumerate(
    project_df.iterrows()
):

    if i >= len(plot_shapes):
        break


    shape = plot_shapes[i]


    polygon_coordinates = [

        [
            site_lat + lat_offset,

            site_lon + lon_offset

        ]

        for lat_offset, lon_offset
        in shape

    ]


    status = row["possession_status"]


    # -----------------------------------------
    # COLOR BASED ON POSSESSION
    # -----------------------------------------

    if status == "NOT IN POSSESSION":

        fill_color = "green"


    elif status == "PARTIALLY POSSESSED":

        fill_color = "orange"


    else:

        fill_color = "red"


    # -----------------------------------------
    # POPUP INFORMATION
    # -----------------------------------------

    popup_html = f"""

    <div style="
        width:320px;
        font-family:Arial;
        font-size:14px;
    ">

        <h3 style="
            margin-bottom:10px;
        ">
            🏞️ LAND PLOT DETAILS
        </h3>

        <b>Plot ID:</b>
        {row["plot_id"]}

        <br>

        <b>Parcel ID:</b>
        {row["parcel_id"]}

        <br>

        <b>Project ID:</b>
        {row["project_id"]}

        <br>

        <b>Project:</b>
        {row["project_name"]}

        <br>

        <b>District:</b>
        {row["district"]}

        <br>

        <b>State:</b>
        {row["state"]}

        <hr>

        <b>Possession:</b>
        {row["possession_percent"]}%

        <br>

        <b>Status:</b>
        {status}

        <br>

        <b>Land Acquired:</b>
        {row["land_acquired_percent"]}%

        <br>

        <b>Delay Risk:</b>
        {row["delay_risk"]}

        <br>

        <b>Delay:</b>
        {row["delay_days"]} days

        <br>

        <b>Compensation:</b>
        {row["compensation_status"]}

        <br>

        <b>Rehabilitation:</b>
        {row["rehabilitation_status"]}

        <br>

        <b>Objections:</b>
        {row["objection_count"]}

    </div>

    """


    # -----------------------------------------
    # ADD POLYGON
    # -----------------------------------------

    folium.Polygon(

        locations=polygon_coordinates,

        color="white",

        weight=3,

        fill=True,

        fill_color=fill_color,

        fill_opacity=0.55,

        popup=folium.Popup(

            popup_html,

            max_width=350

        ),

        tooltip=(

            f"{row['plot_id']} | "

            f"{row['possession_percent']}% possession"

        )

    ).add_to(m)


    # -----------------------------------------
    # PLOT LABEL
    # -----------------------------------------

    center = polygon_coordinates[0]


    folium.Marker(

        location=center,

        icon=folium.DivIcon(

            html=f"""

            <div style="
                font-size:11px;
                font-weight:bold;
                color:white;
                text-shadow:
                    1px 1px 2px black;
                width:100px;
            ">

                {row["plot_id"]}

            </div>

            """

        )

    ).add_to(m)


# =========================================================
# 12. TITLE OVERLAY
# =========================================================

title_html = f"""

<div style="
    position: fixed;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 9999;

    background: rgba(255,255,255,0.95);

    padding: 12px 22px;

    border-radius: 10px;

    box-shadow:
        0 2px 10px rgba(0,0,0,0.25);

    font-family: Arial;

    text-align: center;

">

    <div style="
        font-size:20px;
        font-weight:bold;
    ">

        LAND PARCEL STATUS VIEWER

    </div>

    <div style="
        font-size:12px;
        margin-top:4px;
    ">

        {project_name}

        <br>

        {district}, {state}

    </div>

</div>

"""

m.get_root().html.add_child(

    folium.Element(title_html)

)


# =========================================================
# 13. LEGEND
# =========================================================

legend_html = """

<div style="
    position:fixed;

    bottom:25px;

    left:25px;

    width:230px;

    background:white;

    z-index:9999;

    padding:15px;

    border-radius:10px;

    box-shadow:
        0 2px 10px rgba(0,0,0,0.3);

    font-family:Arial;

">

    <b>LAND POSSESSION STATUS</b>

    <br><br>

    <span style="color:green;font-size:22px;">
        ■
    </span>

    Not in Possession

    <br>

    <span style="color:orange;font-size:22px;">
        ■
    </span>

    Partially Possessed

    <br>

    <span style="color:red;font-size:22px;">
        ■
    </span>

    Fully Possessed

    <br><br>

    <span style="
        color:#555;
        font-size:11px;
    ">

        Prototype parcel layout

    </span>

</div>

"""

m.get_root().html.add_child(

    folium.Element(legend_html)

)


# =========================================================
# 14. FULLSCREEN CONTROL
# =========================================================

Fullscreen().add_to(m)


# =========================================================
# 15. LAYER CONTROL
# =========================================================

folium.LayerControl().add_to(m)


# =========================================================
# 16. SAVE
# =========================================================

m.save(

    "plot_status_map.html"

)


# =========================================================
# 17. SUCCESS MESSAGE
# =========================================================

print("======================================")

print(
    "PROFESSIONAL PLOT MAP CREATED"
)

print("======================================")

print(
    "Project:",
    project_id
)

print(
    "District:",
    district
)

print(
    "Plots displayed:",
    min(
        len(project_df),
        len(plot_shapes)
    )
)

print(
    "Output:",
    "plot_status_map.html"
)

print("======================================")