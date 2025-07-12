# AI-Powered MCQ Generator

This is a fully functional web-based application built using Streamlit and LangChain that allows users to upload educational content (PDF or TXT), and generate high-quality multiple-choice questions (MCQs) using OpenAI's LLM APIs. The app supports dynamic tone, subject configuration, and a clean table view for quiz output.



##  Live Demo

👉 **Try it here:**  
[🧪 Try the Smart MCQ Generator Live](https://promptquiz-bgcuzrmvstfn2hixdv96dg.streamlit.app/)


##  Project Overview

This application leverages powerful AI models through LangChain to generate exam-ready MCQs. It is ideal for educators, trainers, or content creators who want to convert raw notes or reading material into structured quizzes instantly.



##  Features

- Upload `.pdf` or `.txt` educational files
- Extract content automatically using `PyPDF2` or standard text decoding
- Configure subject, tone, and number of MCQs
- Generate MCQs using OpenAI API with LangChain
- Display quiz in:
  - JSON format
  - Table format (clean, structured)
  - Evaluation summary
- Built-in UI animations for smooth experience
- Professional styling with gradient themes and hover effects



##  Tech Stack

- **Frontend/UI**: Streamlit (Custom styled with CSS)
- **Backend Logic**: LangChain, OpenAI, Python
- **Data Processing**: Pandas, JSON, PyPDF2
- **Environment Management**: Anaconda / Virtualenv
- **Logging**: Python logging module
- **Deployment Ready**: Localhost, Streamlit Share, or any cloud VM



## Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/mohitbansal25082006/promptquiz.git
   cd promptquiz
   ```

2. **Create and Activate a Virtual Environment (Anaconda)**
   ```bash
   conda create -p ./env python=3.10 -y
   conda activate ./env
   ```

3. **Install Required Packages**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Set Environment Variables**
   Create a `.env` file in your project folder and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_key_here
   ```

5. **Run the Application**
   ```bash
   streamlit run streamlitAPP.py
   ```



 ## How It Works

1. **User Uploads File**  
   The app supports `.pdf` and `.txt` files and reads them with PyPDF2 or UTF-8 decoders.

2. **Text Sent to LangChain**  
   After reading, the file content is passed to a LangChain-powered OpenAI prompt for MCQ generation.

3. **Quiz Generation**  
   The LLM outputs a JSON structure of MCQs which is parsed and displayed on the UI.

4. **Visualization**  
   The app shows the quiz in JSON, table format, and includes an AI-generated review.



## Example Prompts

1. Input File: "Basics of Photosynthesis (PDF)"

2. Subject: "Biology"

3. Tone: "Conversational"

4. MCQs Generated: 5



## Environment Variables

You must provide your OpenAI API key via environment variable:

```
OPENAI_API_KEY=your_key_here
```

Use the `.env` file in your project root, and make sure `python-dotenv` is installed to load it automatically.



## FAQ

**Q: Can this app be deployed?**  
Yes. You can host it using Streamlit Cloud, AWS EC2, or Vercel + Streamlit CLI.

**Q: Does this support other languages?**  
Currently, it's designed for English content only.

**Q: Can I extend it to export as PDF or integrate quiz platforms?**  
Yes, the backend is modular, and export extensions are possible.


