from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
import numpy as np
import os

# Serve static files
app = Flask(__name__, static_url_path='', static_folder='.')
CORS(app)

# --- Load model ---
model_paths = ["rentease_final_model_.pkl", "rentease_final_model.pkl"]
encoder_paths = ["rentease_final_encoder_.pkl", "rentease_final_encoder.pkl"]

model_file = next((p for p in model_paths if os.path.exists(p)), None)
encoder_file = next((p for p in encoder_paths if os.path.exists(p)), None)

if not model_file:
    raise FileNotFoundError(f"Model file not found. Checked: {model_paths}")
if not encoder_file:
    raise FileNotFoundError(f"Encoder file not found. Checked: {encoder_paths}")

model = pickle.load(open(model_file, "rb"))
columns = pickle.load(open(encoder_file, "rb"))

# Ensure columns match model features
try:
    if hasattr(model, "feature_names_in_"):
        model_cols = list(model.feature_names_in_)
        if not isinstance(columns, (list, tuple)) or len(columns) != len(model_cols):
            columns = model_cols
except Exception:
    pass

# --- Feature mapping dicts ---
city_map = {f[len("City_"):].strip().lower(): f for f in columns if f.startswith("City_")}
locality_map = {f[len("Area Locality_"):].strip().lower(): f for f in columns if f.startswith("Area Locality_")}
area_map = {f[len("Area Type_"):].strip().lower(): f for f in columns if f.startswith("Area Type_")}
furnish_map = {f[len("Furnishing Status_"):].strip().lower(): f for f in columns if f.startswith("Furnishing Status_")}

# --- Prediction function ---
def predict_rent(data):
    input_dict = {col: 0 for col in columns}

    # Numeric features
    input_dict['BHK'] = int(data.get("BHK", 0))
    input_dict['Size'] = float(data.get("Size", 0))
    input_dict['Floor'] = int(data.get("Floor", 0))
    input_dict['Bathroom'] = int(data.get("Bathroom", 0))

    # Categorical features (safe mapping)
    City = str(data.get("City", "other")).strip().lower()
    Locality = str(data.get("Locality", "other")).strip().lower()
    AreaType = str(data.get("AreaType", "nan")).strip().lower()
    Furnishing = str(data.get("Furnishing", "nan")).strip().lower()

    input_dict[city_map.get(City, 'City_other')] = 1
    input_dict[locality_map.get(Locality, 'Area Locality_other')] = 1
    input_dict[area_map.get(AreaType, 'Area Type_nan')] = 1
    input_dict[furnish_map.get(Furnishing, 'Furnishing Status_nan')] = 1

    # DataFrame
    df = pd.DataFrame([input_dict])

    # Predict (log1p → original scale)
    log_pred = model.predict(df)[0]
    rent = np.expm1(log_pred)
    return round(rent)

# --- Routes ---
@app.route("/")
def index():
    return app.send_static_file('index.html')

@app.route("/predict", methods=["POST"])
def predict_route():
    try:
        data = request.json or {}
        rent = predict_rent(data)
        return jsonify({"predicted_rent": rent, "unit": "per month"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Run ---
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5050)
