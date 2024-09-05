import os
from plyer import notification

class NotificationManager:
    def __init__(self):
        self.app_name = "Wuneed"

    def send_notification(self, title: str, message: str):
        notification.notify(
            title=title,
            message=message,
            app_name=self.app_name,
            timeout=10
        )

    def notify_update_available(self, version: str):
        self.send_notification(
            "Update Available",
            f"A new version of Wuneed (v{version}) is available. Run 'wuneed update' to upgrade."
        )

    def notify_insight(self, insight: str):
        self.send_notification(
            "Wuneed Insight",
            insight
        )

notification_manager = NotificationManager()