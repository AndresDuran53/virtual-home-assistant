from datetime import datetime
from utils.datetime_utils import datetime_from_str_person

STATE_HOME = "home"

class Person():
    def __init__(self, 
                 entity_id: str, 
                 name: str, 
                 state: str = '', 
                 last_changed: str = '', 
                 last_updated: str = '', 
                 last_not_home_change: datetime | str = ''):
        self.entity_id = entity_id
        self.name = name
        self.set_state(state, last_changed, last_updated, last_not_home_change)

    def set_state(self, state: str, last_changed: str, last_updated: str, last_not_home_change: datetime | str):
        self.state = state
        self.last_changed = datetime_from_str_person(last_changed)
        self.last_updated = datetime_from_str_person(last_updated)
        if(isinstance(last_not_home_change,datetime)):
            self.last_not_home_change = last_not_home_change
        else:
            self.last_not_home_change = datetime_from_str_person(last_not_home_change)
    
    def is_home(self) -> bool:
        if(self.state):
            return self.state.lower() == STATE_HOME
        else:
            return False

    def just_get_home(self, minutes_to_evaluate = 10) -> bool:
        is_home = self.is_home()
        if not is_home: 
            return False
        minutes_passed = self._minutes_from_last_update()
        if(not minutes_passed): 
            return False
        state_change_recently = minutes_passed<minutes_to_evaluate
        person_just_get_home = is_home and state_change_recently
        return person_just_get_home
    
    def calculate_total_time_outside(self) -> str:
        if (not self.last_not_home_change or not self.last_changed): 
            return "No Information"
        time_outside = self.last_changed - self.last_not_home_change
        total_seconds = time_outside.total_seconds()
        if total_seconds < 3600:
            total_minutes = int(total_seconds / 60)
            text_time_outside = f"{total_minutes} minutes"
        else:
            total_hours = int(total_seconds / 3600)
            total_minutes = int(total_seconds/60 - (total_hours*60))
            text_time_outside = f"{total_hours} hours and {total_minutes} minutes"
        return text_time_outside
    
    def _minutes_from_last_update(self) -> float | None:
        if not self.last_changed:
            return None
        last_change_time = self.last_changed
        datetime_now = datetime.now()
        datetime_now = datetime_now.replace(tzinfo=last_change_time.tzinfo)
        diff_minutes = abs((last_change_time - datetime_now).total_seconds() // 60)
        return diff_minutes
    
    def get_information(self):
        final_text = f" -Name: {self.name}"
        final_text += f"\n -State: {self.state}"
        final_text += f"\n -Last_changed: {self.last_changed}"
        final_text += f"\n -Last_updated: {self.last_updated}"
        final_text += f"\n -Last time leave home: {self.last_not_home_change}"
        final_text += f"\n -Total Time Outside: {self.calculate_total_time_outside()}"
        return final_text

    @classmethod
    def from_dict(cls, data: dict):
        return Person(
            data.get("entity_id",None),
            data.get("name",None),
            data.get("state",None),
            data.get("last_changed",None),
            data.get("last_updated",None)
        )
    
    @classmethod
    def list_from_dict(cls, data: list[dict]):
        final_list = []
        for person in data:
            if(person['entity_id'].startswith('person.')):
                final_list.append(cls.from_dict(person))
        return final_list
