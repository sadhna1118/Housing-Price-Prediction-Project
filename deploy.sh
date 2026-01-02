#!/bin/bash

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Train the models
python model_enhancement.py

# Create static directory for images
mkdir -p static
cp visualizations/*.png static/

# Run the application
python app.py
