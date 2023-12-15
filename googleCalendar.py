from googleapiclient.discovery import build
from google.oauth2 import service_account
import datetime
from googleapiclient.errors import HttpError


class GoogleCalendar:
	def __init__(self):
		key_file = 'calendarprojectPrivKey.json'
		# this now has to be defined as a single element in an array:
		# scope = ("https://www.googleapis.com/auth/calendar.readonly",)
		scope = ["https://www.googleapis.com/auth/calendar.readonly"]
		self.creds = service_account.Credentials.from_service_account_file('calendarprojectPrivKey.json', scopes=scope)

	def getEvents(self):
		totalEventString = ""
		try:
			service = build('calendar', 'v3', credentials=self.creds)

	        # Call the Calendar API
			now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
			print('Getting the upcoming 10 events')
	        # change from primary using the list method: https://developers.google.com/calendar/api/v3/reference/calendarList/list
			events_result = service.events().list(calendarId='googleServiceAccountNameHere@group.calendar.google.com', timeMin=now,maxResults=10, 
	        	singleEvents=True,orderBy='startTime').execute()
			events = events_result.get('items', [])
			for event in events:
				start = event['start'].get('dateTime', event['start'].get('date'))
				try:
					formattedDate = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S%z')
				except ValueError:
	                # recurring events like birthdays just have:
					formattedDate = datetime.datetime.strptime(start, '%Y-%m-%d')
					formattedDate = formattedDate.replace(hour=12)
				oneEventString = formattedDate.strftime("%a %d/%m/%Y %I:%M%p "+event['summary']+"\n")
				print('boo: ', oneEventString)
				totalEventString = totalEventString + oneEventString
		except HttpError as error:
			totalEventString = "Google Calendar isn't happy"

		return totalEventString
