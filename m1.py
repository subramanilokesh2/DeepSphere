import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

# Load your dataset
data = pd.read_csv("data.csv")

# Define your features (X) and target variable (y)
X = data[['earnings', 'earning_potential']]
y = data['prefered_spending_limit']

# Initialize and train a Random Forest Regressor model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# Save the trained model as a .pkl file
joblib.dump(model, 'trainedModel.pkl')