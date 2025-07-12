import json
import traceback
import streamlit as st

# Optional: Logging if you want to track errors
from src.mcqgenerator.logger import logging

# Importing necessary packages from LangChain
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# Read the OpenAI API key securely
key = st.secrets["OPENAI_API_KEY"]

# Initialize the OpenAI Chat Model
llm = ChatOpenAI(
    openai_api_key=key,
    model="gpt-3.5-turbo",
    temperature=0.7
)

# Prompt template for quiz generation
template = """
Text: {text}
You are an expert MCQ maker. Given the above text, it is your job to 
create a quiz of {number} multiple choice questions for {subject} students in {tone} tone.
Make sure the questions are not repeated and check all the questions to be conforming to the text as well.
Make sure to format your response like RESPONSE_JSON below and use it as a guide.
Ensure to make {number} MCQs.

### RESPONSE_JSON
{response_json}
"""

quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "response_json"],
    template=template
)

# Prompt template for quiz evaluation
template2 = """
You are an expert English grammarian and writer.

Given the following multiple-choice quiz intended for {subject} students:

### Quiz MCQs:
{quiz}

**Instructions:**
1. Evaluate the complexity of the quiz and provide a short analysis (maximum 50 words) describing whether the questions are appropriate for the cognitive and analytical abilities of the students.
2. If any questions are too difficult, too simple, or inappropriate, rewrite only those questions so they are better suited to the target students. Use a clear and consistent tone appropriate for {subject} students.
3. If no changes are needed, simply state "All questions are appropriate."

**Response Format:**
Return your answer as a JSON object with the following fields:

{
  "complexity_analysis": "Your 50-word analysis here.",
  "updated_quiz": "The updated quiz here if any questions were changed, otherwise write 'No changes needed.'"
}
"""

quiz_evaluation_prompt = PromptTemplate(
    input_variables=["subject", "quiz"],
    template=template2
)

# Modern chain definitions using pipe syntax
quiz_chain = quiz_generation_prompt | llm | StrOutputParser()
review_chain = quiz_evaluation_prompt | llm | StrOutputParser()

# A function to generate and evaluate the quiz
def generate_and_evaluate(text, number, subject, tone, response_json):
    try:
        quiz_result = quiz_chain.invoke({
            "text": text,
            "number": str(number),
            "subject": subject,
            "tone": tone,
            "response_json": response_json
        })

        review_result = review_chain.invoke({
            "subject": subject,
            "quiz": quiz_result
        })

        return {
            "quiz": quiz_result,
            "review": review_result
        }

    except Exception as e:
        # Return the error so Streamlit can display it
        logging.error(f"Error during generation and evaluation: {traceback.format_exc()}")
        return {
            "error": f"{type(e).__name__}: {str(e)}"
        }
