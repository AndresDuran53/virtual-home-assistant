from utils.custom_logging import CustomLogging
import paho.mqtt.client as mqtt

class MqttConfig:
    broker_address = None
    mqtt_user = None
    mqtt_pass = None
    subscription_topics = []

    def __init__(self, broker_address=None, mqtt_user=None, mqtt_pass=None, subscription_topics=None):
        self.broker_address = broker_address
        self.mqtt_user = mqtt_user
        self.mqtt_pass = mqtt_pass
        self.subscription_topics = subscription_topics

    @classmethod
    def from_json(cls, config_data):
        mqtt_config = MqttConfig(
            broker_address=config_data['mqtt']['brokerAddress'],
            mqtt_user=config_data['mqtt']['mqttUser'],
            mqtt_pass=config_data['mqtt']['mqttPass'],
            subscription_topics=config_data['mqtt']['subscriptionTopics']
        )
        return mqtt_config

class MqttService:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    
    def __init__(self, mqtt_config:MqttConfig = None, on_message = None, client_id="AssistantService"):
        if not hasattr(self, 'client'):
            if mqtt_config is None or on_message is None or client_id is None:
                raise ValueError('MQTT configuration not found at object creation')
            self._configuration(mqtt_config, on_message, client_id)

    def _configuration(self,mqtt_config,on_message,client_id):
        self.logger = CustomLogging("logs/assistant.log")
        self.client = mqtt.Client(client_id=client_id, clean_session=False, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")
        self.client.on_message=on_message
        self.client.username_pw_set(username=mqtt_config.mqtt_user, password=mqtt_config.mqtt_pass)
        self.client.connect(mqtt_config.broker_address) #connect to broker
        self.know_commands = mqtt_config.subscription_topics
        self.subscribe_know_topics()
        self.client.loop_start()

    def subscribe_know_topics(self):
        for know_command in self.know_commands:
            topic = know_command["topic"]
            self.client.subscribe(topic)
    
    def send_message(self,topic,message):
        self.logger.info(f"[Sending] | [Topic]:{topic} | [Message]:{message}")
        self.client.publish(topic,message,qos=1,retain=False)

    def get_command_from_topic(self, topic) -> str:
        for know_command in self.know_commands:
            if know_command["topic"] == topic:
                return know_command["commandName"]
        return None