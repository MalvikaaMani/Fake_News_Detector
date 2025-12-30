import re

SENSATIONAL_WORDS = [
    "shocking", "secret", "exposed", "breaking", "truth",
    "revealed", "conspiracy", "leaked", "miracle"
]

def detect_patterns(text):
    patterns = []

    lower_text = text.lower()

    if any(word in lower_text for word in SENSATIONAL_WORDS):
        patterns.append("Clickbait or sensational language")

    if re.search(r"\b(source|sources say|anonymous)\b", lower_text):
        patterns.append("Anonymous or unverifiable sources")

    if text.count("!") > 3 or text.isupper():
        patterns.append("Excessive punctuation or capitalization")

    if len(text.split()) < 80:
        patterns.append("Very short article (low information content)")

    return patterns
