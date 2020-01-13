import json
import WebElements as WE


class Game:
    _name = None # game name
    _creator = None # string
    _path = None # path as string
    _json = None # json file for WebElements
    _web_elements = dict() # dict of WebElements => [name] = WebElement

    def __init__(self, name, creator, url, json_name):
        self._name = name
        self._creator = creator
        self._url = url
        self._json = json_name
        self.load_web_elements()

    def get_info(self, string):
        if string is None:
            return {'name':self._name, 'creator':self._creator, 'path':self._url, 'web_elem':self._web_elements}
        elif string is 'name':
            return self._name
        elif string is 'creator':
            return self._creator
        elif string is 'url':
            return self._url
        elif string is 'web_elem':
            return self._web_elements

    def load_web_elements(self):
        data = self.readJson(self._path, self._json) # get dict[name] = dict[name \ my_type \ path_type \ path]
        for key in data.keys():
            name = self._web_elements[key]['name']
            my_type = self._web_elements[key]['my_type']
            path_type = self._web_elements[key]['path_type']
            path = self._web_elements[key]['path']

            self._web_elements[name] = WE.WebElements(name, my_type, path_type, path)

    def readJson(self, path, filename):
        with open(path + '/' + filename) as json_file:
            data = json.load(json_file)
        return data

    def writeJson(self, data, filename):
        with open(filename, 'w') as outfile:
            json.dump(data, outfile, indent=4)

