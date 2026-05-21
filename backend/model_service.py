import joblib
import pandas as pd
import xgboost
from pathlib import Path
try:
    from .config import MODEL_PATH
except ImportError:
    from config import MODEL_PATH


# Monkey-patch base XGBModel to ensure unpickling backwards compatibility with newer XGBoost versions
def patched_xgb_getattr(self, name):
    defaults = {
        'use_label_encoder': False,
        'gpu_id': None,
        'importance_type': None,
        'predictor': 'auto',
        'n_jobs': None,
        'validate_parameters': False
    }
    if name in defaults:
        return defaults[name]
    raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

xgboost.sklearn.XGBModel.__getattr__ = patched_xgb_getattr


class SmogModelService:
    def __init__(self):
        self.model_path = Path(MODEL_PATH)
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model file not found at {self.model_path}")
        self.model = joblib.load(self.model_path)

    def predict(self, payload):
        if isinstance(payload, dict):
            df = pd.DataFrame([payload])
        elif isinstance(payload, list):
            df = pd.DataFrame(payload)
        else:
            raise ValueError("Payload must be a dict or list of dicts.")

        prediction = self.model.predict(df)
        return prediction.tolist()
