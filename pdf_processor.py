import PyPDF2
import io
import re

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text content from a PDF file
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        str: Extracted text content
        
    Raises:
        Exception: If PDF cannot be read or processed
    """
    try:
        text = ""
        
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Check if PDF is encrypted
            if pdf_reader.is_encrypted:
                raise Exception("PDF is encrypted and cannot be processed")
            
            # Extract text from all pages
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                
                if page_text:
                    text += page_text + "\n"
        
        # Clean up the text
        text = clean_extracted_text(text)
        
        if not text.strip():
            raise Exception("No readable text content found in PDF")
            
        return text
        
    except Exception as e:
        raise Exception(f"Error reading PDF: {str(e)}")

def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    """
    Extract text content from PDF bytes (for uploaded files)
    
    Args:
        pdf_bytes (bytes): PDF file content as bytes
        
    Returns:
        str: Extracted text content
        
    Raises:
        Exception: If PDF cannot be read or processed
    """
    try:
        text = ""
        
        pdf_file = io.BytesIO(pdf_bytes)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        # Check if PDF is encrypted
        if pdf_reader.is_encrypted:
            raise Exception("PDF is encrypted and cannot be processed")
        
        # Extract text from all pages
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()
            
            if page_text:
                text += page_text + "\n"
        
        # Clean up the text
        text = clean_extracted_text(text)
        
        if not text.strip():
            raise Exception("No readable text content found in PDF")
            
        return text
        
    except Exception as e:
        raise Exception(f"Error reading PDF: {str(e)}")

def clean_extracted_text(text: str) -> str:
    """
    Clean and normalize extracted text
    
    Args:
        text (str): Raw extracted text
        
    Returns:
        str: Cleaned text
    """
    if not text:
        return ""
    
    # Remove excessive whitespace and newlines
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        line = line.strip()
        if line:  # Skip empty lines
            cleaned_lines.append(line)
    
    # Join lines with single spaces
    cleaned_text = ' '.join(cleaned_lines)
    
    # Remove excessive spaces
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    
    return cleaned_text.strip()

def validate_pdf_file(file_path: str) -> bool:
    """
    Validate if a file is a valid PDF
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        bool: True if valid PDF, False otherwise
    """
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            # Try to access the first page to validate
            if len(pdf_reader.pages) > 0:
                return True
        return False
    except:
        return False
