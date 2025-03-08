import os
import pandas as pd
import numpy as np
from sklearn.ensemble import AdaBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import joblib

# Define features
features = [
    "haemoglobin_test", "waistcircum_test", "glucose_test",
    "cholestrol_test", "triglycerides_test", "ldlipoprotein_test",
    "hdlipoprotein_test", "vldlipoprotein_test", "hdlratio_test"
]

# Generate synthetic dataset (1000 samples)
np.random.seed(42)
df = pd.DataFrame(np.random.rand(1000, len(features)) * 100, columns=features)

# Generate random obesity risk labels
df["obesity_risk"] = np.random.choice(["Low", "Medium", "High"], size=1000)

# Encode target labels
df["obesity_risk"] = df["obesity_risk"].map({"Low": 0, "Medium": 1, "High": 2})

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(df[features], df["obesity_risk"], test_size=0.2, random_state=42)

# Scale features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train AdaBoost model
model = AdaBoostClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.2f}")

# ✅ Ensure "subscriptions/models" directory exists before saving
model_dir = "subscriptions/models"
os.makedirs(model_dir, exist_ok=True)

# Save model and scaler in subscriptions/models/
joblib.dump(model, f"{model_dir}/adaboost_model.pkl")
joblib.dump(scaler, f"{model_dir}/scaler.pkl")

print("Model training complete and saved in subscriptions/models/")
