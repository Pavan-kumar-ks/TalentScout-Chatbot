def is_weak_answer(answer):
    weak_phrases = [
        "i don't know",
        "dont know",
        "no idea",
        "not sure",
        "idk"
    ]

    answer_lower = answer.lower()

    return any(phrase in answer_lower for phrase in weak_phrases) or len(answer.strip()) < 5