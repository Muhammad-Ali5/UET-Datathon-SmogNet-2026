# SmogNet Backend

This backend provides:
- `/api/health` for service health checks
- `/api/predict` to run model inference
- `/api/alert` to send WhatsApp alerts through Twilio
- static frontend hosting for HTML pages from `frontend/`

## Setup

1. Install dependencies from the repository root:
   ```powershell
   python -m pip install -r requirements.txt
   ```
2. Copy the environment file:
   ```powershell
   copy .env.example .env
   ```
3. Add your Twilio credentials to `backend\.env`.
4. Start the backend service:
   ```powershell
   python app.py
   ```
5. Open the app in a browser at:
   ```text
   http://127.0.0.1:5000/alerts_manager_smognet.html
   ```

## Example request

```bash
curl -X POST http://127.0.0.1:5000/api/alert \
  -H "Content-Type: application/json" \
  -d '{"recipient": "whatsapp:+1234567890", "message": "Air quality alert!"}'
```
