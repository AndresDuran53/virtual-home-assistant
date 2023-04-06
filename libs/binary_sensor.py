class BinarySensor():
    def __init__(self,entity_id,name,offValue = None, onValue = None):
        self.entity_id = entity_id
        self.name = name
        self.offValue = offValue
        self.onValue = onValue

    def set_value(self,value,unit):
        self.value = value
        self.unit = unit

    def to_text(self):
        name = self.name
        if(self.offValue and self.value == "off"): value = self.offValue
        elif(self.onValue and self.value == "on"): value = self.onValue
        else: value = self.value
        unit = self.unit
        if(value != "unavailable" and unit!=None): value = f"{value}{unit}"
        return(f"{name}: {value}")
    
    @classmethod
    def can_ignore_status(self,sensor):
        if(sensor['entity_id']=="sensor.ijai_v10_16b2_status" and sensor['state']=="charging"): return True
        return False

    @classmethod
    def is_valid(cls,sensor_data):
        is_not_none = sensor_data['state'] is not None
        is_a_sensor = sensor_data['entity_id'].startswith('binary_sensor.')
        return is_not_none and is_a_sensor
    
    @classmethod
    def find_index_by_id(cls,list,id):
        for binary_sensor_index in range(len(list)):
            binary_sensor = list[binary_sensor_index]
            if(binary_sensor.entity_id==id):
                return binary_sensor_index
        return -1
    
    @classmethod
    def exclude_non_important_values(cls,list_binary_sensors):
        result_list = []

        porton_sensor_index = cls.find_index_by_id(list_binary_sensors,"binary_sensor.porton_sensor")
        car_sensor_index = cls.find_index_by_id(list_binary_sensors,"binary_sensor.car_sensor")
        if(porton_sensor_index>=0 and car_sensor_index>=0):
            porton_sensor = list_binary_sensors[porton_sensor_index]
            car_sensor = list_binary_sensors[car_sensor_index]
            if not(porton_sensor.value == "off" and car_sensor.value=="on"):
                result_list.append(porton_sensor)
                result_list.append(car_sensor)
        return result_list