#!/bin/bash

# LaTeX Converter AI - API Key Setup Script

echo "🔑 Setting up OpenAI API Key for LaTeX Converter AI"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

# Check if we're in the backend directory
if [ ! -f "main.py" ]; then
    print_error "Please run this script from the backend directory"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_status "Creating .env file from template..."
    cp config.env .env
fi

# Check current API key
CURRENT_KEY=$(grep "OPENAI_API_KEY" .env | cut -d'=' -f2)

if [ "$CURRENT_KEY" = "your_openai_api_key_here" ]; then
    print_warning "You need to add your OpenAI API key to the .env file"
    echo ""
    print_info "To get your OpenAI API key:"
    print_info "1. Go to: https://platform.openai.com/account/api-keys"
    print_info "2. Sign in to your OpenAI account"
    print_info "3. Click 'Create new secret key'"
    print_info "4. Copy the generated key"
    echo ""
    print_info "Then edit the .env file and replace 'your_openai_api_key_here' with your actual key"
    echo ""
    print_status "Opening .env file for editing..."
    
    # Try to open with different editors
    if command -v nano &> /dev/null; then
        nano .env
    elif command -v vim &> /dev/null; then
        vim .env
    elif command -v code &> /dev/null; then
        code .env
    else
        print_info "Please edit the .env file manually with your preferred editor"
        print_info "File location: $(pwd)/.env"
    fi
    
    echo ""
    print_status "After editing the .env file, you can start the backend with:"
    print_status "./start-backend.sh"
    
else
    print_status "API key is already set in .env file"
    print_status "You can start the backend with: ./start-backend.sh"
fi
