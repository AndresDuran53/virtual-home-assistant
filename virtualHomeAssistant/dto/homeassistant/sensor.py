UNAVAILABLE = "unavailable"
UNKNOWN = "unknown"

class Sensor():
    entity_id: str
    name:str
    value:str
    unit:str

    def __init__(self, entity_id: str, name: str):
        self.entity_id = entity_id
        self.name = name
        self.value = UNAVAILABLE
        self.unit = ''

    def set_value(self, value: str, unit: str):
        self.value = value
        self.unit = unit

    def to_text(self) -> str:
        name = self.name
        value = self.value
        unit = self.unit
        if(unit and value.lower() != UNAVAILABLE and value.lower() != UNKNOWN): value = f"{value}{unit}"
        return(f"{name}: {value}")
    
    @classmethod
    def is_valid(cls, sensor_data: dict) -> bool:
        is_not_none = sensor_data.get('state') is not None
        is_a_sensor = sensor_data.get('entity_id','').startswith('sensor.')
        return is_not_none and is_a_sensor
    
    @classmethod
    def find_index_by_id(cls, list: list, id: str):
        for sensor_index in range(len(list)):
            sensor_aux = list[sensor_index]
            if(sensor_aux.entity_id==id):
                return sensor_index
        return -1
    
    @classmethod
    def from_dict(cls, data: dict):
        return Sensor(
            data.get("entity_id",None),
            data.get("name",None)
        )

    @classmethod
    def list_from_dict(cls, data: list[dict]):
        final_list = []
        for sensor_aux in data:
            sensor_id: str = sensor_aux.get('entity_id','')
            if(sensor_id.startswith('sensor.')):
                final_list.append(cls.from_dict(sensor_aux))
        return final_list