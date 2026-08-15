# Jarvis — Local Voice Assistant

A local voice assistant that listens for a wake word, then a spoken
command, and handles it using one of four skills:

- **Open a website** — "Jarvis, open GitHub" / "Jarvis, open LinkedIn"
- **Suggest GitHub issues** — "Jarvis, find me good first issues in Python"
- **Draft a LinkedIn caption** — "Jarvis, draft a LinkedIn post about my RAG project"
  *(drafts and copies to your clipboard — you review and post it yourself,
  nothing is posted automatically)*
- **General questions** — anything else gets answered directly

Runs entirely on your own computer. No account automation, no auto-posting,
no auto-committing to repos — it opens things and drafts things; you stay
in control of anything that gets published.

## How it works

```
Your voice
    │
    ▼
Speech-to-text (SpeechRecognition + Google's free recognition API)
    │
    ▼
Intent router (Gemini classifies: open_website / github_issues /
                linkedin_caption / general_question)
    │
    ▼
Matching skill runs (skills.py)
    │
    ▼
Text-to-speech reads the result back to you (pyttsx3, runs offline)
```

## Setup

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

**Note on `pyaudio`:** this is the one dependency that sometimes needs an
extra step, because it wraps a system audio library.

- **Windows:** if `pip install pyaudio` fails, run:
  ```bash
  pip install pipwin
  pipwin install pyaudio
  ```
- **macOS:** install the system library first:
  ```bash
  brew install portaudio
  pip install pyaudio
  ```
- **Linux (Debian/Ubuntu):**
  ```bash
  sudo apt-get install portaudio19-dev python3-pyaudio
  pip install pyaudio
  ```

### 2. Set your Google API key

Get a free key at https://aistudio.google.com/app/apikey, then set it as an
environment variable:

**Windows (PowerShell):**
```powershell
$env:GOOGLE_API_KEY="your-key-here"
```
**macOS/Linux:**
```bash
export GOOGLE_API_KEY="your-key-here"
```

(Optional) For higher GitHub search rate limits, also set `GITHUB_TOKEN`
with a personal access token — not required for basic use.

### 3. Customize

- Edit `ASSISTANT_NAME` in `config.py` to change the wake word/name
- Add more sites to the `WEBSITES` dictionary in `config.py`

### 4. Run it

```bash
python main.py
```

Say the assistant's name (default "Jarvis") to get its attention, wait for
"Yes? I'm listening.", then say your command.

## Voice customization

`pyttsx3` uses your operating system's built-in text-to-speech voices. The
code tries to auto-select a deeper/male-sounding voice if your system has
one (`setup_tts()` in `main.py`). To pick a specific voice manually, run:

```python
import pyttsx3
engine = pyttsx3.init()
for v in engine.getProperty("voices"):
    print(v.id, v.name)
```

and set `engine.setProperty("voice", "<the id you want>")` in `main.py`.

## Project structure

```
.
├── main.py            # Listens, speaks, main loop
├── intent_router.py    # Classifies commands into skills (via Gemini)
├── skills.py           # The actual actions: open site, GitHub search, etc.
├── config.py            # Assistant name, known websites, API keys
└── requirements.txt
```

## Extending it

To add a new skill:
1. Write a new function in `skills.py`
2. Add it as an option in the `ROUTER_PROMPT` in `intent_router.py`
3. Add a matching `elif` branch in `route_and_execute()`
