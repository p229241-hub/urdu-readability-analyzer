# Urdu Readability Checker
**Developed by Fayaz Ahmad Khan**

Welcome to the **Urdu Readability Checker**! I developed this project to analyze the complex structure of Urdu text and determine its appropriate educational grade level (Grades 1 through 12). This helps educators, authors, and publishers evaluate whether a book or article is suitable for children or advanced readers.

## 🚀 About the Project
Calculating readability in English is common, but doing it mathematically for Urdu presents unique challenges. To solve this, I designed a system that leverages the **Fry Readability Graph principles** combined with a custom-trained **Multiple Linear Regression Machine Learning Model**. 

I trained this model on a massive dataset of over **243,000 Urdu sentences**, analyzing intricate details like:
- The count of words by their syllable lengths (1 to 8 syllables).
- Average sentence lengths.
- Word complexity.

Because I have extracted the Alpha (Intercept) and Beta (Coefficients) from this massive dataset training phase, the model operates completely independently. It extracts features from any new text directly and accurately calculates a reading complexity score in milliseconds!

## ⚙️ Features
- **Instant Urdu Text Analysis:** Simply paste Urdu text and get an instant Readability Grade level.
- **Scientifically Calibrated:** The Fry-based grading metric has been specifically calibrated to the grammatical constraints of the Urdu language.
- **Beautiful Web Interface:** I designed a clean, responsive UI with options to import `.txt` files, paste text directly, or load pre-built samples.
- **Lightweight & Fast:** The core machine learning model is saved via `joblib`, making predictions lightning-fast without needing to reload the dataset.

## 📂 Project Structure

| File | Purpose |
|------|---------|
| `app.py` | The main Flask backend server. |
| `urdu_features.py` | The logic for extracting syllables, word lengths, and sentence data. |
| `urdu_readability_model.joblib` | My pre-trained Linear Regression machine learning model. |
| `run_linear_regression.py` | The original script I used to process the dataset and train the ML model. |
| `index.html` | The frontend web user interface. |
| `MODEL_EXPLANATION.md` | Detailed breakdown of the exact mathematical equation I derived. |

## 🛠️ How to Run Locally

If you want to test my project on your own machine, follow these steps:

1. Clone or download this repository.
2. Open a terminal and install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the Flask application:
   ```bash
   python app.py
   ```
   *(Note: You can also use `python run_app.py` if present)*
4. Open your web browser and navigate to `http://127.0.0.1:5000` to see the app running!

## ☁️ How to Deploy to the Web (Render)

I have organized this repository so it immediately deploys to cloud providers like **Render.com**. 
1. Link your GitHub repository to Render by creating a **New Web Service**.
2. Select **Python 3** as your environment.
3. Use the following **Build Command**: `pip install -r requirements.txt`
4. Use the following **Start Command**: `gunicorn app:app`

---
*Created with dedication by Fayaz Ahmad Khan.*
