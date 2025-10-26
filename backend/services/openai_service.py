import os
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.system_prompt = """You are an experienced LaTeX converter.
You convert the text file you are given into LaTeX. You need to infer equation, tables, and other elements from the text to make the LaTeX as neat as possible. DO NOT write any of your own content, just work with what the user has already written.
Input format: contents of a text file that needs to be converted into LaTeX.
Output format: the text file converted into LaTeX. The LaTeX file should be a valid LaTeX file that can be compiled using LaTeX."""

    def convert_to_latex(self, text_content):
        """Convert text content to LaTeX using OpenAI API"""
        try:
            logger.info("Starting OpenAI conversion")
            
            response = self.client.chat.completions.create(
                model="gpt-5",  # Using a more reliable model
                messages=[
                    {
                        "role": "system",
                        "content": self.system_prompt
                    },
                    {
                        "role": "user",
                        "content": text_content
                    }
                ]
            )
            
            latex_content = response.choices[0].message.content.strip()
            logger.info(f"OpenAI conversion completed successfully (length: {len(latex_content)})")
            
            return latex_content
            
        except Exception as e:
            logger.error(f"Error in OpenAI conversion: {str(e)}")
            raise Exception(f"OpenAI conversion failed: {str(e)}")

    def convert_with_error_feedback(self, text_content, compilation_error):
        """Convert text to LaTeX with compilation error feedback"""
        try:
            logger.info("Starting OpenAI conversion with error feedback")
            
            enhanced_prompt = self.system_prompt + f"""

IMPORTANT: The previous LaTeX output had compilation errors. Please fix the following issues and provide valid LaTeX that can be compiled:

Compilation Error: {compilation_error}

Please ensure the LaTeX syntax is correct and all required packages are properly referenced."""
            
            response = self.client.chat.completions.create(
                model="gpt-5",
                messages=[
                    {
                        "role": "system",
                        "content": enhanced_prompt
                    },
                    {
                        "role": "user",
                        "content": text_content
                    }
                ]
            )
            
            latex_content = response.choices[0].message.content.strip()
            logger.info(f"OpenAI conversion with error feedback completed (length: {len(latex_content)})")
            
            return latex_content
            
        except Exception as e:
            logger.error(f"Error in OpenAI conversion with error feedback: {str(e)}")
            raise Exception(f"OpenAI conversion with error feedback failed: {str(e)}")
