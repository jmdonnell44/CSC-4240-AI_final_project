"""
Text Extractor Module
Handles PDF and text file processing to extract raw text content.
"""

import pdfplumber
import os
from typing import Optional


class TextExtractor:
    """Extract text from PDF and text files."""
    
    def __init__(self):
        """Initialize the TextExtractor."""
        self.supported_formats = ['.pdf', '.txt']
    
    def extract_from_file(self, file_path: str) -> Optional[str]:
        """
        Extract text from a file (PDF or TXT).
        
        Args:
            file_path: Path to the file
            
        Returns:
            Extracted text as a string, or None if extraction fails
        """
        if not os.path.exists(file_path):
            print(f"Error: File not found: {file_path}")
            return None
        
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.pdf':
            return self._extract_from_pdf(file_path)
        elif file_ext == '.txt':
            return self._extract_from_txt(file_path)
        else:
            print(f"Error: Unsupported file format: {file_ext}")
            print(f"Supported formats: {', '.join(self.supported_formats)}")
            return None
    
    def _extract_from_pdf(self, pdf_path: str) -> Optional[str]:
        """
        Extract text from a PDF file using pdfplumber.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text as a string
        """
        try:
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                print(f"Processing PDF with {len(pdf.pages)} pages...")
                for page_num, page in enumerate(pdf.pages, 1):
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n\n"
                    if page_num % 10 == 0:
                        print(f"Processed {page_num}/{len(pdf.pages)} pages")
            
            print(f"✓ Successfully extracted {len(text)} characters from PDF")
            return text.strip()
        
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return None
    
    def _extract_from_txt(self, txt_path: str) -> Optional[str]:
        """
        Extract text from a plain text file.
        
        Args:
            txt_path: Path to the text file
            
        Returns:
            File contents as a string
        """
        try:
            with open(txt_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            print(f"✓ Successfully read {len(text)} characters from text file")
            return text.strip()
        
        except Exception as e:
            print(f"Error reading text file: {e}")
            return None
    
    def get_file_info(self, file_path: str) -> dict:
        """
        Get information about a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary with file information
        """
        if not os.path.exists(file_path):
            return {"error": "File not found"}
        
        file_size = os.path.getsize(file_path)
        file_ext = os.path.splitext(file_path)[1].lower()
        
        info = {
            "path": file_path,
            "size_bytes": file_size,
            "size_mb": round(file_size / (1024 * 1024), 2),
            "format": file_ext
        }
        
        # For PDFs, get page count
        if file_ext == '.pdf':
            try:
                with pdfplumber.open(file_path) as pdf:
                    info["pages"] = len(pdf.pages)
            except:
                info["pages"] = "Unknown"
        
        return info


if __name__ == "__main__":
    # Test the extractor
    extractor = TextExtractor()
    
    # Test with a sample file
    test_file = "/mnt/user-data/uploads/final_project_CSC4240_5240.pdf"
    
    if os.path.exists(test_file):
        info = extractor.get_file_info(test_file)
        print(f"\nFile Info: {info}")
        
        text = extractor.extract_from_file(test_file)
        if text:
            print(f"\nFirst 500 characters:\n{text[:500]}...")
    else:
        print(f"Test file not found: {test_file}")
