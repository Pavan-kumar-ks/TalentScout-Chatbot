from chatbot.llm_handler import call_llm


def generate_followup(question, answer):
    prompt = f"""
You are a real human interviewer.

Question:
{question}

Candidate Answer:
{answer}

Task:
- Ask ONE short follow-up question
- Keep it natural and conversational
- Focus on a gap in the answer

Rules:
- Max 1–2 lines
- No long explanations
- No labels like "Follow-up Question"
- Use English only

Example:
"How would this work at scale?"

Now generate:
"""
    return call_llm(prompt)