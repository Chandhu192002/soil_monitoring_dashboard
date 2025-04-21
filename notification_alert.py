# Enhanced notification_alert.py with logging, email, and custom alerts
import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import os

# Pushbullet API
PUSHBULLET_API_KEY = "o.S0ZbsRGttKGlSigDSm17YCOXAu9wT6Mi"

# Email credentials (use environment variables for security)
EMAIL_SENDER = os.getenv("ALERT_EMAIL")
EMAIL_PASSWORD = os.getenv("ALERT_EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("ALERT_EMAIL_RECEIVER")

# Thresholds
MOISTURE_THRESHOLD = 30
DISTANCE_THRESHOLD = 10

# Log file
LOG_FILE = "alerts.log"

# Util: log alert
def log_alert(title, body):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now().isoformat()}] {title}: {body}\n")

# Pushbullet notification
def send_pushbullet_notification(title, body):
    url = "https://api.pushbullet.com/v2/pushes"
    headers = {
        "Access-Token": PUSHBULLET_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "type": "note",
        "title": title,
        "body": body
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            print("Pushbullet notification sent.")
        else:
            print("Pushbullet error:", response.text)
    except Exception as e:
        print("Pushbullet exception:", str(e))

# Email alert
def send_email_notification(subject, content):
    if not (EMAIL_SENDER and EMAIL_PASSWORD and EMAIL_RECEIVER):
        print("Email config missing. Skipping.")
        return
    try:
        msg = MIMEText(content)
        msg["Subject"] = subject
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        server.quit()
        print("Email sent.")
    except Exception as e:
        print("Email error:", str(e))

# Combined notification
def notify_all(title, body):
    log_alert(title, body)
    send_pushbullet_notification(title, body)
    send_email_notification(title, body)

# Check values and notify
def check_and_notify(moisture, distance):
    if moisture < MOISTURE_THRESHOLD:
        notify_all("Low Soil Moisture", f"Moisture: {moisture}%. Please water the soil.")
    if distance > DISTANCE_THRESHOLD:
        notify_all("Low Water Level", f"Water level too low: {distance} cm. Refill tank.")

# Debug/test mode
if __name__ == "__main__":
    check_and_notify(moisture=25, distance=15)
