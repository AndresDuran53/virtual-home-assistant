from datetime import datetime
from utils.datetime_utils import datetime_from_str_event

class Event():
    def __init__(self,calendar_id,name,start_time,end_time):
        self.calendar_id = calendar_id
        self.name = name
        self.start_time = datetime_from_str_event(start_time)
        self.end_time = datetime_from_str_event(end_time)

    def to_text(self) -> str:
        datetime_output_format="%A %b %d, %Y at %I:%M%p"
        if(not self.start_time or not self.end_time): 
            return ""
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
    
    @classmethod
    def from_json(cls,calendar_id,event_data):
        return cls(
            calendar_id,
            event_data['summary'],
            event_data['start'].get('dateTime',event_data['start'].get("date")),
            event_data['end'].get('dateTime',event_data['start'].get("date"))
        )
    
    @staticmethod
    def sort_by_start_time(events: list):
        return sorted(events, key=lambda x: x.start_time)