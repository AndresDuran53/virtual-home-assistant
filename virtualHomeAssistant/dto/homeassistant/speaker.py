UNAVAILABLE = "unavailable"
UNKNOWN = "unknown"
IDLE = "idle"
NON_OPERATIONAL = "non-operational"

from device import Device

class Speaker(Device):
    def __init__(self,entity_id,name,state=None,ignoring_states=None):
        super().__init__(entity_id, name, state, ignoring_states=[])
        self.device_type = "Speaker"

