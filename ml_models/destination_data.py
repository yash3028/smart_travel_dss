import pandas as pd

def load_destination_data():
    data = [
        {
            "city": "Hyderabad",
            "interests": "culture,history,food",
            "travel_type": "solo,family,friends",
            "budget": "low,medium",
            "season": "winter,monsoon"
        },
        {
            "city": "Mumbai",
            "interests": "culture,nightlife,food,beach",
            "travel_type": "solo,friends,couple",
            "budget": "medium,high",
            "season": "winter"
        },
        {
            "city": "London",
            "interests": "culture,history,museums,architecture",
            "travel_type": "solo,couple,family",
            "budget": "high",
            "season": "spring,summer"
        },
        {
            "city": "Edinburgh",
            "interests": "history,nature,architecture",
            "travel_type": "solo,couple",
            "budget": "medium,high",
            "season": "summer,autumn"
        }
    ]

    return pd.DataFrame(data)
