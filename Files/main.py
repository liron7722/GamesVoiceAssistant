# imports
import WebDriver as WD
import VoiceAssistant as VA
import GameCenter as GC


class MyMain:
    _GamesCenter = None
    _VoiceAssistant = None
    _WebDriver = None
    _logs = []

    def __init__(self):
        self._GamesCenter = GC.GameCenter()
        self.run()

    def close_all(self):
        if self._VoiceAssistant.close():
            if True: # self._WebDriver.close(): # happen in webdriver already
                return True
            else:
                print('Couldnt close Web Driver')
        else:
            print('Couldnt close Voice Assistant')

    def run_log(self):
        log_text = self._WebDriver.get_command('log')
        last_log = log_text.splitlines()
        temp = last_log
        if self._logs is not None:
            for line in self._logs:
                temp.remove(line)
        self._logs = last_log
        for line in temp:
            self._VoiceAssistant.tts(line)

    def run(self):
        game_name = 'Monopoly'
        print('Staring Game: '+ game_name)
        game = self._GamesCenter.getGame(game_name)
        if game is not None:
            self._WebDriver = WD.MyWebDriver(game)
            self._VoiceAssistant = VA.VoiceAssistant(game)
            stop = False
            while stop is not True:
                command_and_data = self._VoiceAssistant.listen()
                if command_and_data is not None:
                    result, stop = self._WebDriver.get_command(command_and_data['command'], command_and_data['parameters'])
                    self._VoiceAssistant.result_of_command(result, command_and_data['response_text'])
                    self.run_log()
            self.close_all()
        else:
            print('Didnt Got the game')


MyMain()
