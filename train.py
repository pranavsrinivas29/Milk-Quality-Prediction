import pandas as pd
import joblib
import os
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
from sklearn.preprocessing import LabelEncoder

# Set MLflow experiment
mlflow.set_experiment("Milk_Quality_Classification")

# Load dataset
data_path = "data/milknew.csv"
df = pd.read_csv(data_path)

# Features and target
X = df.drop("Grade", axis=1)
y = df["Grade"]

# Encode target if categorical
if y.dtype == "object":
    le = LabelEncoder()
    y = le.fit_transform(y)
    joblib.dump(le, "models/label_encoder.pkl")

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Hyperparameter grid
param_grid = {
    "n_estimators": [50, 100, 200],
    "max_depth": [3, 5, 10]
}

# Manual grid search with MLflow logging
best_score = 0
best_model = None
best_params = {}

for n in param_grid["n_estimators"]:
    for d in param_grid["max_depth"]:
        with mlflow.start_run(nested=True):
            model = RandomForestClassifier(n_estimators=n, max_depth=d, random_state=42)
            model.fit(X_train, y_train)

            y_pred = model.predict(X_test)
            acc = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred, average="weighted")

            # Log hyperparameters and metrics for this run
            mlflow.log_param("n_estimators", n)
            mlflow.log_param("max_depth", d)
            mlflow.log_metric("accuracy", acc)
            mlflow.log_metric("f1_score", f1)

            # Track best model
            if acc > best_score:
                best_score = acc
                best_model = model
                best_params = {
                    "n_estimators": n,
                    "max_depth": d,
                    "accuracy": acc,
                    "f1_score": f1
                }

# Save the best model to disk
os.makedirs("models", exist_ok=True)
joblib.dump(best_model, "models/model.pkl")

# Log the best model in a separate MLflow run
with mlflow.start_run(run_name="Best_Model"):
    mlflow.log_params({
        "n_estimators": best_params["n_estimators"],
        "max_depth": best_params["max_depth"]
    })
    mlflow.log_metrics({
        "accuracy": best_params["accuracy"],
        "f1_score": best_params["f1_score"]
    })

    # Log model artifact
    mlflow.sklearn.log_model(best_model, artifact_path="best_model")

print(f"Best Model → Accuracy: {best_score:.4f}, Params: {best_params}")
