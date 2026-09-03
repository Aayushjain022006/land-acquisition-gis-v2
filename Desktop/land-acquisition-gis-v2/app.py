import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import joblib
from pathlib import Path


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
    }

    .main-header {
        font-size: 34px;
        font-weight: 800;
        color: #16325c;
        margin-bottom: 4px;
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

    .prediction-box {
        padding: 22px;
        border-radius: 14px;
        background: #f8fafc;
        border: 1px solid #e4e7ec;
    }

    .success-box {
        padding: 16px;
        border-radius: 12px;
        background: #ecfdf3;
        border: 1px solid #abefc6;
    }

    .warning-box {
        padding: 16px;
        border-radius: 12px;
        background: #fffaeb;
        border: 1px solid #fedf89;
    }

    .danger-box {
        padding: 16px;
        border-radius: 12px;
        background: #fef3f2;
        border: 1px solid #fecdca;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# FILE CHECK
# =========================================================

DATA_FILE = Path("final_data.csv")
MODEL_FILE = Path("model.pkl")
FEATURE_FILE = Path("model_features.pkl")


if not DATA_FILE.exists():

    st.error("final_data.csv not found.")

    st.stop()


# =========================================================
# LOAD DATA
# =========================================================

df = pd.read_csv(DATA_FILE)


# =========================================================
# LOAD MODEL
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
# HELPER: HTML FILE VIEWER
# =========================================================

def show_html(filename, height=650):

    path = Path(filename)

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
# BASIC KPI CALCULATIONS
# =========================================================

total_projects = (
    df["project_id"].nunique()
    if "project_id" in df.columns
    else len(df)
)


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


average_delay = pd.to_numeric(
    df["delay_days"],
    errors="coerce"
).mean()


average_possession = pd.to_numeric(
    df["possession_percent"],
    errors="coerce"
).mean()


total_plots = (
    len(df)
)


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
    # KPI ROW 1
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
    # QUICK ANALYTICS
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
        '<div class="main-header">Predict Land Acquisition Delay</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub-header">'
        'Use project-level factors to estimate expected delay.'
        '</div>',
        unsafe_allow_html=True
    )


    if model is None:

        st.error(
            "ML model is not available. Run model.py first."
        )

        st.stop()


    # -----------------------------------------------------
    # PROJECT SELECT
    # -----------------------------------------------------

    project_list = (
        df["project_id"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )


    selected_project = st.selectbox(
        "Select Project",
        project_list
    )


    # -----------------------------------------------------
    # SELECT RECORD
    # -----------------------------------------------------

    project_rows = df[
        df["project_id"].astype(str)
        == selected_project
    ]


    if len(project_rows) == 0:

        st.error(
            "No record found for selected project."
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

        st.write(
            row["project_id"]
        )


    with p2:

        st.write("**State**")

        st.write(
            row["state"]
        )


    with p3:

        st.write("**District**")

        st.write(
            row["district"]
        )


    with p4:

        st.write("**Current Risk**")

        st.write(
            row["delay_risk"]
        )


    st.divider()


    # -----------------------------------------------------
    # INPUT FEATURES
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
            value=float(row["land_acquired_percent"])
        )


        pending_approvals = st.number_input(
            "Pending Approvals",
            min_value=0.0,
            value=float(row["pending_approvals"])
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
            value=float(row["legal_cases"])
        )


        affected_families = st.number_input(
            "Affected Families",
            min_value=0.0,
            value=float(row["affected_families"])
        )


    with col2:

        rr_completed = st.number_input(
            "RR Completed (%)",
            min_value=0.0,
            max_value=100.0,
            value=float(row["rr_completed_percent"])
        )


        possession = st.number_input(
            "Possession (%)",
            min_value=0.0,
            max_value=100.0,
            value=float(row["possession_percent"])
        )


        planned_duration = st.number_input(
            "Planned Duration (months)",
            min_value=0.0,
            value=float(row["planned_duration_months"])
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
    # PREDICT
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


        # Ensure exact feature order
        if model_features is not None:

            input_data = input_data[
                model_features
            ]


        predicted_delay = float(
            model.predict(input_data)[0]
        )


        predicted_delay = max(
            0,
            predicted_delay
        )


        # -------------------------------------------------
        # RISK BAND
        # -------------------------------------------------

        if predicted_delay < 120:

            risk = "LOW"

        elif predicted_delay < 240:

            risk = "MEDIUM"

        else:

            risk = "HIGH"


        # -------------------------------------------------
        # RECOMMENDATION
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
                risk
            )


        with r3:

            st.metric(
                "Current Delay",
                f"{float(row['delay_days']):.1f} days"
            )


        # -------------------------------------------------
        # RISK MESSAGE
        # -------------------------------------------------

        if risk == "HIGH":

            st.error(
                "⚠️ HIGH RISK — Immediate intervention recommended."
            )

        elif risk == "MEDIUM":

            st.warning(
                "⚠️ MEDIUM RISK — Close monitoring recommended."
            )

        else:

            st.success(
                "✅ LOW RISK — Routine monitoring recommended."
            )


        # -------------------------------------------------
        # RECOMMENDATION
        # -------------------------------------------------

        st.markdown(
            '<div class="section-title">'
            'Recommended Actions'
            '</div>',
            unsafe_allow_html=True
        )


        for item in recommendations:

            st.write(
                f"• {item}"
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
        'Visualize project locations, risk areas and spatial patterns.'
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
        'Parcel-level possession monitoring.'
        '</div>',
        unsafe_allow_html=True
    )


    # Main parcel map
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
        'Identify high-risk districts, states and regions.'
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
        'Monitor delay trends across states and years.'
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
        '<div class="main-header">Compensation Analytics</div>',
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