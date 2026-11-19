# Movie Genre Classifier 🎬🤖

An AI/ML project that classifies movie genres from plot summaries and keywords using Natural Language Processing (TF-IDF + Multinomial Naive Bayes) with an interactive, modern dark-themed web interface.

---

## ✨ Features
- **Multi-Genre Prediction**: Predicts probabilities for movie genres (Action, Comedy, Horror, Romance, Drama, etc.) based on storyline synopses and tags.
- **Modern Web Interface**: Built with Flask featuring a sleek dark theme with electric cobalt blue accents.
- **REST API Endpoint**: Easy integration via `POST /api/predict`.
- **Lightweight & Fast**: Compact model pipeline for instant real-time inference.

---

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Clone the repository
git clone https://github.com/Mohit-07-max/AI-Project.git
cd "AI Project"

# Create and activate virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r movie_genre_classifier/requirements.txt
```

### 2. Run the Web Application
```bash
python run.py
# or
python movie_genre_classifier/app.py
```
Open your browser and navigate to `http://127.0.0.1:5000`.

### 3. CLI Prediction
```bash
python movie_genre_classifier/predict.py --plot "A secret agent embarks on a dangerous mission to save the world" --keywords "agent, mission, spy"
```

### 4. Retrain the Model
```bash
python movie_genre_classifier/train.py
```

---

## 📁 Project Structure
```
AI Project/
├── movie_genre_classifier/
│   ├── app.py                # Flask web app & REST API
│   ├── train.py              # Model training script
│   ├── predict.py            # CLI prediction script
│   ├── preprocess.py         # Text preprocessing & cleaning
│   ├── make_sample_data.py   # Sample data generator
│   ├── requirements.txt      # Python dependencies
│   ├── data/                 # Training dataset
│   └── models/               # Serialized model & metrics
├── .gitignore
└── README.md
```
