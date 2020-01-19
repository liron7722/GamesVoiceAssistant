# imports
from extra import *
from Game import Game


class GameCenter:
    _list_of_games = []
    _path = None
    _games_folder = 'games files'
    _games_list_file = 'games_list_file.json'

    def __init__(self):
        self._path = get_path() + '/' + self._games_folder
        game_list = readJson(self._path, self._games_list_file)
        for game in game_list:
            item = Game(game['name'], game['creator'], game['url'], game['json_name'], self._path)
            self._list_of_games.append(item)

    def add_game_to_list(self, game):
        if game not in self._list_of_games:
            self._list_of_games.append(game)
            self.save_game_list()

    def save_game_list(self):
        game_list = []
        for game in self._list_of_games:
            data = game.get_info()
            game_list.append(data)
        writeJson(self._path, self._games_list_file, game_list)

    def getGame(self, name):
        game_list = self._list_of_games
        for game in game_list:
            if name == game.get_info('name'):
                return game
            else:
                return None

    def get_list_of_game(self):
        mylist = []
        for game in self._list_of_games:
            mylist.append(game.get_info('name'))
        return mylist