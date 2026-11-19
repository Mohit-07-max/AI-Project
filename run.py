"""Main entry point to run the Movie Genre Classifier web app.

Usage:
    python run.py
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PKG_DIR = BASE_DIR / "movie_genre_classifier"
if str(PKG_DIR) not in sys.path:
    sys.path.insert(0, str(PKG_DIR))

from movie_genre_classifier.app import app

if __name__ == "__main__":
    print("Starting Movie Genre Predictor at http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
