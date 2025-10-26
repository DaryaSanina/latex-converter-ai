#!/bin/bash

# LaTeX Converter Backend Startup Script

echo "Starting LaTeX Converter Backend..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is not installed"
    exit 1
fi

# Check if LaTeX is installed
if ! command -v pdflatex &> /dev/null; then
    echo "Warning: pdflatex is not installed. Installing TeX Live..."
    # Install TeX Live (Ubuntu/Debian)
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y texlive-latex-base texlive-latex-extra texlive-fonts-recommended
    # Install TeX Live (Arch Linux)
    elif command -v pacman &> /dev/null; then
        sudo pacman -S texlive-core texlive-latexextra
    else
        echo "Error: Cannot install LaTeX automatically. Please install TeX Live manually."
        exit 1
    fi
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cat > .env << EOF
OPENAI_API_KEY=your_openai_api_key_here
FLASK_ENV=development
PORT=5000
EOF
    echo "Please edit .env file and add your OpenAI API key"
fi

# Start the Flask application
echo "Starting Flask application..."
export FLASK_APP=app/main.py
export FLASK_ENV=development
python -m flask run --host=0.0.0.0 --port=5000
