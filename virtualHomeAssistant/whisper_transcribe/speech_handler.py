#! python3.7

import io
import speech_recognition as sr
import whisper
import torch
import threading

from datetime import datetime, timedelta, timezone
from queue import Queue
from tempfile import NamedTemporaryFile
from time import sleep

from whisper_transcribe.system_configuration import ParserValues, AudioDeviceConfiguration
from whisper_transcribe.audio_util import AudioUtil
from utils.custom_logging import CustomLogging
from assistant.listener import Listener

logger = CustomLogging("logs/assistant.log")

class SpeechHandler(Listener):
    last_mention = []

    def __init__(self):
        self.args = ParserValues.fromSystemArguments()
        self.silence_timeout = self.args.silence_timeout
        self.transcription = ['']
        self.phrase_time = None
        self.last_sample = bytes()
        self.data_queue = Queue()
        self.recorder = sr.Recognizer()
        self.recorder.dynamic_energy_threshold = False
        self.recorder.energy_threshold = self.args.energy_threshold
        self.record_timeout = self.args.record_timeout

        self.device_index = AudioDeviceConfiguration.get_microphone_device_index(self.args.default_microphone)
        self.temp_file = NamedTemporaryFile().name
        self.audio_model = self.load_mode(self.args)
        logger.info("Model loaded.\n")
        self.source = None
        self.execute()

    def load_mode(self,args):
        ONLY_ENGLISH = False
        model = args.model
        if args.model != "large" and not args.non_english and ONLY_ENGLISH:
            model = model + ".en"
        return whisper.load_model(model)

    def generate_audio_source(self):
        """
        Initializes the audio source and adjusts for ambient noise.
        """
        self.source = sr.Microphone(sample_rate=16000,device_index=self.device_index)
        with self.source:
            self.recorder.adjust_for_ambient_noise(self.source)

        def record_callback(_, audio:sr.AudioData) -> None:
            """
            Threaded callback function to recieve audio data when recordings finish.
            audio: An AudioData containing the recorded bytes.
            """
            data = audio.get_raw_data()
            self.data_queue.put(data)

        # Create a background thread that will pass us raw audio bytes.
        # We could do this manually but SpeechRecognizer provides a nice helper.
        self.recorder.listen_in_background(self.source, record_callback, phrase_time_limit=self.record_timeout)

    def read_complete_audio(self):
        # Read the transcription.
        result = self.audio_model.transcribe(self.temp_file, fp16=torch.cuda.is_available())
        self.transcription = self.result_transcription_handler(result,True)
        self.show_transcription()

    def _update_audio_listened(self):
        """
        Continuously listens for audio and processes it.
        """
        if self.source is None:
            self.generate_audio_source()
        is_speaking = False
        while True:
            try:
                # Pull raw recorded audio from the queue.
                if not self.data_queue.empty() and self.source is not None:
                    # If enough time has passed between recordings, consider the phrase complete.
                    # Clear the current working audio buffer to start over with the new data.
                    has_silence_timeout = self.silence_time_is_up()
                    if has_silence_timeout: self.last_sample = bytes()

                    # This is the last time we received new audio data from the queue.
                    is_speaking = True
                    self.phrase_time = datetime.now(timezone.utc)

                    # Concatenate our current audio data with the latest audio data.
                    self.last_sample = AudioUtil.concat_data_to_current_audio(self.last_sample,self.data_queue)

                    # Use AudioData to convert the raw data to wav data.
                    audio_data = sr.AudioData(self.last_sample, self.source.SAMPLE_RATE, self.source.SAMPLE_WIDTH)
                    wav_data = io.BytesIO(audio_data.get_wav_data())

                    # Write wav data to the temporary file as bytes.
                    AudioUtil.write_temp_audio_file(self.temp_file,wav_data)

                else:
                    if is_speaking and self.silence_time_is_up():
                        self.read_complete_audio()
                        is_speaking = False

            except KeyboardInterrupt:
                logger.error("SpeechHandler interrupted by user.")
                break
            except Exception as e:
                logger.error(f"Unexpected error in SpeechHandler: {e}")
            # Infinite loops are bad for processors, must sleep.
            sleep(0.25)
        

    def execute(self):
        speech_thread = threading.Thread(target=self._update_audio_listened)
        speech_thread.start()

    def silence_time_is_up(self) -> bool:
        """
        Checks if the silence timeout has been exceeded.
        """
        silence_timeout = self.silence_timeout
        phrase_time = self.phrase_time
        if phrase_time is None: return False
        now = datetime.utcnow()
        elapsed_time_delta = now - phrase_time
        has_silence_timeout = phrase_time and elapsed_time_delta > timedelta(seconds=silence_timeout)
        return has_silence_timeout

    def result_transcription_handler(self,result,has_silence_timeout):
        text = result['text'].strip()
        if text is None or text == "": return self.transcription
        # If we detected a pause between recordings, add a new item to our transcripion.
        # Otherwise edit the existing one.
        if has_silence_timeout:
            self.transcription.append(text)
        else:
            self.transcription[-1] = text
        return self.transcription

    def show_transcription(self):
        lastRecord = self.transcription[-1]
        assistant_called = self.assistant_was_called(lastRecord)
        if assistant_called:
            self.last_mention.append(lastRecord)
            logger.info(f"[Assistant was Called] {lastRecord}")
    
    def assistant_was_called(self, string):
        assistantName_keywords = ["Minerva", "mi nerva", "mi nerba", "my nerva", "my nerba", "minerba", "manerva", "minvera", "monerva", "minerma", "minrrva", "miverma", "minerrva", "menerva", "Menirva", "Minarva", "Me nerva", "Mi nervo", "Minerba", "Mivera", "Menerba", "Mi verba"]
        normalized_string = string.lower().replace(".", "").replace(",", "").replace("?", "").replace("!", "")        
        for keyword in assistantName_keywords:
            was_called = keyword.lower() in normalized_string
            if was_called: return True
        return False
    
    def get_next_message(self) -> str | None:
        if len(self.last_mention) > 0:
            texto_a_enviar = self.last_mention.pop(-1)
            return texto_a_enviar
        return None


if __name__ == "__main__":
    speechHandler = SpeechHandler()
    speechHandler.execute()