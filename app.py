from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
import numpy as np
import os

# ---- Flask App ----
app = Flask(__name__, static_folder="static")
CORS(app)

# ---- Load model safely ----
def load_pickle(possible_paths):
    for p in possible_paths:
        if os.path.exists(p):
            return pickle.load(open(p, "rb"))
    return None

model = load_pickle(["rentease_final_model_.pkl", "rentease_final_model.pkl"])
columns = load_pickle(["rentease_final_encoder_.pkl", "rentease_final_encoder.pkl"])

if model is None or columns is None:
    print("⚠️ Model or encoder not found. App will still start.")
    columns = []

# ---- Feature maps (safe even if empty) ----
city_map = {f[len("City_"):].strip().lower(): f for f in columns if f.startswith("City_")}
locality_map = {f[len("Area Locality_"):].strip().lower(): f for f in columns if f.startswith("Area Locality_")}
area_map = {f[len("Area Type_"):].strip().lower(): f for f in columns if f.startswith("Area Type_")}
furnish_map = {f[len("Furnishing Status_"):].strip().lower(): f for f in columns if f.startswith("Furnishing Status_")}

# ---- Prediction ----
def predict_rent(data):
    if model is None or not columns:
        raise Exception("Model not loaded")

    input_dict = {col: 0 for col in columns}

    input_dict["BHK"] = int(data.get("BHK", 0))
    input_dict["Size"] = float(data.get("Size", 0))
    input_dict["Floor"] = int(data.get("Floor", 0))
    input_dict["Bathroom"] = int(data.get("Bathroom", 0))

    city = str(data.get("City", "other")).lower()
    locality = str(data.get("Locality", "other")).lower()
    area = str(data.get("AreaType", "nan")).lower()
    furnish = str(data.get("Furnishing", "nan")).lower()

    input_dict[city_map.get(city, "City_other")] = 1
    input_dict[locality_map.get(locality, "Area Locality_other")] = 1
    input_dict[area_map.get(area, "Area Type_nan")] = 1
    input_dict[furnish_map.get(furnish, "Furnishing Status_nan")] = 1

    df = pd.DataFrame([input_dict])
    log_pred = model.predict(df)[0]
    return round(np.expm1(log_pred))

# ---- Routes ----
@app.route("/")
def home():
    return "RentEase ML API running 🚀"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        rent = predict_rent(request.json or {})
        return jsonify({"predicted_rent": rent, "unit": "per month"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---- Run ----
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
