# imports
import io
import os
from extra import *
import dialogflow_v2 as dialogflow
from rec import Recorder
import simpleaudio as sa

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from google.cloud import texttospeech
from google.api_core.exceptions import InvalidArgument

credential_path = "gamesvoiceassistant-63718bb5249e.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path


class VoiceAssistant:
    _name = 'Daisy'
    _key_word = 'hi ' + _name
    _shutdown_key_word = 'bye ' + _name
    _kw_heard = False
    _chat_commands = ['creators', 'favorite food', 'Default Welcome Intent', 'advice', 'welcome back']
    _game_commands = None
    _status_dict = {'off': 'red', 'on': 'green', 'listen': 'yellow', 'record': 'orange', 'speak': 'blue'}
    _my_status = 'red'
    _advice_counter = 0
    _recorder = Recorder()

    _DIALOGFLOW_PROJECT_ID = 'gamesvoiceassistant'
    _DIALOGFLOW_LANGUAGE_CODE = 'en'
    _SESSION_ID = 'me'

    _language_code ='en-US'
    _voice_gender = texttospeech.enums.SsmlVoiceGender.FEMALE

    def __init__(self, game, my_type=None, name=None):
        self._game_commands = game.get_info('web_elem').keys()
        self.gender(my_type)
        if name is not None:
            self._name = name
        change_status(self._status_dict['off'])

    def gender(self,gender):
        if gender is not None:
            # voice gender ("neutral", "FEMALE", "MALE")
            if gender == 'va':
                self._voice_gender = texttospeech.enums.SsmlVoiceGender.FEMALE
            elif gender == 'opponent':
                self._voice_gender = texttospeech.enums.SsmlVoiceGender.NEUTRAL
            else:
                self._voice_gender = texttospeech.enums.SsmlVoiceGender.MALE

    def open(self):
        self._kw_heard = True
        change_status(self._status_dict['on'])
        hello_text = 'Hello everybody, My name is ' + self._name
        self.ack(hello_text)
        return True

    def close(self):
        self._kw_heard = False
        change_status(self._status_dict['off'])
        massage = 'Goodbye'
        self.ack(massage)
        return True

    def ack(self, text):
        if len(text) < 150:
            print('Voice Assistance said: ' + text)
            self.tts(text)
        else:
            text = text.splitlines()
            for line in text:
                print('Voice Assistance said: ' + line)
                self.tts(line)

    def update_advice_counter(self):
        self._advice_counter += 1
        if self._advice_counter % 10 == 0:
            self.give_advice()

    def give_advice(self):
        self.ack('Running auto advice')
        self.dialog_flow_function('advice')

    def read_log(self, text):
        if text is not None:
            for line in text:
                self.ack(line)

    def listen(self):
        text = None
        while text is None:
            self._recorder.listen()
            text = self.stt()
            if text is not None:
                if self._shutdown_key_word in text:
                    self.close()
                else:
                    if self._kw_heard:
                        return self.dialog_flow_function(text)
                    elif self._key_word in text:
                        self.open()
                text = None

    @staticmethod
    def stt():
        client = speech.SpeechClient()
        string = []
        # The name of the audio file to transcribe
        file_name = os.path.join(os.path.dirname(__file__), 'RECORDING.wav')

        # Loads the audio into memory
        with io.open(file_name, 'rb') as audio_file:
            content = audio_file.read()
            audio = types.RecognitionAudio(content=content)

        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code='en-US')

        # Detects speech in the audio file
        response = client.recognize(config, audio)

        for result in response.results:
            string = result.alternatives[0].transcript

        if len(string) > 0:
            print('User said: ' + string)
            return string
        print('Nothing on the recording')
        return None

    def tts(self, massage):
        client = texttospeech.TextToSpeechClient()
        # Set the text input to be synthesized
        synthesis_input = texttospeech.types.SynthesisInput(text=massage)

        # Build the voice request, select the language code ("en-US") and the ssml
        voice = texttospeech.types.VoiceSelectionParams(
            language_code=self._language_code,
            ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)

        # Select the type of audio file you want returned
        audio_config = texttospeech.types.AudioConfig(
            audio_encoding=texttospeech.enums.AudioEncoding.LINEAR16)

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = client.synthesize_speech(synthesis_input, voice, audio_config)
        change_status(self._status_dict['speak'])
        self.play(response.audio_content)

    def result_of_command(self, result, msg):
        bad_massage = 'Sorry, could not run that command'
        if result:
            self.ack(msg)
        else:
            self.tts(bad_massage)
        return True

    def dialog_flow_function(self, text):
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(self._DIALOGFLOW_PROJECT_ID, self._SESSION_ID)
        text_input = dialogflow.types.TextInput(text=text, language_code=self._DIALOGFLOW_LANGUAGE_CODE)
        query_input = dialogflow.types.QueryInput(text=text_input)

        try:
            response = session_client.detect_intent(session=session, query_input=query_input)
        except InvalidArgument:
            print('Error at dialog_flow_function when trying to get response')
            raise

        response_intent = response.query_result.intent.display_name
        response_text = response.query_result.fulfillment_text
        response_parameters = self.get_parameters(response.query_result.parameters)
        response_confidence = response.query_result.intent_detection_confidence
        print(response)

        #if response_confidence < 0.5:
            #return self.dialog_flow_function('fallback')

        if '?' in response_text:
            self.ack(response_text)
            return self.listen()

        elif response_intent in self._game_commands:
            return {'response_text': response_text, 'command': response_intent, 'parameters': response_parameters}
        elif response_intent in self._chat_commands:
            self.ack(response_text)
            return None

    @staticmethod
    def get_parameters(response):
        parameters = dict()
        for key in response.keys():
            parameters[key] = response[key]
        return parameters

    @staticmethod
    def play(sound):
        fs = 24000  # 44100 samples per second
        # Start playback
        play_obj = sa.play_buffer(sound, 1, 2, fs)
        # Wait for playback to finish before exiting
        play_obj.wait_done()
