from flask import Flask, request, jsonify
from flask_cors import CORS
from pathlib import Path
import re

try:
    from .chatbot import call_groq, SYSTEM_PROMPT
except ImportError:
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from chatbot import call_groq, SYSTEM_PROMPT

try:
    from .model_service import SmogModelService
    from .alerts import AlertService
    from .config import API_HOST, API_PORT, ALERT_THRESHOLD
    from .weather import get_current_weather
except ImportError:
    from model_service import SmogModelService
    from alerts import AlertService
    from config import API_HOST, API_PORT, ALERT_THRESHOLD

FRONTEND_PATH = str(Path(__file__).resolve().parent.parent / "frontend")
app = Flask(__name__, static_folder=FRONTEND_PATH, static_url_path="")
CORS(app, resources={r"/*": {"origins": "*"}})

# Generate live AQI data from datasets on startup
try:
    try:
        from .process_datasets import generate_aqi_data
    except ImportError:
        from process_datasets import generate_aqi_data
    generate_aqi_data()
except Exception as ex:
    print(f"Could not generate live AQI data: {ex}")


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/<path:path>")
def static_proxy(path):
    return app.send_static_file(path)


def get_recipients_from_test_twilio():
    # Return default email recipient
    return ["kamgarhossein@gmail.com"]


@app.route("/api/alert/recipients", methods=["GET"])
def get_recipients():
    nums = get_recipients_from_test_twilio()
    return jsonify({"recipients": nums})


model_service = None
alert_service = None

try:
    model_service = SmogModelService()
    print("Model service loaded successfully.", flush=True)
except Exception as ex:
    print(f"Could not load model: {ex}", flush=True)

try:
    alert_service = AlertService()
    print("Email alert service loaded successfully.", flush=True)
except Exception as ex:
    print(f"Could not initialize Email alert service: {ex}", flush=True)


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "model_loaded": model_service is not None, "alert_ready": alert_service is not None})

@app.route("/api/weather", methods=["GET"])
def weather_endpoint():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "city query parameter required"}), 400
    try:
        data = get_current_weather(city)
    except Exception as e:
        return jsonify({"error": str(e)}), 502
    return jsonify(data)


@app.route("/api/predict", methods=["POST"])
def predict():
    if model_service is None:
        return jsonify({"error": "Model service unavailable."}), 503

    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"error": "JSON payload is required."}), 400

    try:
        data = payload.get("data") or payload
        predictions = model_service.predict(data)
        return jsonify({"predictions": predictions})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400


@app.route("/api/alert", methods=["POST"])
def send_alert():
    if alert_service is None:
        return jsonify({"error": "Alert service unavailable."}), 503

    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"error": "JSON payload is required."}), 400

    recipient = payload.get("recipient")
    message = payload.get("message")
    threshold = payload.get("threshold")
    current_value = payload.get("current_value")

    if not recipient or not message:
        return jsonify({"error": "recipient and message fields are required."}), 400

    if threshold is not None and current_value is not None:
        try:
            current_value = float(current_value)
            threshold = float(threshold)
            if current_value < threshold:
                return jsonify({"sent": False, "reason": "Value is below threshold."}), 200
        except ValueError:
            return jsonify({"error": "threshold and current_value must be numeric."}), 400

    try:
        result = alert_service.send_alert(recipient, message)
        return jsonify({"sent": True, "message": result})
    except RuntimeError as exc:
        err_msg = str(exc)
        print(f"[ALERT ERROR] {err_msg}", flush=True)
        return jsonify({"sent": False, "error": err_msg}), 200
    except Exception as exc:
        return jsonify({"sent": False, "error": str(exc)}), 500


@app.route("/api/chat", methods=["POST"])
def chat():
    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"error": "JSON payload required."}), 400

    history = payload.get("messages", [])
    if not history:
        return jsonify({"error": "messages list is required."}), 400

    # Prepend system prompt
    full_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history

    try:
        reply = call_groq(full_messages)
        return jsonify({"reply": reply})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@app.route("/api/model_stats", methods=["GET"])
def model_stats():
    # Return mock model health, diagnostics, and metrics
    stats = {
        "model_version": "v1.2.3",
        "git_commit": "a1b2c3d",
        "last_trained": "2026-05-20T10:12:00Z",
        "accuracy": 0.872,
        "precision_macro": 0.85,
        "recall_macro": 0.84,
        "f1_macro": 0.845,
        "roc_auc": 0.91,
        "pr_auc": 0.88,
        "latency_avg_ms": 32,
        "latency_p95_ms": 75,
        "throughput_per_sec": 120,
        "dataset": {
            "size": 45000,
            "version": "ds-v4",
            "class_distribution": {"good": 12000, "moderate": 15000, "unhealthy": 9000, "hazardous": 9000}
        },
        "confusion_matrix": [[1100,200,50,10],[120,900,160,20],[20,80,700,40],[5,10,40,400]],
        "roc_curve": {"fpr": [0.0,0.1,0.2,1.0], "tpr": [0.0,0.7,0.85,1.0]},
        "precision_recall_curve": {"precision": [1.0,0.9,0.7,0.2], "recall":[0.0,0.4,0.8,1.0]},
        "feature_importance": [{"feature":"pm25_last_hour","importance":0.34},{"feature":"temperature", "importance":0.12}, {"feature":"humidity", "importance":0.09}],
        "calibration": {"bins":[0.1,0.3,0.5,0.7,0.9], "predicted":[0.08,0.28,0.51,0.72,0.89], "actual":[0.06,0.25,0.5,0.7,0.85]},
        "drift": {"kl_divergence":0.045, "drift_trend": [0.02,0.03,0.04,0.05,0.045]},
        "notes": "Model trained on ds-v4 using LSTM with 12 epochs. Retrain cadence: weekly"
    }
    return jsonify(stats)


if __name__ == "__main__":
    app.run(host=API_HOST, port=API_PORT, debug=True)
