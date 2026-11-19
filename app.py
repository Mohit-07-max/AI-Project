"""Root launcher for the Movie Genre Classifier web app.

Usage:
    python app.py
"""

from run import app

if __name__ == "__main__":
    app.run(debug=True, port=5000)
