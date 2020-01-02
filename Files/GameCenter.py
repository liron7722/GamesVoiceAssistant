import os


class GameList():
    property
    _list = []
    _games_folder = ''

    def __init__(self):
        path = self._games_folder
        arr = os.listdir(path)
        for file in arr:
            self._list.append(file.getMyName())

    def get_games_list(self):
        return self._list
