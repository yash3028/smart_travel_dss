import pickle
from sklearn.metrics.pairwise import cosine_similarity

def recommend_destinations(user_input, top_n=3):
    with open("destination_model.pkl", "rb") as f:
        model_data = pickle.load(f)

    vectorizer = model_data["vectorizer"]
    feature_matrix = model_data["feature_matrix"]
    cities = model_data["cities"]

    user_text = (
        user_input["interest"] + " " +
        user_input["travel_type"] + " " +
        user_input["budget"] + " " +
        user_input["season"]
    )

    user_vector = vectorizer.transform([user_text])
    similarity_scores = cosine_similarity(user_vector, feature_matrix)[0]

    ranked = sorted(
        list(zip(cities, similarity_scores)),
        key=lambda x: x[1],
        reverse=True
    )

    recommendations = [
        {"city": city, "score": round(score, 2)}
        for city, score in ranked[:top_n]
    ]

    return recommendations
