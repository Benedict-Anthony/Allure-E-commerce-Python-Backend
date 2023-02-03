from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib    

def confirm_account(email, subject, body):
        message = MIMEMultipart()
        message["from"] = "benwebdev29@gmail.com"
        message["to"] = email
        message["subject"] = subject
        message.attach(MIMEText(body, "plain"))
        
        try:
            with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp_server:
                smtp_server.ehlo()
                smtp_server.starttls()
                smtp_server.login("benwebdev29@gmail.com","vemsamzsljfbrzlh")
                smtp_server.send_message(message)
                
        except Exception as exec:
            raise exec
        
    
