# imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# class
class MyWebDriver:
    _driver = None
    _wait = 2
    _game = None
    _page = None
    _buttons_map = None
    _commands_map = None
    _creator = 'Liron Revah and Baruh Shalumov'

    def __init__(self, game, page):
        self._game = game
        self._page = page
        self._buttons_map = game.get_buttons_map()
        self._commands_map = game.get_commands_map()
        self.load_game()

# Functions
    # do - close the browser
    def close(self):
        self._driver.quit()
        return True

    # do - return creator names
    def getMyCreator(self):
        return self._creator

    # do - load the game page
    def load_game(self):
        driver = self._driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(self._page)

    # input - type as string, string as string
    # output - return element if found in '_wait' seconds, None otherwise
    def find_elem(self, type, string):
        driver = self._driver
        delay = self._wait
        try:
            if type == 'xpath':
                WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, string)))
                elem = driver.find_element_by_xpath(string)
            elif type == 'id':
                WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, string)))
                elem = driver.find_element_by_id(string)

            return elem
        except:
            print('Could not find: '+ string)
            return None

    # input - elem as web element
    # output - return True if successful, False if not
    # do - click the elem
    def click_elem(self, elem):
        #TODO

    # input - elem as web element, data as string
    # output - return True if successful, False if not
    # do - send the elem the data
    def send_data_to_elem(self, elem, data):
        #TODO

    # input - elem as web element, data as string
    # output - return True if successful, False if not
    # do - send the elem the data
    def read_elem_text(self, elem):
        # TODO

    # output - return True if successful
    # do - if called refresh page of the browser
    def new_game(self):
        self._driver.refresh()
        return True

    # input - command_string as string, data as string
    # output - return True + None if successful, False if not + massage
    # do - check if command is viable, if yes run it
    def get_command(self, command_string, data):
        if command_string == 'new game':
            return self.new_game()
        else:
            if command_string in self._commands_map.keys():
                return self.run_command(self._commands_map[command_string], data)
            return False, 'This command is not viable'

    # input - command_string as list of strings, data as string
    # output - return True + None if successful, False if not + massage
    # do - send data to be checked if viable, if yes lunch command
    def run_command(self, command, data):
        mytype = command[0]
        path = command[1]
        path_type = command[2]
        limit_type = command[3]
        limits = command[4]

        if self.cheak_data_input(limit_type, limits, data):
            return self.execute_command(self, mytype, path, path_type, data)
        else:
            return False, 'data is not viable'

    # input - limit_type as string, limits as list of strings, data as string
    # output - return True + None if good, False if not
    # do - cheak if data is in the limits
    def cheak_data_input(self, limit_type, limits, data):
        # TODO

    def execute_command(self, mytype, path, path_type, data):
        elem = self.find_elem(path_type, path)
        if mytype == 'click':
            return self.click_elem(elem)
        elif mytype == 'send':
            return self.send_data_to_elem(elem, data)
        elif mytype == 'read':
            return self.read_elem_text(elem)
