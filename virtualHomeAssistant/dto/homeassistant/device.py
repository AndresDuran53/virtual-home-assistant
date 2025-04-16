from dto.homeassistant.entity import Entity

class Device(Entity):
    entity_class = ''

    def __init__(self, entity_id: str, name: str, state: str = "", ignoring_states: list[str] = [], visibility: str = 'normal'):
        super().__init__(entity_id, name, state, ignoring_states, visibility)
    
    @classmethod
    def from_dict(cls, data: dict):
        return Device(
            data.get("entity_id",""),
            data.get("name",""),
            data.get("state",""),
            data.get("ignoringStates",[]),
            data.get("visibility", "normal")
        )