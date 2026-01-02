import os
import sys
import numpy as np
import pandas as pd
import joblib
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

# Set style for better-looking plots
sns.set_style('whitegrid')
sns.set_palette('viridis')
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 12

def load_data():
    """Load and prepare the California Housing dataset."""
    print("Loading California Housing dataset...")
    data = fetch_california_housing()
    X = pd.DataFrame(data.data, columns=data.feature_names)
    y = pd.Series(data.target, name='MedHouseVal')
    return X, y

def preprocess_data(X, y, test_size=0.2, random_state=42):
    """Split and scale the data."""
    print("Preprocessing data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    return X_train_scaled, X_test_scaled, y_train, y_test

def tune_hyperparameters(X_train, y_train, cv=3, n_jobs=-1):
    """Find the best hyperparameters using GridSearchCV with a reduced search space."""
    print("\nTuning hyperparameters...")
    param_grid = {
        'n_estimators': [50, 100],
        'max_depth': [10, 20, None],
        'min_samples_split': [2, 5],
        'min_samples_leaf': [1, 2]
    }
    
    try:
        grid_search = GridSearchCV(
            estimator=RandomForestRegressor(random_state=42, n_jobs=n_jobs),
            param_grid=param_grid,
            cv=cv,
            n_jobs=1,  # Set to 1 to prevent memory issues
            verbose=1,
            scoring='neg_mean_squared_error',
            error_score='raise'
        )
        
        grid_search.fit(X_train, y_train)
        print(f"\nBest parameters: {grid_search.best_params_}")
        print(f"Best cross-validation RMSE: {np.sqrt(-grid_search.best_score_):.4f}")
        return grid_search.best_estimator_
        
    except Exception as e:
        print(f"\nError during hyperparameter tuning: {str(e)}")
        print("Falling back to default parameters...")
        model = RandomForestRegressor(random_state=42, n_jobs=n_jobs)
        model.fit(X_train, y_train)
        return model

def train_model(X_train, y_train, tune_hyperparams=True):
    """Train a Random Forest regressor with optional hyperparameter tuning."""
    if tune_hyperparams:
        model = tune_hyperparameters(X_train, y_train)
    else:
        print("\nTraining model with default parameters...")
        model = RandomForestRegressor(random_state=42)
        model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test, feature_names):
    """Evaluate the model and create visualizations."""
    print("\nModel Evaluation")
    print("===============")
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"Mean Squared Error: {mse:.4f}")
    print(f"Root Mean Squared Error: {rmse:.4f}")
    print(f"Mean Absolute Error: {mae:.4f}")
    print(f"R² Score: {r2:.4f}")
    
    # Feature importance
    feature_importance = pd.Series(
        model.feature_importances_,
        index=feature_names
    ).sort_values(ascending=False)
    
    print("\nFeature Importance:")
    print(feature_importance)
    
    # Create visualizations directory
    import os
    os.makedirs('visualizations', exist_ok=True)
    
    # Plot feature importance
    plt.figure(figsize=(12, 6))
    sns.barplot(x=feature_importance.values, y=feature_importance.index)
    plt.title('Feature Importance')
    plt.xlabel('Importance Score')
    plt.tight_layout()
    plt.savefig('visualizations/feature_importance.png', dpi=300, bbox_inches='tight')
    
    # Actual vs Predicted values
    plt.figure(figsize=(10, 10))
    plt.scatter(y_test, y_pred, alpha=0.5)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    plt.xlabel('Actual Prices')
    plt.ylabel('Predicted Prices')
    plt.title('Actual vs Predicted House Prices')
    plt.tight_layout()
    plt.savefig('visualizations/actual_vs_predicted.png', dpi=300)
    
    # Residual plot
    residuals = y_test - y_pred
    plt.figure(figsize=(10, 6))
    sns.residplot(x=y_pred, y=residuals, lowess=True, line_kws={'color': 'red', 'lw': 2})
    plt.axhline(y=0, color='black', linestyle='--')
    plt.xlabel('Predicted Values')
    plt.ylabel('Residuals')
    plt.title('Residual Plot')
    plt.tight_layout()
    plt.savefig('visualizations/residual_plot.png', dpi=300)
    
    print("\nVisualizations saved in the 'visualizations' directory")

def save_model(model, filename='models/california_housing_model.joblib'):
    """Save the trained model to a file."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    joblib.dump(model, filename)
    print(f"\nModel saved to {filename}")

def main():
    # Load and prepare data
    X, y = load_data()
    X_train, X_test, y_train, y_test = preprocess_data(X, y)
    
    # Get feature names
    feature_names = X.columns.tolist()
    
    # Train model with hyperparameter tuning
    model = train_model(X_train, y_train, tune_hyperparams=True)
    
    # Evaluate model
    evaluate_model(model, X_test, y_test, feature_names)
    
    # Save the trained model
    save_model(model)
    
    # Print completion message
    print("\n" + "="*50)
    print("Model training and evaluation complete!")
    print("Check the 'visualizations' directory for evaluation plots.")
    print("The trained model has been saved in the 'models' directory.")
    print("="*50)

if __name__ == "__main__":
    main()
