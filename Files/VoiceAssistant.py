# imports
import io
import os
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
    _name = None
    _key_word = None
    _kw_heard = False
    _favFood = 'human voice'
    _creators = 'Liron Revah and Baruh Shalumov'

    _recorder = Recorder()

    _DIALOGFLOW_PROJECT_ID = 'gamesvoiceassistant'
    _DIALOGFLOW_LANGUAGE_CODE = 'en'
    _SESSION_ID = 'me'
    _session_client = None
    _session = None

    _language_code ='en-US'
    _voice_gender = None
    _stt_client = None
    _tts_client = None

    def __init__(self, game, my_type, name):
        self.startConnection()
        self.gender(my_type)
        if name is not None:
            self._name = name

    def startConnection(self):
        self._session_client = dialogflow.SessionsClient()
        self._session = self._session_client.session_path(self._DIALOGFLOW_PROJECT_ID, self._SESSION_ID)

    def gender(self,my_type):
        if my_type is not None:
            # voice gender ("neutral", "FEMALE", "MALE")
            if my_type == 'va':
                self._name = 'Daisy'
                self._key_word = 'Hello ' + self._name
                self._voice_gender = texttospeech.enums.SsmlVoiceGender.FEMALE
            elif my_type == 'opponent':
                self._voice_gender = texttospeech.enums.SsmlVoiceGender.NEUTRAL
            else:
                self._voice_gender = texttospeech.enums.SsmlVoiceGender.MALE

    def close(self):
        massage = 'Goodbye'
        self.ack(massage)
        return True

    def sayName(self):
        massage = 'My name is ' + self._name
        return self.ack(massage)

    def sayFavFood(self):
        massage = 'My favorite food is ' + self._favFood
        return self.ack(massage)

    def sayCreatorsName(self):
        massage = 'My Creators are ' + self._creators
        return self.ack(massage)

    def listen(self):
        text = None
        while text is None:
            self._recorder.listen()
            text = self.stt()
            if self._kw_heard:
                return self.dialog_flow_function(text)
            elif self._key_word in text:
                hello_text = 'Hello everybody'
                self.ack(hello_text)
                self._kw_heard = True

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

        return string

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


        self.play(self,response.audio_content)
        # play(response.audio_content) # should i use this
        # The response's audio_content is binary.
        with open('output.mp3', 'wb') as out:
            # Write the response to the output file.
            out.write(response.audio_content)
            print('Audio content written to file "output.mp3"')

    def result_of_command(self, result, msg):
        bad_massage = 'Sorry, could not run that command'
        text = self.dialog_flow_function(msg)
        if result:
            self.ack(text)
        else:
            self.tts(bad_massage)
        return True

    def dialog_flow_function(self, text):

        text_input = dialogflow.types.TextInput(text=text, language_code=self._DIALOGFLOW_LANGUAGE_CODE)
        query_input = dialogflow.types.QueryInput(text=text_input)

        try:
            response = self._session_client.detect_intent(session=self._session, query_input=query_input)
        except InvalidArgument:
            raise

        print("Query text:", response.query_result.query_text)
        print("Detected intent:", response.query_result.intent.display_name)
        print("Detected intent confidence:", response.query_result.intent_detection_confidence)
        print("Fulfillment text:", response.query_result.fulfillment_text)

        response_text = response.query_result.fulfillment_text
        response_intent = response.query_result.intent.display_name

        if '?' in response_text:
            self.ack(response_text)
            return self.listen()

        parameters = self.get_parameters(response)
        return response_text, response_intent, parameters

    def get_parameters(self, response):
        # TODO get parameters from response and return dict
        return None

    def ack(self, text):
        print(text)
        self.tts(text)

    def play(self, sound):
        fs = 24000  # 44100 samples per second
        # Start playback
        play_obj = sa.play_buffer(sound, 1, 2, fs)
        # Wait for playback to finish before exiting
        play_obj.wait_done()
