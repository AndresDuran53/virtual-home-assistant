from utils.datetime_utils import datetime_from_str_person

class PersonLocationStatus:
    def __init__(self, entity_id, state, last_changed, last_updated):
        self.entity_id = entity_id
        self.state = state
        self.last_changed = datetime_from_str_person(last_changed)
        self.last_updated = datetime_from_str_person(last_updated)
        

    @classmethod
    def from_json(cls, json_data):
        return cls(
            entity_id=json_data['entity_id'],
            state=json_data['state'],
            last_changed=json_data['last_changed'],
            last_updated=json_data['last_updated']
        )
    
    @classmethod
    def create_person_statuses(cls,json_list):
        person_statuses = []
        for json_data in json_list:
            for data in json_data:
                person_status = PersonLocationStatus.from_json(data)
                person_statuses.append(person_status)
        person_statuses.sort(key=lambda x: x.last_changed)
        return person_statuses
    
    @classmethod
    def find_statuses(cls,person_statuses):
        if(len(person_statuses)==0):
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