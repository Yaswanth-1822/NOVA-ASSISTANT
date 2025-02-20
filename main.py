from voice_handler import listen, speak
from context_manager import generate_contextual_response
from database_handler import reset_conversation_history
from app_control import open_application
from browser_control import search_google

def main(log_function):
    user_id = "user_001"
    reset_conversation_history(user_id)

    speak("Hello! I'm Nova. How can I assist you today?")
    log_function("Nova: Hello! I'm Nova. How can I assist you today?")

    while True:
        user_input = listen()
        log_function(f"You: {user_input}")

        if user_input.lower().startswith("timeout") or "didn't catch" in user_input.lower():
            speak(user_input)
            continue

        if any(cmd in user_input.lower() for cmd in ["exit", "quit", "stop"]):
            speak("Goodbye!")
            log_function("Nova: Goodbye!")
            break

        # Handle application and website commands
        if "open" in user_input.lower():
            response = open_application(user_input)
            speak(response)
            log_function(f"Nova: {response}")
            continue

        # Handle search commands
        if "search" in user_input.lower():
            response = search_google(user_input)
            speak(response)
            log_function(f"Nova: {response}")
            continue

        # Handle other commands
        nova_response = generate_contextual_response(user_input, user_id)
        speak(nova_response)
        log_function(f"Nova: {nova_response}")