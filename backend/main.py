from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import logging
import sys
from dotenv import load_dotenv
import base64
import tempfile
import shutil

# Load environment variables
load_dotenv()

# Add the current directory to Python path so we can import services
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.openai_service import OpenAIService
from services.latex_service import LaTeXService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize services
openai_service = OpenAIService()
latex_service = LaTeXService()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "LaTeX Converter API is running"})

@app.route('/pdf/<filename>', methods=['GET'])
def serve_pdf(filename):
    """Serve PDF files"""
    try:
        # Security check - only allow PDF files
        if not filename.endswith('.pdf'):
            return jsonify({"error": "Invalid file type"}), 400
        
        # Find the PDF file in the latex service temp directory
        pdf_path = os.path.join(latex_service.temp_dir, filename)
        
        if not os.path.exists(pdf_path):
            return jsonify({"error": "PDF file not found"}), 404
        
        return send_file(pdf_path, as_attachment=False, mimetype='application/pdf')
        
    except Exception as e:
        logger.error(f"Error serving PDF: {str(e)}")
        return jsonify({"error": f"Error serving PDF: {str(e)}"}), 500

@app.route('/convert', methods=['POST'])
def convert_to_latex():
    """Convert text to LaTeX and compile it with retry logic"""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({"error": "Missing 'text' field in request body"}), 400
        
        text_content = data['text']
        max_retries = 3
        
        logger.info(f"Processing text conversion request (length: {len(text_content)})")
        
        # Retry logic for LaTeX conversion and compilation
        for attempt in range(max_retries + 1):  # 0, 1, 2, 3 (total 4 attempts)
            try:
                if attempt == 0:
                    # First attempt: normal conversion
                    logger.info(f"Attempt {attempt + 1}: Converting text to LaTeX")
                    latex_content = openai_service.convert_to_latex(text_content)
                else:
                    # Retry attempts: use error feedback
                    logger.info(f"Attempt {attempt + 1}: Retrying with error feedback")
                    error_message = compilation_result.get('error', 'Unknown compilation error')
                    latex_content = openai_service.convert_with_error_feedback(text_content, error_message)
                
                if not latex_content:
                    logger.error(f"Attempt {attempt + 1}: Failed to convert text to LaTeX")
                    if attempt == max_retries:
                        return jsonify({"error": "Failed to convert text to LaTeX after all retries"}), 500
                    continue
                
                # Compile LaTeX to PDF
                logger.info(f"Attempt {attempt + 1}: Compiling LaTeX to PDF")
                compilation_result = latex_service.compile_latex(latex_content)
                
                # If compilation successful, break out of retry loop
                if compilation_result['success']:
                    logger.info(f"Attempt {attempt + 1}: LaTeX compilation successful")
                    break
                else:
                    logger.warning(f"Attempt {attempt + 1}: LaTeX compilation failed - {compilation_result.get('error', 'Unknown error')}")
                    if attempt == max_retries:
                        logger.error(f"All {max_retries + 1} attempts failed")
                        break
                    
            except Exception as e:
                logger.error(f"Attempt {attempt + 1}: Error during conversion/compilation: {str(e)}")
                if attempt == max_retries:
                    return jsonify({"error": f"Conversion failed after all retries: {str(e)}"}), 500
                continue
        
        # Add PDF URL if compilation was successful
        pdf_url = None
        if compilation_result['success'] and compilation_result['pdf_path']:
            pdf_filename = os.path.basename(compilation_result['pdf_path'])
            pdf_url = f"/pdf/{pdf_filename}"
        
        response_data = {
            "success": compilation_result['success'],
            "latex_content": latex_content,
            "compilation": compilation_result,
            "pdf_url": pdf_url,
            "attempts_used": attempt + 1
        }
        
        if compilation_result['success']:
            logger.info(f"Text conversion completed successfully after {attempt + 1} attempt(s)")
        else:
            logger.error(f"Text conversion failed after {attempt + 1} attempt(s)")
        
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Error in convert_to_latex: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.route('/compile', methods=['POST'])
def compile_latex():
    """Compile existing LaTeX content"""
    try:
        data = request.get_json()
        
        if not data or 'latex_content' not in data:
            return jsonify({"error": "Missing 'latex_content' field in request body"}), 400
        
        latex_content = data['latex_content']
        
        logger.info(f"Processing LaTeX compilation request (length: {len(latex_content)})")
        
        # Compile LaTeX
        compilation_result = latex_service.compile_latex(latex_content)
        
        # Add PDF URL if compilation was successful
        pdf_url = None
        if compilation_result['success'] and compilation_result['pdf_path']:
            pdf_filename = os.path.basename(compilation_result['pdf_path'])
            pdf_url = f"/pdf/{pdf_filename}"
        
        response_data = {
            "success": True,
            "compilation": compilation_result,
            "pdf_url": pdf_url
        }
        
        logger.info("LaTeX compilation completed")
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Error in compile_latex: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"Starting LaTeX Converter API on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
