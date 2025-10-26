# LaTeX Converter AI

A full-stack application that converts plain text to LaTeX using OpenAI's GPT-4 and compiles it using a Python backend with TeX Live.

## Features

- **Text to LaTeX Conversion**: Uses OpenAI GPT-4 to intelligently convert plain text to LaTeX
- **Real LaTeX Compilation**: Compiles LaTeX documents using TeX Live (pdflatex)
- **PDF to HTML Conversion**: Converts compiled PDFs to HTML for web display
- **Error Handling**: Comprehensive error handling with user-friendly warnings
- **Modern UI**: Clean, responsive React frontend with real-time feedback
- **Download Support**: Download generated LaTeX files

## Architecture

- **Frontend**: React application with modern UI components
- **Backend**: Python Flask API with OpenAI integration and LaTeX compilation
- **LaTeX Engine**: TeX Live with pdflatex for reliable compilation

## Quick Start

### Option 1: Automated Setup (Recommended)
```bash
./setup.sh
```

### Option 2: Manual Setup

#### Prerequisites
- Python 3.8+
- Node.js 16+
- TeX Live (for LaTeX compilation)
- OpenAI API key

#### Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp config.env .env
# Edit .env and add your OpenAI API key
python app/main.py
```

#### Frontend Setup
```bash
npm install
cp frontend.env .env
npm start
```

## Usage

1. **Start the application**:
   ```bash
   ./start-all.sh
   ```

2. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

3. **Convert text to LaTeX**:
   - Upload a text file or paste content
   - Click "Convert to LaTeX"
   - View the compiled result or raw LaTeX

## API Endpoints

### POST /convert
Convert text to LaTeX and compile it.

**Request**:
```json
{
  "text": "Your text content here"
}
```

**Response**:
```json
{
  "success": true,
  "latex_content": "\\documentclass{article}...",
  "compilation": {
    "success": true,
    "error": null,
    "html_content": "<div>...</div>",
    "log": "LaTeX compilation log"
  }
}
```

### POST /compile
Compile existing LaTeX content.

### GET /health
Health check endpoint.

## Configuration

### Backend Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key
- `FLASK_ENV`: Set to `development` for debug mode
- `PORT`: Backend port (default: 5000)

### Frontend Environment Variables
- `REACT_APP_API_URL`: Backend API URL (default: http://localhost:5000)

## Development

### Backend Development
```bash
cd backend
source venv/bin/activate
python app/main.py
```

### Frontend Development
```bash
npm start
```

### Running Tests
```bash
# Backend tests
cd backend
python -m pytest

# Frontend tests
npm test
```

## Deployment

### Production Backend
```bash
cd backend
source venv/bin/activate
gunicorn -w 4 -b 0.0.0.0:5000 app.main:app
```

### Production Frontend
```bash
npm run build
# Serve the build folder with a web server
```

## Troubleshooting

### LaTeX Compilation Issues
- Ensure TeX Live is properly installed
- Check that pdflatex is available in PATH
- Review compilation logs in the API response

### OpenAI API Issues
- Verify your API key is correct
- Check your OpenAI account credits
- Ensure the API key has proper permissions

### Backend Connection Issues
- Verify the backend is running on the correct port
- Check CORS settings if accessing from different domains
- Review backend logs for error details

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs for error details
3. Open an issue on GitHub