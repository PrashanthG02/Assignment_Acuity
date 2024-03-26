# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 20:38:49 2024

@author: Prashanth Kumar G

This Code is to perform QA testing using Tesseract OCR and SpaCy for NLP.it accept the input query and based on the 
keyword in the query it genarate the answer
"""
import fitz  # PyMuPDF for PDF processing
import pandas as pd  # Pandas for table processing
from pdf2image import convert_from_path  # Convert PDF to images
import pytesseract  # Tesseract OCR for text extraction
import spacy  # SpaCy for NLP

# Preprocessing: Extract text from plots and tables
def extract_text_from_plots_and_tables(pdf_path):
    text_data = []
    pdf_document = fitz.open(pdf_path)
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        page_text = page.get_text()
        # Store text data in a structured format
        text_data.append({"page_number": page_num, "text": page_text})
    return text_data

def preprocess_document(pdf_path):
    # Extract text from plots and tables
    text_data = extract_text_from_plots_and_tables(pdf_path)
    # Perform additional preprocessing tasks as needed
    return text_data

# Question Understanding
def parse_query(query):
    # Use SpaCy or other NLP tools for parsing the query
    # Identify keywords, entities, and intent
    parsed_query = {"keywords": ["taxes","Government", "revenue"], "intent": "plot"}
    return parsed_query

# Query Processing
def process_query(parsed_query, text_data):
    relevant_data = []
    for item in text_data:
        if parsed_query["intent"] == "plot" and any(keyword in item["text"] for keyword in parsed_query["keywords"]):
            relevant_data.append(item)
    return relevant_data

# Answer Generation
def generate_answer(relevant_data):
    answers = []
    for data in relevant_data:
        # Generate answers based on the relevant data
        answers.append(f"Page {data['page_number']}: {data['text']}")
    return answers

if __name__ == "__main__":
    pdf_path = "document.pdf"
    text_data = preprocess_document(pdf_path)

    # Example query
    query = "Show me the taxes trends."
    parsed_query = parse_query(query)
    relevant_data = process_query(parsed_query, text_data)
    answers = generate_answer(relevant_data)

    # Print answers
    for answer in answers:
        print(answer)
