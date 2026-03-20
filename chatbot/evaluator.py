from chatbot.llm_handler import call_llm


def evaluate_answer(question, answer):
    prompt = f"""
You are a VERY STRICT senior technical interviewer.

Question:
{question}

Candidate Answer:
{answer}

Evaluate using this STRICT rubric:

Relevance:
- Completely unrelated → Irrelevant
- Partially related → Weakly Relevant
- Fully addresses question → Relevant

Scoring Guide:
- 1–2 → Completely wrong / irrelevant
- 3–4 → Very weak, vague, lacks understanding
- 5–6 → Basic idea but missing depth
- 7–8 → Good but not complete, lacks edge cases or optimization
- 9–10 → Excellent, detailed, covers trade-offs, real-world usage

IMPORTANT RULES:
- DO NOT give 8+ unless answer includes:
  - real-world reasoning
  - trade-offs OR optimization OR edge cases
- If answer is generic → max score = 6
- If answer is shallow → max score = 5

Output STRICTLY:

Score: <number>/10
Relevance: <Relevant / Weakly Relevant / Irrelevant>
Feedback: <2-3 lines explaining gaps>
"""
    return call_llm(prompt)