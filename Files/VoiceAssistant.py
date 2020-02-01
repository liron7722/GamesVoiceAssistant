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
    _key_word = 'hi ' + _name  # string
    _shutdown_key_word = 'bye ' + _name  # string
    _kw_heard = False  # boolean
    _chat_commands = ['creators', 'favorite food', 'Default Welcome Intent', 'advice', 'welcome back']  # add here everything that is chat only
    _game_commands = None  # list
    _status_dict = {'off': 'red', 'on': 'green', 'listen': 'yellow', 'record': 'orange', 'speak': 'blue'}
    _my_status = 'red'  # color as string
    _advice_counter = 0  # num as int
    _recorder = None  # recorder class

    _DIALOGFLOW_PROJECT_ID = 'gamesvoiceassistant'
    _DIALOGFLOW_LANGUAGE_CODE = 'en'
    _SESSION_ID = 'me'

    _language_code ='en-US'
    _voice_gender = texttospeech.enums.SsmlVoiceGender.FEMALE

    def __init__(self, game, gender_type=None, name=None):
        self._recorder = Recorder()
        self._game_commands = game.get_info('web_elem').keys()
        self.gender(gender_type)
        if name is not None:
            self._name = name
        change_status(self._status_dict['off'])

    # input - gender_type as string
    # do - set gender based on input
    def gender(self,gender_type):
        if gender_type is not None:
            # voice gender ("neutral", "FEMALE", "MALE")
            if gender_type == 'va':
                self._voice_gender = texttospeech.enums.SsmlVoiceGender.FEMALE
            elif gender_type == 'opponent':
                self._voice_gender = texttospeech.enums.SsmlVoiceGender.NEUTRAL
            else:
                self._voice_gender = texttospeech.enums.SsmlVoiceGender.MALE

    # do - call status_change to on
    def open(self):
        massage = 'Hello everybody, My name is ' + self._name
        return self.status_change(True, 'on', massage)

    # do - call status_change to off
    def close(self):
        massage = 'Goodbye'
        return self.status_change(False, 'off', massage)

    # input isOn as boolean, key as string, massage as string
    # do - set keyword to off, set key, say massage
    def status_change(self, isOn, key, massage):
        self._kw_heard = isOn
        change_status(self._status_dict[key])
        self.ack(massage)
        return True

    # input - text as string
    # do - print as say text
    def ack(self, text):
        if len(text) < 150:  # if text is short
            print('Voice Assistance said: ' + text)
            self.tts(text)
        else:  # if text is a long one
            text = text.splitlines()  # split string into list of string
            for line in text:
                print('Voice Assistance said: ' + line)
                self.tts(line)

    # do - inc advice counter, and run advice if needed
    def update_advice_counter(self):
        self._advice_counter += 1
        if self._advice_counter % 10 == 0:
            self.give_advice()

    # do - call for advice from dialog flow
    def give_advice(self):
        self.ack('Running auto advice')
        self.dialog_flow_function('advice')

    # input - text as list of strings
    # do - say all the strings in list
    def read_log(self, text):
        if text is not None:
            for line in text:
                self.ack(line)

    # do - call for recorder listen, set keyword_heard to True/False
    def listen(self):
        text = None
        while text is None:
            self._recorder.listen()  # create sound file
            text = self.stt()  # turn sound file into string
            if text is not None:  # user said something
                if self._shutdown_key_word in text:  # user want to turn off voice assistant
                    self.close()
                else:
                    if self._kw_heard:
                        return self.dialog_flow_function(text)
                    elif self._key_word in text:  # user want to turn on voice assistant
                        self.open()
                text = None

    # do - transfer speech to text
    @staticmethod
    def stt():
        string = []
        client = speech.SpeechClient()
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

        # print what user said
        if len(string) > 0:
            print('User said: ' + string)
            return string

        # print we didnt got anything on the recording
        print('Nothing on the recording')
        return None

    # input - massage as string
    # do - transfer text to speech and play it
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

        change_status(self._status_dict['speak'])  # call for voice assistant led change
        self.play(response.audio_content)  # play sound

    # input - text as string
    # output dict [response_text / response_intent / response_parameters] or None
    # do - send text to dialog flow system and get proper response
    def dialog_flow_function(self, text):
        # initialize dialog flow client
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(self._DIALOGFLOW_PROJECT_ID, self._SESSION_ID)
        text_input = dialogflow.types.TextInput(text=text, language_code=self._DIALOGFLOW_LANGUAGE_CODE)
        query_input = dialogflow.types.QueryInput(text=text_input)

        try:
            response = session_client.detect_intent(session=session, query_input=query_input)
        except InvalidArgument:
            print('Error at dialog_flow_function when trying to get response')
            raise

        # split response to variables
        response_intent = response.query_result.intent.display_name
        response_text = response.query_result.fulfillment_text
        response_parameters = self.get_parameters(response.query_result.parameters)
        response_confidence = response.query_result.intent_detection_confidence
        #print(response)

        # make sure the we confident on chosen path
        #if response_confidence < 0.5:
            #return self.dialog_flow_function('fallback')

        # call for fallow up answer
        if '?' in response_text:
            self.ack(response_text)
            return self.listen()

        # do action on game
        elif response_intent in self._game_commands:
            return {'response_text': response_text, 'command': response_intent, 'parameters': response_parameters}

        # chat with voice assistant
        elif response_intent in self._chat_commands:
            self.ack(response_text)
            return None

    # input - response as dict
    # do - make and return parameters dict
    @staticmethod
    def get_parameters(response):
        parameters = dict()
        for key in response.keys():
            parameters[key] = response[key]
        return parameters

    # input - sound as audio_content
    # do - play sound
    @staticmethod
    def play(sound):
        fs = 24000  # 44100 samples per second
        # Start playback
        play_obj = sa.play_buffer(sound, 1, 2, fs)
        # Wait for playback to finish before exiting
        play_obj.wait_done()

    # input - result as boolean, msg as string
    # do - ack massage
    def result_of_command(self, result, msg):
        bad_massage = 'Sorry, could not run that command'
        self.ack(msg)
        if result is False:
            print(bad_massage)
