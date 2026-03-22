# config.py

import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
GROQ_TIMEOUT_SECONDS = int(os.getenv("GROQ_TIMEOUT_SECONDS", "30"))

# Dedicated translation configuration (separate from interview LLM key).
TRANSLATION_GROQ_API_KEY = os.getenv("TRANSLATION_GROQ_API_KEY")
TRANSLATION_MODEL = os.getenv("TRANSLATION_MODEL", "openai/gpt-oss-120b")
TRANSLATION_TIMEOUT_SECONDS = int(os.getenv("TRANSLATION_TIMEOUT_SECONDS", "20"))