# imports
import WebDriver as WD
import VoiceAssistant as VA
import GameCenter as GC



class MyMain:
    property
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
        self._WebDriver.__init__(game)
        self._VoiceAssistant.__init__(game)
        stop = False
        while stop is not True:
            commands_and_data = self._VoiceAssistant.listen()
            for command in commands_and_data.keys():
                data = commands_and_data[command]
                result, stop = self._WebDriver.get_command(command, data)
                self._VoiceAssistant.result_of_command(result)



def run():
    A = MyMain()
    A.run()




