# train_budget_model.py
from common_imports import *

df = pd.read_csv("budget_data.csv")

X = df.drop("recommended_budget", axis=1)
y = df["recommended_budget"]

categorical_features = ["city", "travel_type", "interest"]
numeric_features = ["days"]

preprocessor = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
    ("num", StandardScaler(), numeric_features)
])

model = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(n_estimators=200, random_state=42))
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model.fit(X_train, y_train)

preds = model.predict(X_test)
print("MAE:", mean_absolute_error(y_test, preds))

joblib.dump(model, "budget_model.pkl")
