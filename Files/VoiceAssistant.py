# imports
import foldername.file.py

# globals


class VoiceAssistant:
    property
    _Name = 'Daisy'
    _key_word = 'hello daisy'
    _day = '1'
    _month = '1'
    _year = '2020'
    _birthDate = _day + '/' + _month + '/' + _year
    _favFood = 'data'
    _creators = 'Liron Revah and Baruh Shalumov'

    def __init__(self):
        #TODO

    def close(self):
        massage = 'Goodbye'
        self.tts(massage)
        return True

    def listen(self):
        #TODO

    # output - return Today Day, Month and Year as int
    def getTodayDate(self):
        from datetime import date
        today = date.today()
        day = today.strftime("%d")
        month = today.strftime("%m")
        year = today.strftime("%Y")
        return int(day), int(month), int(year)

    def sayName(self):
        massage = 'My name is ' + self._Name
        return self.tts(massage)

    def sayBirthDate(self):
        massage = 'I born on the ' + self._birthDate
        return self.tts(massage)

    def sayFavFood(self):
        massage = 'My favorite food is ' + self._favFood
        return self.tts(massage)

    def sayCreatorsName(self):
        massage = 'My Creators are ' + self._creators
        return self.tts(massage)


    def tts(self, massage):
        # TODO
