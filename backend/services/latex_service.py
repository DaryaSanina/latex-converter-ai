import os
import subprocess
import tempfile
import logging
import shutil
from pathlib import Path

logger = logging.getLogger(__name__)

class LaTeXService:
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
        self.latex_command = self._find_latex_command()
        
    def _find_latex_command(self):
        """Find the available LaTeX command"""
        commands = ['pdflatex', 'xelatex', 'lualatex']
        for cmd in commands:
            if shutil.which(cmd):
                logger.info(f"Using LaTeX command: {cmd}")
                return cmd
        raise Exception("No LaTeX command found. Please install TeX Live or MiKTeX")
    
    def compile_latex(self, latex_content):
        """Compile LaTeX content to PDF"""
        try:
            logger.info("Starting LaTeX compilation")
            
            # Create temporary files
            tex_file = os.path.join(self.temp_dir, "document.tex")
            pdf_file = os.path.join(self.temp_dir, "document.pdf")
            
            # Write LaTeX content to file
            with open(tex_file, 'w', encoding='utf-8') as f:
                f.write(latex_content)
            
            # Compile LaTeX to PDF
            pdf_result = self._compile_to_pdf(tex_file, pdf_file)
            
            result = {
                'success': pdf_result['success'],
                'error': pdf_result['error'],
                'pdf_path': pdf_file if pdf_result['success'] else None,
                'log': pdf_result.get('log', '')
            }
            
            logger.info(f"LaTeX compilation completed: success={result['success']}")
            return result
            
        except Exception as e:
            logger.error(f"Error in LaTeX compilation: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'pdf_path': None,
                'log': ''
            }
    
    def _compile_to_pdf(self, tex_file, pdf_file):
        """Compile LaTeX file to PDF"""
        try:
            # Run pdflatex command
            cmd = [
                self.latex_command,
                '-interaction=nonstopmode',
                '-output-directory', self.temp_dir,
                '-jobname', 'document',
                tex_file
            ]
            
            logger.info(f"Running command: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,  # 30 second timeout
                cwd=self.temp_dir
            )
            
            # Check if PDF was created
            if os.path.exists(pdf_file):
                logger.info("PDF compilation successful")
                return {
                    'success': True,
                    'error': None,
                    'log': result.stdout + result.stderr
                }
            else:
                error_msg = f"PDF compilation failed. Exit code: {result.returncode}"
                logger.error(f"{error_msg}\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}")
                return {
                    'success': False,
                    'error': error_msg,
                    'log': result.stdout + result.stderr
                }
                
        except subprocess.TimeoutExpired:
            error_msg = "LaTeX compilation timed out"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg,
                'log': 'Compilation timed out after 30 seconds'
            }
        except Exception as e:
            error_msg = f"LaTeX compilation error: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg,
                'log': str(e)
            }
    
    
    def cleanup(self):
        """Clean up temporary files"""
        try:
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
                logger.info("Cleaned up temporary files")
        except Exception as e:
            logger.error(f"Error cleaning up temporary files: {str(e)}")
    
    def __del__(self):
        """Destructor to clean up temporary files"""
        self.cleanup()
