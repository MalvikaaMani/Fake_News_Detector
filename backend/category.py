# backend/category.py

CATEGORIES = {
    "Health": [
        "health", "medicine", "covid", "vaccine", "hiv",
        "hospital", "doctor", "medical"
    ],
    "Politics": [
        "election", "government", "minister", "congress",
        "party", "politics", "vote", "parliament"
    ],
    "Science": [
        "research", "study", "scientist",
        "experiment", "laboratory"
    ]
}


def detect_category(text):
    """
    Detect news category using weighted keyword matching
    """
    text = text.lower()
    scores = {category: 0 for category in CATEGORIES}

    for category, keywords in CATEGORIES.items():
        for word in keywords:
            scores[category] += text.count(word)

    best_category = max(scores, key=scores.get)

    if scores[best_category] == 0:
        return "General"

    return best_category


def category_warning(category):
    """
    Return ethical warning based on news category
    """
    if category == "Health":
        return (
            "⚠ Health misinformation can cause serious harm. "
            "Verify with official medical or government health sources."
        )

    if category == "Politics":
        return (
            "⚠ Political misinformation can influence public opinion. "
            "Cross-check with multiple trusted news sources."
        )

    if category == "Science":
        return (
            "⚠ Scientific claims should be verified using "
            "peer-reviewed or authoritative sources."
        )

    return "General news content detected."
