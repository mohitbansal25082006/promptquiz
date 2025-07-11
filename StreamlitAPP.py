import os
import json
import traceback
import pandas as pd
from io import BytesIO   
from dotenv import load_dotenv
import streamlit as st
from langchain_community.callbacks.manager import get_openai_callback
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.MCQGenerator import generate_and_evaluate
from src.mcqgenerator.logger import logging


# Load environment variables
load_dotenv()

# --------------------------- CONFIGURATION ---------------------------
st.set_page_config(
    page_title="💡 Smart MCQ Generator",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main {
        background: linear-gradient(to right, #f0f2f5, #d9e4f5);
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 0.4rem;
        font-size: 16px;
        padding: 0.5rem 1rem;
        transition: transform 0.2s ease;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        background-color: #45a049;
    }
    .stFileUploader label {
        font-weight: bold;
        color: #3f51b5;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------- LOAD JSON TEMPLATE --------------------------
try:
    with open("Response.json", "r") as file:
        RESPONSE_JSON = json.load(file)
except Exception as e:
    st.error("❌ Failed to load Response.json. Make sure the file exists.")
    logging.error(traceback.format_exc())
    st.stop()

# -------------------------- HEADER --------------------------
st.title("📚 AI-powered MCQ Generator")
st.markdown("""
    Welcome to the smart Multiple Choice Question generator app using LangChain and OpenAI.
    Upload educational content and generate clean, readable quizzes with a single click!
""")

# -------------------------- SIDEBAR --------------------------
st.sidebar.title("⚙️ Configuration")
st.sidebar.markdown("""
Upload your educational material and fine-tune how the questions are generated.
""")

with st.sidebar:
    tone = st.selectbox("🎯 Tone", ["Formal", "Conversational", "Informal"], index=0)
    subject = st.text_input("📘 Subject", value="General Knowledge")
    mcq_count = st.slider("🔢 Number of MCQs", min_value=3, max_value=50, value=5)

# -------------------------- MAIN INPUT FORM --------------------------
with st.form("upload_form"):
    st.subheader("📤 Upload File")
    uploaded_file = st.file_uploader("Choose a .pdf or .txt file", type=["pdf", "txt"])
    submitted = st.form_submit_button("🚀 Generate MCQs")

if submitted:
    if uploaded_file is None:
        st.warning("⚠️ Please upload a file to continue.")
        st.stop()

    try:
        text = read_file(uploaded_file)
        logging.info("File read successfully.")
    except Exception as e:
        st.error(f"❌ File reading error: {e}")
        logging.error(traceback.format_exc())
        st.stop()

    with st.spinner("⏳ Generating your MCQs using AI..."):
        try:
            with get_openai_callback() as cb:
                result = generate_and_evaluate(
                    text=text,
                    number=mcq_count,
                    subject=subject,
                    tone=tone,
                    response_json=json.dumps(RESPONSE_JSON)
                )

            quiz = result["quiz"]
            review = result["review"]

            st.success("✅ Successfully generated MCQs!")

            col1, col2 = st.columns(2)

            with col1:
                with st.expander("📄 View Raw Quiz JSON"):
                    st.json(json.loads(quiz))

            with col2:
                with st.expander("📝 View AI Evaluation"):
                    st.json(json.loads(review))

            # Table View
            st.subheader("📊 Quiz Table View")
            table_data = get_table_data(quiz)
            if table_data:
                df = pd.DataFrame(table_data)
                df = df.head(mcq_count)  # Ensure only mcq_count rows shown
                st.dataframe(df, use_container_width=True, height=400)
            else:
                st.warning("⚠️ Could not parse quiz into table format.")

        except Exception as e:
            st.error(f"❌ Error during quiz generation: {e}")
            logging.error(traceback.format_exc())

# -------------------------- FOOTER --------------------------
st.markdown("""
---
✨ Built with ❤️ using [LangChain](https://www.langchain.com/), [Streamlit](https://streamlit.io/), and [OpenAI](https://openai.com/).
""")
