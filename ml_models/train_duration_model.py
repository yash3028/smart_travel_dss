# train_duration_model.py
from common_imports import *

df = pd.read_csv("duration_data.csv")

X = df.drop("ideal_duration", axis=1)
y = df["ideal_duration"]

categorical_features = ["city", "interest"]
numeric_features = ["attractions"]

preprocessor = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
    ("num", StandardScaler(), numeric_features)
])

model = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(
        n_estimators=150,
        random_state=42
    ))
])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model.fit(X_train, y_train)

preds = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, preds))

joblib.dump(model, "duration_model.pkl")

print("✅ duration_model.pkl created")
