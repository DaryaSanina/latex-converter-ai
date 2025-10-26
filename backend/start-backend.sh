#!/bin/bash

# LaTeX Converter AI - Backend Startup Script

echo "🚀 Starting LaTeX Converter Backend..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the backend directory
if [ ! -f "main.py" ]; then
    print_error "Please run this script from the backend directory"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_error "Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_warning ".env file not found. Creating from template..."
    cp config.env .env
    print_warning "Please edit .env and add your OpenAI API key before starting the backend"
    exit 1
fi

# Check if OpenAI API key is set
if grep -q "your_openai_api_key_here" .env; then
    print_error "Please edit .env file and add your real OpenAI API key"
    print_error "You can get your API key from: https://platform.openai.com/account/api-keys"
    exit 1
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Check if LaTeX is installed
if ! command -v pdflatex &> /dev/null; then
    print_error "LaTeX (pdflatex) is not installed. Please install TeX Live first."
    print_error "Arch Linux: sudo pacman -S texlive-core texlive-latexextra"
    print_error "Ubuntu/Debian: sudo apt-get install texlive-latex-base texlive-latex-extra"
    exit 1
fi

# Start the Flask application
print_status "Starting LaTeX Converter Backend API..."
print_status "Backend will be available at: http://localhost:5000"
print_status "Health check: http://localhost:5000/health"
print_status "Press Ctrl+C to stop the server"
echo ""

python main.py
