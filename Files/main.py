# imports
import WebDriver as WD
import VoiceAssistant as VA
import GameCenter as GC


class MyMain:
    _GamesCenter = None
    _VoiceAssistant = None
    _WebDriver = None

    def __init__(self):
        self._GamesCenter = GC.GameCenter()
        while True:
            self.run()

    # do - call close function of everything
    def close_all(self):
        if self._VoiceAssistant.close():
            return True
        else:
            print('Could not close Voice Assistant')

    # do - game menu
    def choose_game(self):
        list_of_games = self._GamesCenter.get_list_of_game()
        print('Choose Game:')
        for index in range(len(list_of_games)):
            print(str(index + 1) + ': ' + list_of_games[index])
        input = 0  # TODO input from user as int
        return list_of_games[input]

    # do - start game
    def initialize_game(self, game_name):
        print('Staring Game: ' + game_name)
        game = self._GamesCenter.getGame(game_name)
        if game is not None:
            self._WebDriver = WD.MyWebDriver(game)
            self._VoiceAssistant = VA.VoiceAssistant(game, led_func=self._WebDriver.led_update)
            return True
        print('Did not Got a game to load')
        return False

    # do - get log update and read it
    def log(self):
        log_update = self._WebDriver.run_log()
        self._VoiceAssistant.read_log(log_update)

    # output - stop flag as boolean
    # do - run commands, and advices
    def user_interface(self):
        stop = False
        command_and_data = self._VoiceAssistant.listen()  # dict[command \ parameters \ text] = string \ dict
        if command_and_data is not None:
            result, stop, msg = self._WebDriver.get_command(command_and_data['command'], command_and_data['parameters'],
                                                            command_and_data['response_text'])
            self._VoiceAssistant.result_of_command(result, msg)  # announce the result of the command
            self._VoiceAssistant.update_advice_counter()
        return stop

    # do - run game
    def run(self):
        result = None
        game_name = self.choose_game()
        should_i_run = self.initialize_game(game_name)
        if should_i_run:
            stop = False
            while stop is not True:
                self.log()  # log Updates
                stop = self.user_interface()  # User Interface
            result = self.close_all()
        if result is not None:
            print('Is everything got shutdown: ' + str(result))


MyMain()
