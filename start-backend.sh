#!/bin/bash
echo "Starting LaTeX Converter Backend..."
cd backend
source venv/bin/activate
python app/main.py
