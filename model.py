import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import pickle

# Load the dataset
data = pd.DataFrame({
    'earnings': [40000,70000,76000,87500,75000,90000,75000,65000,50000,100000,35000,60000],
    'earning_potential': [80000,75000,80400,90800,80000,100000,82000,70000,52000,110000,40000,65000],
    'spending_limit': [15000,15000,30000,50000,34500,50000,42000,23500,45000,78200,10000,30000]
})

# Define features (X) and target variable (y)
X = data[['earnings', 'earning_potential']]
y = data['spending_limit']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train a Random Forest Regressor model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")

import pickle
pkl_file_path='trainedModel.pkl'
with open(pkl_file_path, 'wb') as pkl_file:
    pickle.dump(model, pkl_file)
print(f"PKL file '{pkl_file_path}' has been created.")