from email.mine.Multipart import MIMEMultipart
from email.mine.MIMIEText import MIMEText

def confirm_account(email, subject, message):
    message = MimeMultipart()
    message["from"] = ""
    message["to"] = email
    message["subject"] = subject
    message.attacth(MIIMEText(mesaage, "plain"))
