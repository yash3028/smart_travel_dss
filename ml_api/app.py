from flask import Flask, request, jsonify
import pandas as pd
import joblib
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
budget_model = joblib.load("../ml_models/budget_model.pkl")
duration_model = joblib.load("../ml_models/duration_model.pkl")

# ------------------ HEALTH CHECK ------------------
@app.route("/health", methods=["GET"])
def health():
    return "OK"

# ------------------ BUDGET ------------------
@app.route("/predict/budget", methods=["POST"])
def predict_budget():
    data = request.get_json(force=True)

    df = pd.DataFrame([{
        "city": data["city"],
        "days": data["days"],
        "travel_type": data["travel_type"],
        "interest": data["interest"]
    }])

    pred = budget_model.predict(df)[0]
    return jsonify({"predicted_budget": float(pred)})

# ------------------ DURATION ------------------
@app.route("/predict/duration", methods=["POST"])
def predict_duration():
    data = request.get_json(force=True)

    df = pd.DataFrame([{
        "city": data["city"],
        "interest": data["interest"],
        "attractions": data["attractions"]
    }])

    pred = duration_model.predict(df)[0]
    return jsonify({"predicted_duration": str(pred)})

# ------------------ RUN ------------------
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)
