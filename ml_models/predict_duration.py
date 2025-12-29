# predict_duration.py
import joblib
import pandas as pd

model = joblib.load("duration_model.pkl")

def predict_duration(city, interest, attractions):
    df = pd.DataFrame([[city, interest, attractions]],
                      columns=["city", "interest", "attractions"])
    return model.predict(df)[0]
