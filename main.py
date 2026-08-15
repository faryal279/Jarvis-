"""
main.py — Main continuous voice listening loop.
"""

import speech_recognition as sr
import pyttsx3
import sys
from skills import open_website, play_youtube_song, search_github_projects, answer_general_question

engine = pyttsx3.init()
engine.setProperty('rate', 170)

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
            audio = recognizer.listen(source, timeout=6, phrase_time_limit=10)
            text = recognizer.recognize_google(audio).lower().strip()
            print(f"You said: {text}")
            return text
        except Exception:
            return ""

def process_command(cmd):
    if not cmd:
        return

    # Filter out incomplete broken inputs
    bad_phrases = ["hey jarvis please open my", "open my", "open", "jarvis open", "just open", "please open"]
    if cmd in bad_phrases:
        print("Ignored incomplete command...")
        return

    # Intent 1: Playing YouTube Music
    song_keywords = ["play", "song", "music", "wajah tum ho", "audio"]
    if any(w in cmd for w in song_keywords):
        res = play_youtube_song(cmd)
        speak(res)
        return

    # Intent 2: GitHub Project Search Intent
    project_keywords = ["search project", "open project", "find project", "projects according", "project according"]
    if any(w in cmd for w in project_keywords):
        res = search_github_projects(cmd)
        speak(res)
        return

    # Intent 3: Opening GitHub Profile / Specific Websites
    if "open" in cmd or "github" in cmd or "youtube" in cmd or "profile" in cmd:
        site = cmd.replace("open", "").replace("my", "").replace("account", "").strip()
        res = open_website(site)
        speak(res)
        return

    # Intent 4: Exit Program
    if any(w in cmd for w in ["exit", "stop", "quit", "bye"]):
        speak("Goodbye!")
        sys.exit()

    # Intent 5: Fallback General Google Search
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