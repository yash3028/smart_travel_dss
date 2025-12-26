# predict_budget.py
import joblib
import pandas as pd

model = joblib.load("budget_model.pkl")

def predict_budget(city, days, travel_type, interest):
    df = pd.DataFrame([[city, days, travel_type, interest]],
                      columns=["city", "days", "travel_type", "interest"])
    return int(model.predict(df)[0])
