from flask import Flask, render_template, jsonify, request, send_from_directory
from pathlib import Path
import os
import pandas as pd
import joblib


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_FILE = BASE_DIR / "final_data.csv"
MODEL_FILE = BASE_DIR / "model.pkl"
FEATURE_FILE = BASE_DIR / "model_features.pkl"


# ============================================================
# FLASK APP
# ============================================================

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates"),
    static_folder=str(BASE_DIR / "static")
)


# ============================================================
# LOAD DATA
# ============================================================

df = pd.DataFrame()

try:
    if DATA_FILE.exists():
        df = pd.read_csv(DATA_FILE)
        print(f"Dataset loaded successfully: {len(df)} rows")
    else:
        print("WARNING: final_data.csv not found.")

except Exception as e:
    print("Dataset loading error:", e)


# ============================================================
# LOAD MODEL
# ============================================================

model = None

try:
    if MODEL_FILE.exists():
        model = joblib.load(MODEL_FILE)
        print("ML model loaded successfully.")
    else:
        print("WARNING: model.pkl not found.")

except Exception as e:
    print("Model loading error:", e)


# ============================================================
# LOAD MODEL FEATURES
# ============================================================

model_features = None

try:
    if FEATURE_FILE.exists():
        model_features = joblib.load(FEATURE_FILE)

        # Convert common formats to list
        if isinstance(model_features, dict):
            if "features" in model_features:
                model_features = model_features["features"]
            elif "columns" in model_features:
                model_features = model_features["columns"]

        if hasattr(model_features, "tolist"):
            model_features = model_features.tolist()

        if isinstance(model_features, str):
            model_features = [model_features]

        model_features = list(model_features)

        print("Model features loaded successfully.")
        print("Model features:", model_features)

    else:
        print("WARNING: model_features.pkl not found.")

except Exception as e:
    print("Feature loading error:", e)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def safe_float(value, default=0.0):
    try:
        if value is None:
            return default

        if pd.isna(value):
            return default

        return float(value)

    except (TypeError, ValueError):
        return default


def safe_int(value, default=0):
    try:
        if value is None:
            return default

        if pd.isna(value):
            return default

        return int(float(value))

    except (TypeError, ValueError):
        return default


def clean_text(value, default="-"):
    if value is None:
        return default

    try:
        if pd.isna(value):
            return default
    except Exception:
        pass

    return str(value)


def get_first_existing(row, names, default=0):
    """
    Get the first matching value from a pandas row
    using several possible column names.
    """

    for name in names:
        if name in row.index:
            value = row[name]

            if not pd.isna(value):
                return value

    return default


def normalize_risk(value):
    risk = clean_text(value, "LOW").strip().upper()

    if risk not in {"HIGH", "MEDIUM", "LOW"}:
        return "LOW"

    return risk


def risk_css_class(value):
    risk = normalize_risk(value)

    if risk == "HIGH":
        return "risk-high"

    if risk == "MEDIUM":
        return "risk-medium"

    return "risk-low"


# ============================================================
# BASIC DATA PREPARATION
# ============================================================

total_records = len(df)

if not df.empty and "project_id" in df.columns:

    total_projects = (
        df["project_id"]
        .dropna()
        .astype(str)
        .nunique()
    )

else:
    total_projects = total_records


# ============================================================
# RISK COUNTS
# ============================================================

if not df.empty and "delay_risk" in df.columns:

    normalized_risks = (
        df["delay_risk"]
        .fillna("LOW")
        .astype(str)
        .str.strip()
        .str.upper()
    )

    high_risk = int((normalized_risks == "HIGH").sum())
    medium_risk = int((normalized_risks == "MEDIUM").sum())
    low_risk = int((normalized_risks == "LOW").sum())

else:

    high_risk = 0
    medium_risk = 0
    low_risk = 0


# ============================================================
# AVERAGES
# ============================================================

if not df.empty:

    if "delay_days" in df.columns:
        delay_series = pd.to_numeric(
            df["delay_days"],
            errors="coerce"
        )

        average_delay = float(
            delay_series.mean()
        ) if not delay_series.dropna().empty else 0.0

    else:
        average_delay = 0.0


    if "possession_percent" in df.columns:
        possession_series = pd.to_numeric(
            df["possession_percent"],
            errors="coerce"
        )

        average_possession = float(
            possession_series.mean()
        ) if not possession_series.dropna().empty else 0.0

    else:
        average_possession = 0.0

else:

    average_delay = 0.0
    average_possession = 0.0


# ============================================================
# RISK PERCENTAGES
# ============================================================

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

    high_percent = 0.0
    medium_percent = 0.0
    low_percent = 0.0


# ============================================================
# PROJECT IDS
# ============================================================

if not df.empty and "project_id" in df.columns:

    projects = sorted(
        df["project_id"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

else:

    projects = []


# ============================================================
# PROJECT TABLE
# ============================================================

project_table = []

if not df.empty:

    working_df = df.copy()

    # Sort by delay if available
    if "delay_days" in working_df.columns:

        working_df["_sort_delay"] = pd.to_numeric(
            working_df["delay_days"],
            errors="coerce"
        )

        working_df = working_df.sort_values(
            "_sort_delay",
            ascending=False,
            na_position="last"
        )

    # Keep dashboard responsive
    working_df = working_df.head(250)

    for _, row in working_df.iterrows():

        risk = normalize_risk(
            row.get("delay_risk", "LOW")
        )

        project_table.append({

            "project_id":
                clean_text(
                    row.get("project_id", "-")
                ),

            "project_name":
                clean_text(
                    row.get("project_name", "-")
                ),

            "state":
                clean_text(
                    row.get("state", "-")
                ),

            "district":
                clean_text(
                    row.get("district", "-")
                ),

            "delay_risk":
                risk,

            "risk_class":
                risk_css_class(risk),

            "delay_days":
                round(
                    safe_float(
                        row.get("delay_days", 0)
                    ),
                    1
                ),

            "possession_percent":
                round(
                    safe_float(
                        row.get(
                            "possession_percent",
                            0
                        )
                    ),
                    1
                )

        })


# ============================================================
# ATTENTION PROJECTS
# ============================================================

attention_projects = []

if not df.empty:

    attention_df = df.copy()

    if "delay_days" in attention_df.columns:

        attention_df["_delay_numeric"] = pd.to_numeric(
            attention_df["delay_days"],
            errors="coerce"
        )

        attention_df = (
            attention_df
            .sort_values(
                "_delay_numeric",
                ascending=False,
                na_position="last"
            )
            .head(8)
        )

    else:

        attention_df = attention_df.head(8)


    for _, row in attention_df.iterrows():

        risk = normalize_risk(
            row.get("delay_risk", "LOW")
        )

        attention_projects.append({

            "project_id":
                clean_text(
                    row.get(
                        "project_id",
                        "-"
                    )
                ),

            "district":
                clean_text(
                    row.get(
                        "district",
                        "-"
                    )
                ),

            "delay_risk":
                risk,

            "risk_class":
                risk_css_class(risk),

            "delay_days":
                round(
                    safe_float(
                        row.get(
                            "delay_days",
                            0
                        )
                    ),
                    1
                )

        })


# ============================================================
# DASHBOARD
# ============================================================

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


# ============================================================
# MAPS / CHARTS / HTML FILES
# ============================================================

@app.route("/files/<path:filename>")
def serve_files(filename):

    requested_file = BASE_DIR / filename

    if not requested_file.exists():
        return (
            jsonify({
                "error": f"File not found: {filename}"
            }),
            404
        )

    return send_from_directory(
        str(BASE_DIR),
        filename
    )


# ============================================================
# PREDICTION
# ============================================================

@app.route(
    "/api/predict",
    methods=["POST"]
)
def predict():

    # --------------------------------------------------------
    # CHECK MODEL
    # --------------------------------------------------------

    if model is None:

        return jsonify({
            "error": "ML model could not be loaded."
        }), 500


    # --------------------------------------------------------
    # CHECK DATASET
    # --------------------------------------------------------

    if df.empty:

        return jsonify({
            "error": "final_data.csv could not be loaded."
        }), 500


    try:

        data = request.get_json(
            silent=True
        )


        if not isinstance(data, dict):

            return jsonify({
                "error": "Invalid prediction data."
            }), 400


        project_id = clean_text(
            data.get("project_id"),
            ""
        )


        if not project_id:

            return jsonify({
                "error": "Project ID is required."
            }), 400


        # ----------------------------------------------------
        # FIND SELECTED PROJECT
        # ----------------------------------------------------

        if "project_id" not in df.columns:

            return jsonify({
                "error": "project_id column is missing."
            }), 500


        selected_rows = df[
            df["project_id"]
            .astype(str)
            .eq(project_id)
        ]


        if selected_rows.empty:

            return jsonify({
                "error":
                    f"Project {project_id} not found."
            }), 404


        selected_row = selected_rows.iloc[0]


        # ----------------------------------------------------
        # USER INPUTS
        # ----------------------------------------------------

        possession = safe_float(
            data.get(
                "possession",
                get_first_existing(
                    selected_row,
                    [
                        "possession_percent",
                        "possession"
                    ],
                    0
                )
            )
        )


        land_acquired = safe_float(
            data.get(
                "land_acquired",
                get_first_existing(
                    selected_row,
                    [
                        "land_acquired_percent",
                        "land_acquired"
                    ],
                    0
                )
            )
        )


        pending_approvals = safe_float(
            data.get(
                "pending_approvals",
                get_first_existing(
                    selected_row,
                    [
                        "pending_approvals"
                    ],
                    0
                )
            )
        )


        compensation_pending = safe_float(
            data.get(
                "compensation_pending",
                get_first_existing(
                    selected_row,
                    [
                        "compensation_pending_percent",
                        "compensation_pending"
                    ],
                    0
                )
            )
        )


        legal_cases = safe_float(
            data.get(
                "legal_cases",
                get_first_existing(
                    selected_row,
                    [
                        "legal_cases"
                    ],
                    0
                )
            )
        )


        affected_families = safe_float(
            data.get(
                "affected_families",
                get_first_existing(
                    selected_row,
                    [
                        "affected_families"
                    ],
                    0
                )
            )
        )


        rr_completed = safe_float(
            data.get(
                "rr_completed",
                get_first_existing(
                    selected_row,
                    [
                        "rr_completed_percent",
                        "rr_completed"
                    ],
                    0
                )
            )
        )


        planned_duration = safe_float(
            data.get(
                "planned_duration",
                get_first_existing(
                    selected_row,
                    [
                        "planned_duration_months",
                        "planned_duration"
                    ],
                    0
                )
            )
        )


        environmental = safe_int(
            data.get(
                "environmental",
                get_first_existing(
                    selected_row,
                    [
                        "environmental_clearance"
                    ],
                    0
                )
            )
        )


        forest = safe_int(
            data.get(
                "forest",
                get_first_existing(
                    selected_row,
                    [
                        "forest_clearance"
                    ],
                    0
                )
            )
        )


        # ----------------------------------------------------
        # BASE INPUT DATA
        #
        # Start from the actual project row wherever possible.
        # This makes prediction more compatible with the model
        # that was trained from final_data.csv.
        # ----------------------------------------------------

        if model_features:

            input_row = {}


            for feature in model_features:

                # Existing value from dataset
                if feature in selected_row.index:

                    input_row[feature] = selected_row[feature]

                else:

                    input_row[feature] = 0


            input_df = pd.DataFrame(
                [input_row]
            )


            # ------------------------------------------------
            # OVERRIDE COMMON USER-CONTROLLED FEATURES
            # ------------------------------------------------

            feature_aliases = {

                "possession_percent":
                    possession,

                "possession":
                    possession,

                "land_acquired_percent":
                    land_acquired,

                "land_acquired":
                    land_acquired,

                "pending_approvals":
                    pending_approvals,

                "compensation_pending_percent":
                    compensation_pending,

                "compensation_pending":
                    compensation_pending,

                "legal_cases":
                    legal_cases,

                "affected_families":
                    affected_families,

                "rr_completed_percent":
                    rr_completed,

                "rr_completed":
                    rr_completed,

                "planned_duration_months":
                    planned_duration,

                "planned_duration":
                    planned_duration,

                "environmental_clearance":
                    environmental,

                "forest_clearance":
                    forest

            }


            for feature, value in feature_aliases.items():

                if feature in input_df.columns:

                    input_df[feature] = value


            # Ensure exact feature order
            input_df = input_df[
                model_features
            ]


        else:

            # ------------------------------------------------
            # FALLBACK INPUT
            # ------------------------------------------------

            input_df = pd.DataFrame([{

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
                    environmental,

                "forest_clearance":
                    forest

            }])


        # ----------------------------------------------------
        # CLEAN NUMERIC VALUES
        # ----------------------------------------------------

        for column in input_df.columns:

            if pd.api.types.is_numeric_dtype(
                input_df[column]
            ):

                input_df[column] = pd.to_numeric(
                    input_df[column],
                    errors="coerce"
                )


        input_df = input_df.fillna(0)


        # ----------------------------------------------------
        # PREDICTION
        # ----------------------------------------------------

        predicted_delay = float(
            model.predict(input_df)[0]
        )


        predicted_delay = max(
            0.0,
            predicted_delay
        )


        # ----------------------------------------------------
        # RISK LEVEL
        # ----------------------------------------------------

        if predicted_delay < 120:

            risk = "LOW"

        elif predicted_delay < 240:

            risk = "MEDIUM"

        else:

            risk = "HIGH"


        # ----------------------------------------------------
        # CURRENT DELAY
        # ----------------------------------------------------

        current_delay = safe_float(
            selected_row.get(
                "delay_days",
                0
            )
        )


        # ----------------------------------------------------
        # AI RECOMMENDATION
        # ----------------------------------------------------

        recommendations = []


        if possession < 50:

            recommendations.append(
                "Prioritize land possession."
            )


        if compensation_pending > 40:

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


        if environmental == 0:

            recommendations.append(
                "Resolve environmental clearance."
            )


        if forest == 0:

            recommendations.append(
                "Resolve forest clearance."
            )


        if not recommendations:

            recommendations.append(
                "Continue routine monitoring."
            )


        recommendation = " ".join(
            recommendations
        )


        # ----------------------------------------------------
        # RESPONSE
        # ----------------------------------------------------

        return jsonify({

            "success":
                True,

            "project_id":
                project_id,

            "predicted_delay":
                round(
                    predicted_delay,
                    1
                ),

            "risk":
                risk,

            "current_delay":
                round(
                    current_delay,
                    1
                ),

            "recommendation":
                recommendation

        })


    except Exception as e:

        print(
            "Prediction error:",
            repr(e)
        )

        return jsonify({

            "success":
                False,

            "error":
                str(e)

        }), 500


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/api/health")
def health():

    return jsonify({

        "status":
            "online",

        "dataset_loaded":
            not df.empty,

        "dataset_rows":
            int(len(df)),

        "model_loaded":
            model is not None,

        "features_loaded":
            model_features is not None

    })


# ============================================================
# LOCAL SERVER
# ============================================================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5001
        )
    )

    print()
    print("=" * 65)
    print("LANDGUARD AI CUSTOM WEB DASHBOARD")
    print("=" * 65)
    print(f"Dataset rows : {len(df)}")
    print(f"Projects     : {total_projects}")
    print(
        "ML Model     :",
        "Loaded" if model is not None else "Not Loaded"
    )
    print(
        "Features     :",
        "Loaded" if model_features is not None else "Not Loaded"
    )
    print("=" * 65)

    if port == 5001:

        print(
            "Open: http://127.0.0.1:5001"
        )

    print("=" * 65)
    print()

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )