# Urdu Readability Checker — Complete Project Explanation (A–Z)

This document explains the entire project from data to final grade, including all formulae and the full working pipeline.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Dataset & Preprocessing](#2-dataset--preprocessing)
3. [Linear Regression Model](#3-linear-regression-model)
4. [Fry Readability Formula](#4-fry-readability-formula)
5. [Feature Extraction from Urdu Text](#5-feature-extraction-from-urdu-text)
6. [Grade Calculation — Complete Flow](#6-grade-calculation--complete-flow)
7. [Web Application Flow](#7-web-application-flow)
8. [All Formulae Summary](#8-all-formulae-summary)
9. [File Structure](#9-file-structure)

---

## 1. Project Overview

### Purpose

The **Urdu Readability Checker** determines how difficult a piece of Urdu text is to read and assigns it a **grade level (1–12)**:

- **Grade 1** = Easiest (young children, ages 6–8)
- **Grade 12** = Hardest (high school / college level)

### Use Cases

- Children's book publishers
- Educational content creators
- Textbook writers
- Teachers selecting appropriate reading material

### High-Level Flow

```
Urdu Text Input → Feature Extraction → Fry Metrics → Grade (1–12) → Display to User
```

---

## 2. Dataset & Preprocessing

### Raw Dataset (`input_to_linear_regression2.xlsx`)

| Column | Description |
|--------|-------------|
| `Sentence` | Original Urdu sentence |
| `1-syllable_words` | Count of 1-syllable words in the sentence |
| `2-syllable_words` | Count of 2-syllable words |
| ... | ... |
| `8-syllable_words` | Count of 8-syllable words |
| `word_length-1` | Count of 1-character words |
| `word_length-2` | Count of 2-character words |
| ... | ... |
| `word_length-8` | Count of 8-character words |
| `sentence_length` | Number of words in the sentence |
| `avg_syllable/avg_word_length` | Target ratio (readability metric) |

### Preprocessing Steps

1. **Drop `Unnamed: 8`** — Empty column (100% null)
2. **Remove rows with null values** — `dataset.dropna()`
3. **Keep duplicates** — As per project requirement

### Preprocessing Formula

```
Cleaned_Data = Raw_Data.drop(columns=["Unnamed: 8"]).dropna()
```

### Output

- **File:** `input_to_linear_regression2_cleaned.csv`
- **Rows:** ~243,913 (after removing ~9,782 null rows)
- **Columns:** 20

---

## 3. Linear Regression Model

### Model Purpose

The model predicts **`avg_syllable/avg_word_length`** (a readability ratio) from 17 linguistic features.

### Linear Regression Equation

```
y = α + β₁x₁ + β₂x₂ + ... + β₁₇x₁₇
```

Where:

- **y** = predicted value (`avg_syllable/avg_word_length`)
- **α (alpha)** = intercept
- **βᵢ (beta)** = coefficient for feature i
- **xᵢ** = value of feature i

### Alpha (α)

**Formula:**
```
α = model.intercept_
```

**Meaning:** The baseline value of y when all features are zero.

### Beta (β)

**Formula:**
```
βᵢ = model.coef_[i]   for each feature i
```

**Meaning:** How much y changes when feature xᵢ increases by 1, holding other features constant.

### Gamma (γ)

**Formula:**
```
γ = R² = model.score(X_test, y_test)
```

**Meaning:** The proportion of variance in y explained by the model. R² = 1 means perfect fit; R² = 0 means no fit.

### Full Equation (Expanded)

```
y = α + β₁(1-syllable_words) + β₂(2-syllable_words) + ... + β₈(8-syllable_words)
      + β₉(word_length-1) + ... + β₁₆(word_length-8) + β₁₇(sentence_length)
```

### Training

- **Features (X):** 17 columns (syllable counts, word-length counts, sentence_length)
- **Target (y):** `avg_syllable/avg_word_length`
- **Split:** 80% train, 20% test
- **Algorithm:** Ordinary Least Squares (OLS) Linear Regression

### Output

- **File:** `urdu_readability_model.joblib`
- Contains: model, alpha, beta, gamma, feature_cols

---

## 4. Fry Readability Formula

### Origin

The **Fry Readability Graph** (Edward Fry, 1968) estimates reading grade from two metrics:

1. **X-axis:** Syllables per 100 words  
2. **Y-axis:** Sentences per 100 words  

### Standard Fry Formulae

#### X (Syllables per 100 words)

For a 100-word passage:
```
X = Total syllables in the 100-word passage
```

For per-sentence data:
```
X = (Total syllables in text / Total words in text) × 100
```

**With syllable counts by length (1–8 syllables):**
```
Total syllables = (1×n₁) + (2×n₂) + (3×n₃) + ... + (8×n₈)
```
where nᵢ = number of words with i syllables.

```
X = (Total syllables / sentence_length) × 100
```

#### Y (Sentences per 100 words)

For a 100-word passage:
```
Y = Number of sentences in the 100-word passage
```

For per-sentence data (one sentence):
```
Y = 100 / Words per sentence = 100 / sentence_length
```

**Example:** 10 words per sentence → Y = 100/10 = **10** sentences per 100 words.

### Fry Graph Interpretation

- **High X + Low Y** → Hard (difficult words, long sentences)
- **Low X + High Y** → Easy (simple words, short sentences)

---

## 5. Feature Extraction from Urdu Text

When a user enters Urdu text, we extract features programmatically.

### Step 1: Sentence Splitting

```
Sentences = split(text by [.!?۔؟\n])
```

### Step 2: Word Extraction

Words = sequences of Urdu/Arabic characters (Unicode range: 0600–08FF).

### Step 3: Syllable Estimation per Word

**Method A — With diacritics (harakat):**
```
syllables = count(vowel characters: ا و ی + harakat)
```

**Method B — Without diacritics (heuristic):**
```
syllables = max(1, min(8, (character_count + 1) // 2))
```

**Approximate:** Urdu has ~2–3 characters per syllable. So:
- 1–2 chars → 1 syllable  
- 3–4 chars → 2 syllables  
- 5–6 chars → 3 syllables  
- etc.

### Step 4: Aggregate Features

For each sentence, count:

- **nᵢ** = number of words with i syllables (i = 1 to 8)
- **mⱼ** = number of words with j characters (j = 1 to 8)
- **sentence_length** = total words / number of sentences

**Formulae:**
```
1-syllable_words = (sum of n₁ over all sentences) / number_of_sentences
2-syllable_words = (sum of n₂) / number_of_sentences
...
8-syllable_words = (sum of n₈) / number_of_sentences

word_length-1 = (sum of m₁) / number_of_sentences
...
word_length-8 = (sum of m₈) / number_of_sentences

sentence_length = total_words / number_of_sentences
```

---

## 6. Grade Calculation — Complete Flow

### When User Submits Text

#### Step 1: Extract Features

```python
features = extract_features(text)
# Returns: { "1-syllable_words": ..., "2-syllable_words": ..., ..., "sentence_length": ... }
```

#### Step 2: Compute Fry Metrics

**Total syllables:**
```
Total_syllables = (1×1-syllable_words + 2×2-syllable_words + ... + 8×8-syllable_words) × n_sentences
```

Actually, the features are stored as per-sentence averages, so:
```
Total_syllables = (1×f₁ + 2×f₂ + ... + 8×f₈) × n_sent
```
where fᵢ = features[f"{i}-syllable_words"] and n_sent = number of sentences.

**Syllables per 100 words:**
```
syll_per_100 = (Total_syllables / total_words) × 100
            = (Total_syllables / (sentence_length × n_sent)) × 100
```

**Sentences per 100 words:**
```
sent_per_100 = 100 / sentence_length
```

#### Step 3: Map to Grade (Fry-Based, Calibrated)

**Normalize to 0–1:**
```
syll_norm = (syll_per_100 - 100) / 150    # 100→0, 250→1
sent_norm = (sent_per_100 - 2) / 23
```

**Difficulty score:**
```
difficulty = syll_norm × 0.55 + (1 - sent_norm) × 0.45
```

**Meaning:**
- High syllables → harder
- Low sentences (long sentences) → harder

**Final grade:**
```
grade = 1 + difficulty × 11
grade = round(clip(grade, 1, 12))
```

**Result:** Integer between 1 and 12.

---

## 7. Web Application Flow

### Architecture

```
User Browser ←→ Flask Server (app.py) ←→ urdu_features.py
                    ↓
              urdu_readability_model.joblib (optional)
```

### Request Flow

1. User enters Urdu text in the textarea.
2. User clicks **"Analyze Readability"**.
3. Front-end sends `POST /api/analyze` with `{ "text": "..." }`.
4. Backend calls `predict_grade(text)`.
5. `predict_grade`:
   - Calls `compute_fry_metrics(text)` → (syll_per_100, sent_per_100)
   - Calls `fry_grade_from_metrics(syll_per_100, sent_per_100)` → grade
   - Optionally loads model and predicts ratio for display
6. Response: `{ grade, syllables_per_100, sentences_per_100, message, message_en }`.
7. Front-end displays: grade badge, scale bar, metrics, tips.

---

## 8. All Formulae Summary

### Preprocessing

| Step | Formula |
|------|---------|
| Drop null | `data = data.dropna()` |
| Drop column | `data = data.drop(columns=["Unnamed: 8"])` |

### Feature Extraction

| Metric | Formula |
|--------|---------|
| Syllables per word (heuristic) | `syllables = max(1, min(8, (len(chars) + 1) // 2))` |
| Total syllables | `Σ (i × nᵢ)` for i = 1..8 |
| Per-sentence avg | `feature_i = count_i / n_sentences` |

### Fry Metrics

| Metric | Formula |
|--------|---------|
| Syllables per 100 words | `(Total_syllables / total_words) × 100` |
| Sentences per 100 words | `100 / sentence_length` |

### Grade Calculation

| Step | Formula |
|------|---------|
| syll_norm | `(syll_per_100 - 100) / 150` |
| sent_norm | `(sent_per_100 - 2) / 23` |
| difficulty | `syll_norm × 0.55 + (1 - sent_norm) × 0.45` |
| grade | `round(clip(1 + difficulty × 11, 1, 12))` |

### Linear Regression (Model)

| Term | Formula |
|------|---------|
| Prediction | `y = α + Σ βᵢxᵢ` |
| Alpha | `α = model.intercept_` |
| Beta | `βᵢ = model.coef_[i]` |
| Gamma (R²) | `γ = 1 - SS_res/SS_tot` |

---

## 9. File Structure

```
check/
├── app.py                    # Flask backend, /api/analyze
├── index.html                # Web UI
├── urdu_features.py          # Feature extraction, Fry metrics, grade mapping
├── run_linear_regression.py  # Train model, save joblib
├── run_app.py                # Start web server
├── preprocess_data.py        # Clean dataset
├── fry_graph.py              # Generate Fry diagram
├── setup_and_run.py          # One-file setup for new laptop
├── requirements.txt          # Python dependencies
├── urdu_readability_model.joblib  # Trained model
├── input_to_linear_regression2.xlsx       # Raw data
├── input_to_linear_regression2_cleaned.csv # Cleaned data
├── fry_readability_diagram.png             # Fry graph image
├── explain.md                # This file
├── FRY_FORMULAE.md           # Fry formulae reference
└── README.md                 # Quick start
```

---

## 10. Quick Reference: End-to-End Example

**Input:** `"سعودی عرب کی کابینہ نے منگل کو مملکت"`

1. **Sentences:** 1  
2. **Words:** 8 (سعودی, عرب, کی, کابینہ, نے, منگل, کو, مملکت)  
3. **Syllables (heuristic):** 2, 2, 1, 3, 1, 2, 1, 3 → total = 15  
4. **syll_per_100:** (15/8) × 100 = **187.5**  
5. **sent_per_100:** 100/8 = **12.5**  
6. **syll_norm:** (187.5 - 100)/150 = 0.58  
7. **sent_norm:** (12.5 - 2)/23 = 0.46  
8. **difficulty:** 0.58×0.55 + 0.54×0.45 = 0.56  
9. **grade:** 1 + 0.56×11 = **7.2** → **Grade 7**

**Output:** "This text is suitable for Grade 7 readers."

---

*End of explain.md*
