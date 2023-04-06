[![License](https://img.shields.io/badge/license-CC%20BY--NC--SA%204.0-green)](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.es)

<img  width="480" src="media/vha_banner.png">

# Virtual Home Aassistant
Virtual Home assistant is a home assistant designed to improve the user experience in their home through intelligent management of IoT devices and task automation.

## Manual Installation
- Clone this repository on your computer.
- Install the required packages
    ```
    pip install -r requirements.txt
    ```
- Create a configuration.json file in the data folder of the project and configure the devices and services you want to integrate with Home Assistant. Be sure to follow the configuration_template.json format.
- Run the assistant.py file to start the assistant.

## Docker Usage
- Build Docker image: 
    ```
    docker build --tag gptassistant-image .
    ```
- Run Docker image:
    ```
    docker run -d --restart unless-stopped --name gptassistant gptassistant-image
    ```

## Features

* Control of IoT devices through HomeAssistant and MQTT.
* Generation of natural language responses through a GPT-3-turbo model.
* Generation of audio files through the Google Cloud TTS API.
* Playback of audio files on home speakers using the [SpeakerManager](https://github.com/AndresDuran53/speaker-manager) program.

## License
Zarus IoT Controller is an open source code. All files are licenced under Creative Commons [Reconocimiento-NoComercial-CompartirIgual 4.0 Internacional](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.es)