import os
import time
import threading
import psutil
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Gmail API imports
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from tensorflow.keras.callbacks import Callback
import base64
# =====================
# Gmail API Setup
# =====================
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

def gmail_service():
    """Authenticate with Gmail API using credentials.json"""
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    creds = flow.run_local_server(port=0)
    return build("gmail", "v1", credentials=creds)

def send_gmail_alert(service, sender, receiver, subject, body):
    """Send email via Gmail API"""
    message = MIMEText(body)
    message["to"] = receiver
    message["from"] = sender
    message["subject"] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    msg = {"raw": raw}
    service.users().messages().send(userId="me", body=msg).execute()
    print("📧 Gmail API alert sent.")

class CPUUsageMonitor:
    def __init__(self, gmail_service, sender, receiver, threshold=85, check_interval=5):
        self.threshold = threshold
        self.check_interval = check_interval
        self.paused = False
        self._stop_flag = False
        self.gmail_service = gmail_service
        self.sender = sender
        self.receiver = receiver

    def get_cpu_usage(self):
        return psutil.cpu_percent(interval=1)

    def send_email_alert(self, usage):
        subject = "🚨 CPU Usage Alert"
        body = f"CPU usage reached {usage:.2f}%. Monitoring paused until it cools down."
        try:
            send_gmail_alert(self.gmail_service, self.sender, self.receiver, subject, body)
        except Exception as e:
            print(f"❌ Gmail API failed: {e}")

    def monitor(self):
        while not self._stop_flag:
            usage = self.get_cpu_usage()
            print(f"💻 CPU Usage: {usage:.2f}%")

            if usage > self.threshold and not self.paused:
                print("🔥 High CPU usage detected! Pausing training...")
                self.send_email_alert(usage)
                self.paused = True
            elif usage <= self.threshold and self.paused:
                print("✅ CPU usage normalized. Resuming training...")
                self.paused = False

            time.sleep(self.check_interval)

    def start(self):
        self.thread = threading.Thread(target=self.monitor, daemon=True)
        self.thread.start()

    def stop(self):
        self._stop_flag = True
        self.thread.join()

class CPUMonitorCallback(Callback):
    def __init__(self, monitor):
        super().__init__()
        self.monitor = monitor

    def on_batch_begin(self, batch, logs=None):
        if self.monitor.paused:
            print("⏸ Training paused due to CPU load...")
            while self.monitor.paused:  # wait until safe
                time.sleep(5)

"""

  $$$$$ ADD THIS FOLLOWINF LINES TO TRAINING[MAY BE COMPONENTS] FOR API BASED EMAIL NOTIFICATION WHILE TRAINING
  ##### Generate credentials.json And save it (same place as your cpu_monitor.py or stage_03_training_pipeline.py).
  Never commit credentials.json to GitHub (add it to .gitignore). It contains your client secret.


service = gmail_service()

# 2. Start CPU Monitor in background
monitor = CPUUsageMonitor(
    gmail_service=service,
    sender=os.getenv("sender"),     # replace with your Gmail
    receiver=os.getenv("receiver"),     # replace with recipient
    threshold=85,
    check_interval=5
)
monitor.start()
# Now start training
try:
    

    load_model.fit(train_generator,
                epochs=m.params_epochs,
                steps_per_epoch=steps_per_epoch,
                validation_steps=validation_steps,
                validation_data=valid_generator,
                callbacks=[
            CPUMonitorCallback(monitor),
            EarlyStopping(
                monitor="val_loss",       # metric to watch
                patience=3,               # stop after 3 bad epochs
                restore_best_weights=True # rollback to best weights
            )
        ]
    )
except KeyboardInterrupt:
    print("🛑 Training interrupted manually.")  
                            """




class CPUUsageMonitor_smtp:
    def __init__(self, threshold=85, check_interval=5):
        self.threshold = threshold
        self.check_interval = check_interval
        self.paused = False
        self._stop_flag = False

        # Load credentials from environment
        self.email_sender = os.getenv("EMAIL_SENDER")
        self.email_password = os.getenv("EMAIL_PASSWORD")
        self.email_receiver = os.getenv("EMAIL_RECEIVER")
    def get_cpu_usage(self):
        return psutil.cpu_percent(interval=1)

    def send_email_alert(self, usage):
        subject = "🚨 CPU Usage Alert"
        body = f"CPU usage reached {usage:.2f}%. Monitoring paused until it cools down."

        msg = MIMEMultipart()
        msg['From'] = self.email_sender
        msg['To'] = self.email_receiver
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.sendmail(self.email_sender, self.email_receiver, msg.as_string())
            print("📧 Email alert sent.")
        except Exception as e:
            print(f"❌ Failed to send email: {e}")

    def monitor(self):
        while not self._stop_flag:
            usage = self.get_cpu_usage()
            import logging
            logging.basicConfig(filename="cpu_monitor.log", level=logging.INFO)

            logging.info(f"CPU Usage: {usage:.2f}%")


            if usage > self.threshold and not self.paused:
                print("High CPU usage detected! Pausing monitoring...")
                self.send_email_alert(usage)
                self.paused = True
            elif usage <= self.threshold and self.paused:
                print("CPU usage normalized. Resuming monitoring...")
                self.paused = False

            time.sleep(self.check_interval)

    def start(self):
        self.thread = threading.Thread(target=self.monitor, daemon=True)
        self.thread.start()

    def stop(self):
        self._stop_flag = True
        self.thread.join()

# Example usage
if __name__ == "__main__":
    monitor = CPUUsageMonitor(threshold=85, check_interval=5)
    monitor.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        monitor.stop()
        print("🛑 Monitoring stopped.")



class CPUMonitor_temperature:
    def __init__(self, threshold=85, check_interval=5):
        self.threshold = threshold
        self.check_interval = check_interval
        self.paused = False
        self._stop_flag = False
        self.w = wmi.WMI(namespace="root\\wmi")

        # Load credentials from environment
        self.email_sender = os.getenv("EMAIL_SENDER")
        self.email_password = os.getenv("EMAIL_PASSWORD")
        self.email_receiver = os.getenv("EMAIL_RECEIVER")

    def get_cpu_temp(self):
        temps = self.w.MSAcpi_ThermalZoneTemperature()
        if temps:
            return (temps[0].CurrentTemperature / 10.0) - 273.15
        return None

    def send_email_alert(self, temp):
        subject = "🔥 CPU Temperature Alert"
        body = f"CPU temperature reached {temp:.2f}°C. Training paused until it cools down."

        msg = MIMEMultipart()
        msg['From'] = self.email_sender
        msg['To'] = self.email_receiver
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(self.email_sender, self.email_password)
                server.sendmail(self.email_sender, self.email_receiver, msg.as_string())
            print("📧 Email alert sent.")
        except Exception as e:
            print(f"❌ Failed to send email: {e}")

    def monitor(self):
        while not self._stop_flag:
            temp = self.get_cpu_temp()
            if temp:
                print(f"🌡️ CPU Temp: {temp:.2f}°C")
                if temp > self.threshold and not self.paused:
                    print("🔥 Overheating! Pausing training...")
                    self.send_email_alert(temp)
                    self.paused = True
                elif temp <= self.threshold and self.paused:
                    print("✅ Temperature normalized. Resuming training...")
                    self.paused = False
            time.sleep(self.check_interval)

    def start(self):
        self.thread = threading.Thread(target=self.monitor, daemon=True)
        self.thread.start()

    def stop(self):
        self._stop_flag = True
        self.thread.join()
