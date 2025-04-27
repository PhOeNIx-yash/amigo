import webbrowser

def searchGoogle(query):
    """Search Google with the provided query."""
    query = query.replace("google", "").strip()
    webbrowser.open(f"https://www.google.com/search?q={query}")

def searchYoutube(query):
    """Search YouTube with the provided query."""
    query = query.replace("youtube", "").strip()
    webbrowser.open(f"https://www.youtube.com/results?search_query={query}")