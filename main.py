"""
main.py — Main continuous voice listening loop with enhanced intent parsing.
"""

import speech_recognition as sr
import pyttsx3
import sys
from skills import open_website, play_youtube_song, search_github_projects, answer_general_question
from config import VOICE_RATE, LISTEN_TIMEOUT, PHRASE_TIME_LIMIT

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()
engine.setProperty('rate', VOICE_RATE)

def speak(text):
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 1.0  # Gives enough pause time to complete long sentences
    
    with sr.Microphone() as source:
        print("\nListening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=LISTEN_TIMEOUT, phrase_time_limit=PHRASE_TIME_LIMIT)
            text = recognizer.recognize_google(audio).lower().strip()
            print(f"You said: {text}")
            return text
        except Exception:
            return ""

def normalize_command(cmd):
    """
    Fixes common speech-to-text misspellings for accents (e.g., 'lindlin' -> 'linkedin').
    """
    replacements = {
        "lindlin": "linkedin",
        "linked in": "linkedin",
        "yt": "youtube",
        "git hub": "github",
        "git": "github"
    }
    for word, replacement in replacements.items():
        cmd = cmd.replace(word, replacement)
    return cmd

def process_command(cmd):
    if not cmd:
        return

    # Normalize accent / misheard words
    cmd = normalize_command(cmd)

    # Filter out incomplete broken inputs
    bad_phrases = ["hey jarvis please open my", "open my", "open", "jarvis open", "just open", "please open"]
    if cmd in bad_phrases:
        print("Ignored incomplete command...")
        return

    # Intent 1: Exit Program
    if any(w in cmd for w in ["exit", "stop", "quit", "bye"]):
        speak("Goodbye!")
        sys.exit()

    # Intent 2: Playing YouTube Music
    song_keywords = ["play", "song", "music", "wajah tum ho", "audio"]
    if any(w in cmd for w in song_keywords):
        res = play_youtube_song(cmd)
        speak(res)
        return

    # Intent 3: GitHub Project Search Intent
    project_keywords = ["search project", "open project", "find project", "projects according", "project according"]
    if any(w in cmd for w in project_keywords):
        res = search_github_projects(cmd)
        speak(res)
        return

    # Intent 4: Opening Websites / Social Platforms (LinkedIn, GitHub, YouTube)
    if any(k in cmd for k in ["open", "github", "youtube", "linkedin", "profile", "account"]):
        site = cmd.replace("open", "").replace("my", "").replace("account", "").strip()
        res = open_website(site)
        speak(res)
        return

    # Intent 5: Fallback General Search / Question Answering
    res = answer_general_question(cmd)
    speak(res)

def main():
    speak("Jarvis is online and ready.")
    while True:
        cmd = listen()
        if cmd:
            process_command(cmd)

if __name__ == "__main__":
    main()
