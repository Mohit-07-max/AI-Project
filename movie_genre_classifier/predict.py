"""Predict the genre of a movie from its plot summary and keywords.

    python predict.py --plot "A soldier must stop a terrorist before the city explodes" --keywords "bomb, mission"
    python predict.py            (no arguments: asks you to type a plot)
"""

import argparse
import sys
from pathlib import Path

import joblib

PACKAGE_DIR = Path(__file__).resolve().parent
if str(PACKAGE_DIR) not in sys.path:
    sys.path.insert(0, str(PACKAGE_DIR))

try:
    import preprocess  # noqa: F401  (the saved model needs this module to be importable)
except ImportError:
    from movie_genre_classifier import preprocess  # noqa: F401
    sys.modules["preprocess"] = preprocess

MODEL_PATH = Path(__file__).parent / "models" / "genre_model.joblib"


def load_model(path=MODEL_PATH):
    if not Path(path).exists():
        raise FileNotFoundError(f"No trained model at {path}. Run:  python train.py")
    return joblib.load(path)


def predict_genres(model, plot, keywords="", top=3):
    """Returns the `top` most likely genres as [(genre, probability), ...], best first."""
    text = f"{plot} {keywords}".strip()
    if not text:
        raise ValueError("Enter a plot summary or some keywords.")
    probabilities = model.predict_proba([text])[0]
    ranked = sorted(zip(model.classes_, probabilities), key=lambda pair: pair[1], reverse=True)
    return [(str(genre), float(prob)) for genre, prob in ranked[:top]]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--plot")
    parser.add_argument("--keywords", default="")
    args = parser.parse_args()
    plot = args.plot or input("Plot summary: ")
    keywords = args.keywords if args.plot else input("Keywords (optional): ")
    for genre, prob in predict_genres(load_model(), plot, keywords):
        print(f"{genre:<10} {prob:6.1%}")
