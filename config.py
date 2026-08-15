import os

# API Keys and Tokens
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "YOUR_ACTUAL_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "YOUR_ACTUAL_GITHUB_TOKEN")

# Assistant Wake Word
WAKE_WORD = "jarvis"

# Website shortcuts dictionary
WEBSITES = {
    "google": "https://www.google.com",
    "github": "https://www.github.com",
    "linkedin": "https://www.linkedin.com",
    "youtube": "https://www.youtube.com",
    "chatgpt": "https://chat.openai.com",
}