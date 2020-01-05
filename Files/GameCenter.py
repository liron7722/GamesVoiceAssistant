# imports
import os
import json
import Files.Game as G


class GameCenter:
    _list_of_games = []
    _games_folder = 'game py files'
    _games_list_file = 'games_list_file.json'

    def __init__(self):
        games_list_file = self._games_list_file
        path = self._games_folder
        game_list = self.readJson(path, games_list_file)
        for game in game_list:
            self._list_of_games.append(G.Game(game['name'], game['file'], game['creator'], game['url']))

    def add_game_to_list(self, game):
        if game not in self._list_of_games:
            self._list_of_games.append(game)
            self.save_game_list()

    def save_game_list(self):
        my_list = list()
        for game in self._list_of_games:
            my_dict = game.get_my_dict()
            my_list.append(my_dict)
        self.writeJson(self, my_list, self._games_list_file)

    def getGame(self, name):
        game_list = self._games_list_file
        for game in game_list:
            if name == game.get_name():
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