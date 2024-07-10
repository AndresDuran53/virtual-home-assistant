from dto.homeassistant.entity import Entity

class Device(Entity):
    entity_class = ''

    def __init__(self, entity_id: str, name: str, state: str = "", ignoring_states: list[str] = []):
        super().__init__(entity_id, name, state, ignoring_states)
    
    @classmethod
    def from_dict(cls, data: dict):
        return Device(
            data.get("entity_id",None),
            data.get("name",None),
            data.get("state",None),
            data.get("ignoringStates",None)
        )