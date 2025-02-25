from datetime import datetime
import os.path
from datetime import timedelta


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pytz

# If modifying these scopes, delete the file token.json.
# SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
SCOPES = ["https://www.googleapis.com/auth/calendar"]

START = datetime.now(pytz.timezone('America/New_York')).strftime('%Y-%m-%dT%H:%M:%S')
END = (datetime.now(pytz.timezone('America/New_York')) + timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%S')

def create_event(title, description="(Omni Generated Empty Description)", start_date=START, end_date=END, guests="", timezone='America/Indianapolis', location=' ', recurrence=[], recurring=' ', amountRecur=' '):
  if not title or len(title) < 1:
    title = 'Omni-Title'

  if not description or len(description) < 1:
    title = "(Omni Generated Empty Description)"

  if not start_date or len(start_date) < 1:
    start_date = "(Omni Generated Empty Date)"

  if not end_date or len(end_date) < 1:
    end_date = "(Omni Generated Empty Date)"

  if len(start_date) != 19:
    start_date = start_date[0:19]
  if len(end_date) != 19:
    end_date = end_date[0:19]
  # creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  # if os.path.exists("token.json"):
  #   creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # # If there are no (valid) credentials available, let the user log in.
  # if not creds or not creds.valid:
  #   if creds and creds.expired and creds.refresh_token:
  #     creds.refresh(Request())
  #   else:
  #     flow = InstalledAppFlow.from_client_secrets_file(
  #         "credentials.json", SCOPES
  #     )
    #   creds = flow.run_local_server(port=0)
    # # Save the credentials for the next run
    # with open("token.json", "w") as token:
    #   token.write(creds.to_json())
    
  if recurring != ' ':
    if amountRecur != ' ':
      recurrence.append(f'RRULE:FREQ={recurring};{amountRecur}')
    else: 
      recurrence = [f'RRULE:FREQ={recurring}',]
    

  try:
    # service = build("calendar", "v3", credentials=creds)

    event = {
      'summary': title,
      'location': location,
      'description': description,
      'start': {
        'dateTime': start_date,
        'timeZone': timezone,
      },
      'end': {
        'dateTime': end_date,
        'timeZone': timezone,
      },
      'recurrence': recurrence,
      'attendees': guests,
      'reminders': {
        'useDefault': False,
        'overrides': [
          {'method': 'email', 'minutes': 24 * 60},
          {'method': 'popup', 'minutes': 10},
        ],
      },
    }
    return event
    # event = service.events().insert(calendarId='primary', body=event).execute()
    # print('Event created: %s' % (event.get('htmlLink')))

  except HttpError as error:
    print(f"An error occurred: {error}")

  # event = service.events().insert(calendarId='primary', body=event).execute()
  # print('Event created: %s' % (event.get('htmlLink')))

# def main():
#   """Shows basic usage of the Google Calendar API.
#   Prints the start and name of the next 10 events on the user's calendar.
#   """

#   create_event(title='Function Test',location='walc',description=' ', start_date='2025-02-20T09:00:00', end_date='2025-02-20T11:00:00',guests=[{'email': 'madhavsv05@gmail.com'},], recurring='WEEKLY', amountRecur='COUNT=3')
#   # creds = None
#   # The file token.json stores the user's access and refresh tokens, and is
#   # created automatically when the authorization flow completes for the first
#   # time.

#   # if os.path.exists("token.json"):
#   #   creds = Credentials.from_authorized_user_file("token.json", SCOPES)
#   # # If there are no (valid) credentials available, let the user log in.
#   # if not creds or not creds.valid:
#   #   if creds and creds.expired and creds.refresh_token:
#   #     creds.refresh(Request())
#   #   else:
#   #     flow = InstalledAppFlow.from_client_secrets_file(
#   #         "credentials.json", SCOPES
#   #     )
#   #     creds = flow.run_local_server(port=0)
#   #   # Save the credentials for the next run
#   #   with open("token.json", "w") as token:
#   #     token.write(creds.to_json())

#   # try:
#   #   service = build("calendar", "v3", credentials=creds)

#   #   event = {
#   #     'summary': 'test2',
#   #     'location': 'corec',
#   #     'description': 'Test',
#   #     'start': {
#   #       'dateTime': '2025-02-20T09:00:00',
#   #       'timeZone': 'America/Indianapolis',
#   #     },
#   #     'end': {
#   #       'dateTime': '2025-02-20T11:00:00',
#   #       'timeZone': 'America/Indianapolis',
#   #     },
#   #     'recurrence': [
#   #     ],
#   #     'attendees': [
#   #       {'email': 'madhavsv05@gmail.com'},
#   #       {'email': 'vpmadhav@gmail.com'},
#   #     ],
#   #     'reminders': {
#   #       'useDefault': False,
#   #       'overrides': [
#   #         {'method': 'popup', 'minutes': 30},
#   #       ],
#   #     },
#   #   }

#   #   event = service.events().insert(calendarId='primary', body=event).execute()
#   #   print('Event created: %s' % (event.get('htmlLink')))

#   # except HttpError as error:
#   #   print(f"An error occurred: {error}")


# if __name__ == "__main__":
#   main()