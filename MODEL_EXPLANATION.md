# Urdu Readability Linear Regression Model Explanation

This document contains a full explanation of the `run_linear_regression.py` script, including its structure, logic, and the resulting mathematical parameters (Alpha, Beta, and Gamma) that it generated upon execution.

## 1. Linear Regression Output Parameters

When the model is trained against your dataset, it calculates these mathematical scores:

- **Alpha (Intercept)**: `1.022090`  
  *This is the baseline prediction when all features are exactly zero.*
- **Gamma (R² Score)**: `0.176322`  
  *Indicates the percentage of the variance in the predicted readability score that can be explained by the input features. This denotes an approximate 17.6% explained variance.*
- **Root Mean Squared Error (RMSE)**: `0.1750`  

### Beta (Coefficients)
The beta coefficients show the magnitude of the impact each feature has on the final readability prediction. Notice how sentence length and syllable counts correlate differently to the output constraint:

* `1-syllable_words`: `0.072768`
* `2-syllable_words`: `0.075913`
* `3-syllable_words`: `0.079541`
* `4-syllable_words`: `0.085829`
* `5-syllable_words`: `0.084758`
* `6-syllable_words`: `0.051990`
* `7-syllable_words`: `0.036880`
* `8-syllable_words`: `0.022127`
* `word_length-1`: `-0.088196`
* `word_length-2`: `-0.094919`
* `word_length-3`: `-0.096960`
* `word_length-4`: `-0.100059`
* `word_length-5`: `-0.102691`
* `word_length-6`: `-0.106491`
* `word_length-7`: `-0.110798`
* `word_length-8`: `-0.121828`
* `sentence_length`: `0.022337`

### The Derived Mathematical Formula
Because the model has been trained on the dataset to find the best mathematical relationship, it has produced these specific Alpha (Intercept) and Beta (Coefficients) values. This means you **no longer need the dataset** to calculate readability. You just need to extract the features from any new Urdu text and plug them into this exact derived formula:

```text
Readability Complexity Score = 
    1.022090  (Alpha/Intercept)
  + (0.072768 * count of 1-syllable_words)
  + (0.075913 * count of 2-syllable_words)
  + (0.079541 * count of 3-syllable_words)
  + (0.085829 * count of 4-syllable_words)
  + (0.084758 * count of 5-syllable_words)
  + (0.051990 * count of 6-syllable_words)
  + (0.036880 * count of 7-syllable_words)
  + (0.022127 * count of 8-syllable_words)
  - (0.088196 * count of word_length-1)
  - (0.094919 * count of word_length-2)
  - (0.096960 * count of word_length-3)
  - (0.100059 * count of word_length-4)
  - (0.102691 * count of word_length-5)
  - (0.106491 * count of word_length-6)
  - (0.110798 * count of word_length-7)
  - (0.121828 * count of word_length-8)
  + (0.022337 * sentence_length)
```

---

## 2. Explanation of the Code and Pipeline

The script `run_linear_regression.py` manages an entire end-to-end data processing and model-training pipeline. Here is a step-by-step breakdown of how it works:

### Step 1: Data Loading & Cleaning
Initially, the script attempts to load a pre-cleaned CSV (`input_to_linear_regression2_cleaned.csv`). If it cannot find this file, it gracefully falls back to your original Excel workbook (`input_to_linear_regression2.xlsx`), strips out unnecessary artifacts (such as the `Unnamed: 8` column), and drops any rows that contain missing information to ensure a clean dataset.

### Step 2: Feature Selection (X and Y axis mapping)
The script tells the machine learning model exactly what properties it should learn from (`X`). It isolates features like the sentence distribution broken down by syllable density (e.g., `1-syllable_words`, `2-syllable_words`) and specific word-string lengths.
The output truth that the model is trying to predict (`y`) is the `avg_syllable/avg_word_length` ratio, which mathematically represents the textual difficulty or "complexity."

### Step 3: Dataset Splitting
The line `train_test_split(X, y, test_size=0.2, random_state=42)` slices the data into two discrete parts:
- **80% Training Data:** Used by the model to "learn" how syllable patterns logically map to the difficulty of reading.
- **20% Testing Data:** Kept hidden during training. It is later queried to predict against, which evaluates the model's intelligence and calculates its Gamma score.

### Step 4: Training & Saving the Model
`LinearRegression().fit()` invokes the actual algorithmic learning process. Once the linear math function calculates the weights (betas) for the defined metrics, it uses `joblib.dump` to save the trained model to permanent disk storage (`urdu_readability_model.joblib`). By freezing the model to a file, the Flask web UI can immediately utilize it to evaluate live Urdu text inputs without retraining itself linearly each time.

### Step 5: Diagram Production
Finally, the script executes an external asset `exec(open("fry_graph.py"...))`. This renders a visual "Fry Readability Diagram" using plotting tools, providing a standardized proof of statistical validity for the trained model to help you understand where typical sentence complexity metrics fall visually.
