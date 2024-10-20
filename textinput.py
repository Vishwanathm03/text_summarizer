import streamlit as st
from google.cloud import aiplatform
import pdfplumber
import google.generativeai as genai
import os
from PIL import Image

# Set the environment variable
genai.configure(api_key="AIzaSyAYO3fpjC4wTPDy2Q8_SZ5K9RaLunjsZ5I")

# Function to extract text from PDF using pdfplumber
def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text



# Function to get a summary from Gemini-pro API
def summarize_text(text):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([f"Please summarize the following text:\n\n{text}"])  # Increase timeout
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"

# Function to question text using Gemini-pro API
def question_text(text, question):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([f"Please answer the following question based on the provided text:\n\nText: {text}\n\nQuestion: {question}"])
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"

# Streamlit app
def main():
    
    image = Image.open('image.png')
    st.image(image,width=100,)
    
    st.markdown("<h1 style=' color: white;'>PDF Summarizer and Question-Answering</h1>", unsafe_allow_html=True)

    

    # User input for the text
    user_input = st.text_area("Please enter the text you want to save:", height=200)
    if st.button("Get Summary"):
        if user_input:
            summary = summarize_text(user_input)
            st.subheader("Summary")
            st.write(summary)
        else:
            st.error("Please enter some text before summarizing.")
    
    

        # Ask a question
    question = st.text_input("Enter your question about the text")
    if st.button("Get Answer"):
        if question and user_input:
            answer = question_text(user_input, question)
            st.subheader("Answer")
            st.write(answer)
        else:
            st.warning("Please enter both the text and a question to get an answer.")

if __name__ == "__main__":
    main()