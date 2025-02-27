import google.generativeai as genai

genai.configure(api_key="AIzaSyBQn0U844Y3uLyKtp2sdA33yI7MfQLS2eU")
models = genai.list_models()
for m in models:
    print(m)
