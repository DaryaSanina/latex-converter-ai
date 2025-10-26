# Troubleshooting Guide

## Common Issues and Solutions

### 1. Port 5000 Already in Use

**Problem**: `Address already in use` error when starting the backend.

**Solution**:
```bash
cd backend
./manage-port.sh kill
./start-backend.sh
```

**Manual Solution**:
```bash
# Find what's using port 5000
ss -tlnp | grep :5000

# Kill the process (replace PID with actual process ID)
kill <PID>

# Or force kill if needed
kill -9 <PID>
```

### 2. API Key Not Working

**Problem**: "Incorrect API key provided" or "test_key" error.

**Solution**:
```bash
cd backend
./setup-api-key.sh
```

**Manual Solution**:
1. Get your API key from: https://platform.openai.com/account/api-keys
2. Edit the `.env` file:
   ```bash
   nano .env
   ```
3. Replace `your_openai_api_key_here` with your actual key:
   ```
   OPENAI_API_KEY=sk-your-actual-key-here
   ```

### 3. Module Import Errors

**Problem**: "No module named 'services'" error.

**Solution**: This has been fixed! If you still see this error:
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### 4. LaTeX Compilation Errors

**Problem**: LaTeX compilation fails.

**Check LaTeX Installation**:
```bash
which pdflatex
pdflatex --version
```

**Install LaTeX** (if missing):
```bash
# Arch Linux
sudo pacman -S texlive-core texlive-latexextra

# Ubuntu/Debian
sudo apt-get install texlive-latex-base texlive-latex-extra texlive-fonts-recommended
```

### 5. Frontend Can't Connect to Backend

**Problem**: Frontend shows connection errors.

**Check Backend Status**:
```bash
curl http://localhost:5000/health
```

**Check Frontend Configuration**:
```bash
# Make sure .env file exists in project root
cat .env
# Should contain: REACT_APP_API_URL=http://localhost:5000
```

### 6. Permission Errors

**Problem**: Permission denied when running scripts.

**Solution**:
```bash
chmod +x backend/*.sh
chmod +x *.sh
```

## Quick Fix Commands

```bash
# Complete reset and restart
cd backend
./manage-port.sh kill
./setup-api-key.sh  # Follow prompts to set API key
./start-backend.sh

# In another terminal, start frontend
npm start
```

## Verification Steps

1. **Backend Health Check**:
   ```bash
   curl http://localhost:5000/health
   # Should return: {"status":"healthy","message":"LaTeX Converter API is running"}
   ```

2. **Test API Endpoint**:
   ```bash
   curl -X POST http://localhost:5000/convert \
     -H "Content-Type: application/json" \
     -d '{"text": "Hello world"}'
   ```

3. **Frontend Access**:
   - Open http://localhost:3000
   - Upload a text file or paste content
   - Click "Convert to LaTeX"

## Getting Help

If you're still having issues:

1. Check the logs in the terminal where you started the backend
2. Check browser console for frontend errors
3. Verify all environment variables are set correctly
4. Make sure all dependencies are installed

## Environment Files

**Backend (.env)**:
```
OPENAI_API_KEY=sk-your-actual-key-here
FLASK_ENV=development
PORT=5000
```

**Frontend (.env)**:
```
REACT_APP_API_URL=http://localhost:5000
```
