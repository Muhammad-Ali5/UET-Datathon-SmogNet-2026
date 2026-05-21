# SmogGuard / SmogNet

This repository includes:
- `backend/` - Flask API, model loading, Twilio WhatsApp alert delivery, and frontend hosting
- `frontend/` - HTML pages for dashboard, alerts, city details, analytics
- `ml_models/` - trained model artifacts used by the backend

## Step-by-step run instructions

1. Install Python dependencies:
   ```powershell
   python -m pip install -r requirements.txt
   ```
2. Create the backend environment file:
   ```powershell
   copy backend\.env.example backend\.env
   ```
3. Edit `backend\.env` and add your Twilio settings:
   - `TWILIO_ACCOUNT_SID`
   - `TWILIO_AUTH_TOKEN`
   - `TWILIO_WHATSAPP_FROM`
4. Start the backend server from the repository root:
   ```powershell
   python backend\app.py
   ```
5. Open the frontend in your browser using the server URL:
   - `http://127.0.0.1:5000/alerts_manager_smognet.html`

## What is integrated

- The Flask backend serves static frontend pages from `frontend/`
- The alert manager calls `/api/alert` on the same server
- The model service loads `ml_models/best_smognet_model.pkl` for predictions
- Twilio WhatsApp alerts send messages through your configured account

## Notes

- If you do not yet have Twilio credentials, the backend will still start, but `/api/alert` will return an alert service error.
- Make sure the `ml_models/` directory contains `best_smognet_model.pkl`.
- Use the Flask server URL, not `file://`, so the frontend and API communicate correctly.
