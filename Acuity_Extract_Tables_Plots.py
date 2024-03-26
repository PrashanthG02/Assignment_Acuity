# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 20:38:49 2024

@author: Prashanth Kumar G

This Code is to find the page numbers of tables and plots, to store them in a JSON file
In this code it takes the pdf as input and then convert the pdf pages into an images,
and iterate through each page to extract the text using Tesseract OCR. Finally, it generate
a JSON file which stores in dictionary form which contrains page number, tables and plots in that page
"""
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import json

# Path to your PDF file
pdf_path = "document.pdf"

# Initialize Tesseract OCR
# You may need to adjust the path to Tesseract executable accordingly
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract'

# Initialize empty dictionary to store positions of tables and plots
plots_and_tables = {}

# Open the PDF file
pdf_document = fitz.open(pdf_path)

# Iterate through each page of the PDF
for page_number in range(len(pdf_document)):
    # Load the page
    page = pdf_document.load_page(page_number)
    
    # Convert the page to an image
    pix = page.get_pixmap()
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    
    # Extract text using Tesseract OCR
    text = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    
    # Initialize lists to store bounding boxes of tables and plots
    tables = []
    plots = []
    
    # Iterate through OCR results to identify tables and plots
    for i, conf in enumerate(text['conf']):
        if int(conf) > 80:  # Confidence threshold
            x = text['left'][i]
            y = text['top'][i]
            width = text['width'][i]
            height = text['height'][i]
            
            # Check if the extracted text indicates a table or plot (you may need to adapt this based on your document)
            if "table" in text['text'][i].lower():
                tables.append({"x": x, "y": y, "width": width, "height": height})
            elif "figure" in text['text'][i].lower():
                plots.append({"x": x, "y": y, "width": width, "height": height})
    
    # Store positions of tables and plots for the current page
    plots_and_tables[str(page_number+1)] = {"tables": tables, "plots": plots}

# Save the positions of tables and plots as a JSON file
with open("Acuity_Assignement1_plots_and_tables.json", "w") as json_file:
    json.dump(plots_and_tables, json_file, indent=4)

print("Extraction completed. JSON file saved successfully.")

