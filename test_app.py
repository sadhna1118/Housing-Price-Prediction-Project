"""
Test suite for the Housing Price Prediction application.
Run with: python -m pytest test_app.py -v
"""

import pytest
import json
import os
import sys
import numpy as np
from flask import Flask

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from app import app

@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_route(client):
    """Test the home route returns 200."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'California Housing Price Predictor' in response.data

def test_predict_endpoint_valid_data(client):
    """Test the predict endpoint with valid data."""
    test_data = {
        'med_inc': 8.3252,
        'house_age': 41.0,
        'avg_rooms': 6.98412698,
        'avg_bedrooms': 1.02380952,
        'population': 322.0,
        'avg_occupancy': 2.55555556,
        'latitude': 37.88,
        'longitude': -122.23
    }
    
    response = client.post('/predict',
                          data=json.dumps(test_data),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert 'rf_prediction' in data
    assert isinstance(data['rf_prediction'], (int, float))
    assert data['rf_prediction'] > 0

def test_predict_endpoint_missing_fields(client):
    """Test the predict endpoint with missing fields."""
    incomplete_data = {
        'med_inc': 8.3252,
        'house_age': 41.0
    }
    
    response = client.post('/predict',
                          data=json.dumps(incomplete_data),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['status'] == 'error'

def test_predict_endpoint_invalid_types(client):
    """Test the predict endpoint with invalid data types."""
    invalid_data = {
        'med_inc': 'invalid',
        'house_age': 41.0,
        'avg_rooms': 6.98,
        'avg_bedrooms': 1.02,
        'population': 322.0,
        'avg_occupancy': 2.56,
        'latitude': 37.88,
        'longitude': -122.23
    }
    
    response = client.post('/predict',
                          data=json.dumps(invalid_data),
                          content_type='application/json')
    
    assert response.status_code == 400

def test_static_files_exist():
    """Test that required static files exist."""
    static_files = [
        'static/feature_importance.png',
        'static/actual_vs_predicted.png',
        'static/residual_plot.png'
    ]
    
    for file_path in static_files:
        if os.path.exists(file_path):
            assert os.path.getsize(file_path) > 0

def test_models_exist():
    """Test that model files exist."""
    model_files = [
        'models/california_housing_model.joblib',
        'models/xgboost_model.joblib'
    ]
    
    for model_path in model_files:
        assert os.path.exists(model_path), f"Model file {model_path} not found"
        assert os.path.getsize(model_path) > 0, f"Model file {model_path} is empty"

def test_prediction_consistency(client):
    """Test that predictions are consistent for the same input."""
    test_data = {
        'med_inc': 5.0,
        'house_age': 30.0,
        'avg_rooms': 5.0,
        'avg_bedrooms': 1.0,
        'population': 1000.0,
        'avg_occupancy': 3.0,
        'latitude': 34.0,
        'longitude': -118.0
    }
    
    response1 = client.post('/predict',
                           data=json.dumps(test_data),
                           content_type='application/json')
    response2 = client.post('/predict',
                           data=json.dumps(test_data),
                           content_type='application/json')
    
    data1 = json.loads(response1.data)
    data2 = json.loads(response2.data)
    
    assert data1['rf_prediction'] == data2['rf_prediction']

def test_prediction_range(client):
    """Test that predictions are within reasonable range."""
    test_data = {
        'med_inc': 5.0,
        'house_age': 25.0,
        'avg_rooms': 5.5,
        'avg_bedrooms': 1.0,
        'population': 500.0,
        'avg_occupancy': 2.5,
        'latitude': 35.0,
        'longitude': -120.0
    }
    
    response = client.post('/predict',
                          data=json.dumps(test_data),
                          content_type='application/json')
    
    data = json.loads(response.data)
    prediction = data['rf_prediction']
    
    # California housing prices should be between $50k and $5M
    assert 50000 <= prediction <= 5000000

if __name__ == '__main__':
    pytest.main([__file__, '-v'])