from dto.homeassistant.sensor import Sensor

UNAVAILABLE = "unavailable"
UNKNOWN = "unknown"

class BinarySensor(Sensor):
    def __init__(self,entity_id,name,offValue = None, onValue = None):
        self.entity_id = entity_id
        self.name = name
        self.offValue = offValue
        self.onValue = onValue
        self.value = UNAVAILABLE
        self.unit = None

    def set_value(self,value,unit):
        self.value = value
        self.unit = unit

    def get_binary_value(self):
        value = None
        if(self.offValue and self.value == "off"): value = self.offValue
        elif(self.onValue and self.value == "on"): value = self.onValue
        else: value = self.value
        return value

    def to_text(self):
        name = self.name
        value = self.get_binary_value()
        unit = self.unit
        if(unit!=None and value.lower() != UNAVAILABLE and value.lower() != UNKNOWN): value = f"{value}{unit}"
        return(f"{name}: {value}")

    @classmethod
    def is_valid(cls,sensor_data):
        is_not_none = sensor_data['state'] is not None
        is_a_sensor = sensor_data['entity_id'].startswith('binary_sensor.')
        return is_not_none and is_a_sensor