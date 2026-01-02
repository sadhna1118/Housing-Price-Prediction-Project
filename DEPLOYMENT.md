# Deployment Guide

## Prerequisites

- Python 3.9 or higher
- pip package manager
- Virtual environment (recommended)
- Docker (optional, for containerized deployment)

## Local Deployment

### 1. Environment Setup

**Windows:**
```powershell
# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install --upgrade pip
pip install -r requirements_new.txt
```

**Linux/Mac:**
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements_new.txt
```

### 2. Train Models

Before running the application, ensure models are trained:

```bash
# Train the Random Forest model
python house_price_prediction.py

# Train the XGBoost model
python model_enhancement.py
```

This will create:
- `models/california_housing_model.joblib`
- `models/xgboost_model.joblib`
- Visualization plots in `visualizations/` and `static/`

### 3. Run the Application

**Development Mode:**
```bash
python app.py
```

The application will be available at `http://localhost:5000`

**Production Mode (using Gunicorn):**
```bash
gunicorn --bind 0.0.0.0:5000 app:app
```

## Docker Deployment

### 1. Build Docker Image

```bash
docker build -t housing-predictor .
```

### 2. Run Docker Container

```bash
docker run -p 5000:5000 housing-predictor
```

The application will be available at `http://localhost:5000`

### 3. Docker Compose (Optional)

Create a `docker-compose.yml` file:

```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./models:/app/models
      - ./static:/app/static
    environment:
      - FLASK_ENV=production
```

Run with:
```bash
docker-compose up
```

## Cloud Deployment

### Heroku

1. Install Heroku CLI
2. Create a `Procfile`:
   ```
   web: gunicorn app:app
   ```
3. Deploy:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### AWS EC2

1. Launch an EC2 instance (Ubuntu recommended)
2. SSH into the instance
3. Install dependencies:
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv
   ```
4. Clone your repository
5. Follow local deployment steps
6. Set up Nginx as reverse proxy (optional)

### Google Cloud Platform

1. Use App Engine or Cloud Run
2. Create `app.yaml`:
   ```yaml
   runtime: python39
   entrypoint: gunicorn -b :$PORT app:app
   ```
3. Deploy:
   ```bash
   gcloud app deploy
   ```

## Environment Variables

Create a `.env` file for configuration:

```env
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
MODEL_PATH=models/
```

## Troubleshooting

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### Model Loading Errors
Ensure models are trained before running the app:
```bash
python house_price_prediction.py
python model_enhancement.py
```

### Missing Dependencies
```bash
pip install -r requirements_new.txt --force-reinstall
```

## Performance Optimization

### Gunicorn Workers

For production, use multiple workers:
```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
```

### Nginx Configuration

Example Nginx config:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Monitoring

- Use application logs for debugging
- Monitor response times and error rates
- Set up health check endpoint (recommended)

## Security Considerations

1. Use environment variables for sensitive data
2. Enable HTTPS in production
3. Implement rate limiting
4. Keep dependencies updated
5. Use strong secret keys

## Backup

Regularly backup:
- Trained model files (`models/`)
- Configuration files
- Static assets (`static/`)
- Database (if applicable)