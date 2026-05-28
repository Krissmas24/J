import requests
import json
from core.database import db

def send_webhook(event_type, details):
    webhook_url = db.get_setting("webhook_url", "")
    if not webhook_url:
        return

    payload = {
        "embeds": [{
            "title": f"J Macro - {event_type}",
            "description": details,
            "color": 0xFFD700,  # Gold
            "footer": {"text": "v0.01.000.0000 | Rebirth"}
        }]
    }

    try:
        requests.post(webhook_url, json=payload, timeout=5)
    except Exception as e:
        db.log_event("ERROR", f"Webhook failed: {e}")
