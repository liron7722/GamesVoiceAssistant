# imports
from extra import *
from Game import Game
import os


class GameCenter:
    _list_of_games = None  # list
    _path = None  # string
    _games_folder = None  # string
    _games_list_file = None  # string

    def __init__(self):
        self._list_of_games = []
        self._games_folder = 'games files'
        self._games_list_file = 'games_list_file.json'
        self._path = get_path() + '/' + self._games_folder
        game_list = readJson(self._path, self._games_list_file)
        pwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        for game in game_list:
            print(game['url'])
            item = Game(game['name'], game['creator'], os.path.join(pwd, game['url']), game['json_name'], self._path)
            self._list_of_games.append(item)

    # input - game as Game
    # do - check if game is saved in list, if not save it
    def add_game_to_list(self, game):
        if game not in self._list_of_games:
            self._list_of_games.append(game)
            self.save_game_list()

    # do - save game list
    def save_game_list(self):
        game_list = []
        for game in self._list_of_games:
            data = game.get_info()
            game_list.append(data)
        writeJson(self._path, self._games_list_file, game_list)

    # output - return Game
    # do - if name is in the game list
    def getGame(self, name):
        game_list = self._list_of_games
        for game in game_list:
            if name == game.get_info('name'):
                return game
            else:
                return None

    # output - return list of string (game names)
    def get_list_of_game(self):
        mylist = []  # list
        for game in self._list_of_games:
            mylist.append(game.get_info('name'))
        return mylist