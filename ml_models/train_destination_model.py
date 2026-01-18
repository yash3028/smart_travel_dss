import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from destination_data import load_destination_data

def train_destination_model():
    df = load_destination_data()

    df["combined_features"] = (
        df["interests"] + " " +
        df["travel_type"] + " " +
        df["budget"] + " " +
        df["season"]
    )

    vectorizer = TfidfVectorizer(stop_words="english")
    feature_matrix = vectorizer.fit_transform(df["combined_features"])

    model_data = {
        "vectorizer": vectorizer,
        "feature_matrix": feature_matrix,
        "cities": df["city"].tolist()
    }

    with open("destination_model.pkl", "wb") as f:
        pickle.dump(model_data, f)

    print("Destination recommendation model trained for 4 cities.")

if __name__ == "__main__":
    train_destination_model()
