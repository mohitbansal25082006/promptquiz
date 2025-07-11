import os
import json
import traceback
from io import BytesIO

import PyPDF2


def read_file(file):
    """
    Reads content from a PDF or TXT file-like object.
    
    Parameters:
        file: file-like object with .name and .read()
    
    Returns:
        text content as a string
    """
    if file.name.endswith(".pdf"):
        try:
            # PyPDF2 needs a file-like object
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return text.strip()
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            raise Exception("Error reading the PDF file.")
    
    elif file.name.endswith(".txt"):
        try:
            return file.read().decode("utf-8").strip()
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            raise Exception("Error reading the text file.")
    
    else:
        raise Exception("Unsupported file format. Only .pdf and .txt files are supported.")


def get_table_data(quiz_str):
    """
    Converts a JSON string of quiz data into a list of dictionaries suitable for tabular display.
    
    Parameters:
        quiz_str: JSON string representing the quiz
    
    Returns:
        list of dicts: [{MCQ, Choices, Correct}]
    """
    try:
        # Convert string to dictionary
        quiz_dict = json.loads(quiz_str)
        quiz_table_data = []
        
        # Extract data for each question
        for key, value in quiz_dict.items():
            mcq = value["mcq"]
            options = " || ".join(
                [f"{opt} -> {opt_text}" for opt, opt_text in value["options"].items()]
            )
            correct = value["correct"]
            quiz_table_data.append({
                "MCQ": mcq,
                "Choices": options,
                "Correct": correct
            })
        
        return quiz_table_data
    
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False
