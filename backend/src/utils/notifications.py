import requests
from src.core.settings import get_settings
from src.utils.logger import log_event

settings = get_settings()

def notify_admin(message: str) -> bool:
    """Kritik hataları Slack üzerinden bildirir"""
    try:
        webhook_url = settings.SLACK_WEBHOOK_URL
        payload = {"text": f"🚨 {message}"}
        response = requests.post(webhook_url, json=payload)
        
        if response.status_code == 200:
            log_event("INFO", "notifications", "Bildirim başarıyla gönderildi")
            return True
        else:
            log_event("ERROR", "notifications", f"Bildirim gönderilemedi: {response.text}")
            return False
    except Exception as e:
        log_event("ERROR", "notifications", f"Bildirim hatası: {str(e)}")
        return False 