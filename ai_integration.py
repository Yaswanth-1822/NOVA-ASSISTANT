import requests

# Replace with your actual Gemini API key
GEMINI_API_KEY = "AIzaSyBQn0U844Y3uLyKtp2sdA33yI7MfQLS2eU"

GEMINI_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

def ai_response(prompt):
    try:
        headers = {"Content-Type": "application/json"}

        data = {
            "contents": [{"parts": [{"text": prompt}]}]  # Correct Gemini API request format
        }

        response = requests.post(GEMINI_ENDPOINT, json=data, headers=headers)

        if response.status_code == 200:
            candidates = response.json().get("candidates", [])
            if candidates:
                full_response = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "I'm not sure about that.")
                
                # Summarize response to 2-3 sentences
                sentences = full_response.split(". ")
                summarized_response = ". ".join(sentences[:3]) + "." if len(sentences) > 2 else full_response

                return summarized_response.strip()
            else:
                return "No valid response from Gemini."
        elif response.status_code == 401:
            return "Error: Unauthorized - Check API Key and ensure billing is enabled."
        else:
            return f"Error: Gemini API returned status {response.status_code}"

    except Exception as e:
        return f"Error: {e}"