class Sensor():
    def __init__(self,entity_id,name):
        self.entity_id = entity_id
        self.name = name

    def set_value(self,value,unit):
        self.value = value
        self.unit = unit

    def to_text(self):
        name = self.name
        value = self.value
        unit = self.unit
        if(value != "unavailable" and unit!=None): value = f"{value}{unit}"
        return(f"{name}: {value}")
    
    @classmethod
    def is_valid(cls,sensor_data):
        is_not_none = sensor_data['state'] is not None
        is_a_sensor = sensor_data['entity_id'].startswith('sensor.')
        return is_not_none and is_a_sensor
    
    @classmethod
    def find_index_by_id(cls,list,id):
        for sensor_index in range(len(list)):
            sensor_aux = list[sensor_index]
            if(sensor_aux.entity_id==id):
                return sensor_index
        return -1