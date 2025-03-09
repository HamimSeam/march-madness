import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load preprocessed data
data = pd.read_csv("data/processed_results.csv")

# Split features and labels
X = data[['SeedDiff']]
y = data['Result']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.4f}")

# Save the trained model
with open("data/march_madness_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model training complete. Saved as march_madness_model.pkl")
