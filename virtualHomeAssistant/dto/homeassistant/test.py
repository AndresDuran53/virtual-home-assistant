from sensor import Sensor
from binary_sensor import BinarySensor
from person import Person
from people_manager import PeopleManager
from device import Device
from light import Light
from speaker import Speaker
from event import Event

sensor = Sensor("sensor1","sensor1")
print(sensor.to_text())

binarySensor = BinarySensor("binarySensor1","binarySensor1")
print(binarySensor.to_text())

person1 = Person("person1","person1")
#print(person1.get_information())

person2 = Person("person2","person2")
#print(person2.get_information())

peopleManager = PeopleManager([person1,person2])
print(peopleManager.all_to_text())

device1 = Device("device1","device1")
print(device1.to_text())

light1 = Light("light1","light1")
print(light1.to_text())

speaker1 = Speaker("speaker1","speaker1")
print(speaker1.to_text())