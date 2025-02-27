import requests
import google.generativeai as genai
from google import genai
# Replace with your actual Gemini API key
# GEMINI_API_KEY = "AIzaSyBHkBd1rszhGlwsumjUhRsiD13jlj2KpTU"

# Configure Gemini API

client = genai.Client(api_key="AIzaSyBHkBd1rszhGlwsumjUhRsiD13jlj2KpTU")


def generate_response(prompt):
    try:
        response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
    )
        return  response.text

    except Exception as e:
        return f"Error: {e}"











# import google.generativeai as genai

# # Configure Gemini API
# genai.configure(api_key="AIzaSyBHkBd1rszhGlwsumjUhRsiD13jlj2KpTU")
# model = genai.GenerativeModel('gemini-2.0-flash')

# def generate_response(prompt):
#     response = model.generate_content(prompt)
#     return response.text