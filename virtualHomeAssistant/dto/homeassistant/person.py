from datetime import datetime
from utils.datetime_utils import datetime_from_str_person

STATE_HOME = "home"

class Person():
    def __init__(self,entity_id,name,state=None,last_changed=None,last_updated=None,last_not_home_change=None):
        self.entity_id = entity_id
        self.name = name
        self.state = state
        self.set_state(state,last_changed,last_updated,last_not_home_change)

    def set_state(self,state,last_changed,last_updated,last_not_home_change):
        self.state = state
        self.last_changed = datetime_from_str_person(last_changed)
        self.last_updated = datetime_from_str_person(last_updated)
        if(isinstance(last_not_home_change,datetime)):
            self.last_not_home_change = last_not_home_change
        else:
            self.last_not_home_change = datetime_from_str_person(last_not_home_change)
    
    def is_home(self) -> bool:
        if not self.state:
            return False
        is_home_value = self.state.lower() == STATE_HOME
        return is_home_value

    def just_get_home(self,minutes_to_evaluate = 10) -> bool:
        is_home = self.is_home()
        if not is_home:
            return False
        minutes_passed = self._minutes_from_last_update()
        state_change_recently = minutes_passed<minutes_to_evaluate
        person_just_get_home = is_home and state_change_recently
        return person_just_get_home
    
    def calculate_total_time_outside(self):
        if self.last_not_home_change is None: 
            return None
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
    
    def _minutes_from_last_update(self):
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
    def from_json(cls,data):
        return Person(
            data["entity_id"],
            data["state"],
            data["last_changed"],
            data["last_updated"]
        )
    
    @classmethod
    def list_from_json(cls,json_data):
        final_list = []
        for person in json_data:
            if(person['entity_id'].startswith('person.')):
                final_list.append(cls.from_json(person))
        return final_list
