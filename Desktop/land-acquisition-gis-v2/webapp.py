from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    send_from_directory
)

from pathlib import Path
import pandas as pd
import joblib


# =========================================================
# PATH SETUP
# =========================================================

BASE_DIR = Path(__file__).resolve().parent


# =========================================================
# FLASK APP
# =========================================================

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates"),
    static_folder=str(BASE_DIR / "static")
)


# =========================================================
# FILE PATHS
# =========================================================

DATA_FILE = BASE_DIR / "final_data.csv"
MODEL_FILE = BASE_DIR / "model.pkl"
FEATURE_FILE = BASE_DIR / "model_features.pkl"


# =========================================================
# LOAD DATASET
# =========================================================

try:

    df = pd.read_csv(DATA_FILE)

    print(
        f"Dataset loaded successfully: {len(df)} rows"
    )

except Exception as error:

    print(
        "Dataset loading error:",
        error
    )

    df = pd.DataFrame()


# =========================================================
# LOAD MACHINE LEARNING MODEL
# =========================================================

model = None
model_features = None


if MODEL_FILE.exists():

    try:

        model = joblib.load(
            MODEL_FILE
        )

        print(
            "ML model loaded successfully."
        )

    except Exception as error:

        print(
            "Model loading error:",
            error
        )


if FEATURE_FILE.exists():

    try:

        model_features = joblib.load(
            FEATURE_FILE
        )

        print(
            "Model features loaded successfully."
        )

    except Exception as error:

        print(
            "Feature loading error:",
            error
        )


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def safe_number(value, default=0.0):

    try:

        if pd.isna(value):
            return default

        return float(value)

    except Exception:

        return default


def risk_class(risk):

    value = str(
        risk
    ).strip().upper()


    if value == "HIGH":

        return "risk-high"


    if value == "MEDIUM":

        return "risk-medium"


    return "risk-low"


# =========================================================
# KPI CALCULATIONS
# =========================================================

if not df.empty:

    total_records = len(df)


    if "project_id" in df.columns:

        total_projects = (
            df["project_id"]
            .dropna()
            .astype(str)
            .nunique()
        )

    else:

        total_projects = total_records


    if "delay_risk" in df.columns:

        high_risk = (
            df["delay_risk"]
            .astype(str)
            .str.strip()
            .str.upper()
            .eq("HIGH")
            .sum()
        )


        medium_risk = (
            df["delay_risk"]
            .astype(str)
            .str.strip()
            .str.upper()
            .eq("MEDIUM")
            .sum()
        )


        low_risk = (
            df["delay_risk"]
            .astype(str)
            .str.strip()
            .str.upper()
            .eq("LOW")
            .sum()
        )

    else:

        high_risk = 0
        medium_risk = 0
        low_risk = 0


    average_delay = pd.to_numeric(

        df.get(
            "delay_days",
            pd.Series(dtype=float)
        ),

        errors="coerce"

    ).mean()


    average_possession = pd.to_numeric(

        df.get(
            "possession_percent",
            pd.Series(dtype=float)
        ),

        errors="coerce"

    ).mean()

else:

    total_records = 0
    total_projects = 0

    high_risk = 0
    medium_risk = 0
    low_risk = 0

    average_delay = 0
    average_possession = 0


if pd.isna(average_delay):
    average_delay = 0


if pd.isna(average_possession):
    average_possession = 0


# =========================================================
# RISK PERCENTAGES
# =========================================================

if total_records > 0:

    high_percent = round(
        (high_risk / total_records) * 100,
        1
    )

    medium_percent = round(
        (medium_risk / total_records) * 100,
        1
    )

    low_percent = round(
        (low_risk / total_records) * 100,
        1
    )

else:

    high_percent = 0
    medium_percent = 0
    low_percent = 0


# =========================================================
# PROJECT TABLE
# =========================================================

project_table = []


if not df.empty:

    for _, row in df.head(250).iterrows():

        project_table.append({

            "project_id":
                str(
                    row.get(
                        "project_id",
                        "-"
                    )
                ),

            "project_name":
                str(
                    row.get(
                        "project_name",
                        "-"
                    )
                ),

            "state":
                str(
                    row.get(
                        "state",
                        "-"
                    )
                ),

            "district":
                str(
                    row.get(
                        "district",
                        "-"
                    )
                ),

            "delay_risk":
                str(
                    row.get(
                        "delay_risk",
                        "LOW"
                    )
                ),

            "risk_class":
                risk_class(
                    row.get(
                        "delay_risk",
                        "LOW"
                    )
                ),

            "delay_days":
                round(
                    safe_number(
                        row.get(
                            "delay_days",
                            0
                        )
                    ),
                    1
                ),

            "possession_percent":
                round(
                    safe_number(
                        row.get(
                            "possession_percent",
                            0
                        )
                    ),
                    1
                )

        })


# =========================================================
# PROJECTS NEEDING ATTENTION
# =========================================================

attention_projects = []


if (
    not df.empty
    and "delay_days" in df.columns
):

    attention_df = df.copy()


    attention_df["delay_numeric"] = pd.to_numeric(

        attention_df["delay_days"],

        errors="coerce"

    )


    attention_df = (

        attention_df
        .sort_values(
            "delay_numeric",
            ascending=False,
            na_position="last"
        )
        .head(8)

    )


    for _, row in attention_df.iterrows():

        attention_projects.append({

            "project_id":
                str(
                    row.get(
                        "project_id",
                        "-"
                    )
                ),

            "district":
                str(
                    row.get(
                        "district",
                        "-"
                    )
                ),

            "delay_risk":
                str(
                    row.get(
                        "delay_risk",
                        "LOW"
                    )
                ),

            "risk_class":
                risk_class(
                    row.get(
                        "delay_risk",
                        "LOW"
                    )
                ),

            "delay_days":
                round(
                    safe_number(
                        row.get(
                            "delay_days",
                            0
                        )
                    ),
                    1
                )

        })


# =========================================================
# PROJECT IDs
# =========================================================

if (
    not df.empty
    and "project_id" in df.columns
):

    projects = sorted(

        df["project_id"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()

    )

else:

    projects = []


# =========================================================
# DASHBOARD ROUTE
# =========================================================

@app.route("/")
def dashboard():

    return render_template(

        "dashboard.html",

        total_projects=total_projects,

        high_risk=high_risk,

        medium_risk=medium_risk,

        low_risk=low_risk,

        total_records=total_records,

        average_delay=average_delay,

        average_possession=average_possession,

        high_percent=high_percent,

        medium_percent=medium_percent,

        low_percent=low_percent,

        project_table=project_table,

        attention_projects=attention_projects,

        projects=projects

    )


# =========================================================
# SERVE EXISTING MAPS / CHARTS
# =========================================================

@app.route(
    "/files/<path:filename>"
)
def serve_files(filename):

    return send_from_directory(

        str(BASE_DIR),

        filename

    )


# =========================================================
# AI PREDICTION API
# =========================================================

@app.route(
    "/api/predict",
    methods=["POST"]
)
def predict():

    if model is None:

        return jsonify({

            "error":
                "model.pkl could not be loaded."

        }), 500


    if df.empty:

        return jsonify({

            "error":
                "final_data.csv could not be loaded."

        }), 500


    try:

        data = request.get_json(
            silent=True
        )


        if not data:

            return jsonify({

                "error":
                    "No prediction data received."

            }), 400


        project_id = str(

            data.get(
                "project_id",
                ""
            )

        )


        if not project_id:

            return jsonify({

                "error":
                    "Project ID is required."

            }), 400


        project_rows = df[

            df["project_id"]
            .astype(str)
            .eq(project_id)

        ]


        if project_rows.empty:

            return jsonify({

                "error":
                    f"Project {project_id} not found."

            }), 404


        row = project_rows.iloc[0]


        # =================================================
        # MODEL INPUT
        # =================================================

        input_data = pd.DataFrame(

            [{

                "land_acquired_percent":
                    safe_number(
                        data.get(
                            "land_acquired",
                            0
                        )
                    ),

                "pending_approvals":
                    safe_number(
                        data.get(
                            "pending_approvals",
                            0
                        )
                    ),

                "compensation_pending_percent":
                    safe_number(
                        data.get(
                            "compensation_pending",
                            0
                        )
                    ),

                "legal_cases":
                    safe_number(
                        data.get(
                            "legal_cases",
                            0
                        )
                    ),

                "affected_families":
                    safe_number(
                        data.get(
                            "affected_families",
                            0
                        )
                    ),

                "rr_completed_percent":
                    safe_number(
                        data.get(
                            "rr_completed",
                            0
                        )
                    ),

                "possession_percent":
                    safe_number(
                        data.get(
                            "possession",
                            0
                        )
                    ),

                "planned_duration_months":
                    safe_number(
                        data.get(
                            "planned_duration",
                            0
                        )
                    ),

                "environmental_clearance":
                    int(
                        safe_number(
                            data.get(
                                "environmental",
                                0
                            )
                        )
                    ),

                "forest_clearance":
                    int(
                        safe_number(
                            data.get(
                                "forest",
                                0
                            )
                        )
                    )

            }]

        )


        # =================================================
        # FEATURE ORDER
        # =================================================

        if model_features is not None:

            feature_list = list(
                model_features
            )


            missing_features = [

                feature

                for feature in feature_list

                if feature
                not in input_data.columns

            ]


            if missing_features:

                return jsonify({

                    "error":
                        "Model feature mismatch. "
                        f"Missing: {missing_features}"

                }), 500


            input_data = input_data[
                feature_list
            ]


        # =================================================
        # MODEL PREDICTION
        # =================================================

        prediction = float(

            model.predict(
                input_data
            )[0]

        )


        prediction = max(
            0,
            prediction
        )


        # =================================================
        # RISK
        # =================================================

        if prediction < 120:

            predicted_risk = "LOW"

        elif prediction < 240:

            predicted_risk = "MEDIUM"

        else:

            predicted_risk = "HIGH"


        # =================================================
        # INPUT VALUES
        # =================================================

        possession = safe_number(
            data.get(
                "possession",
                0
            )
        )


        compensation_pending = safe_number(
            data.get(
                "compensation_pending",
                0
            )
        )


        legal_cases = safe_number(
            data.get(
                "legal_cases",
                0
            )
        )


        pending_approvals = safe_number(
            data.get(
                "pending_approvals",
                0
            )
        )


        environmental = int(

            safe_number(
                data.get(
                    "environmental",
                    0
                )
            )

        )


        forest = int(

            safe_number(
                data.get(
                    "forest",
                    0
                )
            )

        )


        # =================================================
        # RECOMMENDATION
        # =================================================

        actions = []


        if possession < 50:

            actions.append(
                "Prioritize land possession."
            )


        if compensation_pending > 50:

            actions.append(
                "Accelerate compensation processing."
            )


        if legal_cases > 0:

            actions.append(
                "Review pending legal cases."
            )


        if pending_approvals > 0:

            actions.append(
                "Expedite pending approvals."
            )


        if environmental == 0:

            actions.append(
                "Resolve environmental clearance."
            )


        if forest == 0:

            actions.append(
                "Resolve forest clearance."
            )


        if not actions:

            actions.append(
                "Continue routine monitoring."
            )


        recommendation = " ".join(
            actions
        )


        # =================================================
        # CURRENT DELAY
        # =================================================

        current_delay = safe_number(

            row.get(
                "delay_days",
                0
            )

        )


        # =================================================
        # RESPONSE
        # =================================================

        return jsonify({

            "predicted_delay":
                prediction,

            "risk":
                predicted_risk,

            "current_delay":
                current_delay,

            "recommendation":
                recommendation

        })


    except Exception as error:

        print(
            "Prediction error:",
            error
        )


        return jsonify({

            "error":
                str(error)

        }), 400


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route(
    "/api/health"
)
def health():

    return jsonify({

        "status":
            "online",

        "dataset_loaded":
            not df.empty,

        "dataset_rows":
            len(df),

        "model_loaded":
            model is not None

    })


# =========================================================
# LOCAL SERVER
# =========================================================

if __name__ == "__main__":

    print()
    print("=" * 60)
    print(
        "LANDGUARD AI CUSTOM WEB DASHBOARD"
    )
    print("=" * 60)

    print(
        "Dataset rows:",
        len(df)
    )

    print(
        "Projects:",
        total_projects
    )

    print(
        "ML Model:",
        "Loaded"
        if model is not None
        else "Not Loaded"
    )

    print("=" * 60)

    print(
        "Open: http://127.0.0.1:5001"
    )

    print("=" * 60)
    print()


    app.run(

        host="0.0.0.0",

        port=5001,

        debug=True

    )