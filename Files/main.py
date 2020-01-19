# imports
import WebDriver as WD
import VoiceAssistant as VA
import GameCenter as GC


class MyMain:
    _GamesCenter = None
    _VoiceAssistant = None
    _WebDriver = None

    def __init__(self):
        self.run()

    def close_all(self):
        if self._WebDriver.close():
            if self._VoiceAssistant.close():
                return True
            else:
                print('Couldnt close Voice Assistant')
        else:
            print('Couldnt close Web Driver')

    def run(self):
        game_name = 'Monopoly'
        print('Staring Game: '+ game_name)
        game = self._GamesCenter.getGame(game_name)
        self._WebDriver(game)
        self._VoiceAssistant(game, 'va', None)
        stop = False
        while stop is not True:
            commands_and_data, msg = self._VoiceAssistant.listen()
            for command in commands_and_data.keys():
                data = commands_and_data[command]
                result, stop = self._WebDriver.get_command(command, data)
                self._VoiceAssistant.result_of_command(result, msg)
                # TODO make if got log command do read log





