UNAVAILABLE = "unavailable"
UNKNOWN = "unknown"
IDLE = "idle"
NON_OPERATIONAL = "non-operational"

class Device():
    def __init__(self,entity_id,name,state=None,ignoring_states=None):
        self.entity_id = entity_id
        self.name = name
        self.device_type = "General Device"
        self.set_state(state)
        self.set_ignoring_states(ignoring_states)

    def set_state(self,state):
        if (not state): self.state = UNAVAILABLE
        else: self.state = state

    def set_ignoring_states(self,ignoring_states):
        if (not ignoring_states): self.ignoring_states = []
        else: self.ignoring_states = ignoring_states

    def needs_to_be_ignore(self):
        return self.state in self.ignoring_states

    def to_text(self):
        name = self.name
        device_type = self.device_type
        if(self.state): state = self.state
        else: state = UNAVAILABLE
        if(self.state == IDLE): state = NON_OPERATIONAL
        return(f"{device_type} - {name}: {state}")
    
    @classmethod
    def exclude_non_important_from_list(cls,list_general_device):
        result_list = []
        for general_device in list_general_device:
            if(not general_device.needs_to_be_ignore()):
                result_list.append(general_device)
        return result_list