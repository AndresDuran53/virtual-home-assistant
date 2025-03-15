import json
from dto.homeassistant.entity import Entity

class InputText(Entity):
    entity_class = 'input_text.'

    def __init__(self, entity_id: str, name: str, state: str = '', ignoring_states: list[str] = []):
        super().__init__(entity_id, name, state, ignoring_states)

    def get_messages(self) -> list[str]:
        # Convertir el string de la clave 'state' en una lista de Python
        messages = json.loads(self.state.replace("\n",""))
        
        # Limpiar los mensajes removiendo espacios y saltos de línea innecesarios
        cleaned_messages = [msg.strip() for msg in messages if msg and isinstance(msg, str)]
        
        return cleaned_messages
    
    def to_text(self) -> str:
        name = self.name
        state = self.state
        if(self.state): state = self.get_messages()
        else: state = self.UNAVAILABLE
        return(f"{name}: {state}")