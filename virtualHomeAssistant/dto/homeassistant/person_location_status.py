from utils.datetime_utils import datetime_from_str_person
from datetime import datetime

class PersonLocationStatus:
    entity_id: str
    state: str
    last_changed: datetime
    last_updated: datetime

    def __init__(self, entity_id: str, state: str, last_changed: str, last_updated: str):
        self.entity_id = entity_id
        self.state = state
        self.last_changed = datetime_from_str_person(last_changed) # type: ignore
        self.last_updated = datetime_from_str_person(last_updated) # type: ignore
        

    @classmethod
    def from_json(cls, json_data: dict):
        return PersonLocationStatus(
            entity_id=json_data.get('entity_id', None),
            state=json_data.get('state', None),
            last_changed=json_data.get('last_changed', None),
            last_updated=json_data.get('last_updated', None)
        )
    
    @classmethod
    def create_person_statuses(cls, json_list: list):
        person_statuses: list[PersonLocationStatus] = []
        for json_data in json_list:
            for data in json_data:
                person_status = PersonLocationStatus.from_json(data)
                person_statuses.append(person_status)
        person_statuses.sort(key=lambda x: x.last_changed)
        return person_statuses
    
    @classmethod
    def find_statuses(cls, person_statuses_aux: list):
        person_statuses: list[PersonLocationStatus] = person_statuses_aux
        if(not person_statuses):
            return None
        latest_home_status = next((status for status in person_statuses if status.state == "home"), None)
        if latest_home_status:
            home_statuses = sorted((status for status in person_statuses if status.state == "home"),
                                key=lambda x: x.last_changed, reverse=True)
            if len(home_statuses) > 1:
                latest_home_status_aux = home_statuses[1]
            else:
                latest_home_status_aux = home_statuses[0]

            not_home_status = next((status for status in person_statuses if status.state != "home" and status.last_changed > latest_home_status_aux.last_changed), None)
            if not_home_status:
                return not_home_status     
        return person_statuses[0]