import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error


# =========================================================
# 1. LOAD DATASET
# =========================================================

df = pd.read_csv("final_data.csv")


# =========================================================
# 2. FEATURES
# =========================================================

features = [
    "land_acquired_percent",
    "pending_approvals",
    "compensation_pending_percent",
    "legal_cases",
    "affected_families",
    "rr_completed_percent",
    "possession_percent",
    "planned_duration_months",
    "environmental_clearance",
    "forest_clearance"
]


target = "delay_days"


# =========================================================
# 3. SELECT REQUIRED COLUMNS
# =========================================================

data = df[
    features + [target]
].copy()


# =========================================================
# 4. CONVERT YES / NO COLUMNS
# =========================================================

for column in [
    "environmental_clearance",
    "forest_clearance"
]:

    data[column] = (
        data[column]
        .astype(str)
        .str.strip()
        .str.lower()
        .map({
            "yes": 1,
            "no": 0
        })
        .fillna(0)
    )


# =========================================================
# 5. CONVERT NUMERIC COLUMNS
# =========================================================

for column in features + [target]:

    data[column] = pd.to_numeric(
        data[column],
        errors="coerce"
    )


# =========================================================
# 6. REMOVE MISSING VALUES
# =========================================================

data = data.dropna()


# =========================================================
# 7. INPUT AND TARGET
# =========================================================

X = data[features]

y = data[target]


# =========================================================
# 8. TRAIN / TEST SPLIT
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.20,

    random_state=42
)


# =========================================================
# 9. CREATE RANDOM FOREST MODEL
# =========================================================

model = RandomForestRegressor(

    n_estimators=100,

    random_state=42,

    n_jobs=-1

)


# =========================================================
# 10. TRAIN MODEL
# =========================================================

model.fit(

    X_train,

    y_train

)


# =========================================================
# 11. TEST MODEL
# =========================================================

predictions = model.predict(

    X_test

)


# =========================================================
# 12. CALCULATE ERROR
# =========================================================

mae = mean_absolute_error(

    y_test,

    predictions

)


# =========================================================
# 13. SAVE MODEL
# =========================================================

joblib.dump(

    model,

    "model.pkl"

)


# =========================================================
# 14. SAVE FEATURE NAMES
# =========================================================

joblib.dump(

    features,

    "model_features.pkl"

)


# =========================================================
# 15. DISPLAY RESULTS
# =========================================================

print()
print("==========================================")
print("LAND ACQUISITION DELAY PREDICTION MODEL")
print("==========================================")

print()

print(
    "Dataset records:",
    len(data)
)

print(
    "Training records:",
    len(X_train)
)

print(
    "Testing records:",
    len(X_test)
)

print()

print(
    "Mean Absolute Error:",
    round(mae, 2),
    "days"
)

print()

print(
    "Model:",
    "Random Forest Regressor"
)

print()

print(
    "MODEL TRAINED SUCCESSFULLY"
)

print()

print(
    "Saved model:",
    "model.pkl"
)

print(
    "Saved features:",
    "model_features.pkl"
)

print()

print("==========================================")