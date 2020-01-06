# imports
import os
import Files.Game as G
import Files.Recorder as R
from pydub.playback import play

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from google.cloud import texttospeech


class VoiceAssistant:
    property
    _name = 'Daisy'
    _key_word = 'hello ' + _name
    _kw_heard = False
    _favFood = 'human voice'
    _creators = 'Liron Revah and Baruh Shalumov'

    _recorder = R.Recorder()

    _voice_gender = texttospeech.enums.SsmlVoiceGender.FEMALE
    _language_code ='en-US'
    _credential_path = "SpeechClassAPI2.json" #TODO our own json
    _stt_client = speech.SpeechClient()
    _tts_client = texttospeech.TextToSpeechClient()

    def __init__(self, name, my_type):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self._credential_path

        if name is not None:
            self._name = name

        if my_type is not None:
            # voice gender ("neutral", "FEMALE", "MALE")
            if my_type == 'va':
                self._voice_gender = texttospeech.enums.SsmlVoiceGender.FEMALE
            elif my_type == 'opponent':
                self._voice_gender = texttospeech.enums.SsmlVoiceGender.NEUTRAL
            else:
                self._voice_gender = texttospeech.enums.SsmlVoiceGender.MALE

    def close(self):
        massage = 'Goodbye'
        self.tts(massage)
        return True

    def sayName(self):
        massage = 'My name is ' + self._Name
        return self.tts(massage)

    def sayFavFood(self):
        massage = 'My favorite food is ' + self._favFood
        return self.tts(massage)

    def sayCreatorsName(self):
        massage = 'My Creators are ' + self._creators
        return self.tts(massage)

    def stt(self, sound):
        string = []
        audio = types.RecognitionAudio(content=sound)

        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code = self._language_code)

        # Detects speech in the audio file
        response = self._stt_client.recognize(config, audio)

        for result in response.results:
             string.append(result.alternatives[0].transcript)

        return string

    def tts(self, massage):
        # Set the text input to be synthesized
        synthesis_input = texttospeech.types.SynthesisInput(text = massage)

        # Build the voice request, select the language code ("en-US") and the ssml
        voice = texttospeech.types.VoiceSelectionParams(
            language_code = self._language_code,
            ssml_gender = self._voice_gender)

        # Select the type of audio file you want returned
        audio_config = texttospeech.types.AudioConfig(
            audio_encoding = texttospeech.enums.AudioEncoding.LINEAR16)

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = self._tts_client.synthesize_speech(synthesis_input, voice, audio_config)

        # play(response.audio_content) # should i use this
        play_obj = response.audio_content.play()
        play_obj.wait_done()  # Wait until sound has finished playing

    def listen(self):
        sound = None
        while sound is None:
            sound = self._recorder.listen()
            text = self.stt(self, sound)
            if self._kw_heard:
                commands_and_data = self.extract_info(text)
                return commands_and_data
            else:
                if text is self._key_word:
                    self._kw_heard = True

    def extract_info(self, text):
        result = dict()
        # TODO send to function that convert list of text to commands and data dict, return result
        return result

    def result_of_command(self, result):
        # TODO What should this class do with what happend with the command
        return None


