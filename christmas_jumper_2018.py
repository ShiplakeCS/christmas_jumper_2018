"""
Christmas Jumper 2018

Basic workflow:


Check for internet connection
- If connection, light up star and proceed to following

Check for new email to adimmick@shiplake.org.uk

If email found, trigger lights to flash on jumper

Repeat

Resources:
- https://developers.google.com/resources/api-libraries/documentation/gmail/v1/python/latest/gmail_v1.users.messages.html#list
- https://developers.google.com/gmail/api/quickstart/python
"""

#from __future__ import print_function
from time import sleep
from googleapiclient.discovery import build
import urllib
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
log_line = 0

class LightsController:

    @staticmethod
    def star_on():
        print("Star on")

    @staticmethod
    def star_off():
        print("Star off")

    @staticmethod
    def tree_on():
        print("Tree on")

    @staticmethod
    def tree_off():
        print("Tree off")

    @staticmethod
    def flash_star(count=10):
        for i in range(count):
            LightsController.star_on()
            sleep(0.5)
            LightsController.star_off()
            sleep(0.5)

    @staticmethod
    def flash_tree(count=10):
        for i in range(count):
            LightsController.tree_on()
            sleep(0.5)
            LightsController.tree_off()
            sleep(0.5)


def print_log(msg):
    global log_line
    print("{}: {}".format(log_line, msg))
    log_line += 1


def get_gmail_service():

    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)

    service = build('gmail', 'v1', http=creds.authorize(Http()))

    return service


def connect_and_check_for_email(check_delay=2):

    # Get gmail service

    service = get_gmail_service()
    LightsController.star_off()

    # Initialise list of message_ids to check whether newly collected message has already been seen
    # Clearing this each time the routine starts has a convenient bug in that it will always retrieve at least one
    # message, meaning that the jumper will definitely flash when it establishes a connection.
    message_ids = []

    # Start listening loop
    while True:

        print_log("Checking for messages ({} second delay)...".format(check_delay))

        # Get latest message from Gmail INBOX
        msg_results = service.users().messages().list(userId='me', labelIds="INBOX", maxResults = 1).execute()

        for msg in msg_results['messages']:
            if msg['id'] not in message_ids:
                print_log("New message detected, id: {}".format(msg['id']))
                message_ids.append(msg['id'])
                LightsController.flash_tree()

        # Wait before checking for next message
        sleep(check_delay)



if __name__ == '__main__':

    # Start connect and check loop

    while True:
        try:
            connect_and_check_for_email(5)
        except Exception as e:
            print_log("Exception raised. Likely no Internet connection.")
            print_log("Waiting 10 seconds before trying again...")
            LightsController.star_on()
            sleep(10)
            LightsController.star_off()
