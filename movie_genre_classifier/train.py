"""Train the movie genre classifier (TF-IDF + Multinomial Naive Bayes) and save it.

Quick start (uses the built-in synthetic sample data):
    python make_sample_data.py
    python train.py

With a real dataset:
    python train.py --data data/tmdb_5000_movies.csv --plot-col overview --keywords-col keywords --genre-col genres
    python train.py --data data/wiki_movie_plots.csv --plot-col Plot --keywords-col "" --genre-col Genre

The genre column may hold one genre ("Action"), several ("Action|Comedy") or a JSON list as in the TMDB file.
Only the first genre of each movie is used, because this model predicts one label.
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

try:
    from preprocess import clean_text
except ImportError:
    from movie_genre_classifier.preprocess import clean_text
    import movie_genre_classifier.preprocess as preprocess
    sys.modules["preprocess"] = preprocess

BASE = Path(__file__).parent
GENRE_ALIASES = {"romantic": "romance", "romantic comedy": "romance", "horror/thriller": "horror"}


def _parse_list(value):
    """Turns '[{"id": 1, "name": "Action"}]' or '["a", "b"]' into ['Action'] / ['a', 'b']; returns None if it is not JSON."""
    if not isinstance(value, str) or not value.strip().startswith("["):
        return None
    try:
        items = json.loads(value)
    except json.JSONDecodeError:
        return None
    return [str(i.get("name", "")) if isinstance(i, dict) else str(i) for i in items]


def first_genre(value):
    if pd.isna(value):
        return None
    names = _parse_list(value)
    if names is not None:
        return names[0] if names else None
    return re.split(r"[|,/;]", str(value))[0].strip() or None


def keywords_text(value):
    if pd.isna(value):
        return ""
    names = _parse_list(value)
    return " ".join(names) if names is not None else re.sub(r"[|;,]", " ", str(value))


def load_dataset(path, plot_col, keywords_col, genre_col, genres):
    df = pd.read_csv(path)
    for col in (plot_col, genre_col):
        if col not in df.columns:
            raise SystemExit(f"Column '{col}' not found in {path}. Columns are: {list(df.columns)}")

    wanted = {g.lower(): g for g in genres}
    df["genre"] = df[genre_col].map(first_genre).map(
        lambda g: wanted.get(GENRE_ALIASES.get(str(g).lower(), str(g).lower())) if g else None)
    keywords = df[keywords_col].map(keywords_text) if keywords_col and keywords_col in df.columns else ""
    df["text"] = df[plot_col].fillna("").astype(str) + " " + keywords
    df = df.dropna(subset=["genre"])
    df = df[df["text"].str.strip().str.len() > 10]
    return df[["text", "genre"]].reset_index(drop=True)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--data", default=str(BASE / "data" / "movies_sample.csv"))
    p.add_argument("--plot-col", default="plot")
    p.add_argument("--keywords-col", default="keywords", help='use "" if the file has no keywords column')
    p.add_argument("--genre-col", default="genre")
    p.add_argument("--genres", default="Action,Comedy,Horror,Romance,Drama", help="comma-separated genres to keep")
    p.add_argument("--test-size", type=float, default=0.2)
    p.add_argument("--alpha", type=float, default=0.5, help="Naive Bayes smoothing")
    p.add_argument("--cv", type=int, default=5, help="cross-validation folds (0 to skip)")
    p.add_argument("--model-out", default=str(BASE / "models" / "genre_model.joblib"))
    args = p.parse_args()

    genres = [g.strip() for g in args.genres.split(",") if g.strip()]
    df = load_dataset(args.data, args.plot_col, args.keywords_col, args.genre_col, genres)
    print(f"Loaded {len(df)} movies from {args.data}")
    print(df["genre"].value_counts().to_string(), "\n")
    if df["genre"].nunique() < 2 or df["genre"].value_counts().min() < 5:
        raise SystemExit("Need at least 2 genres with 5+ movies each. Check --genre-col and --genres.")

    x_train, x_test, y_train, y_test = train_test_split(
        df["text"], df["genre"], test_size=args.test_size, random_state=42, stratify=df["genre"])

    model = Pipeline([
        ("tfidf", TfidfVectorizer(preprocessor=clean_text, ngram_range=(1, 2), min_df=2, sublinear_tf=True)),
        ("nb", MultinomialNB(alpha=args.alpha)),
    ])
    model.fit(x_train, y_train)

    predictions = model.predict(x_test)
    accuracy = accuracy_score(y_test, predictions)
    labels = list(model.classes_)
    print(f"Test accuracy: {accuracy:.3f}  ({len(x_test)} test movies)\n")
    print(classification_report(y_test, predictions, zero_division=0))
    matrix = confusion_matrix(y_test, predictions, labels=labels)
    print("Confusion matrix (rows = real genre, columns = predicted):")
    print(pd.DataFrame(matrix, index=labels, columns=labels).to_string(), "\n")

    cv_mean = None
    if args.cv and args.cv > 1:
        scores = cross_val_score(model, df["text"], df["genre"], cv=args.cv)
        cv_mean = float(scores.mean())
        print(f"{args.cv}-fold cross-validation accuracy: {cv_mean:.3f} (+/- {scores.std():.3f})")

    model.fit(df["text"], df["genre"])  # final model learns from every movie
    Path(args.model_out).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, args.model_out)
    metrics = {
        "trained_at": datetime.now(timezone.utc).isoformat(), "data": args.data, "rows": len(df),
        "test_accuracy": accuracy, "cv_accuracy": cv_mean, "labels": labels, "confusion_matrix": matrix.tolist(),
        "report": classification_report(y_test, predictions, output_dict=True, zero_division=0),
    }
    Path(args.model_out).with_name("metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(f"\nSaved model to {args.model_out}")


if __name__ == "__main__":
    main()
