# budget_data.py
import pandas as pd
import numpy as np
import joblib

np.random.seed(42)

cities = ["Hyderabad", "Mumbai", "London", "Edinburgh"]
travel_types = ["solo", "couple", "family"]
interests = ["culture", "nature", "shopping", "nightlife"]

data = []

for _ in range(1000):
    city = np.random.choice(cities)
    days = np.random.randint(2, 8)
    travel_type = np.random.choice(travel_types)
    interest = np.random.choice(interests)
    
    base_cost = {
    "Hyderabad": 60,
    "Mumbai": 75,
    "London": 160,
    "Edinburgh": 140
}[city]
    

    multiplier = {"solo": 1, "couple": 1.7, "family": 2.5}[travel_type]
    noise = np.random.randint(-100, 150)

    budget = int(base_cost * days * multiplier + noise)

    data.append([city, days, travel_type, interest, budget])

df = pd.DataFrame(data, columns=[
    "city", "days", "travel_type", "interest", "recommended_budget"
])


df.to_csv("budget_data.csv", index=False)
