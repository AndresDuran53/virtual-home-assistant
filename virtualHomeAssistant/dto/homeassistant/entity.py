
class Entity():
    UNAVAILABLE = "unavailable"
    UNKNOWN = "unknown"
    IDLE = "idle"
    NON_OPERATIONAL = "non-operational"
    entity_class = 'NO_CLASS.'
    entity_id: str
    name: str
    state:str
    unit:str
    ignoring_states: list[str]

    def __init__(self, entity_id: str, name: str, state: str = '', ignoring_states: list[str] = []):
        self.entity_id = entity_id
        self.name = name
        self.set_state(state)
        self.set_ignoring_states(ignoring_states)

    def set_state(self, state: str, unit: str = ''):
        if (not state): self.state = self.UNAVAILABLE
        else: self.state = state
        self.unit = unit

    def set_ignoring_states(self, ignoring_states: list[str]):
        if (not ignoring_states): self.ignoring_states = []
        else: self.ignoring_states = ignoring_states

    def needs_to_be_ignore(self) -> bool:
        return self.state in self.ignoring_states

    def to_text(self) -> str:
        name = self.name
        state = self.state
        if(self.state): state = self.state
        else: state = self.UNAVAILABLE
        unit = self.unit
        if(unit and state.lower() != self.UNAVAILABLE and state.lower() != self.UNKNOWN): state = f"{state}{unit}"
        return(f"{name}: {state}")
    
    @classmethod
    def find_index_by_id(cls, list: list, id: str):
        for entity_index in range(len(list)):
            entity_aux = list[entity_index]
            if(entity_aux.entity_id==id):
                return entity_index
        return -1
    
    @classmethod
    def is_valid(cls, entity_data: dict[str, str]) -> bool:
        is_not_none = entity_data.get('state') is not None
        is_a_valid_entity = entity_data.get('entity_id','').startswith(cls.entity_class)
        return is_not_none and is_a_valid_entity
    
    @classmethod
    def exclude_non_important_from_list(cls, list_entities: list):
        result_list = []
        entity_aux: Entity
        for entity_aux in list_entities:
            if(not entity_aux.needs_to_be_ignore()):
                result_list.append(entity_aux)
        return result_list

    @classmethod
    def from_dict(cls, data: dict):
        entity_id = data.get("entity_id")
        if(entity_id):
            return cls(
                entity_id,
                data.get("name",entity_id),
                data.get("state",""),
                ignoring_states = data.get("ignoringStates", [])
            )

    @classmethod
    def list_from_dict(cls, data: list[dict]):
        final_list = []
        for entity_aux in data:
            entity_id: str = entity_aux.get('entity_id','')
            if(entity_id and entity_id.startswith(cls.entity_class)):
                final_list.append(cls.from_dict(entity_aux))
        return final_list