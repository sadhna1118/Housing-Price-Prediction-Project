# API Documentation

## Base URL
```
http://localhost:5000
```

## Endpoints

### 1. Home Page
```
GET /
```

**Description:** Returns the main web interface for the housing price predictor.

**Response:**
- Status Code: 200
- Content-Type: text/html
- Body: HTML page with prediction form and visualization displays

---

### 2. Predict House Price
```
POST /predict
```

**Description:** Predicts California housing prices using trained Random Forest and XGBoost models.

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "med_inc": 8.3252,
  "house_age": 41.0,
  "avg_rooms": 6.98412698,
  "avg_bedrooms": 1.02380952,
  "population": 322.0,
  "avg_occupancy": 2.55555556,
  "latitude": 37.88,
  "longitude": -122.23
}
```

**Parameters:**

| Parameter | Type | Required | Description | Range |
|-----------|------|----------|-------------|-------|
| med_inc | float | Yes | Median income in block group (in $10,000s) | 0.5 - 15.0 |
| house_age | float | Yes | Median house age in block group (years) | 1.0 - 52.0 |
| avg_rooms | float | Yes | Average number of rooms per household | 1.0 - 15.0 |
| avg_bedrooms | float | Yes | Average number of bedrooms per household | 0.5 - 10.0 |
| population | float | Yes | Block group population | 3.0 - 35000.0 |
| avg_occupancy | float | Yes | Average household size | 0.5 - 10.0 |
| latitude | float | Yes | Block group latitude | 32.5 - 42.0 |
| longitude | float | Yes | Block group longitude | -124.5 - -114.0 |

**Success Response:**
```json
{
  "rf_prediction": 452600.0,
  "xgb_prediction": 445800.0,
  "status": "success"
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| rf_prediction | float | Predicted price from Random Forest model (in USD) |
| xgb_prediction | float or null | Predicted price from XGBoost model (in USD), null if model unavailable |
| status | string | "success" if prediction was successful |

**Error Response:**
```json
{
  "error": "Error message describing what went wrong",
  "status": "error"
}
```

**Status Codes:**
- 200: Successful prediction
- 400: Bad request (invalid input data)
- 500: Internal server error

---

### 3. Serve Static Files
```
GET /static/<filename>
```

**Description:** Serves static files like images and visualizations.

**Parameters:**
- `filename`: Name of the static file (e.g., feature_importance.png)

**Example:**
```
GET /static/feature_importance.png
```

**Response:**
- Status Code: 200
- Content-Type: image/png (for images)
- Body: File content

---

## Usage Examples

### cURL

**Basic Prediction:**
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "med_inc": 8.3,
    "house_age": 41,
    "avg_rooms": 6.98,
    "avg_bedrooms": 1.02,
    "population": 322,
    "avg_occupancy": 2.56,
    "latitude": 37.88,
    "longitude": -122.23
  }'
```

### Python (requests)

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

headers = {"Content-Type": "application/json"}

response = requests.post(url, data=json.dumps(data), headers=headers)
result = response.json()

print(f"Random Forest Prediction: ${result['rf_prediction']:,.2f}")
if result['xgb_prediction']:
    print(f"XGBoost Prediction: ${result['xgb_prediction']:,.2f}")
```

### JavaScript (Fetch API)

```javascript
const url = "http://localhost:5000/predict";

const data = {
  med_inc: 8.3252,
  house_age: 41.0,
  avg_rooms: 6.98412698,
  avg_bedrooms: 1.02380952,
  population: 322.0,
  avg_occupancy: 2.55555556,
  latitude: 37.88,
  longitude: -122.23
};

fetch(url, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(data)
})
  .then(response => response.json())
  .then(result => {
    console.log('Random Forest:', result.rf_prediction);
    console.log('XGBoost:', result.xgb_prediction);
  })
  .catch(error => console.error('Error:', error));
```

## Feature Descriptions

### Input Features

1. **Median Income (med_inc)**: The median income of households in the block group, measured in tens of thousands of dollars.

2. **House Age (house_age)**: The median age of houses in the block group, measured in years.

3. **Average Rooms (avg_rooms)**: The average number of rooms per household in the block group.

4. **Average Bedrooms (avg_bedrooms)**: The average number of bedrooms per household in the block group.

5. **Population (population)**: The total population in the block group.

6. **Average Occupancy (avg_occupancy)**: The average number of household members (population/households).

7. **Latitude (latitude)**: The geographical latitude of the block group.

8. **Longitude (longitude)**: The geographical longitude of the block group.

## Model Information

### Random Forest Regressor
- **Algorithm**: Ensemble of decision trees
- **Training Dataset**: California Housing Dataset from scikit-learn
- **Performance Metrics**:
  - R² Score: ~0.80
  - RMSE: ~0.51
  - MAE: ~0.33

### XGBoost Regressor
- **Algorithm**: Gradient boosted decision trees
- **Training Dataset**: California Housing Dataset from scikit-learn
- **Hyperparameter Tuning**: GridSearchCV with cross-validation
- **Performance Metrics**: Comparable to Random Forest with slight variations

## Error Handling

### Common Errors

1. **Missing Required Fields**
   - Status: 400
   - Solution: Ensure all 8 required parameters are included

2. **Invalid Data Types**
   - Status: 400
   - Solution: All parameters must be numeric (float or int)

3. **Out of Range Values**
   - Status: May return prediction but with lower confidence
   - Solution: Use values within the specified ranges

4. **Model Not Loaded**
   - Status: 500
   - Solution: Ensure models are trained and saved in the `models/` directory

## Rate Limiting

Currently, there is no rate limiting implemented. For production deployment, consider implementing rate limiting to prevent abuse.

## CORS

CORS is not enabled by default. To enable for cross-origin requests, modify the Flask app configuration.

## Authentication

No authentication is currently required. For production deployment, consider adding authentication for the API endpoints.