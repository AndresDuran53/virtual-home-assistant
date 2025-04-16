from dto.homeassistant.sensor import Sensor

class BinarySensor(Sensor):
    entity_class = 'binary_sensor.'
    offValue: str
    onValue: str

    def __init__(self, entity_id: str, name: str, state: str = '', ignoring_states: list[str] = [], visibility: str = 'normal', offValue = 'off', onValue = 'on'):
        super().__init__(entity_id, name, state, ignoring_states, visibility)
        self.offValue = offValue
        self.onValue = onValue

    def get_binary_value(self) -> str:
        if(self.state == "off"): state = self.offValue
        elif(self.state == "on"): state = self.onValue
        else: state = self.state
        return state

    def to_text(self) -> str:
        name = self.name
        state = self.get_binary_value()
        return(f"{name}: {state}")
    
    @classmethod
    def from_dict(cls, data: dict):
        entity_id = data.get("entity_id")
        name = data.get("name",entity_id)
        state = data.get("state","")
        ignoring_states = data.get("ignoringStates", [])
        visibility = data.get("visibility", "normal")
        offValue = data.get("offValue", "off")
        onValue = data.get("onValue", "on")
        if(entity_id and name and offValue and onValue):
            return BinarySensor(
                entity_id,
                name,
                state,
                ignoring_states,
                visibility,
                offValue,
                onValue
            )