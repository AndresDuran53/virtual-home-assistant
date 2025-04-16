from dto.homeassistant.event import Event
from utils.datetime_utils import get_happening_text

class Calendar():
    calendar_id: str
    calendar_owner: str

    def __init__(self, calendar_id: str, calendar_owner: str):
        self.calendar_id = calendar_id
        self.calendar_owner = calendar_owner
        self.events = []

    def set_events(self, events: list[Event]):
        self.events = Event.sort_by_start_time(events)

    def add_event(self, event: Event):
        self.events.append(event)
        self.events = Event.sort_by_start_time(self.events)

    def to_text(self) -> str:
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
    
    @classmethod
    def from_dict(cls, data: dict):
        return Calendar(
            data.get("entity_id",""),
            data.get("owner","")
        )
    
    @classmethod
    def list_from_dict(cls, data: list[dict]):
        final_list = []
        for calendar in data:
            if(calendar['entity_id'].startswith('calendar.')):
                final_list.append(cls.from_dict(calendar))
        return final_list