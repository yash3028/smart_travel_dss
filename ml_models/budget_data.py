# budget_data.py
import pandas as pd
import numpy as np

np.random.seed(42)

cities = ["Paris", "Berlin", "Rome", "Amsterdam", "Barcelona"]
travel_types = ["solo", "couple", "family"]
interests = ["culture", "nature", "shopping", "nightlife"]

data = []

for _ in range(1000):
    city = np.random.choice(cities)
    days = np.random.randint(2, 8)
    travel_type = np.random.choice(travel_types)
    interest = np.random.choice(interests)
    
    base_cost = {
        "Paris": 150,
        "Berlin": 100,
        "Rome": 130,
        "Amsterdam": 140,
        "Barcelona": 120
    }[city]

    multiplier = {"solo": 1, "couple": 1.7, "family": 2.5}[travel_type]
    noise = np.random.randint(-100, 150)

    budget = int(base_cost * days * multiplier + noise)

    data.append([city, days, travel_type, interest, budget])

df = pd.DataFrame(data, columns=[
    "city", "days", "travel_type", "interest", "recommended_budget"
])

df.to_csv("budget_data.csv", index=False)
