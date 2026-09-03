import pandas as pd
import folium


# =========================================================
# 1. LOAD DEMO DATASET
# =========================================================

df = pd.read_csv("plot_demo_data.csv")


# =========================================================
# 2. CREATE POSSESSION STATUS
# =========================================================

def get_status(percent):

    if percent == 0:
        return "NOT IN POSSESSION"

    elif percent < 100:
        return "PARTIALLY POSSESSED"

    else:
        return "FULLY POSSESSED"


df["possession_status"] = (
    df["possession_percent"]
    .apply(get_status)
)


# =========================================================
# 3. SELECT 5 DEMO PLOTS
# =========================================================

project_df = (
    df.head(5)
    .reset_index(drop=True)
)


# =========================================================
# 4. PROJECT INFORMATION
# =========================================================

project_id = project_df["project_id"].iloc[0]

project_name = project_df["project_name"].iloc[0]

district = project_df["district"].iloc[0]

state = project_df["state"].iloc[0]


# =========================================================
# 5. APPROXIMATE LOCATION
# =========================================================

PROJECT_LOCATION = {

    "Maharashtra": [19.7515, 75.7139],

    "Gujarat": [22.2587, 71.1924],

    "Madhya Pradesh": [22.9734, 78.6569],

    "Rajasthan": [27.0238, 74.2179],

    "Delhi": [28.6139, 77.2090],

    "Punjab": [31.1471, 75.3412],

    "Haryana": [29.0588, 76.0856],

    "Uttar Pradesh": [26.8467, 80.9462],

    "Bihar": [25.0961, 85.3131],

    "Jharkhand": [23.6102, 85.2799],

    "West Bengal": [22.9868, 87.8550],

    "Odisha": [20.9517, 85.0985],

    "Chhattisgarh": [21.2787, 81.8661],

    "Telangana": [18.1124, 79.0193],

    "Andhra Pradesh": [15.9129, 79.7400],

    "Karnataka": [15.3173, 75.7139],

    "Tamil Nadu": [11.1271, 78.6569],

    "Kerala": [10.8505, 76.2711],

    "Assam": [26.2006, 92.9376],

    "Himachal Pradesh": [31.1048, 77.1734],

    "Uttarakhand": [30.0668, 79.0193],

    "Jammu and Kashmir": [33.7782, 76.5762]
}


base_lat, base_lon = PROJECT_LOCATION.get(
    state,
    [22.5, 79.0]
)


# =========================================================
# 6. CREATE MAP
# =========================================================

m = folium.Map(

    location=[
        base_lat,
        base_lon
    ],

    zoom_start=17,

    tiles=None

)


# =========================================================
# 7. SATELLITE MAP
# =========================================================

folium.TileLayer(

    tiles=(
        "https://server.arcgisonline.com/"
        "ArcGIS/rest/services/World_Imagery/"
        "MapServer/tile/{z}/{y}/{x}"
    ),

    attr="Esri World Imagery",

    name="Satellite",

    overlay=False

).add_to(m)


# =========================================================
# 8. STREET MAP
# =========================================================

folium.TileLayer(

    "OpenStreetMap",

    name="Street Map",

    overlay=False

).add_to(m)


# =========================================================
# 9. CONNECTED LAND PARCEL SHAPES
# =========================================================

plot_shapes = [

    # PLOT 1
    [
        (0.0000, 0.0000),
        (0.0017, 0.0002),
        (0.0015, 0.0022),
        (0.0001, 0.0025),
        (-0.0002, 0.0012)
    ],

    # PLOT 2
    [
        (0.0017, 0.0002),
        (0.0035, 0.0000),
        (0.0037, 0.0013),
        (0.0034, 0.0024),
        (0.0015, 0.0022)
    ],

    # PLOT 3
    [
        (-0.0002, 0.0012),
        (0.0001, 0.0025),
        (0.0015, 0.0022),
        (0.0016, 0.0044),
        (0.0001, 0.0047),
        (-0.0004, 0.0030)
    ],

    # PLOT 4
    [
        (0.0015, 0.0022),
        (0.0034, 0.0024),
        (0.0036, 0.0044),
        (0.0016, 0.0044)
    ],

    # PLOT 5
    [
        (0.0001, 0.0047),
        (0.0016, 0.0044),
        (0.0036, 0.0044),
        (0.0033, 0.0062),
        (0.0015, 0.0067),
        (0.0000, 0.0062)
    ]

]


# =========================================================
# 10. ADD ROAD
# =========================================================

road_coordinates = [

    [
        base_lat - 0.0018,
        base_lon - 0.0030
    ],

    [
        base_lat - 0.0014,
        base_lon + 0.0080
    ]

]


folium.PolyLine(

    road_coordinates,

    color="white",

    weight=18,

    opacity=0.95

).add_to(m)


# =========================================================
# 11. ADD PLOTS
# =========================================================

for i, (_, row) in enumerate(
    project_df.iterrows()
):

    shape = plot_shapes[i]


    # -----------------------------------------------------
    # Convert local coordinates to map coordinates
    # -----------------------------------------------------

    polygon = [

        [
            base_lat + lat,
            base_lon + lon
        ]

        for lat, lon in shape

    ]


    # -----------------------------------------------------
    # Get possession status
    # -----------------------------------------------------

    status = row["possession_status"]


    # -----------------------------------------------------
    # Set color
    # -----------------------------------------------------

    if status == "NOT IN POSSESSION":

        color = "green"

    elif status == "PARTIALLY POSSESSED":

        color = "orange"

    else:

        color = "red"


    # -----------------------------------------------------
    # Popup
    # -----------------------------------------------------

    popup_html = f"""

    <div style="
        width:360px;
        font-family:Arial;
    ">

        <h2 style="
            margin-top:0;
            color:#222;
        ">

            LAND PLOT DETAILS

        </h2>


        <p>

            <b>Plot ID:</b>
            {row["plot_id"]}

        </p>


        <p>

            <b>Parcel ID:</b>
            {row["parcel_id"]}

        </p>


        <p>

            <b>Project ID:</b>
            {row["project_id"]}

        </p>


        <p>

            <b>Project:</b>
            {row["project_name"]}

        </p>


        <p>

            <b>District:</b>
            {row["district"]}

        </p>


        <p>

            <b>State:</b>
            {row["state"]}

        </p>


        <hr>


        <p>

            <b>Possession:</b>
            {row["possession_percent"]}%

        </p>


        <p>

            <b>Possession Status:</b>
            {status}

        </p>


        <p>

            <b>Land Acquired:</b>
            {row["land_acquired_percent"]}%

        </p>


        <p>

            <b>Delay Risk:</b>
            {row["delay_risk"]}

        </p>


        <p>

            <b>Delay:</b>
            {row["delay_days"]} days

        </p>


        <p>

            <b>Compensation:</b>
            {row["compensation_status"]}

        </p>


        <p>

            <b>Rehabilitation:</b>
            {row["rehabilitation_status"]}

        </p>


        <p>

            <b>Objections:</b>
            {row["objection_count"]}

        </p>

    </div>

    """


    # -----------------------------------------------------
    # Add polygon
    # -----------------------------------------------------

    folium.Polygon(

        locations=polygon,

        color="white",

        weight=3,

        fill=True,

        fill_color=color,

        fill_opacity=0.65,

        popup=folium.Popup(

            popup_html,

            max_width=390

        ),

        tooltip=(

            f"{row['plot_id']} | "
            f"{row['possession_percent']}%"

        )

    ).add_to(m)


    # -----------------------------------------------------
    # Find center
    # -----------------------------------------------------

    center_lat = (

        base_lat

        + sum(
            point[0]
            for point in shape
        ) / len(shape)

    )


    center_lon = (

        base_lon

        + sum(
            point[1]
            for point in shape
        ) / len(shape)

    )


    # -----------------------------------------------------
    # Plot ID
    # -----------------------------------------------------

    folium.Marker(

        location=[

            center_lat,
            center_lon

        ],

        icon=folium.DivIcon(

            html=f"""

            <div style="

                font-size:11px;

                font-weight:bold;

                color:white;

                background:rgba(0,0,0,0.60);

                padding:4px 7px;

                border-radius:5px;

                white-space:nowrap;

                text-align:center;

            ">

                {row["plot_id"]}

            </div>

            """

        )

    ).add_to(m)


# =========================================================
# 12. TITLE
# =========================================================

title_html = f"""

<div style="

    position:fixed;

    top:20px;

    left:50%;

    transform:translateX(-50%);

    z-index:9999;

    background:white;

    padding:15px 30px;

    border-radius:12px;

    box-shadow:
        0 4px 16px rgba(0,0,0,0.30);

    font-family:Arial;

    text-align:center;

    min-width:460px;

">


    <div style="

        font-size:22px;

        font-weight:bold;

    ">

        LAND PARCEL STATUS VIEWER

    </div>


    <div style="

        font-size:13px;

        margin-top:6px;

        color:#444;

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

    z-index:9999;

    background:white;

    padding:17px;

    width:250px;

    border-radius:12px;

    box-shadow:
        0 4px 16px rgba(0,0,0,0.30);

    font-family:Arial;

">


    <div style="

        font-size:16px;

        font-weight:bold;

        margin-bottom:12px;

    ">

        LAND POSSESSION STATUS

    </div>


    <div style="margin-bottom:6px;">

        <span style="
            color:green;
            font-size:22px;
        ">■</span>

        Not in Possession

    </div>


    <div style="margin-bottom:6px;">

        <span style="
            color:orange;
            font-size:22px;
        ">■</span>

        Partially Possessed

    </div>


    <div style="margin-bottom:6px;">

        <span style="
            color:red;
            font-size:22px;
        ">■</span>

        Fully Possessed

    </div>


    <hr>


    <div style="
        font-size:11px;
        color:#666;
    ">

        Prototype parcel boundaries

    </div>

</div>

"""


m.get_root().html.add_child(

    folium.Element(legend_html)

)


# =========================================================
# 14. LAYER CONTROL
# =========================================================

folium.LayerControl().add_to(m)


# =========================================================
# 15. SAVE MAP
# =========================================================

m.save(

    "land_plot_map.html"

)


# =========================================================
# 16. SUCCESS MESSAGE
# =========================================================

print("==========================================")

print(
    "5-PLOT DEMO MAP CREATED SUCCESSFULLY"
)

print("==========================================")

print(
    "Project:",
    project_id
)

print(
    "Plots shown:",
    len(project_df)
)

print(
    "Possession values:",
    project_df["possession_percent"].tolist()
)

print(
    "Output:",
    "land_plot_map.html"
)

print("==========================================")