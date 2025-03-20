[![License](https://img.shields.io/badge/license-CC%20BY--NC--SA%204.0-green)](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.es)

<img width="480" src="media/vha_banner.png" alt="Virtual Home Assistant Banner">

# Virtual Home Assistant
Virtual Home Assistant is a smart home assistant designed to enhance the user experience by intelligently managing IoT devices and automating tasks.

---

## Manual Installation

1. Clone this repository to your computer:
    ```bash
    git clone https://github.com/AndresDuran53/virtual-home-assistant.git
    cd virtual-home-assistant
    ```

2. Install the PortAudio library on your Linux system:
    ```bash
    apt-get install libportaudio2 libportaudiocpp0 portaudio19-dev
    ```

3. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Create a `configuration.json` file in the `data` folder and configure the devices and services you want to integrate with Home Assistant. Use the `configuration_template.json` file as a reference.

5. Run the assistant:
    ```bash
    python3 virtualHomeAssistant/main.py
    ```

---

## Docker Usage

1. Build the Docker image:
    ```bash
    docker build --tag gptassistant-image .
    ```

2. Run the Docker container:
    ```bash
    docker run -d \
    --restart unless-stopped \
    --name gptassistant \
    -e TZ=America/Costa_Rica \
    --network host \
    gptassistant-image
    ```

---

## File Configuration

### MQTT Configuration

The MQTT section contains the configuration for the MQTT broker that the assistant uses to subscribe to and publish messages. The following parameters need to be set:

- `brokerAddress`: The address of the MQTT broker.
- `mqttUser`: The username to authenticate with the MQTT broker.
- `mqttPass`: The password to authenticate with the MQTT broker.
- `subscriptionTopics`: An array of objects representing the topics the assistant should subscribe to. Each object contains:
  - `commandName`: The name of the command associated with the topic.
  - `topic`: The topic to subscribe to.

### OpenAI Configuration

The OpenAI section contains the configuration for the OpenAI API. The following parameters need to be set:

- `apiKey`: The API key for the OpenAI API.
- `model`: The name of the OpenAI model to use.
- `maxTokensPerRequestsSended`: The maximum number of tokens to send per request.
- `maxTokensPerRequestsRecieved`: The maximum number of tokens to receive per request.
- `maxTokensPerDay`: The maximum number of tokens the assistant can use per day.
- `usedCharsFilename`: The file where the assistant will store the number of used tokens.
- `initialConversation`: An array of objects representing the initial conversation between the user and the assistant. Each object contains:
  - `role`: The role of the speaker (`system`, `user`, or `assistant`).
  - `content`: The message spoken by the speaker.

### Home Assistant Configuration

The Home Assistant section contains the configuration for the Home Assistant API. The following parameters need to be set:

- `url`: The URL of the Home Assistant API.
- `haToken`: The long-lived access token to authenticate with the Home Assistant API.
- `people`: An array of objects representing the people who live in the house. Each object contains:
  - `name`: The name of the person.
  - `id`: The ID of the person in Home Assistant.
- `calendars`: An array of objects representing the calendars in Home Assistant. Each object contains:
  - `owner`: The owner of the calendar.
  - `id`: The ID of the calendar in Home Assistant.
- `binarySensors`: An array of objects representing the binary sensors in Home Assistant. Each object contains:
  - `name`: The name of the binary sensor.
  - `id`: The ID of the binary sensor in Home Assistant.
  - `offValue`: The state of the binary sensor when it's off.
  - `onValue`: The state of the binary sensor when it's on.
- `sensors`: An array of objects representing the sensors in Home Assistant. Each object contains:
  - `name`: The name of the sensor.
  - `id`: The ID of the sensor in Home Assistant.
  - `ignoringStates`: An array of states to ignore for the sensor.
- `generalDevices`: An array of objects representing the general devices in Home Assistant. Each object contains:
  - `name`: The name of the device.
  - `id`: The ID of the device in Home Assistant.
  - `ignoringStates`: An array of states to ignore for the device.

---

## Features

- **IoT Device Control**: Manage IoT devices through Home Assistant and MQTT.
- **Natural Language Responses**: Generate responses using the OpenAI GPT model.
- **Audio File Generation**: Create audio files using the Google Cloud TTS API.
- **Speaker Playback**: Play audio files on home speakers using the [SpeakerManager](https://github.com/AndresDuran53/speaker-manager) program.

---

## License

Virtual Home Assistant is open-source software licensed under the Creative Commons [Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.es) license.