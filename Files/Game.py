

class Game:

    def __init__(self, name, file, creator, url):
        self._name = name
        self._file = file
        self._creator = creator
        self._page_location = url

    def get_name(self):
        return self._name

    def get_creator(self):
        return self._creator

    def get_File(self):
        return self._file

    def get_url(self):
        return self._page_location

    def get_my_dict(self):
        return {'name':self.get_name(),
                'file': self.get_File(),
                'creator':self.get_creator(),
                'url':self.get_url()
                }
