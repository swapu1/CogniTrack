import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

# Load the dataset you provided
df = pd.read_csv('datasets_410614_786211_parkinsons.csv')

# Prepare data: Drop 'name' (ID) and 'status' (Target)
X = df.drop(['name', 'status'], axis=1)
y = df['status']

# Split and Scale
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

# Train the Random Forest Model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Save the files to your directory
with open('parkinsons_model.pkl', 'wb') as f:
    pickle.dump(model, f)
with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

print("✅ Model files generated: 'parkinsons_model.pkl' and 'scaler.pkl'")
print(f"Accuracy: {model.score(scaler.transform(X_test), y_test)*100:.2f}%")
