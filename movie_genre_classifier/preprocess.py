"""Text cleaning used by both training and prediction (NLP preprocessing step)."""

import re

from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

# Extra words that appear in almost every plot summary and say nothing about the genre
STOP_WORDS = set(ENGLISH_STOP_WORDS) | {"film", "movie", "story", "plot"}
_WORD = re.compile(r"[a-z]+")


def clean_text(text) -> str:
    """lowercase -> keep letters only -> drop very short words and stop words."""
    tokens = _WORD.findall(str(text).lower())
    return " ".join(t for t in tokens if len(t) > 2 and t not in STOP_WORDS)
