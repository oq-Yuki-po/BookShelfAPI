import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class MailService:
    def __init__(self):
        pass

    def send_email(self, receiver_email: str, subject: str, body: str):
        sender_email = os.getenv("GMAIL_ADDRESS")
        password = os.getenv("GMAIL_PASSWORD")

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        try:
            server.login(sender_email, password)
            server.send_message(msg)
        except smtplib.SMTPAuthenticationError:
            pass
        finally:
            server.quit()
