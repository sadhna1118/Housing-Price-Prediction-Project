# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Setup (Choose One Method)

**Option A: Automated Deployment (Recommended)**

Windows:
```powershell
.\deploy_windows.ps1
```

Linux/Mac:
```bash
chmod +x deploy.sh
./deploy.sh
```

**Option B: Manual Setup**

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 3. Install dependencies
pip install -r requirements_new.txt

# 4. Train models (if not already trained)
python house_price_prediction.py
python model_enhancement.py
```

### Step 2: Run the Application

```bash
python app.py
```

### Step 3: Use the Application

**Web Browser:**
1. Open http://localhost:5000
2. Fill in the property details form
3. Click "Predict House Price"
4. View predictions from both models

**API (Python):**
```python
import requests

response = requests.post('http://localhost:5000/predict', json={
    "med_inc": 8.3,
    "house_age": 41,
    "avg_rooms": 6.98,
    "avg_bedrooms": 1.02,
    "population": 322,
    "avg_occupancy": 2.56,
    "latitude": 37.88,
    "longitude": -122.23
})

print(response.json())
```

**API (cURL):**
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"med_inc": 8.3, "house_age": 41, "avg_rooms": 6.98, "avg_bedrooms": 1.02, "population": 322, "avg_occupancy": 2.56, "latitude": 37.88, "longitude": -122.23}'
```

## 🐳 Docker Quick Start

```bash
# Build
docker build -t housing-predictor .

# Run
docker run -p 5000:5000 housing-predictor

# Access at http://localhost:5000
```

## ✅ Verify Installation

Check if everything is working:

```bash
# Test imports
python -c "import flask, sklearn, xgboost, plotly; print('✓ All dependencies OK')"

# Check models exist
python -c "import os; print('✓ Models OK' if os.path.exists('models/california_housing_model.joblib') else '✗ Train models first')"

# Run tests
python -m pytest test_app.py -v
```

## 🎯 Common Use Cases

### 1. Single Prediction
Use the web interface at http://localhost:5000

### 2. Batch Predictions
```python
import requests

properties = [
    {"med_inc": 8.3, "house_age": 41, ...},
    {"med_inc": 5.2, "house_age": 25, ...},
    # ... more properties
]

for prop in properties:
    response = requests.post('http://localhost:5000/predict', json=prop)
    print(response.json()['rf_prediction'])
```

### 3. Load Model Directly
```python
import joblib
import numpy as np

model = joblib.load('models/california_housing_model.joblib')
sample = np.array([[8.3, 41, 6.98, 1.02, 322, 2.56, 37.88, -122.23]])
price = model.predict(sample)[0] * 100000
print(f"${price:,.2f}")
```

## 📊 Understanding Results

The application returns predictions from two models:
- **Random Forest**: Ensemble learning method, robust and reliable
- **XGBoost**: Gradient boosting, often more accurate for complex patterns

Compare both predictions for confidence assessment.

## 🔧 Troubleshooting

**Port 5000 already in use:**
```bash
# Change port in app.py or:
python app.py --port 5001
```

**Models not found:**
```bash
python house_price_prediction.py
python model_enhancement.py
```

**Import errors:**
```bash
pip install -r requirements_new.txt --force-reinstall
```

## 📚 Next Steps

- Read [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for detailed API usage
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
- See [PROJECT_STATUS.md](PROJECT_STATUS.md) for complete project overview

## 💡 Tips

1. Use the health check endpoint to verify the app is running: http://localhost:5000/health
2. Check model info at: http://localhost:5000/model-info
3. Run tests regularly: `python -m pytest test_app.py -v`
4. Keep models updated by retraining periodically
5. Monitor logs for any prediction errors

## 🎉 You're Ready!

Your housing price prediction application is now ready to use. Start making predictions!