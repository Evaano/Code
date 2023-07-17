import os
import pytesseract
from pdf2image import convert_from_path
import re

def extract_invoice_number(text):
    invoice_number = ""

    # Find the first occurrence of the patterns in the text
    for pattern in invoice_patterns:
        invoice_match = re.search(pattern, text, re.IGNORECASE)
        if invoice_match:
            invoice_number = invoice_match.group(1)
            break

    return invoice_number

def ocr_pdf_to_text(pdf_path, text_path):
    # Convert PDF to a single image
    images = convert_from_path(pdf_path, poppler_path=r"C:\Program Files\poppler\Library\bin")

    # Perform OCR on the image
    text = pytesseract.image_to_string(images[0], lang='eng')

    # Extract invoice number from the extracted text
    invoice_number = extract_invoice_number(text)

    # Save the invoice number to a text file
    with open(text_path, "w", encoding="utf-8") as file:
        file.write(f"Invoice Number: {invoice_number}\n")

# Define the invoice patterns and PO pattern
invoice_patterns = [r"INV-(\d+)"]
po_pattern = r"PO[-:]?\s?(\d+)"

# Get PDF and text file paths using os
pdf_path = os.path.join(os.getcwd(), "example.pdf")
text_path = os.path.join(os.getcwd(), "output.txt")

# Call the function
ocr_pdf_to_text(pdf_path, text_path)
