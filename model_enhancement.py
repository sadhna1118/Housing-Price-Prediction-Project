import xgboost as xgb
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
import numpy as np
from sklearn.datasets import fetch_california_housing
import plotly.express as px
import joblib
import os

# Load data
data = fetch_california_housing()
X = pd.DataFrame(data.data, columns=data.feature_names)
y = data.target

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# XGBoost model with hyperparameter tuning
print("Training XGBoost model...")
xgb_model = xgb.XGBRegressor(objective='reg:squarederror', random_state=42)

param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [3, 6, 9],
    'learning_rate': [0.01, 0.1, 0.3]
}

grid_search = GridSearchCV(
    estimator=xgb_model,
    param_grid=param_grid,
    cv=3,
    scoring='neg_mean_squared_error',
    n_jobs=-1,
    verbose=1
)

grid_search.fit(X_train, y_train)

# Save the best model
os.makedirs('models', exist_ok=True)
joblib.dump(grid_search.best_estimator_, 'models/xgboost_model.joblib')

# Evaluate
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)

print("\nXGBoost Model Performance:")
print(f"Best Parameters: {grid_search.best_params_}")
print(f"R² Score: {r2_score(y_test, y_pred):.4f}")
print(f"RMSE: {np.sqrt(mean_squared_error(y_test, y_pred)):.4f}")

# Feature Importance
feature_importance = pd.DataFrame({
    'Feature': X.columns,
    'Importance': best_model.feature_importances_
}).sort_values('Importance', ascending=False)

# Save feature importance plot
os.makedirs('visualizations', exist_ok=True)
fig = px.bar(feature_importance, x='Importance', y='Feature', orientation='h',
             title='Feature Importance (XGBoost)')
fig.write_image('visualizations/xgboost_feature_importance.png')
