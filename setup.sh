#!/bin/bash

# LaTeX Converter AI - Complete Setup Script

echo "🚀 Setting up LaTeX Converter AI with Python Backend..."

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

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    print_error "Please run this script from the project root directory"
    exit 1
fi

print_status "Setting up Python Backend..."

# Backend setup
cd backend

# Check Python installation
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check LaTeX installation
if ! command -v pdflatex &> /dev/null; then
    print_warning "LaTeX is not installed. Installing TeX Live..."
    if command -v pacman &> /dev/null; then
        sudo pacman -S texlive-core texlive-latexextra --noconfirm
    elif command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y texlive-latex-base texlive-latex-extra texlive-fonts-recommended
    else
        print_error "Cannot install LaTeX automatically. Please install TeX Live manually."
        exit 1
    fi
fi

# Create virtual environment
if [ ! -d "venv" ]; then
    print_status "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install -r requirements.txt

# Create environment file if it doesn't exist
if [ ! -f ".env" ]; then
    print_status "Creating environment configuration..."
    cp config.env .env
    print_warning "Please edit backend/.env and add your OpenAI API key"
fi

print_status "Backend setup completed!"

# Frontend setup
print_status "Setting up React Frontend..."
cd ..

# Install Node.js dependencies
if [ ! -d "node_modules" ]; then
    print_status "Installing Node.js dependencies..."
    npm install
fi

# Create frontend environment file if it doesn't exist
if [ ! -f ".env" ]; then
    print_status "Creating frontend environment configuration..."
    cp frontend.env .env
fi

print_status "Frontend setup completed!"

# Create startup scripts
print_status "Creating startup scripts..."

# Backend startup script
cat > start-backend.sh << 'EOF'
#!/bin/bash
echo "Starting LaTeX Converter Backend..."
cd backend
source venv/bin/activate
python app/main.py
EOF

# Frontend startup script
cat > start-frontend.sh << 'EOF'
#!/bin/bash
echo "Starting LaTeX Converter Frontend..."
npm start
EOF

# Full startup script
cat > start-all.sh << 'EOF'
#!/bin/bash
echo "Starting LaTeX Converter AI (Backend + Frontend)..."

# Start backend in background
echo "Starting backend..."
cd backend
source venv/bin/activate
python app/main.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start frontend
echo "Starting frontend..."
cd ..
npm start &
FRONTEND_PID=$!

echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo "Press Ctrl+C to stop both services"

# Wait for user interrupt
trap "echo 'Stopping services...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
EOF

chmod +x start-backend.sh start-frontend.sh start-all.sh

print_status "Setup completed successfully!"
echo ""
echo "📋 Next Steps:"
echo "1. Edit backend/.env and add your OpenAI API key"
echo "2. Run './start-all.sh' to start both backend and frontend"
echo "3. Or run './start-backend.sh' and './start-frontend.sh' separately"
echo ""
echo "🌐 URLs:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:5000"
echo "   Health Check: http://localhost:5000/health"
echo ""
print_status "Happy coding! 🎉"
