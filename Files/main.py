# imports
import Files.WebDriver as WD
import Files.VoiceAssistant as VA
import Files.GameCenter as GC


class MyMain:
    property
    _exit_key_words = ['close game', 'i want to quit']
    _GamesCenter = None
    _VoiceAssistant = None
    _WebDriver = None

    def __init__(self):
        self._GamesCenter = GC.GameCenter
        self._VoiceAssistant = VA.VoiceAssistant
        self._WebDriver = WD.MyWebDriver

    def close_all(self):
        if self._WebDriver.close():
            if self._VoiceAssistant.close():
                return True
            else:
                print('Couldnt close Voice Assistant')
        else:
            print('Couldnt close Web Driver')

    def run(self):
        game_name = 'monopoly'
        game = self._GamesCenter.getGame(game_name)
        self._WebDriver.__init__(game, game.get_url)
        self._VoiceAssistant.__init__(game)
        stop = False
        while stop is not True:
            commands_and_data = self._VoiceAssistant.listen()
            for command in commands_and_data.keys():
                if command in self._exit_key_words:
                    self.close_all()
                    stop = True
                    break
                else:
                    data = commands_and_data[command]
                    result = self._WebDriver.get_command(command, data)
                    self._VoiceAssistant.result_of_command(result)



