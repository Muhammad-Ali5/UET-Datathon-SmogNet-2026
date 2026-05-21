import smtplib
from email.message import EmailMessage

try:
    from .config import SMTP_USER, SMTP_PASSWORD, SMTP_HOST, SMTP_PORT
except ImportError:
    from config import SMTP_USER, SMTP_PASSWORD, SMTP_HOST, SMTP_PORT


class AlertService:
    def __init__(self):
        if not SMTP_USER or not SMTP_PASSWORD:
            raise ValueError("SMTP credentials are required. Set SMTP_USER and SMTP_PASSWORD in backend/.env.")
        
        self.user = SMTP_USER
        self.password = SMTP_PASSWORD
        self.host = SMTP_HOST
        self.port = SMTP_PORT

    def send_alert(self, recipient: str, body: str):
        try:
            msg = EmailMessage()
            msg.set_content(body)
            msg['Subject'] = 'Air Pollution Alert 🚨⚠️ from SmogNet'
            msg['From'] = self.user
            msg['To'] = recipient

            # Using SSL to connect to Gmail
            with smtplib.SMTP_SSL(self.host, self.port) as server:
                server.login(self.user, self.password)
                server.send_message(msg)

            return {
                "status": "delivered",
                "to": recipient,
                "body": body,
            }
        except Exception as e:
            raise RuntimeError(f"SMTP error: {str(e)}") from e
