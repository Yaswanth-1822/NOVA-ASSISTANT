
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
            "mvgr college":"https://www.mvgrce.edu.in",
            "facebook":"https://www.facebook.com"
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