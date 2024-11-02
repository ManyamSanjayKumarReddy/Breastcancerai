from dotenv import load_dotenv
import streamlit as st
import os
import textwrap
import google.generativeai as genai
from IPython.display import Markdown
from streamlit_extras.add_vertical_space import add_vertical_space  # New import for spacing

# Load environment variables
load_dotenv()

def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

# Configure API key for Google Gemini LLM
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("API Key for Google Gemini LLM is missing. Please set it in the .env file.")
else:
    genai.configure(api_key=api_key)

def get_gemini_response(question):
    try:
        model = genai.GenerativeModel('gemini-pro')
        # Requesting a structured response without asterisks
        response = model.generate_content(
            f"Provide a well-structured response to the following question about breast cancer. Use headings, bullet points, bold text and remove extra characters where appropriate. Question: {question}"
        ) 
        return response.text
    except Exception as e:
        st.error(f"An error occurred while retrieving the response: {e}")
        return None


# Initialize the Streamlit app
st.set_page_config(page_title="Breast Cancer AI Assistant", page_icon="🩺")
st.markdown("<h1 style='text-align: center; color: #FF7F50;'>Breast Cancer AI Assistant  Medxbay</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Ask questions about breast cancer, and I'll provide information based on the latest medical knowledge.</p>", unsafe_allow_html=True)

# Add some space
add_vertical_space(2)

# User input container
with st.container():
    st.markdown("### 🧐 Ask a Question")
    user_input = st.text_input("Enter your question about breast cancer:", key="user_question")
    submit_button = st.button("Get the Answer 💡")

# Handle response generation on button click
if submit_button:
    if not user_input.strip():
        st.warning("Please enter a question before submitting.")
    else:
        with st.spinner("Thinking..."):
            response = get_gemini_response(user_input)
        if response:
            st.markdown("<h2 style='color: #0167FF;'>The Response is:</h2>", unsafe_allow_html=True)
            st.markdown(f"<div style='background-color: #f9f9f9; padding: 15px; border-radius: 8px; line-height: 1.5;'>{response}</div>", unsafe_allow_html=True)

# Sample question section
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("### 📋 Sample Questions on Breast Cancer")

# Combine understanding and prevention questions
all_questions = [
    "What is breast cancer, and what are its common symptoms?",
    "What are the different types of breast cancer?",
    "How does breast cancer develop, and what are its risk factors?",
    "What are the survival rates for different stages of breast cancer?",
    "What lifestyle changes can help reduce my risk of breast cancer?",
    "Are there specific diets or foods that can lower my breast cancer risk?",
]

for question in all_questions:
    if st.button(f"➡️ {question}", key=question):
        user_input = question
        response = get_gemini_response(user_input)
        if response:
            st.markdown("<h2 style='color: #4CAF50;'>The Response:</h2>", unsafe_allow_html=True)
            st.markdown(f"<div style='background-color: #f9f9f9; padding: 15px; border-radius: 8px; line-height: 1.5;'>{response}</div>", unsafe_allow_html=True)

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<footer style='text-align: center;'>Made with ❤️ by Medxbay</footer>", unsafe_allow_html=True)
