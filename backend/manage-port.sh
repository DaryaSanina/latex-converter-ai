#!/bin/bash

# LaTeX Converter AI - Port Management Script

echo "🔌 Managing Port 5000 for LaTeX Converter AI"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
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

# Function to check what's using port 5000
check_port() {
    echo "Checking what's using port 5000..."
    
    # Try different methods to check the port
    if command -v ss &> /dev/null; then
        PORT_INFO=$(ss -tlnp | grep :5000)
    elif command -v netstat &> /dev/null; then
        PORT_INFO=$(netstat -tlnp | grep :5000)
    elif command -v lsof &> /dev/null; then
        PORT_INFO=$(lsof -i :5000)
    else
        print_error "No port checking tools available (ss, netstat, lsof)"
        return 1
    fi
    
    if [ -z "$PORT_INFO" ]; then
        print_status "Port 5000 is free"
        return 0
    else
        print_warning "Port 5000 is in use:"
        echo "$PORT_INFO"
        return 1
    fi
}

# Function to kill processes on port 5000
kill_port_processes() {
    echo "Attempting to free port 5000..."
    
    # Try to find and kill processes using port 5000
    if command -v ss &> /dev/null; then
        PIDS=$(ss -tlnp | grep :5000 | grep -o 'pid=[0-9]*' | cut -d'=' -f2)
    elif command -v netstat &> /dev/null; then
        PIDS=$(netstat -tlnp | grep :5000 | grep -o '[0-9]*/python' | cut -d'/' -f1)
    elif command -v lsof &> /dev/null; then
        PIDS=$(lsof -ti :5000)
    else
        print_error "No tools available to find processes on port 5000"
        return 1
    fi
    
    if [ -z "$PIDS" ]; then
        print_status "No processes found on port 5000"
        return 0
    fi
    
    for PID in $PIDS; do
        print_warning "Killing process $PID on port 5000..."
        kill $PID
        sleep 1
        
        # Check if process is still running
        if kill -0 $PID 2>/dev/null; then
            print_warning "Process $PID still running, force killing..."
            kill -9 $PID
        fi
    done
    
    sleep 2
    check_port
}

# Main script logic
case "${1:-check}" in
    "check")
        check_port
        ;;
    "kill")
        kill_port_processes
        ;;
    "free")
        kill_port_processes
        ;;
    *)
        echo "Usage: $0 {check|kill|free}"
        echo ""
        echo "Commands:"
        echo "  check  - Check what's using port 5000"
        echo "  kill   - Kill processes using port 5000"
        echo "  free   - Same as kill"
        echo ""
        check_port
        ;;
esac
