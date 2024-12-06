from openai import OpenAI  # Updated import syntax
import PyPDF2
import os
import sys
from typing import List, Dict, Optional

class PDFAnalyzer:
    def __init__(self, api_key: str, categories: List[str]):
        """
        Initialize the PDF Analyzer with OpenAI API key and categories list.
        
        Args:
            api_key: OpenAI API key
            categories: List of possible categories (including "none")
        """
        self.categories = categories
        self.client = OpenAI(api_key=api_key)  # Updated initialization
        
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text content from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            str: Extracted text content
        """
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text
    
    def analyze_content(self, text: str) -> Dict[str, str]:
        """
        Analyze the content using OpenAI API to generate description and category.
        
        Args:
            text: Text content to analyze
            
        Returns:
            Dict containing description and category
        """
        # Create prompt for the AI
        categories_str = ", ".join(self.categories)
        prompt = f"""Analyze the following text and:
1. Create a brief description (max 100 words)
2. Categorize it into ONE of these categories: {categories_str}
If none of the categories fit, use "none"

Text to analyze:
{text[:1000]}...  # Truncate text to avoid token limits

Respond in this format:
Description: [your description]
Category: [selected category]"""

        # Call OpenAI API
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=200
        )
        
        # Parse response
        response_text = response.choices[0].message.content
        description = ""
        category = ""
        
        for line in response_text.split('\n'):
            if line.startswith('Description:'):
                description = line.replace('Description:', '').strip()
            elif line.startswith('Category:'):
                category = line.replace('Category:', '').strip()
        
        return {
            'description': description,
            'category': category
        }
    
    def process_pdf(self, pdf_path: str) -> Dict[str, str]:
        """
        Process a PDF file: extract text and analyze content.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dict containing the analysis results
        """
        text = self.extract_text_from_pdf(pdf_path)
        analysis = self.analyze_content(text)
        return {
            'filename': os.path.basename(pdf_path),
            'description': analysis['description'],
            'category': analysis['category']
        }

# Example usage
if __name__ == "__main__":
    # Define your categories
    categories = ["Technical", "Financial", "Legal", "Marketing", "Notes", "Lesson Plan", "none"]
    
    api_key_env = os.getenv("API_KEY_OPENAI")
    if not api_key_env:
        print("Error: API_KEY_OPENAI environment variable not set")
        sys.exit(1)

    # Initialize analyzer with your OpenAI API key
    analyzer = PDFAnalyzer(
        api_key=api_key_env,
        categories=categories
    )

    # Get path
    if len(sys.argv) != 2:
        path_src = "./document.pdf"
        print(f"no document specified, trying {path_src}")
    else:
        path_src = sys.argv[1]
    
    # Process a single PDF
    result = analyzer.process_pdf(path_src)
    print(f"Filename: {result['filename']}")
    print(f"Description: {result['description']}")
    print(f"Category: {result['category']}")
    
    # Process multiple PDFs in a directory
    def process_directory(directory_path: str) -> List[Dict[str, str]]:
        results = []
        for filename in os.listdir(directory_path):
            if filename.endswith('.pdf'):
                pdf_path = os.path.join(directory_path, filename)
                result = analyzer.process_pdf(pdf_path)
                results.append(result)
        return results
