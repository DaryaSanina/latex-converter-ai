from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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

@app.route('/convert', methods=['POST'])
def convert_to_latex():
    """Convert text to LaTeX and compile it"""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({"error": "Missing 'text' field in request body"}), 400
        
        text_content = data['text']
        
        logger.info(f"Processing text conversion request (length: {len(text_content)})")
        
        # Step 1: Convert text to LaTeX using OpenAI
        latex_content = openai_service.convert_to_latex(text_content)
        
        if not latex_content:
            return jsonify({"error": "Failed to convert text to LaTeX"}), 500
        
        # Step 2: Compile LaTeX to PDF and HTML
        compilation_result = latex_service.compile_latex(latex_content)
        
        response_data = {
            "success": True,
            "latex_content": latex_content,
            "compilation": compilation_result
        }
        
        logger.info("Text conversion completed successfully")
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
        
        response_data = {
            "success": True,
            "compilation": compilation_result
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
