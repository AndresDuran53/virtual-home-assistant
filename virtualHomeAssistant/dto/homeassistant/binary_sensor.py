from dto.homeassistant.sensor import Sensor

UNAVAILABLE = "unavailable"
UNKNOWN = "unknown"

class BinarySensor(Sensor):
    entity_id: str
    name: str
    offValue: str
    onValue: str
    value: str

    def __init__(self, entity_id: str, name: str, offValue = 'off', onValue = 'on'):
        self.entity_id = entity_id
        self.name = name
        self.offValue = offValue
        self.onValue = onValue
        self.value = UNAVAILABLE

    def set_value(self, value: str, unit: str):
        self.value = value

    def get_binary_value(self) -> str:
        if(self.value == "off"): value = self.offValue
        elif(self.value == "on"): value = self.onValue
        else: value = self.value
        return value

    def to_text(self) -> str:
        name = self.name
        value = self.get_binary_value()
        return(f"{name}: {value}")

    @classmethod
    def is_valid(cls, sensor_data: dict) -> bool:
        is_not_none = sensor_data.get('state') is not None
        is_a_sensor = sensor_data.get('entity_id','').startswith('binary_sensor.')
        return is_not_none and is_a_sensor
    
    @classmethod
    def from_dict(cls, data: dict):
        return BinarySensor(
            data.get("entity_id",None),
            data.get("name",None),
            data.get("offValue",None),
            data.get("onValue",None)
        )

    @classmethod
    def list_from_dict(cls, data: list[dict]):
        final_list = []
        for binary_sensor_aux in data:
            binary_sensor_id: str = binary_sensor_aux.get('entity_id','')
            if(binary_sensor_id.startswith('binary_sensor.')):
                final_list.append(cls.from_dict(binary_sensor_aux))
        return final_list