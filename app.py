from flask import Flask, render_template, request, jsonify, send_from_directory
import joblib
import numpy as np
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='static')
app.config['JSON_SORT_KEYS'] = False

# Serve static files
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

# Load models
try:
    model = joblib.load('models/california_housing_model.joblib')
    xgboost_model = joblib.load('models/xgboost_model.joblib')
    print("Models loaded successfully!")
except Exception as e:
    print(f"Error loading models: {e}")
    # Create dummy models if loading fails
    from sklearn.ensemble import RandomForestRegressor
    model = RandomForestRegressor()
    xgboost_model = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        features = np.array([[
            float(data['med_inc']),
            float(data['house_age']),
            float(data['avg_rooms']),
            float(data['avg_bedrooms']),
            float(data['population']),
            float(data['avg_occupancy']),
            float(data['latitude']),
            float(data['longitude'])
        ]])
        
        # Get predictions from both models
        rf_pred = float(model.predict(features)[0])
        xgb_pred = float(xgboost_model.predict(features)[0]) if xgboost_model else None
        
        return jsonify({
            'rf_prediction': rf_pred * 100000,  # Convert to actual price
            'xgb_prediction': xgb_pred * 100000 if xgboost_model else None,
            'status': 'success'
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 400

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring."""
    try:
        model_status = {
            'rf_model': model is not None,
            'xgb_model': xgboost_model is not None
        }
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'models': model_status
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

@app.route('/model-info')
def model_info():
    """Return information about loaded models."""
    info = {
        'models': {
            'random_forest': {
                'loaded': model is not None,
                'path': 'models/california_housing_model.joblib'
            },
            'xgboost': {
                'loaded': xgboost_model is not None,
                'path': 'models/xgboost_model.joblib'
            }
        },
        'features': [
            'MedInc', 'HouseAge', 'AveRooms', 'AveBedrms',
            'Population', 'AveOccup', 'Latitude', 'Longitude'
        ]
    }
    return jsonify(info)

if __name__ == '__main__':
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    logger.info("Starting Flask application...")
    logger.info(f"Random Forest model loaded: {model is not None}")
    logger.info(f"XGBoost model loaded: {xgboost_model is not None}")
    app.run(debug=True, host='0.0.0.0', port=5000)
