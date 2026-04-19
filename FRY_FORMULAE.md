# Fry Readability Graph — Formulae for X-axis and Y-axis

## Overview

The Fry Graph uses two values plotted on a graph to estimate reading grade level (1–15):
- **X-axis:** Average number of **syllables** per 100 words  
- **Y-axis:** Average number of **sentences** per 100 words  

---

## Standard Fry Method (Edward Fry, 1968)

### Step 1: Select three 100-word passages
- One from the **beginning** of the text  
- One from the **middle**  
- One from the **end**  
- Skip proper nouns  

### Step 2: For each 100-word passage, compute:

#### X-axis: Syllables per 100 words

**Formula:**
```
X = Total syllables in the 100-word passage
```

Since the passage is exactly 100 words, the count is already "per 100 words."

**Average over 3 passages:**
```
X = (Syllables₁ + Syllables₂ + Syllables₃) / 3
```

**Syllable counting rules:**
- One syllable per vowel sound (e.g., cat=1, black-bird=2, con-ti-nen-tal=5)
- Endings like -y, -ed, -le usually add a syllable (read-y, bott-le)
- Don’t rely on word length (e.g., "through" = 1 syllable)

**Typical range:** 108 to 172 (Fry adds 100 to “syllables over one” in some versions; here we use raw syllable count.)

---

#### Y-axis: Sentences per 100 words

**Formula:**
```
Y = Number of sentences in the 100-word passage
```

(Count partial sentences to the nearest tenth, e.g., 4.3 sentences.)

**Average over 3 passages:**
```
Y = (Sentences₁ + Sentences₂ + Sentences₃) / 3
```

**Typical range:** 2.0 to 25+

---

## Alternative: Using per-sentence data

If you have **per-sentence** statistics (e.g., from your Urdu dataset):

### X-axis (syllables per 100 words) for one sentence:
```
X_sentence = (Total syllables in sentence / Words in sentence) × 100
```

**With syllable counts by length (1–8 syllables):**
```
Total syllables = (1×n₁) + (2×n₂) + (3×n₃) + ... + (8×n₈)
```
where n₁ = count of 1-syllable words, n₂ = count of 2-syllable words, etc.

```
X_sentence = (Total syllables / sentence_length) × 100
```

### Y-axis (sentences per 100 words) for one sentence:
```
Y_sentence = 100 / Words per sentence
         = 100 / sentence_length
```

**Example:**  
- Sentence has 10 words → Y = 100/10 = **10** sentences per 100 words  
- Sentence has 5 words → Y = 100/5 = **20** sentences per 100 words  

---

## Summary

| Axis | Formula | Range (Fry graph) |
|------|---------|-------------------|
| **X** (Syllables per 100 words) | Total syllables in 100-word sample (or per-sentence: `(syllables/words)×100`) | 108 – 172 |
| **Y** (Sentences per 100 words) | Number of sentences in 100-word sample (or per-sentence: `100/words_per_sentence`) | 2 – 25 |

---

## How to use the graph

1. Compute X and Y using the formulae above.  
2. Plot the point (X, Y) on the Fry Graph.  
3. The grade level is the number in the region where the point falls (1 = easiest, 15 = hardest).  
4. If the point falls in the “long words” or “long sentences” areas, the result is considered invalid.
