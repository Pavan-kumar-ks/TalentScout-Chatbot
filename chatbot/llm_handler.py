from config import GROQ_API_KEY
import requests
def call_llm(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.3-70b-versatile",  # safer model
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()

    # ✅ HANDLE ERRORS PROPERLY
    if "choices" not in response_json:
        return f"LLM Error: {response_json}"

    return response_json["choices"][0]["message"]["content"]