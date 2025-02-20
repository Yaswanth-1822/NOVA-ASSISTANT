import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyC5a7sxTBCk-4GhiWvrrrQNIeeSsMoXeCM")
model = genai.GenerativeModel('gemini-pro')

def generate_response(prompt):
    response = model.generate_content(prompt)
    return response.text