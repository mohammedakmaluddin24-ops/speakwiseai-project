import re
from collections import Counter

FILLER_PATTERNS = {
    "um": r"\bum+\b",
    "uh": r"\buh+\b",
    "like": r"\blike\b",
    "actually": r"\bactually\b",
    "basically": r"\bbasically\b",
    "you know": r"\byou\s+know\b",
}

STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "but",
    "by",
    "for",
    "from",
    "has",
    "have",
    "i",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "our",
    "so",
    "that",
    "the",
    "this",
    "to",
    "was",
    "we",
    "were",
    "with",
    "you",
    "your",
}


def _words(text: str) -> list[str]:
    return re.findall(r"\b[\w']+\b", (text or "").lower())


def total_words(text: str) -> int:
    """Return the number of spoken words in a transcript."""
    return len(_words(text))


def count_fillers(text: str) -> int:
    """Count common verbal fillers in a transcript."""
    normalized_text = (text or "").lower()
    return sum(len(re.findall(pattern, normalized_text)) for pattern in FILLER_PATTERNS.values())


def calculate_wpm(text: str, duration_minutes: float) -> float:
    """Calculate words per minute, guarding against zero-length audio."""
    if duration_minutes <= 0:
        return 0.0
    return round(total_words(text) / duration_minutes, 1)


def top_words(text: str, limit: int = 20) -> dict[str, int]:
    """Return the most frequent meaningful words for word-cloud generation."""
    words = [word for word in _words(text) if word not in STOP_WORDS and len(word) > 2]
    return dict(Counter(words).most_common(limit))
