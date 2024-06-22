UNAVAILABLE = "unavailable"
UNKNOWN = "unknown"
IDLE = "idle"
NON_OPERATIONAL = "non-operational"

class Device():
    def __init__(self, entity_id: str, name: str, state = "", ignoring_states: list[str] = []):
        self.entity_id = entity_id
        self.name = name
        self.device_type = "General Device"
        self.set_state(state)
        self.set_ignoring_states(ignoring_states)

    def set_state(self, state: str):
        if (not state): self.state = UNAVAILABLE
        else: self.state = state

    def set_ignoring_states(self, ignoring_states: list[str]):
        if (not ignoring_states): self.ignoring_states = []
        else: self.ignoring_states = ignoring_states

    def needs_to_be_ignore(self) -> bool:
        return self.state in self.ignoring_states

    def to_text(self) -> str:
        name = self.name
        device_type = self.device_type
        if(self.state): state = self.state
        else: state = UNAVAILABLE
        if(self.state == IDLE): state = NON_OPERATIONAL
        return(f"{device_type} - {name}: {state}")
    
    @classmethod
    def exclude_non_important_from_list(cls, list_general_device: list):
        result_list = []
        for general_device in list_general_device:
            if(not general_device.needs_to_be_ignore()):
                result_list.append(general_device)
        return result_list
    
    @classmethod
    def from_dict(cls, data: dict):
        return Device(
            data.get("entity_id",None),
            data.get("name",None),
            data.get("state",None),
            data.get("ignoringStates",None)
        )
    
    @classmethod
    def list_from_dict(cls, data: list[dict]):
        final_list = []
        for device in data:
            final_list.append(cls.from_dict(device))
        return final_list