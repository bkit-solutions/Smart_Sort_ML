import os
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# -----------------------------
# Flask App Initialization
# -----------------------------
app = Flask(__name__)
app.secret_key = "super-secret-key"   # Change in production

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
HISTORY_FILE = os.path.join(BASE_DIR, "history.json")
MODEL_PATH = os.path.join(BASE_DIR, "healthy_vs_rotten.h5")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -----------------------------
# Model + Class Labels
# -----------------------------
model = load_model(MODEL_PATH)

class_names = [
    'Apple___Healthy', 'Apple___Rotten',
    'Banana___Healthy', 'Banana___Rotten',
    'Bellpepper___Healthy', 'Bellpepper___Rotten',
    'Carrot___Healthy', 'Carrot___Rotten',
    'Cucumber___Healthy', 'Cucumber___Rotten',
    'Grape___Healthy', 'Grape___Rotten',
    'Guava___Healthy', 'Guava___Rotten',
    'Jujube___Healthy', 'Jujube___Rotten',
    'Mango___Healthy', 'Mango___Rotten',
    'Orange___Healthy', 'Orange___Rotten',
    'Pomegranate___Healthy', 'Pomegranate___Rotten',
    'Potato___Healthy', 'Potato___Rotten',
    'Strawberry___Healthy', 'Strawberry___Rotten',
    'Tomato___Healthy', 'Tomato___Rotten'
]

ALLOWED_EXT = {"png", "jpg", "jpeg"}

# -----------------------------
# Utility Functions
# -----------------------------
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT


def cleanup_uploads():
    """Keep only the 20 latest uploaded images."""
    files = sorted(
        [os.path.join(UPLOAD_FOLDER, f) for f in os.listdir(UPLOAD_FOLDER)],
        key=os.path.getctime
    )
    if len(files) > 20:
        for old in files[:-20]:
            os.remove(old)


def preprocess_image(img_path):
    """Pre-process image according to your model."""
    img = load_img(img_path, target_size=(150, 150))
    img_array = img_to_array(img) / 255.0
    return np.expand_dims(img_array, axis=0)


def predict_image(img_path):
    """Run inference and return top label + confidence."""
    arr = preprocess_image(img_path)
    pred = model.predict(arr)
    idx = np.argmax(pred)
    confidence = float(np.max(pred)) * 100
    return class_names[idx], round(confidence, 2)


def append_history(entry):
    history = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                history = json.load(f)
        except:
            history = []

    history.insert(0, entry)   # newest first
    history = history[:200]

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

# -----------------------------
# Routes
# -----------------------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file uploaded.")
            return redirect(request.url)

        file = request.files["file"]

        if file.filename == "":
            flash("Please choose an image.")
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash("Only PNG, JPG, JPEG allowed.")
            return redirect(request.url)

        # save
        filename = secure_filename(datetime.utcnow().strftime("%Y%m%d_%H%M%S_") + file.filename)
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(save_path)

        cleanup_uploads()

        # prediction
        label, conf = predict_image(save_path)

        # store history entry
        append_history({
            "filename": filename,
            "label": label,
            "confidence": conf,
            "time": datetime.utcnow().isoformat()
        })

        return render_template("result.html",
                               image_url=url_for("static", filename=f"uploads/{filename}"),
                               label=label,
                               confidence=conf)

    return render_template("predict.html")


@app.route("/dashboard")
def dashboard():
    history = load_history()

    total = len(history)
    healthy = sum(1 for h in history if "Healthy" in h["label"])
    rotten = sum(1 for h in history if "Rotten" in h["label"])

    # Per-day counts for charts
    counts_by_day = {}
    for h in history:
        day = h["time"][:10]
        if day not in counts_by_day:
            counts_by_day[day] = {"total": 0, "rotten": 0}
        counts_by_day[day]["total"] += 1
        if "Rotten" in h["label"]:
            counts_by_day[day]["rotten"] += 1

    latest = history[:50]

    return render_template("dashboard.html",
                           total=total,
                           healthy=healthy,
                           rotten=rotten,
                           counts_by_day=counts_by_day,
                           latest=latest)


@app.route("/team")
def team():
    return render_template("team.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        print("Message from:", request.form.get("name"), request.form.get("email"))
        flash("Thank you! Your message has been received.")
        return redirect(url_for("contact"))
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
