AI-Powered Resume Enhancer

An AI-powered web application that enhances resumes for a specific target role using a hosted LLM (Groq), with automatic comparison between original and improved versions.

🔗 Live App: (https://resume-enhancer-ai.streamlit.app/)

# Local Setup

1. Clone the repository

`git clone https://github.com/Projato/ResumeEnhancer.git`
`cd ResumeEnhancer`

2. Install dependencies (using uv)

`uv sync`

3. Set your Groq API key
Create a .env file:

`GROQ_API_KEY=your_key_here`

4. Run locally
Web App (Recommended)

`streamlit run app.py`

CLI Version
`python main.py`