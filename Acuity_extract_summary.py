# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 20:38:49 2024

@author: Prashanth Kumar G

This Code is to extract the summary of the document and to store them in a JSON file
In this code it takes the pdf as input and then convert the pdf pages into an images, extract the text using 
OpenCV tool and using Tesseract OCR. Finally, it generate a JSON file which stores the summary of the document
"""

import cv2
from pdf2image import convert_from_path
import pytesseract
import json
import numpy as np

# Path to your PDF file
pdf_path = "document.pdf"

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract'

# Function to extract text from a page using Tesseract OCR
def extract_text_from_page(page):
    # Convert page to grayscale
    gray_page = cv2.cvtColor(page, cv2.COLOR_BGR2GRAY)
    
    # Use pytesseract to perform OCR
    text = pytesseract.image_to_string(gray_page)
    return text

# Function to detect tables and plots using image processing
def detect_tables_and_plots(page):       
    # detect rectangles (tables/plots) using contour detection
    gray_page = cv2.cvtColor(page, cv2.COLOR_BGR2GRAY)
    _, binary_page = cv2.threshold(gray_page, 0, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(binary_page, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # List to store bounding boxes of detected tables and plots
    bounding_boxes = []
    
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        bounding_boxes.append({"x": x, "y": y, "width": w, "height": h})
    
    return bounding_boxes

# Convert PDF to images
pages = convert_from_path(pdf_path)

# Dictionary to store plots and tables for each page
result_dict = {}

# Iterate through each page
for i, page in enumerate(pages, start=1):
    # Convert the page to a NumPy array
    page_np = np.array(page)
    
    # Extract text from the page
    text = extract_text_from_page(page_np)

    # Detect tables and plots in the page
    table_and_plot_boxes = detect_tables_and_plots(page_np)
    
    # Store the bounding boxes along with the page number
    result_dict[f"Page {i}"] = {"text": text, "tables_and_plots": table_and_plot_boxes}

# Write the result dictionary to a JSON file
output_file = "Acuity_Assignment_plots_and_tables_summary.json"
with open(output_file, "w") as json_file:
    json.dump(result_dict, json_file, indent=4)

print("JSON file created successfully.")
