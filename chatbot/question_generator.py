from chatbot.prompt_engine import build_question_prompt
from chatbot.llm_handler import call_llm
import re


def generate_questions(tech_stack, experience):
    prompt = build_question_prompt(tech_stack, experience)

    response = call_llm(prompt)

    # 🔥 Extract numbered questions properly
    questions = re.split(r"\n\d+\.\s", response)

    # Clean results
    questions = [q.strip() for q in questions if q.strip()]

    # If parsing fails, fallback
    if len(questions) <= 1:
        return [response]

    return questions