import streamlit as st
from dotenv import load_dotenv

load_dotenv() # load all the environment variables
import os
import google.generativeai as genai

# Set up Google API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to generate summary based on input text
def generate_gemini_content(input_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt+input_text)
    return response.text

def generate_gemini_answer(input_text, prompt, question):
    model = genai.GenerativeModel("gemini-pro")
    answer = model.generate_content(prompt+question+input_text)
    return answer.text