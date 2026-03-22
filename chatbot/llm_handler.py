from config import GROQ_API_KEY, GROQ_MODEL, GROQ_TIMEOUT_SECONDS
import requests


def call_llm(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.4
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=GROQ_TIMEOUT_SECONDS)
        response_json = response.json()
    except Exception as e:
        return f"LLM Error: {e}"

    # ✅ HANDLE ERRORS PROPERLY
    if "choices" not in response_json:
        return f"LLM Error: {response_json}"

    return response_json["choices"][0]["message"]["content"]