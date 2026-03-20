def analyze_sentiment(text):
    text = text.lower()

    if any(word in text for word in ["confused", "don't know", "dont know", "not sure", "difficult", "hard"]):
        return "negative"

    elif any(word in text for word in ["yes", "sure", "i think", "correct", "confident", "definitely"]):
        return "positive"

    return "neutral"