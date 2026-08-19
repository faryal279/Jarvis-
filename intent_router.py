"""
intent_router.py — Turns spoken commands into action skills using Gemini 2.5.
"""

import json
import re
from google import genai
from config import GOOGLE_API_KEY, WEBSITES
import skills

_client = genai.Client(api_key=GOOGLE_API_KEY)
_MODEL_NAME = "gemini-2.5-flash"

KNOWN_SITES = ", ".join(WEBSITES.keys())

ROUTER_PROMPT = f"""You are an intelligent intent classifier for a voice assistant.
Classify the user's spoken command into EXACTLY one of these intents:

1. "open_website": User wants to open a site or profile (e.g. "open github", "open my profile", "open youtube", "open google", "open linkedin").
   Parameter: The name of the site or specific request (e.g., "github", "my profile", "youtube").

2. "github_issues": User explicitly asks to find/search open source issues, projects, or beginner repositories to contribute to on GitHub (e.g. "find python projects on github", "suggest beginner issues").
   Parameter: The programming language or topic.

3. "linkedin_caption": User wants to write or draft a post/caption for LinkedIn (e.g., "write a linkedin post about AI", "draft a post").
   Parameter: The topic of the post.

4. "general_question": Questions, general talking, queries, commands that require an answer or information.
   Parameter: The user's prompt verbatim.

Known website shortcuts: {KNOWN_SITES}

Respond with ONLY valid JSON in this exact structure:
{{{{"intent": "...", "parameter": "..."}}}}

Command: "{{command}}"
"""


def _strip_code_fences(text: str) -> str:
    """Cleans up markdown code fences from the LLM output."""
    text = text.strip()
    text = re.sub(r"^```(json)?", "", text, flags=re.IGNORECASE)
    text = re.sub(r"```$", "", text)
    return text.strip()


def route_and_execute(command: str) -> str:
    """Classifies spoken text and triggers the appropriate action."""
    cmd = command.strip().lower()
    if not cmd:
        return "I didn't hear any command."

    # Direct manual overrides for instant and foolproof web/profile opening
    if "my github" in cmd or "my profile" in cmd or "my account" in cmd or "github profile" in cmd:
        return skills.suggest_github_issues("my profile")

    if cmd.startswith("open "):
        site_target = cmd.replace("open ", "").strip()
        return skills.open_website(site_target)

    prompt = ROUTER_PROMPT.format(command=cmd.replace('"', "'"))
    try:
        response = _client.models.generate_content(model=_MODEL_NAME, contents=prompt)
        raw = _strip_code_fences(response.text)
        parsed = json.loads(raw)
        intent = parsed.get("intent", "general_question")
        parameter = parsed.get("parameter", cmd)
    except Exception:
        intent = "general_question"
        parameter = cmd

    if intent == "open_website":
        return skills.open_website(parameter)
    elif intent == "github_issues":
        return skills.suggest_github_issues(parameter)
    elif intent == "linkedin_caption":
        return skills.draft_linkedin_caption(parameter)
    else:
        return skills.answer_general_question(parameter)
