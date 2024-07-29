import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import time
from sort import *

from PyQt6.QtCore import QThread, pyqtSignal



class sendEmail(QThread):
    def __init__(self, senderEmail, senderPassword , recipientEmail, subject, message, imagePath):
        super().__init__()
        self.senderEmail = senderEmail
        self.senderPassword = senderPassword
        self.recipientEmail = recipientEmail
        self.subject = subject
        self.message = message
        self.imagePath = imagePath


    def run(self):
        # Create a multipart message object
        msg = MIMEMultipart('alternative')
        msg['From'] = self.senderEmail
        msg['To'] = self.recipientEmail
        msg['Subject'] = self.subject

        # Create both plain text and HTML versions of the email
        text = 'This is a plain text email.'
        html = f'<html><body><>{self.message}</h1></body></html>'

        # Attach the plain text and HTML versions to the email
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        msg.attach(part1)
        msg.attach(part2)

        # Open the image file in binary mode
        with open(self.imagePath, 'rb') as img:
            mime_base = MIMEBase('application', 'octet-stream')
            mime_base.set_payload(img.read())
            encoders.encode_base64(mime_base)
            mime_base.add_header('Content-Disposition', f'attachment; filename={self.imagePath.split("/")[-1]}')
            msg.attach(mime_base)

        # SMTP server settings for Outlook
        smtp_server = 'smtp-mail.outlook.com'
        smtp_port = 587

        try:

            # Create a secure SSL/TLS connection to the SMTP server
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()

            # Login to your Outlook email account
            server.login(self.senderEmail, self.senderPassword)

            # Send the email
            server.sendmail(self.senderEmail, self.recipientEmail, msg.as_string())

            # Record the end time
            # Calculate the time taken to send the email

            print("Email sent successfully!")

        except smtplib.SMTPException as e:
            print("Error sending email:", str(e))

        finally:
            # Close the connection to the SMTP server
            server.quit()





