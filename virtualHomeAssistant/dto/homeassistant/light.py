UNAVAILABLE = "unavailable"
UNKNOWN = "unknown"
IDLE = "idle"
NON_OPERATIONAL = "non-operational"

from device import Device

class Light(Device):
    def __init__(self,entity_id,name,state=None,ignoring_states=None):
        self.entity_id = entity_id
        self.name = name
        self.device_type = "Light"
        self.set_state(state)
        self.set_ignoring_states(ignoring_states)

    def set_state(self,state):
        if (not state): self.state = UNAVAILABLE
        else: self.state = state

    def set_ignoring_states(self,ignoring_states):
        if (not ignoring_states): self.ignoring_states = []
        else: self.ignoring_states = ignoring_states

