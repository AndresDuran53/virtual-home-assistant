from dto.homeassistant.entity import Entity

class Sensor(Entity):
    entity_class = 'sensor.'

    def __init__(self, entity_id: str, name: str, state: str = '', ignoring_states: list[str] = [], visibility: str = 'normal'):
        super().__init__(entity_id, name, state, ignoring_states, visibility)