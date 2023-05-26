from dto.homeassistant.event import Event
from utils.datetime_utils import get_happening_text

class Calendar():
    calendar_id: str
    calendar_owner: str

    def __init__(self,calendar_id,calendar_owner):
        self.calendar_id = calendar_id
        self.calendar_owner = calendar_owner
        self.events = []

    def set_events(self,events):
        self.events = Event.sort_by_start_time(events)

    def add_event(self,event: Event):
        self.events.append(event)
        self.events = Event.sort_by_start_time(self.events)

    def to_text(self):
        if(len(self.events) == 0): return ""
        final_text = f"{self.calendar_owner} events: ["
        for event in self.events:
            happening_text = get_happening_text(event)
            final_text += f"\n-({happening_text}) {event.to_text()}"
        final_text += "]"
        return final_text
    
    @classmethod
    def create_event_from_json(cls,calendar_id,event):
        return Event.from_json(calendar_id,event)