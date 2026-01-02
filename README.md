# 🏠 California Housing Price Prediction

A comprehensive machine learning application for predicting California housing prices using Random Forest and XGBoost models. Features a modern web interface built with Flask and interactive visualizations.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.0+-orange.svg)](https://scikit-learn.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-1.5+-red.svg)](https://xgboost.readthedocs.io/)

## 🌟 Features

- **Dual Model Predictions**: Compare Random Forest and XGBoost model predictions
- **Interactive Web Interface**: User-friendly form for inputting property details
- **Real-time Predictions**: Instant price predictions via REST API
- **Data Visualizations**: Feature importance plots and model performance charts
- **Model Persistence**: Pre-trained models saved for quick predictions
- **Comprehensive Testing**: Full test suite with pytest
- **Docker Support**: Containerized deployment ready
- **Production Ready**: Gunicorn server configuration included

## 📊 Model Performance

### Random Forest Regressor
- **R² Score**: 0.8049
- **RMSE**: 0.5057
- **MAE**: 0.3278

### XGBoost Regressor
- **R² Score**: ~0.81
- **Hyperparameter Tuned**: GridSearchCV with cross-validation
- **Optimized Parameters**: Automatically selected

## 🚀 Quick Start

### Windows
```powershell
# Run the automated deployment script
.\deploy_windows.ps1
```

### Linux/Mac
```bash
# Run the deployment script
chmod +x deploy.sh
./deploy.sh
```

### Manual Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd predictive-analytics
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   .\venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements_new.txt
   ```

4. **Train models**
   ```bash
   python house_price_prediction.py
   python model_enhancement.py
   ```

5. **Run the application**
   ```bash
   # Development
   python app.py
   
   # Production
   gunicorn --bind 0.0.0.0:5000 app:app
   ```

6. **Access the application**
   ```
   http://localhost:5000
   ```

## 📁 Project Structure

```
predictive-analytics/
├── app.py                          # Flask web application
├── house_price_prediction.py       # Random Forest model training
├── model_enhancement.py            # XGBoost model training
├── test_app.py                     # Test suite
├── models/                         # Trained models
│   ├── california_housing_model.joblib
│   └── xgboost_model.joblib
├── static/                         # Static assets and visualizations
│   ├── feature_importance.png
│   ├── xgboost_feature_importance.png
│   ├── actual_vs_predicted.png
│   └── residual_plot.png
├── templates/                      # HTML templates
│   └── index.html
├── visualizations/                 # Generated plots
├── requirements_new.txt            # Python dependencies
├── Dockerfile                      # Docker configuration
├── deploy.sh                       # Linux/Mac deployment script
├── deploy_windows.ps1              # Windows deployment script
├── DEPLOYMENT.md                   # Deployment guide
├── API_DOCUMENTATION.md            # API documentation
└── README.md                       # This file
```

## 🔧 Usage

### Web Interface

1. Navigate to `http://localhost:5000`
2. Enter property details in the form:
   - Median Income
   - House Age
   - Average Rooms
   - Average Bedrooms
   - Population
   - Average Occupancy
   - Latitude
   - Longitude
3. Click "Predict House Price"
4. View predictions from both models with comparison chart

### API Usage

```python
import requests
import json

url = "http://localhost:5000/predict"

data = {
    "med_inc": 8.3252,
    "house_age": 41.0,
    "avg_rooms": 6.98412698,
    "avg_bedrooms": 1.02380952,
    "population": 322.0,
    "avg_occupancy": 2.55555556,
    "latitude": 37.88,
    "longitude": -122.23
}

response = requests.post(url, json=data)
result = response.json()

print(f"Random Forest: ${result['rf_prediction']:,.2f}")
print(f"XGBoost: ${result['xgb_prediction']:,.2f}")
```

### Command Line

```python
import joblib
import numpy as np

# Load models
rf_model = joblib.load('models/california_housing_model.joblib')
xgb_model = joblib.load('models/xgboost_model.joblib')

# Make prediction
sample = np.array([[8.3252, 41.0, 6.98, 1.02, 322.0, 2.56, 37.88, -122.23]])
rf_pred = rf_model.predict(sample)[0] * 100000
xgb_pred = xgb_model.predict(sample)[0] * 100000

print(f"Random Forest: ${rf_pred:,.2f}")
print(f"XGBoost: ${xgb_pred:,.2f}")
```

## 🧪 Testing

Run the test suite:

```bash
# Install pytest
pip install pytest

# Run all tests
python -m pytest test_app.py -v

# Run with coverage
pip install pytest-cov
python -m pytest test_app.py --cov=app --cov-report=html
```

## 🐳 Docker Deployment

```bash
# Build the image
docker build -t housing-predictor .

# Run the container
docker run -p 5000:5000 housing-predictor

# Access at http://localhost:5000
```

## 📚 Documentation

- **[API Documentation](API_DOCUMENTATION.md)**: Detailed API endpoints and usage
- **[Deployment Guide](DEPLOYMENT.md)**: Comprehensive deployment instructions
- **Jupyter Notebook**: `house_price_prediction.ipynb` for exploratory analysis

## 🔑 Input Features

| Feature | Description | Range |
|---------|-------------|-------|
| Median Income | Block group median income ($10,000s) | 0.5 - 15.0 |
| House Age | Median house age (years) | 1.0 - 52.0 |
| Average Rooms | Average rooms per household | 1.0 - 15.0 |
| Average Bedrooms | Average bedrooms per household | 0.5 - 10.0 |
| Population | Block group population | 3.0 - 35000.0 |
| Average Occupancy | Average household size | 0.5 - 10.0 |
| Latitude | Block group latitude | 32.5 - 42.0 |
| Longitude | Block group longitude | -124.5 - -114.0 |

## 🛠️ Technologies

- **Backend**: Flask, Gunicorn
- **ML Models**: scikit-learn, XGBoost
- **Data Processing**: pandas, NumPy
- **Visualization**: matplotlib, seaborn, Plotly
- **Frontend**: HTML, Tailwind CSS, JavaScript
- **Containerization**: Docker
- **Testing**: pytest

## 📈 Future Enhancements

- [ ] Add more regression models (LightGBM, CatBoost)
- [ ] Implement model versioning and A/B testing
- [ ] Add user authentication and API keys
- [ ] Create model monitoring dashboard
- [ ] Implement batch prediction endpoints
- [ ] Add explainability features (SHAP, LIME)
- [ ] Deploy to cloud platforms (AWS, GCP, Azure)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Dataset**: [California Housing Dataset](https://scikit-learn.org/stable/datasets/real_world.html#california-housing-dataset)
- **Frameworks**: scikit-learn, XGBoost, Flask
- **Visualization**: Plotly, matplotlib, seaborn

## 📧 Contact

For questions or feedback, please open an issue on the repository.
