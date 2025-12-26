# duration_data.py
import pandas as pd
import numpy as np

np.random.seed(42)

cities = ["Paris", "Berlin", "Rome", "Amsterdam", "Barcelona"]
interests = ["culture", "nature", "shopping", "nightlife"]

data = []

for _ in range(800):
    city = np.random.choice(cities)
    interest = np.random.choice(interests)
    attractions = np.random.randint(8, 30)

    if attractions < 12:
        duration = "Short"
    elif attractions < 20:
        duration = "Medium"
    else:
        duration = "Long"

    data.append([city, interest, attractions, duration])

df = pd.DataFrame(data, columns=[
    "city", "interest", "attractions", "ideal_duration"
])

df.to_csv("duration_data.csv", index=False)
