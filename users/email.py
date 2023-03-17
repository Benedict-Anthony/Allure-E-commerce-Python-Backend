from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from pathlib import Path
import smtplib    
from decouple import config


def send_mail(email, subject, body):
    sender = config("SENDER_EMAIL")
    password = config("SENDER_PASSWORD")
    message = MIMEMultipart()
    message["from"] = "Allure"
    message["to"] = email
    message["subject"] = subject
    message.attach(MIMEText(body, "plain"))
    message.attach(MIMEImage(Path("publik/assets/allure.png").read_bytes()))
        
    try:
        with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp_server:
            smtp_server.ehlo()
            smtp_server.starttls()
            smtp_server.login(sender,password)
            smtp_server.send_message(message)
            
    except Exception as exec:
        raise exec
    
    
