def analyze_sentiment(text):
    text = text.lower()

    positive_words = ["good", "great", "confident", "sure", "yes", "correct"]
    negative_words = ["confused", "don't know", "dont know", "not sure", "difficult", "no idea"]

    if any(word in text for word in positive_words):
        return "positive"

    elif any(word in text for word in negative_words):
        return "negative"

    return "neutral"