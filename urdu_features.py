"""
Extract readability features from Urdu text.
Uses improved syllable estimation and Fry-based grading calibrated to Urdu dataset.
"""

import re

# Urdu/Arabic script
URDU_CHARS = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]+')

# Urdu long vowels and vowel markers (increase syllable count)
URDU_VOWELS = re.compile(r'[\u0627\u0648\u064A\u06CC\u0621\u0622\u0623\u0625\u0649\u064A\u06D2\u064B\u064C\u064D\u064E\u064F\u0650\u0651\u0652\u0670]')

def estimate_syllables_urdu(word: str) -> int:
    """
    Improved syllable count for Urdu words.
    - Counts vowel nuclei (long vowels ا و ی + harakat)
    - Fallback: word length heuristic for unmarked text
    """
    word = word.strip()
    if not word:
        return 0
    chars = [c for c in word if '\u0600' <= c <= '\u06FF' or '\u0750' <= c <= '\u08FF']
    n = len(chars)
    if n == 0:
        return 1
    # Count explicit vowels/diacritics
    vowel_count = len(URDU_VOWELS.findall(word))
    if vowel_count >= 1:
        return max(1, min(8, vowel_count))
    # No diacritics: Urdu ~2-3 chars per syllable. Longer words = more syllables.
    return max(1, min(8, (n + 1) // 2))

def extract_features(text: str) -> dict:
    """Extract features for model. Returns dict with feature_cols keys."""
    sentences = re.split(r'[.!?۔؟\n]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    if not sentences:
        return None

    syll_counts = {i: 0 for i in range(1, 9)}
    word_len_counts = {i: 0 for i in range(1, 9)}
    total_words = 0

    for sent in sentences:
        words = re.findall(URDU_CHARS, sent)
        words = [w for w in words if len(w) > 0]
        total_words += len(words)
        for word in words:
            syl = estimate_syllables_urdu(word)
            syll_counts[min(syl, 8)] += 1
            wlen = min(len(word), 8)
            word_len_counts[wlen] += 1

    if total_words == 0:
        return None

    n_sent = len(sentences)
    avg_words_per_sent = total_words / n_sent

    features = {}
    for i in range(1, 9):
        features[f"{i}-syllable_words"] = syll_counts[i] / n_sent
    for i in range(1, 9):
        features[f"word_length-{i}"] = word_len_counts[i] / n_sent
    features["sentence_length"] = avg_words_per_sent

    return features

def compute_fry_metrics(text: str) -> tuple:
    """
    Compute syllables per 100 words and sentences per 100 words.
    Returns (syllables_per_100, sentences_per_100) or (None, None) if no valid text.
    """
    features = extract_features(text)
    if features is None:
        return None, None

    syll_cols = [f"{i}-syllable_words" for i in range(1, 9)]
    total_syllables = sum(i * features[c] for i, c in enumerate(syll_cols, 1))
    sent_length = features["sentence_length"]

    # Per 100 words: (syllables per word) * 100, (sentences per word) * 100
    syll_per_100 = (total_syllables / sent_length) * 100
    sent_per_100 = 100 / sent_length

    return syll_per_100, sent_per_100

def fry_grade_from_metrics(syll_per_100: float, sent_per_100: float) -> int:
    """
    Map Fry metrics to grade (1-12) using calibration from Urdu dataset.
    Dataset range: syll 100-250, sent 2-25.
    High syllables + low sentences = harder (higher grade).
    """
    # Clamp to observed range
    syll = max(100, min(250, syll_per_100))
    sent = max(2, min(25, sent_per_100))

    # Normalize: syll 100->0, 250->1; sent 2->0, 25->1
    syll_norm = (syll - 100) / 150
    sent_norm = (sent - 2) / 23

    # Difficulty: high syllables + low sentences = hard
    difficulty = syll_norm * 0.55 + (1 - sent_norm) * 0.45
    grade = 1 + difficulty * 11
    return max(1, min(12, int(round(grade))))
