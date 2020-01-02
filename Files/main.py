import WebDriver
import VoiceAssistant
import GameList


class MyMain:
    property
    _Games_list = None
    _VoiceAssistant = None
    _WebDriver = None

    def __init__(self):
        self._Games_list = GameList.get_games_list()
        self._VoiceAssistant = VoiceAssistant()
        self._WebDriver = WebDriver()
