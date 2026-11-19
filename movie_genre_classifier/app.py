"""Small web app for interactive genre prediction.

    python app.py        then open http://127.0.0.1:5000
JSON API:  POST /api/predict   {"plot": "...", "keywords": "..."}
"""

from flask import Flask, jsonify, render_template_string, request

from predict import load_model, predict_genres

app = Flask(__name__)
MAX_CHARS = 5000

try:
    MODEL = load_model()
    MODEL_ERROR = None
except FileNotFoundError as error:
    MODEL, MODEL_ERROR = None, str(error)

PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="dark">
  <title>Movie Genre Predictor</title>
  <style>
    :root {
      color-scheme: dark;
      --bg: #08090d;
      --surface: #0f1320;
      --surface-border: #1a233a;
      --input-bg: #090c14;
      --input-border: #1e2a47;
      --text: #f8faff;
      --text-muted: #8fa0c2;
      --cobalt: #0052ff;
      --cobalt-hover: #1a6aff;
      --cobalt-glow: rgba(0, 82, 255, 0.45);
      --cobalt-gradient: linear-gradient(135deg, #0047ff 0%, #0066ff 100%);
      --bar-track: #151b2c;
      --accent-color: #0052ff;
      accent-color: var(--accent-color);
    }
    * { box-sizing: border-box; }
    body {
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      max-width: 680px;
      margin: 40px auto;
      padding: 0 20px;
      color: var(--text);
      background-color: var(--bg);
      background-image: radial-gradient(circle at 50% -20%, rgba(0, 82, 255, 0.22) 0%, transparent 65%);
      background-repeat: no-repeat;
      min-height: 100vh;
      line-height: 1.5;
    }
    h1 {
      margin-bottom: 6px;
      font-weight: 700;
      letter-spacing: -0.02em;
      color: #ffffff;
    }
    h1 span {
      color: #3b82f6;
      background: linear-gradient(135deg, #4d8eff 0%, #0052ff 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    p.sub {
      color: var(--text-muted);
      margin-top: 0;
      margin-bottom: 24px;
      font-size: 0.98rem;
    }
    label {
      display: block;
      font-weight: 600;
      margin: 18px 0 8px;
      color: #e2e8f0;
      font-size: 0.92rem;
    }
    textarea, input {
      width: 100%;
      box-sizing: border-box;
      padding: 13px 15px;
      background: var(--input-bg);
      color: var(--text);
      border: 1px solid var(--input-border);
      border-radius: 10px;
      font: inherit;
      transition: border-color 0.2s, box-shadow 0.2s;
    }
    textarea:focus, input:focus {
      outline: none;
      border-color: var(--cobalt);
      box-shadow: 0 0 0 3px rgba(0, 82, 255, 0.3), 0 0 16px rgba(0, 82, 255, 0.15);
    }
    textarea::placeholder, input::placeholder {
      color: #4f5f7f;
    }
    button {
      margin-top: 20px;
      padding: 12px 28px;
      border: 0;
      border-radius: 999px;
      background: var(--cobalt-gradient);
      color: #ffffff;
      font: 600 1rem inherit;
      cursor: pointer;
      box-shadow: 0 4px 18px var(--cobalt-glow);
      transition: all 0.2s ease;
    }
    button:hover {
      background: linear-gradient(135deg, #1459ff 0%, #1f78ff 100%);
      box-shadow: 0 6px 24px rgba(0, 82, 255, 0.65);
      transform: translateY(-1px);
    }
    button:active {
      transform: translateY(0);
      box-shadow: 0 2px 10px var(--cobalt-glow);
    }
    .card {
      margin-top: 28px;
      padding: 24px;
      background: var(--surface);
      border: 1px solid var(--surface-border);
      border-radius: 14px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), 0 0 20px rgba(0, 82, 255, 0.08);
    }
    .card h2 {
      margin-top: 0;
      margin-bottom: 18px;
      font-size: 1.25rem;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .badge {
      display: inline-block;
      padding: 4px 12px;
      background: rgba(0, 82, 255, 0.18);
      border: 1px solid rgba(0, 82, 255, 0.45);
      color: #70a5ff;
      border-radius: 999px;
      font-size: 0.95rem;
      font-weight: 700;
      letter-spacing: 0.02em;
    }
    .row {
      display: flex;
      align-items: center;
      gap: 14px;
      margin: 12px 0;
    }
    .row span:first-child {
      width: 90px;
      font-weight: 600;
      color: #e2e8f0;
      font-size: 0.95rem;
    }
    .bar {
      flex: 1;
      height: 12px;
      background: var(--bar-track);
      border-radius: 99px;
      overflow: hidden;
    }
    .bar i {
      display: block;
      height: 100%;
      background: linear-gradient(90deg, #0047ff 0%, #0091ff 100%);
      box-shadow: 0 0 10px rgba(0, 82, 255, 0.7);
      border-radius: 99px;
    }
    .row span:last-child {
      width: 48px;
      text-align: right;
      color: var(--text-muted);
      font-variant-numeric: tabular-nums;
      font-size: 0.9rem;
    }
    .err {
      color: #fca5a5;
      background: rgba(220, 38, 38, 0.15);
      border: 1px solid rgba(239, 68, 68, 0.35);
      padding: 12px 16px;
      border-radius: 10px;
      margin-top: 18px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
  </style>
</head>
<body>
  <h1>Movie <span>Genre Predictor</span></h1>
  <p class="sub">Paste a plot summary (and optional keywords) to predict the genre.</p>
  {% if model_error %}<div class="err"><span>⚠️</span> <span>{{ model_error }}</span></div>{% endif %}
  <form method="post">
    <label for="plot">Plot summary</label>
    <textarea id="plot" name="plot" rows="6" maxlength="5000" required placeholder="Describe the storyline...">{{ plot }}</textarea>
    <label for="keywords">Keywords (optional)</label>
    <input id="keywords" name="keywords" maxlength="500" value="{{ keywords }}" placeholder="e.g. bomb, chase, mission">
    <button type="submit">Predict genre</button>
  </form>
  {% if error %}<div class="err"><span>⚠️</span> <span>{{ error }}</span></div>{% endif %}
  {% if results %}
  <div class="card">
    <h2>Predicted genre: <span class="badge">{{ results[0][0] }}</span></h2>
    {% for genre, prob in results %}
    <div class="row">
      <span>{{ genre }}</span>
      <div class="bar"><i style="width:{{ (prob*100)|round(1) }}%"></i></div>
      <span>{{ (prob*100)|round(1) }}%</span>
    </div>
    {% endfor %}
  </div>
  {% endif %}
</body>
</html>"""


@app.route("/", methods=["GET", "POST"])
def index():
    plot = request.form.get("plot", "")[:MAX_CHARS]
    keywords = request.form.get("keywords", "")[:500]
    results, error = None, None
    if request.method == "POST":
        if MODEL is None:
            error = MODEL_ERROR
        else:
            try:
                results = predict_genres(MODEL, plot, keywords, top=5)
            except ValueError as problem:
                error = str(problem)
    return render_template_string(PAGE, plot=plot, keywords=keywords, results=results, error=error, model_error=MODEL_ERROR)


@app.post("/api/predict")
def api_predict():
    data = request.get_json(silent=True) or {}
    if MODEL is None:
        return jsonify(error=MODEL_ERROR), 503
    try:
        results = predict_genres(MODEL, str(data.get("plot", ""))[:MAX_CHARS], str(data.get("keywords", ""))[:500], top=5)
    except ValueError as problem:
        return jsonify(error=str(problem)), 400
    return jsonify(genre=results[0][0], probabilities=[{"genre": g, "probability": round(p, 4)} for g, p in results])


if __name__ == "__main__":
    app.run(debug=False)
