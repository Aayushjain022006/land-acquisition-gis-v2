import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import joblib
from pathlib import Path


# =========================================================
# BASE DIRECTORY
# =========================================================

BASE_DIR = Path(__file__).resolve().parent


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="LandGuard AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .block-container {
        padding-top: 1.2rem;
        padding-left: 2rem;
        padding-right: 2rem;
        padding-bottom: 2rem;
    }

    .main-header {
        font-size: 34px;
        font-weight: 800;
        color: #16325c;
        margin-bottom: 5px;
    }

    .sub-header {
        color: #667085;
        font-size: 15px;
        margin-bottom: 20px;
    }

    .section-title {
        font-size: 22px;
        font-weight: 700;
        color: #16325c;
        margin-top: 20px;
        margin-bottom: 12px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# FILE PATHS
# =========================================================

DATA_FILE = BASE_DIR / "final_data.csv"
MODEL_FILE = BASE_DIR / "model.pkl"
FEATURE_FILE = BASE_DIR / "model_features.pkl"


# =========================================================
# CHECK DATASET
# =========================================================

if not DATA_FILE.exists():

    st.error(
        "final_data.csv not found in the application folder."
    )

    st.stop()


# =========================================================
# LOAD DATASET
# =========================================================

try:

    df = pd.read_csv(DATA_FILE)

except Exception as e:

    st.error(
        f"Unable to load final_data.csv: {e}"
    )

    st.stop()


# =========================================================
# LOAD ML MODEL
# =========================================================

model = None
model_features = None


if MODEL_FILE.exists():

    try:

        model = joblib.load(MODEL_FILE)

    except Exception as e:

        st.warning(
            f"Could not load model.pkl: {e}"
        )


if FEATURE_FILE.exists():

    try:

        model_features = joblib.load(
            FEATURE_FILE
        )

    except Exception:

        model_features = None


# =========================================================
# FUNCTION TO DISPLAY HTML MAP / CHART
# =========================================================

def show_html(filename, height=650):

    path = BASE_DIR / filename


    if not path.exists():

        st.warning(
            f"{filename} not found."
        )

        return


    try:

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            html = file.read()


        components.html(
            html,
            height=height,
            scrolling=False
        )


    except Exception as e:

        st.error(
            f"Unable to display {filename}: {e}"
        )


# =========================================================
# KPI CALCULATIONS
# =========================================================

if "project_id" in df.columns:

    total_projects = df["project_id"].nunique()

else:

    total_projects = len(df)


if "delay_risk" in df.columns:

    high_risk = (
        df["delay_risk"]
        .astype(str)
        .str.upper()
        .eq("HIGH")
        .sum()
    )


    medium_risk = (
        df["delay_risk"]
        .astype(str)
        .str.upper()
        .eq("MEDIUM")
        .sum()
    )


    low_risk = (
        df["delay_risk"]
        .astype(str)
        .str.upper()
        .eq("LOW")
        .sum()
    )

else:

    high_risk = 0
    medium_risk = 0
    low_risk = 0


average_delay = pd.to_numeric(
    df["delay_days"],
    errors="coerce"
).mean()


average_possession = pd.to_numeric(
    df["possession_percent"],
    errors="coerce"
).mean()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        "## 🛡️ LandGuard AI"
    )

    st.caption(
        "Predictive Land Acquisition Analytics"
    )

    st.divider()


    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Predict Delay",
            "GIS Risk Map",
            "Plot Status",
            "Risk Analytics",
            "Delay Analytics",
            "Compensation"
        ]
    )


    st.divider()


    st.markdown(
        """
        **AI Decision Support**

        Proactive monitoring of land
        acquisition, possession and delay risk.

        **GIS • Analytics • ML Prediction**
        """
    )


# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    st.markdown(
        '<div class="main-header">LandGuard AI</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="sub-header">'
        'Predictive Land Acquisition Monitoring & GIS Analytics'
        '</div>',
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # KPI CARDS
    # -----------------------------------------------------

    c1, c2, c3, c4, c5 = st.columns(5)


    with c1:

        st.metric(
            "Total Projects",
            f"{total_projects:,}"
        )


    with c2:

        st.metric(
            "High Risk",
            f"{high_risk:,}"
        )


    with c3:

        st.metric(
            "Medium Risk",
            f"{medium_risk:,}"
        )


    with c4:

        st.metric(
            "Average Delay",
            f"{average_delay:.1f} days"
        )


    with c5:

        st.metric(
            "Average Possession",
            f"{average_possession:.1f}%"
        )


    # -----------------------------------------------------
    # GIS MAP
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        'GIS Risk & Land Parcel Map'
        '</div>',
        unsafe_allow_html=True
    )


    show_html(
        "land_plot_map.html",
        height=700
    )


    # -----------------------------------------------------
    # ANALYTICS
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        'Key Analytics'
        '</div>',
        unsafe_allow_html=True
    )


    tab1, tab2, tab3 = st.tabs(
        [
            "Risk Distribution",
            "Projects by State",
            "Average Delay by State"
        ]
    )


    with tab1:

        show_html(
            "risk_distribution.html",
            height=600
        )


    with tab2:

        show_html(
            "projects_by_state.html",
            height=600
        )


    with tab3:

        show_html(
            "average_delay_by_state.html",
            height=600
        )


# =========================================================
# PREDICT DELAY
# =========================================================

elif page == "Predict Delay":

    st.markdown(
        '<div class="main-header">'
        'Predict Land Acquisition Delay'
        '</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="sub-header">'
        'Estimate expected project delay using the trained ML model.'
        '</div>',
        unsafe_allow_html=True
    )


    if model is None:

        st.error(
            "ML model not available. Please make sure model.pkl is present."
        )

        st.stop()


    # -----------------------------------------------------
    # PROJECT LIST
    # -----------------------------------------------------

    project_list = (
        df["project_id"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )


    if not project_list:

        st.error(
            "No project records available."
        )

        st.stop()


    selected_project = st.selectbox(
        "Select Project",
        project_list
    )


    # -----------------------------------------------------
    # GET SELECTED RECORD
    # -----------------------------------------------------

    project_rows = df[
        df["project_id"].astype(str)
        == selected_project
    ]


    if project_rows.empty:

        st.error(
            "Selected project record not found."
        )

        st.stop()


    row = project_rows.iloc[0]


    # -----------------------------------------------------
    # PROJECT INFORMATION
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        'Project Information'
        '</div>',
        unsafe_allow_html=True
    )


    p1, p2, p3, p4 = st.columns(4)


    with p1:

        st.write("**Project ID**")
        st.write(row["project_id"])


    with p2:

        st.write("**State**")
        st.write(row["state"])


    with p3:

        st.write("**District**")
        st.write(row["district"])


    with p4:

        st.write("**Current Risk**")
        st.write(row["delay_risk"])


    st.divider()


    # -----------------------------------------------------
    # PREDICTION INPUTS
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        'Prediction Inputs'
        '</div>',
        unsafe_allow_html=True
    )


    col1, col2 = st.columns(2)


    with col1:

        land_acquired = st.number_input(
            "Land Acquired (%)",
            min_value=0.0,
            max_value=100.0,
            value=float(
                row["land_acquired_percent"]
            )
        )


        pending_approvals = st.number_input(
            "Pending Approvals",
            min_value=0.0,
            value=float(
                row["pending_approvals"]
            )
        )


        compensation_pending = st.number_input(
            "Compensation Pending (%)",
            min_value=0.0,
            max_value=100.0,
            value=float(
                row["compensation_pending_percent"]
            )
        )


        legal_cases = st.number_input(
            "Legal Cases",
            min_value=0.0,
            value=float(
                row["legal_cases"]
            )
        )


        affected_families = st.number_input(
            "Affected Families",
            min_value=0.0,
            value=float(
                row["affected_families"]
            )
        )


    with col2:

        rr_completed = st.number_input(
            "RR Completed (%)",
            min_value=0.0,
            max_value=100.0,
            value=float(
                row["rr_completed_percent"]
            )
        )


        possession = st.number_input(
            "Possession (%)",
            min_value=0.0,
            max_value=100.0,
            value=float(
                row["possession_percent"]
            )
        )


        planned_duration = st.number_input(
            "Planned Duration (months)",
            min_value=0.0,
            value=float(
                row["planned_duration_months"]
            )
        )


        environmental = st.selectbox(
            "Environmental Clearance",
            ["Yes", "No"],
            index=(
                0
                if str(
                    row["environmental_clearance"]
                ).strip().lower() == "yes"
                else 1
            )
        )


        forest = st.selectbox(
            "Forest Clearance",
            ["Yes", "No"],
            index=(
                0
                if str(
                    row["forest_clearance"]
                ).strip().lower() == "yes"
                else 1
            )
        )


    # -----------------------------------------------------
    # PREDICT BUTTON
    # -----------------------------------------------------

    if st.button(
        "🔮 Predict Delay",
        type="primary",
        use_container_width=True
    ):


        input_data = pd.DataFrame(
            [{
                "land_acquired_percent":
                    land_acquired,

                "pending_approvals":
                    pending_approvals,

                "compensation_pending_percent":
                    compensation_pending,

                "legal_cases":
                    legal_cases,

                "affected_families":
                    affected_families,

                "rr_completed_percent":
                    rr_completed,

                "possession_percent":
                    possession,

                "planned_duration_months":
                    planned_duration,

                "environmental_clearance":
                    1 if environmental == "Yes"
                    else 0,

                "forest_clearance":
                    1 if forest == "Yes"
                    else 0
            }]
        )


        # -------------------------------------------------
        # MATCH MODEL FEATURE ORDER
        # -------------------------------------------------

        if model_features is not None:

            input_data = input_data[
                model_features
            ]


        # -------------------------------------------------
        # PREDICT DELAY
        # -------------------------------------------------

        predicted_delay = float(
            model.predict(input_data)[0]
        )


        predicted_delay = max(
            0,
            predicted_delay
        )


        # -------------------------------------------------
        # RISK LEVEL
        # -------------------------------------------------

        if predicted_delay < 120:

            predicted_risk = "LOW"

        elif predicted_delay < 240:

            predicted_risk = "MEDIUM"

        else:

            predicted_risk = "HIGH"


        # -------------------------------------------------
        # RECOMMENDATIONS
        # -------------------------------------------------

        recommendations = []


        if possession < 50:

            recommendations.append(
                "Prioritize land possession."
            )


        if compensation_pending > 50:

            recommendations.append(
                "Accelerate compensation processing."
            )


        if legal_cases > 0:

            recommendations.append(
                "Review pending legal cases."
            )


        if pending_approvals > 0:

            recommendations.append(
                "Expedite pending approvals."
            )


        if environmental == "No":

            recommendations.append(
                "Resolve environmental clearance."
            )


        if forest == "No":

            recommendations.append(
                "Resolve forest clearance."
            )


        if not recommendations:

            recommendations.append(
                "Continue routine monitoring."
            )


        # -------------------------------------------------
        # RESULT
        # -------------------------------------------------

        st.markdown(
            '<div class="section-title">'
            'Prediction Result'
            '</div>',
            unsafe_allow_html=True
        )


        r1, r2, r3 = st.columns(3)


        with r1:

            st.metric(
                "Predicted Delay",
                f"{predicted_delay:.1f} days"
            )


        with r2:

            st.metric(
                "Predicted Risk",
                predicted_risk
            )


        with r3:

            current_delay = pd.to_numeric(
                row["delay_days"],
                errors="coerce"
            )

            st.metric(
                "Current Delay",
                f"{current_delay:.1f} days"
            )


        # -------------------------------------------------
        # RISK MESSAGE
        # -------------------------------------------------

        if predicted_risk == "HIGH":

            st.error(
                "⚠️ HIGH RISK — Immediate intervention recommended."
            )

        elif predicted_risk == "MEDIUM":

            st.warning(
                "⚠️ MEDIUM RISK — Close monitoring recommended."
            )

        else:

            st.success(
                "✅ LOW RISK — Routine monitoring recommended."
            )


        # -------------------------------------------------
        # RECOMMENDATIONS
        # -------------------------------------------------

        st.markdown(
            '<div class="section-title">'
            'Recommended Actions'
            '</div>',
            unsafe_allow_html=True
        )


        for recommendation in recommendations:

            st.write(
                f"• {recommendation}"
            )


# =========================================================
# GIS RISK MAP
# =========================================================

elif page == "GIS Risk Map":

    st.markdown(
        '<div class="main-header">GIS Risk Map</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="sub-header">'
        'Visualize project locations and regional risk.'
        '</div>',
        unsafe_allow_html=True
    )


    show_html(
        "land_acquisition_map.html",
        height=750
    )


    st.markdown(
        '<div class="section-title">'
        'Risk Heatmap'
        '</div>',
        unsafe_allow_html=True
    )


    show_html(
        "risk_heatmap.html",
        height=750
    )


# =========================================================
# PLOT STATUS
# =========================================================

elif page == "Plot Status":

    st.markdown(
        '<div class="main-header">Land Plot Status</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="sub-header">'
        'Parcel-level land possession monitoring.'
        '</div>',
        unsafe_allow_html=True
    )


    show_html(
        "land_plot_map.html",
        height=750
    )


    st.markdown(
        '<div class="section-title">'
        'Plot Status Map'
        '</div>',
        unsafe_allow_html=True
    )


    show_html(
        "plot_status_map.html",
        height=650
    )


# =========================================================
# RISK ANALYTICS
# =========================================================

elif page == "Risk Analytics":

    st.markdown(
        '<div class="main-header">Risk Analytics</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="sub-header">'
        'Identify high-risk districts and regional patterns.'
        '</div>',
        unsafe_allow_html=True
    )


    tab1, tab2, tab3 = st.tabs(
        [
            "Risk Heatmap",
            "High Risk Districts",
            "Risk Distribution"
        ]
    )


    with tab1:

        show_html(
            "risk_heatmap.html",
            height=700
        )


    with tab2:

        show_html(
            "high_risk_by_district.html",
            height=700
        )


    with tab3:

        show_html(
            "risk_distribution.html",
            height=650
        )


# =========================================================
# DELAY ANALYTICS
# =========================================================

elif page == "Delay Analytics":

    st.markdown(
        '<div class="main-header">Delay Analytics</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="sub-header">'
        'Monitor acquisition delay trends across states and years.'
        '</div>',
        unsafe_allow_html=True
    )


    tab1, tab2 = st.tabs(
        [
            "Average Delay by State",
            "Average Delay by Year"
        ]
    )


    with tab1:

        show_html(
            "average_delay_by_state.html",
            height=700
        )


    with tab2:

        show_html(
            "average_delay_by_year.html",
            height=700
        )


# =========================================================
# COMPENSATION
# =========================================================

elif page == "Compensation":

    st.markdown(
        '<div class="main-header">'
        'Compensation Analytics'
        '</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="sub-header">'
        'Monitor compensation and rehabilitation progress.'
        '</div>',
        unsafe_allow_html=True
    )


    show_html(
        "compensation_status.html",
        height=700
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()


st.caption(
    "LandGuard AI • GIS • Analytics • Machine Learning • SIH Prototype"
)