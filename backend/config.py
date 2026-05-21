from pathlib import Path
from dotenv import load_dotenv
import os

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))

MODEL_PATH = os.getenv("MODEL_PATH", str(ROOT.parent / "ml_models" / "best_smognet_model.pkl"))
LABEL_ENCODER_PATH = os.getenv("LABEL_ENCODER_PATH", str(ROOT.parent / "ml_models" / "label_encoder.pkl"))
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "5000"))
ALERT_THRESHOLD = float(os.getenv("ALERT_THRESHOLD", "100"))
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "your-openweather-api-key")

