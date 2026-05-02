import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pickle

# Load dataset
df = pd.read_csv('flood_data.csv')

# Convert text columns to numbers
df['province'] = df['province'].astype('category').cat.codes
df['district'] = df['district'].astype('category').cat.codes

# Features and target
X = df.drop(['aid_needed', 'total_population', 'total_households',
             'displaced_individuals', 'displaced_households',
             'displacement_ratio'], axis=1)
y = df['aid_needed']

# Split data into training and testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Test the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("✅ Model trained successfully!")
print(f"Accuracy: {accuracy * 100:.2f}%")
print(f"\nDetailed Report:\n{classification_report(y_test, y_pred)}")

# Save the model
with open('flood_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("\n✅ Model saved as flood_model.pkl")
print("Trained columns:", list(X.columns))

