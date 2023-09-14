import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64
from email.mime.text import MIMEText

class GmailSender:
    def __init__(self, configs) -> None:
        self.SCOPES = ['https://www.googleapis.com/auth/gmail.send']
        self.mail_from = configs["mail_from"]
        self.mail_to = configs["mail_to"]

    # Authorizing
    def auth(self):
        if os.path.exists('gmail_sender/token.json'):
            creds = Credentials.from_authorized_user_file('gmail_sender/token.json', self.SCOPES)
            return creds
        
    # Creating mail content
    def create_message(self, sender, to, subject, message_text):
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}


    # Sending the mail
    def send_message(self, message_subject, message):
        creds = self.auth()    
        service = build('gmail', 'v1', credentials=creds)
        message = self.create_message(self.mail_from, self.mail_to, message_subject, message)
        
        try:
            message = (service.users().messages().send(userId='me', body=message)
                    .execute())
            print(f"-----Mail sent to {self.mail_to}-----")
            return message
        except Exception as error:
            print(error)