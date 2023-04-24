import pytz
from datetime import datetime,timedelta,timezone

class Person():
    def __init__(self,entity_id,name,state=None,last_changed=None,last_updated=None,last_not_home_change=None):
        self.entity_id = entity_id
        self.name = name
        self.state = state
        if(last_changed): self.last_changed = self.datetime_from_str(last_changed)
        if(last_updated): self.last_updated = self.datetime_from_str(last_updated)
        if(last_not_home_change): self.last_not_home_change = self.datetime_from_str(last_not_home_change)

    def set_state(self,state,last_changed,last_updated,last_not_home_change):
        self.state = state
        self.last_changed = self.datetime_from_str(last_changed)
        self.last_updated = self.datetime_from_str(last_updated)
        self.last_not_home_change = self.datetime_from_str(last_not_home_change)

    def minutes_from_last_update(self):
        last_change_time = self.last_changed

        datetime_now = datetime.now()
        datetime_now = datetime_now.replace(tzinfo=last_change_time.tzinfo)

        diff_minutes = abs((last_change_time - datetime_now).total_seconds() // 60)
        return diff_minutes

    def just_get_home(self,minutes_to_evaluate = 5):
        is_home = self.state.lower()=="home"
        minutes_passed = self.minutes_from_last_update()
        state_change_recently = minutes_passed<minutes_to_evaluate
        return  is_home and state_change_recently
    
    def calculate_total_time_outside(self):
        if self.last_not_home_change is None: return None
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
    
    def get_information(self):
        final_text = f" -Name: {self.name}"
        final_text += f"\n -State: {self.state}"
        final_text += f"\n -Last_changed: {self.last_changed}"
        final_text += f"\n -Last_updated: {self.last_updated}"
        final_text += f"\n -Last time leave home: {self.last_not_home_change}"
        final_text += f"\n -Total Time Outside: {self.calculate_total_time_outside()}"
        return final_text
    
    @classmethod
    def get_people_just_get_home(cls,people_list):
        final_list = []
        for person in people_list:
            if(person.just_get_home()): final_list.append(person)
        return final_list

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
        for sensor in json_data:
            if(sensor['entity_id'].startswith('person.')):
                final_list.append(cls.from_json(sensor))
        return final_list
    
    @classmethod
    def datetime_from_str(cls,date_str):
        datetime_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f%z").replace(tzinfo=pytz.UTC)
        datetime_minus_6 = pytz.timezone('America/Mexico_City')
        datetime_utc_minus_6 = datetime_obj.astimezone(datetime_minus_6)
        return datetime_utc_minus_6
    
class Greeting():
    people_list = []

    def __init__(self,people_list):
        self.people_list = people_list
    
    def get_names(self):
        final_list = []
        for person in self.people_list:
            final_list.append(person.name)
        return final_list

    def to_text(self):
        if(len(self.people_list)==0):return ""
        final_text = "People arriving at the house: ["
        for person in self.people_list:
            final_text += f"\n{person.name}"
        final_text +="]"
        return final_text
