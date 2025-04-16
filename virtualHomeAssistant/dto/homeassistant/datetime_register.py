from datetime import datetime
from dto.homeassistant.entity import Entity

class DatetimeRegister(Entity):
    entity_class = 'input_datetime.'
    ignoring_until_minutes_ago: int

    def __init__(self, entity_id: str, name: str, state: str = "", ignoring_until_minutes_ago: str = "0"):
        super().__init__(entity_id, name, state, [], "important")
        self.set_ignoring_times(ignoring_until_minutes_ago)

    def set_ignoring_times(self, ignoring_until_minutes_ago: str):
        if (not ignoring_until_minutes_ago): self.ignoring_until_minutes_ago = 0
        else:
            try:
                self.ignoring_until_minutes_ago = int(ignoring_until_minutes_ago)
            except ValueError:
                raise ValueError(f"Invalid value for ignoring_until_minutes_ago: '{ignoring_until_minutes_ago}' is not a valid number.")

    def needs_to_be_ignore(self) -> bool:
        if(not self.state):
            return True
        
        try:
            last_change_time = datetime.strptime(self.state, '%Y-%m-%d %H:%M:%S')
            if(not last_change_time): 
                return True
        except:
            return True
        
        datetime_now = datetime.now()
        diff_minutes = abs((last_change_time - datetime_now).total_seconds() // 60)
        if(diff_minutes < self.ignoring_until_minutes_ago):
            return True
        return False

    def to_text(self) -> str:
        name = self.name
        if(self.state): state = self.state
        else: state = self.UNAVAILABLE
        return(f"Accion Necesaria - {name}: {state}")
    
    @classmethod
    def from_dict(cls, data: dict):
        return DatetimeRegister(
            data.get("entity_id",""),
            data.get("name",""),
            data.get("state",""),
            data.get("ignoringTime","0")
        )
    
    @classmethod
    def list_from_dict(cls, data: list[dict]):
        final_list = []
        for datetimeRegister in data:
            final_list.append(cls.from_dict(datetimeRegister))
        return final_list