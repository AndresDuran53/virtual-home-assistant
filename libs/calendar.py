from datetime import datetime, timezone, timedelta
import pytz

class Calendar():
    def __init__(self,calendar_id,calendar_owner):
        self.calendar_id = calendar_id
        self.calendar_owner = calendar_owner
        self.events = []

    def set_events(self,events):
        self.events = Event.sort_by_start_time(events)

    def add_event(self,event):
        self.events.append(event)
        self.events = Event.sort_by_start_time(self.events)

    def to_text(self):
        if(len(self.events) == 0): return ""
        final_text = f"{self.calendar_owner} events: ["
        for event in self.events:
            happening_text = self.get_happening_text(event)
            final_text += f"\n-({happening_text}) {event.to_text()}"
        final_text += "]"
        return final_text
    
    @classmethod
    def create_event_from_json(cls,calendar_id,event):
        return Event.from_json(calendar_id,event)
    
    @staticmethod
    def get_happening_text(event):
        tz = pytz.timezone('America/Costa_Rica')
        now = datetime.now(tz=tz)
        if (event.end_time < now):
            return "Past event"
        elif (event.start_time <= now and event.end_time >= now):
            return "Event happening"
        else:
            return "Future event"



class Event():
    def __init__(self,calendar_id,name,start_time,end_time):
        self.calendar_id = calendar_id
        self.name = name
        self.start_time = self.datetime_from_str(start_time)
        self.end_time = self.datetime_from_str(end_time)

    def to_text(self):
        datetime_output_format="%A %b %d, %Y at %I:%M%p"
        if(self.start_time != self.end_time):
            start_time = self.start_time.strftime(datetime_output_format)
            end_time = self.end_time.strftime(datetime_output_format)
            time = f"From {start_time} to {end_time}"
        else:
            time = self.start_time.strftime("%A %b %d, %Y")
        return(f"{self.name}: {time}")

    @classmethod
    def get_days_difference(cls,date_str):
        date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        today = datetime.now()
        difference = date_obj - today
        return difference.days
    
    def datetime_from_str(cls,date_str):
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S%z')
        except:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            date_obj = date_obj.replace(tzinfo=timezone(timedelta(hours=-6)))
        return date_obj
    
    @classmethod
    def from_json(cls,calendar_id,event_data):
        return cls(
            calendar_id,
            event_data['summary'],
            event_data['start'].get('dateTime',event_data['start'].get("date")),
            event_data['end'].get('dateTime',event_data['start'].get("date"))
        )
    
    @staticmethod
    def sort_by_start_time(events):
        return sorted(events, key=lambda x: x.start_time)