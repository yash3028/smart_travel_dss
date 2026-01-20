from flask import Flask, request, jsonify
import pandas as pd
import joblib
from flask_cors import CORS
import pickle
from sklearn.metrics.pairwise import cosine_similarity
import os

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DESTINATION_MODEL_PATH = os.path.join(
    BASE_DIR, "..", "ml_models", "destination_model.pkl"
)

print("Model path:", DESTINATION_MODEL_PATH)
print("Exists:", os.path.exists(DESTINATION_MODEL_PATH))

budget_model = joblib.load("../ml_models/budget_model.pkl")
duration_model = joblib.load("../ml_models/duration_model.pkl")
destination_model = joblib.load("../ml_models/destination_model.pkl")


with open("../ml_models/destination_model.pkl", "rb") as f:
    model_data = pickle.load(f)

vectorizer = model_data["vectorizer"]
feature_matrix = model_data["feature_matrix"]
cities = model_data["cities"]

# ------------------ DESTINATION RECOMMENDATION ------------------
@app.route("/recommend/destinations", methods=["POST"])
def recommend_destinations():
    data = request.get_json(force=True)

    user_text = (
        data["interest"] + " " +
        data["travel_type"] + " " +
        data["budget"] + " " +
        data["season"]
    )

    user_vector = vectorizer.transform([user_text])

    similarity_scores = cosine_similarity(
        user_vector,
        feature_matrix
    )[0]   # <-- NumPy array indexing (NOT df[0])

    top_n = data.get("top_n", 3)

    ranked = sorted(
        zip(cities, similarity_scores),
        key=lambda x: x[1],
        reverse=True
    )

    recommendations = [
        {
            "city": city,
            "score": round(float(score), 2)
        }
        for city, score in ranked[:top_n]
    ]

    return jsonify({"recommendations": recommendations})

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


# ------------------ RUN ------------------
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)
