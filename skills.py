"""
skills.py — Handles website opening, GitHub actions, YouTube playback, and searches.
"""

import webbrowser
import pywhatkit
import urllib.parse

def open_website(site_name: str) -> str:
    """Handles website opening and GitHub profile navigation."""
    clean_site = site_name.strip().lower()

    # 1. Special Handling for GitHub Profile & Repositories
    github_profile_triggers = [
        "github account", "github profile", "my github", 
        "get up profile", "git profile", "my profile", "my repos"
    ]
    if any(trigger in clean_site for trigger in github_profile_triggers):
        # Direct GitHub Profile / Repositories page
        webbrowser.open("https://github.com?tab=repositories")
        return "Opening your GitHub profile and repositories."

    # General GitHub main page
    if "github" in clean_site:
        webbrowser.open("https://github.com")
        return "Opening GitHub."

    # 2. Special Handling for YouTube
    if "youtube" in clean_site:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube."

    # Fallback search for other custom links
    target_url = f"https://www.google.com/search?q={urllib.parse.quote(site_name)}"
    webbrowser.open(target_url)
    return f"Searching for {site_name} on Google."


def search_github_projects(query: str) -> str:
    """Searches open-source projects or good first issues on GitHub based on query."""
    clean_query = query.lower()
    
    # Remove filler speech words
    fillers = [
        "jarvis", "please", "search", "find", "open", "project", "projects", 
        "according to my profile", "according to", "my profile", "for me", 
        "on github", "github", "i get up profile and"
    ]
    for word in fillers:
        clean_query = clean_query.replace(word, "")
    
    clean_query = clean_query.strip()
    
    # Default keyword if speech recognition mistranslated
    if not clean_query or len(clean_query) < 2:
        clean_query = "python"

    # Open GitHub search page directly for relevant projects
    search_url = f"https://github.com/search?q={urllib.parse.quote(clean_query)}+label%3A%22good+first+issue%22"
    webbrowser.open(search_url)
    return f"Searching GitHub for {clean_query} projects."


def play_youtube_song(query: str) -> str:
    """Directly plays requested songs or videos on YouTube."""
    clean_query = query.lower()
    
    fillers = ["hey jarvis", "jarvis", "please", "play", "a song", "song", "on youtube", "youtube", "can you", "my"]
    for word in fillers:
        clean_query = clean_query.replace(word, "")
    
    clean_query = clean_query.strip()
    if not clean_query:
        clean_query = "wajah tum ho"

    try:
        pywhatkit.playonyt(clean_query)
        return f"Playing {clean_query} on YouTube."
    except Exception:
        search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(clean_query)}"
        webbrowser.open(search_url)
        return f"Opening {clean_query} on YouTube."


def answer_general_question(question: str) -> str:
    """General Google Search fallback."""
    search_url = f"https://www.google.com/search?q={urllib.parse.quote(question)}"
    webbrowser.open(search_url)
    return f"Searching Google for {question}."