from __future__ import print_function
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from uuid import uuid4

SCOPES = ['https://www.googleapis.com/auth/calendar']

class Event:
    """
        Class with the logic for create a new meet in the calendar
        Author José Cruz
        Version 1.0.0
    """

    def __init__(self):
        self.summary = "New Meet"
        self.guests = []
        self.date = None
        self.times = None
        self.schedule = {
            "start": None,
            "end": None
        }
        self.service = self.getService()
        # self.meetEvent = self.createEvent(guests, schedule, service, summary)

    def getService(self):
        """
            Function that create and get the authorization for use the google calendar

            Returns
            --------
            service : build
                The authorized service for the google calendar
        """

        creds = None

        if os.path.exists('assets/token.json'):
            creds = Credentials.from_authorized_user_file('assets/token.json', SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'assets/credentials.json', SCOPES
                )
                creds = flow.run_local_server(port=0)

            with open('assets/token.json', 'w') as token:
                token.write(creds.to_json())

        service = build('calendar', 'v3', credentials=creds)

        return service

        """now = datetime.datetime.utcnow().isoformat() + 'Z'
        print('Getting upcoming 10 events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True).execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(event)"""
    
    def createEvent(self):
        """
            Function that create a new meet in the calendar

            Parameters
            -----------
            guests : List[Dict[str, str]]
                All the emails for the people invited to the meet
            schedule : Dict[str, str]
                Start and end time for the meet
            service : build
                the authorized service for access to google calendar
            summary : str
                The name of the meet

            Returns
            --------
            event : Obj
                The info of the created event in the google calendar
        """
        
        event = {
            "summary": self.summary,
            "start": {
                "dateTime": self.schedule["start"],
                "timeZone": "America/Bogota"
            },
            "end": {
                "dateTime": self.schedule["end"],
                "timeZone": "America/Bogota"
            },
            "attendees": self.guests,
            "conferenceData": {
                "createRequest": {
                    "requestId": f"{uuid4().hex}",
                    "conferenceSolutionKey": {
                        "type": "hangoutsMeet"
                    }
                }
            },
            "reminders": {"useDefault": True}
        }

        event = self.service.events().insert(calendarId="primary", sendNotifications=True, body=event, conferenceDataVersion=1).execute()

        return event
