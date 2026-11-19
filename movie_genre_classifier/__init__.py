"""Movie Genre Classifier package."""

from .predict import load_model, predict_genres
from .preprocess import clean_text

__all__ = ["load_model", "predict_genres", "clean_text"]
