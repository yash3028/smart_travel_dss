# train_duration_model.py
from common_imports import *

df = pd.read_csv("duration_data.csv")

X = df.drop("ideal_duration", axis=1)
y = df["ideal_duration"]

categorical_features = ["city", "interest"]
numeric_features = ["attractions"]

preprocessor = ColumnTransformer([
    ("cat", OneHotEncoder(), categorical_features),
    ("num", StandardScaler(), numeric_features)
])

model = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(n_estimators=150))
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model.fit(X_train, y_train)

print("Accuracy:", accuracy_score(y_test, model.predict(X_test)))

joblib.dump(model, "duration_model.pkl")
