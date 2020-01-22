

class WebElements:
    _name = None # string
    _type = None # button, info, textbox
    _string_type = None # id, xpath, etc..
    _string = None # string

    def __init__(self, name, my_type, string_type, string):
        self._name = name
        self._type = my_type
        self._string_type = string_type
        self._string = string

    def get_data(self, string=None):
        if string is None:
            return self._name, self._type, self._string_type, self._string
        elif string is 'name':
            return self._name
        elif string is 'type':
            return self._type
        elif string is 'string_type':
            return self._string_type
        elif string is 'string':
            return self._string