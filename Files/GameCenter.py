# imports
import json
import Files.Game as G


class GameCenter:
    _list_of_games = []
    _games_folder = 'games files'
    _games_list_file = 'games_list_file.json'

    def __init__(self):
        game_list = self.readJson(self._games_folder, self._games_list_file)
        for game in game_list:
            item = G.Game(game['name'], game['creator'], game['url'], game['json_name'])
            self._list_of_games.append(item)

    def add_game_to_list(self, game):
        if game not in self._list_of_games:
            self._list_of_games.append(game)
            self.save_game_list()

    def save_game_list(self):
        for game in self._list_of_games:
            item = game.get_my_dict()
            self._list_of_games.append(item)
        self.writeJson(self._list_of_games, self._games_list_file)

    def getGame(self, name):
        game_list = self._games_list_file
        for game in game_list:
            if name is game.get_name():
                return game
            else:
                return None

    def readJson(self, path, filename):
        with open(path + '/' + filename) as json_file:
            data = json.load(json_file)
        return data

    def writeJson(self, data, filename):
        with open(filename, 'w') as outfile:
            json.dump(data, outfile, indent=4)