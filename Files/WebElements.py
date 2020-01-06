

class WebElements():
    _name = None # string
    _type = None # button, info, textbox
    _path_type = None # id, xpath, etc..
    _path = None # string

    def __init__(self, name, my_type, path_type, path):
        self._name = name
        self._type = my_type
        self._path_type = path_type
        self._path = path

    def get_data(self, string):
        if string is None:
            return self._name, self._type, self._path_type, self._path
        elif string is 'name':
            return self._name
        elif string is 'type':
            return self._type
        elif string is 'path_type':
            return self._path_type
        elif string is 'path':
            return self._path