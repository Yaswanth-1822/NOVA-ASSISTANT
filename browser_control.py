#
#  import os
# import webbrowser
# import requests

# def search_google(command):
#     try:
#         query = command.replace("search", "").strip().lower()

#         websites = {
#             "youtube": "https://www.youtube.com",
#             "facebook": "https://www.facebook.com",
#             "linkedin": "https://www.linkedin.com",
#             "twitter": "https://www.twitter.com",
#             "instagram": "https://www.instagram.com",
#             "flipkart": "https://www.flipkart.com",
#             "wikipedia": "https://www.wikipedia.org"
#         }

#         if query in websites:
#             url = websites[query]
#             print(f"Opening {query} directly: {url}")
#             webbrowser.open(url)
#             return

#         search_url = f"https://api.duckduckgo.com/?q={query}&format=json"
#         print(f"Searching for: {query}")

#         response = requests.get(search_url)
#         data = response.json()

#         if "AbstractURL" in data and data["AbstractURL"]:
#             first_link = data["AbstractURL"]
#         elif "Results" in data and len(data["Results"]) > 0:
#             first_link = data["Results"][0]["FirstURL"]
#         else:
#             first_link = f"https://www.google.com/search?q={query}"

#         print(f"Opening: {first_link}")
#         webbrowser.open(first_link)

#     except Exception as e:
#         print(f"Error searching: {e}")
import webbrowser

def search_google(command):
    try:
        # Extract the search query or website name
        query = command.replace("search", "").strip().lower()

        # List of common websites
        websites = {
            "youtube": "https://www.youtube.com",
            "google": "https://www.google.com",
            "twitter": "https://www.twitter.com",
            "instagram": "https://www.instagram.com",
            "gmail": "https://mail.google.com",
            "amazon": "https://www.amazon.com",
            "flipkart": "https://www.flipkart.com",
            "wikipedia": "https://www.wikipedia.org",
        }

        # Check if the query matches a known website
        if query in websites:
            url = websites[query]
            webbrowser.open(url)
            return f"Opened {query}."
        else:
            # If the query is a URL (e.g., "abc.com"), open it directly
            if "." in query:  # Simple check for a URL
                if not query.startswith(("http://", "https://")):
                    query = f"https://{query}"
                webbrowser.open(query)
                return f"Opened {query}."
            else:
                # If it's not a URL, search for it on Google
                search_url = f"https://www.google.com/search?q={query}"
                webbrowser.open(search_url)
                return f"Searching Google for: {query}."
    except Exception as e:
        return f"Error: {str(e)}"