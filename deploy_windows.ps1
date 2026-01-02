# Windows PowerShell Deployment Script for Housing Price Predictor
# Run with: .\deploy_windows.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Housing Price Predictor - Deployment" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.9 or higher from https://www.python.org/downloads/" -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host "`nCreating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "Virtual environment already exists" -ForegroundColor Green
} else {
    python -m venv venv
    if ($?) {
        Write-Host "✓ Virtual environment created" -ForegroundColor Green
    } else {
        Write-Host "✗ Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
}

# Activate virtual environment
Write-Host "`nActivating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
Write-Host "✓ Virtual environment activated" -ForegroundColor Green

# Upgrade pip
Write-Host "`nUpgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet
Write-Host "✓ pip upgraded" -ForegroundColor Green

# Install dependencies
Write-Host "`nInstalling dependencies..." -ForegroundColor Yellow
pip install -r requirements_new.txt --quiet
if ($?) {
    Write-Host "✓ Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Create necessary directories
Write-Host "`nCreating directories..." -ForegroundColor Yellow
$directories = @("models", "static", "visualizations", "templates")
foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir | Out-Null
        Write-Host "✓ Created $dir directory" -ForegroundColor Green
    } else {
        Write-Host "✓ $dir directory exists" -ForegroundColor Green
    }
}

# Check if models exist
Write-Host "`nChecking for trained models..." -ForegroundColor Yellow
$modelsExist = $true
if (-not (Test-Path "models\california_housing_model.joblib")) {
    Write-Host "⚠ Random Forest model not found" -ForegroundColor Yellow
    $modelsExist = $false
}
if (-not (Test-Path "models\xgboost_model.joblib")) {
    Write-Host "⚠ XGBoost model not found" -ForegroundColor Yellow
    $modelsExist = $false
}

# Train models if they don't exist
if (-not $modelsExist) {
    Write-Host "`nTraining models (this may take several minutes)..." -ForegroundColor Yellow
    
    Write-Host "Training Random Forest model..." -ForegroundColor Yellow
    python house_price_prediction.py
    if ($?) {
        Write-Host "✓ Random Forest model trained" -ForegroundColor Green
    } else {
        Write-Host "✗ Failed to train Random Forest model" -ForegroundColor Red
    }
    
    Write-Host "Training XGBoost model..." -ForegroundColor Yellow
    python model_enhancement.py
    if ($?) {
        Write-Host "✓ XGBoost model trained" -ForegroundColor Green
    } else {
        Write-Host "✗ Failed to train XGBoost model" -ForegroundColor Red
    }
} else {
    Write-Host "✓ Models already trained" -ForegroundColor Green
}

# Copy visualization files to static folder
Write-Host "`nCopying visualizations to static folder..." -ForegroundColor Yellow
if (Test-Path "visualizations\*.png") {
    Copy-Item -Path "visualizations\*.png" -Destination "static\" -Force
    Write-Host "✓ Visualizations copied" -ForegroundColor Green
} else {
    Write-Host "⚠ No visualizations found to copy" -ForegroundColor Yellow
}

# Run tests (optional)
Write-Host "`nRunning tests..." -ForegroundColor Yellow
if (Test-Path "test_app.py") {
    pip install pytest --quiet
    python -m pytest test_app.py -v
    if ($?) {
        Write-Host "✓ All tests passed" -ForegroundColor Green
    } else {
        Write-Host "⚠ Some tests failed" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠ Test file not found, skipping tests" -ForegroundColor Yellow
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Deployment Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To start the application:" -ForegroundColor Yellow
Write-Host "  Development mode: python app.py" -ForegroundColor White
Write-Host "  Production mode:  gunicorn --bind 0.0.0.0:5000 app:app" -ForegroundColor White
Write-Host ""
Write-Host "The application will be available at:" -ForegroundColor Yellow
Write-Host "  http://localhost:5000" -ForegroundColor White
Write-Host ""

# Ask if user wants to start the application
$response = Read-Host "Do you want to start the application now? (Y/N)"
if ($response -eq 'Y' -or $response -eq 'y') {
    Write-Host "`nStarting Flask application..." -ForegroundColor Yellow
    python app.py
}