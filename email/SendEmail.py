# NOTE delete file from here C:\Users\gad-t\.credentials

# % reset
from __future__ import print_function
import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import httplib2
import os
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

def get_credentials(CLIENT_SECRET_FILE):
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def SendMessage(service, user_id, message):

  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print ('Message Id: %s' % message['id'])
    return message
  except errors.HttpError:
    print ('An error occurred: %s' % error)


def CreateMessage(sender, to, subject, message_text):
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}


SCOPES = 'https://mail.google.com/'
CLIENT_SECRET_FILE ='C:\\Users\gad-t\Documents\GitHub\MegaPortal\BackEnd\Google_API\client_secret.json'
APPLICATION_NAME = 'tet'
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
credentials = get_credentials(CLIENT_SECRET_FILE)
http = credentials.authorize(httplib2.Http())
service = discovery.build('gmail', 'v1', http=http)

admin="burkerobotics@gmail.com"
user_id=admin
sender=admin

# XXX: WHAT TO GET FROM FRONT End
########################################################
patient="gtoucha000@citymail.cuny.edu"
message_text="test "
subject=" this message was sent from Python (DCap CCNY team)"
########################################################

to=patient
message= CreateMessage(sender, to, subject, message_text)
SendMessage(service,user_id,message)
