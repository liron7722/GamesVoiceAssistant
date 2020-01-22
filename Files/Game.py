from extra import *
import WebElements as WebElem


class Game:
    _name = None # game name
    _creator = None # string
    _url = None # path as string
    _json = None # json file for WebElements
    _path = None  # path as string
    _web_elements = None  # dict of WebElements => [intent name] = WebElement

    def __init__(self, name, creator, url, json_name, path):
        self._name = name
        self._creator = creator
        self._url = url
        self._json = json_name
        self._path = path
        self.load_web_elements()

    def get_info(self, string=None):
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
        self._web_elements = dict()
        data = readJson(self._path, self._json) # get dict[name] = dict[name \ my_type \ path_type \ path] = 'string'
        for key in data.keys():
            self._web_elements[key] = WebElem.WebElements(key, data[key]['my_type'], data[key]['string_type'], data[key]['string'])
