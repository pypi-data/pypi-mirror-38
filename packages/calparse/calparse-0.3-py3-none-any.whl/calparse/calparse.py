import os
import caldav
from datetime import datetime, timedelta


class CalDavParser(caldav.DAVClient):
    def __init__(
        self, 
        url, 
        username, 
        password, 
        start_date, 
        end_date, 
        parse_list=[
            'SUMMARY', 
            'DESCRIPTION', 
            'LOCATION', 
            'DTSTART', 
            'DTEND'
        ], 
        single_calendar=False, 
        *args, 
        **kwargs
    ):
        super(CalDavParser, self).__init__(url, *args, **kwargs)
        self.calendar_url = url
        self.username = username
        self.password = password
        self.start_date = start_date
        self.end_date = end_date
        self.parse_list = parse_list
        self.is_single_calendar = single_calendar
        self.client = None
        self.principal = None
    
    @classmethod
    def parse_escaped(value):
        return value.replace('\\,', ',').replace('\\;', ';').replace('\\n', '\n')

    def init_client(self):
        if not self.password or not self.username:
            raise ValueError('Cannot create CalDAV Client without explicitly set attributes "username" and "password".')

        self.client = caldav.DAVClient(self.url, username=self.username, password=self.password)
        self.principal = self.client.principal()

    def get_events_by_date(self):
        if not self.start_date or not isinstance(self.start_date, datetime):
            raise ValueError('Cannot parse calendar events by date, missing value for attribute "start_date".')
        
        if not self.end_date or not isinstance(self.end_date, datetime):
            raise ValueError('Cannot parse calendar events by date, mising value for attribute "end_date".')
        
        
        if not self.is_single_calendar:
            calendars = self.principal.calendars()
        else:
            calendars = [caldav.objects.Calendar(client=self.client, url=self.url)]

        for calendar in calendars:
            events = []
            results = calendar.date_search(self.start_date, self.end_date)
            for event in results:
                lines = [line for line in event.data.replace('\r\n ', '').split('\r\n') if line.strip()]
                if sum('END:VEVENT' in line for line in lines) > 1:
                    parsed = []
                    sub_events = [list(filter(None, l.split('|'))) for l in '|'.join(lines).split('END:VEVENT')]
                    for sub_event in sub_events:
                        parsed_sub = {}
                        for line in sub_event:
                            key, value = line.split(':', 1)
                            if key in self.parse_list:
                                parsed_sub[key] = self.parse_escaped(value)
                        parsed.append(parsed_sub)
                    events.extend(parsed)
                else:
                    parsed = {}
                    for line in lines:
                        key, value = line.split(':', 1)
                        if key in self.parse_list:
                            parsed[key] = self.parse_escaped(value)
                    events.append(parsed)
        
        return list(filter(None, events))

