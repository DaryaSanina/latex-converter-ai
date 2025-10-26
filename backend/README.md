# LaTeX Converter Backend

A Python Flask backend service that handles text-to-LaTeX conversion using OpenAI API and LaTeX compilation using TeX Live.

## ✅ Status: WORKING

The backend is now fully functional! The module import issues have been resolved.

## Quick Start

1. **Set up your OpenAI API key**:
   ```bash
   cd backend
   cp config.env .env
   # Edit .env and add your real OpenAI API key
   ```

2. **Start the backend**:
   ```bash
   ./start-backend.sh
   ```

3. **Test the API**:
   ```bash
   curl http://localhost:5000/health
   ```

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

Create a `.env` file with:
```
OPENAI_API_KEY=your_actual_openai_api_key_here
FLASK_ENV=development
PORT=5000
```

## Troubleshooting

### Module Import Errors
✅ **FIXED**: The "No module named 'services'" error has been resolved by:
- Moving main.py to the backend root directory
- Adding proper sys.path configuration
- Using compatible package versions

### OpenAI API Errors
- Ensure you have a valid OpenAI API key
- Check your OpenAI account credits
- Verify the API key has proper permissions

### LaTeX Compilation Errors
- Ensure TeX Live is installed: `which pdflatex`
- Check that pdflatex is available in PATH
- Review compilation logs in the API response

## Dependencies

- Python 3.8+
- TeX Live (for LaTeX compilation)
- OpenAI API key

## Package Versions

The following versions are tested and working:
- Flask==3.0.0
- Flask-CORS==4.0.0
- openai==1.12.0
- python-dotenv==1.0.0
- httpx==0.25.2

## Development

```bash
# Activate virtual environment
source venv/bin/activate

# Run in development mode
python main.py

# Run with gunicorn (production)
gunicorn -w 4 -b 0.0.0.0:5000 main:app
```

## Testing

Test the API endpoints:

```bash
# Health check
curl http://localhost:5000/health

# Convert text (requires valid OpenAI API key)
curl -X POST http://localhost:5000/convert \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world"}'
```

## Logs

The application logs all operations to stdout with appropriate log levels:
- `INFO`: Normal operations
- `ERROR`: Errors and exceptions
- `WARNING`: Non-critical issues

## Next Steps

1. Add your real OpenAI API key to `.env`
2. Start the backend: `./start-backend.sh`
3. Start the frontend: `npm start` (from project root)
4. Access the application at http://localhost:3000