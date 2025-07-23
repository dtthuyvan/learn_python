import os
from google import genai
from google.genai import types
import pdfplumber

def read_file(folder, pdf_filename):
    # Tạo đường dẫn tuyệt đối đến file PDF
    pdf_path = os.path.join(folder, pdf_filename)
    
    summary = ""
    error = None

    try:
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"File '{pdf_filename}' not found in the 'static' folder.")

        extracted_text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    extracted_text += page_text + "\n"
        
        return extracted_text
            #prompt = f"Please provide a detailed summary of the following document:\n\n---\n\n{extracted_text}"
            #response = chat_model.generate_content(prompt)
            #summary = response.text

    except Exception as e:
        error = f"An error occurred: {e}"
        return None