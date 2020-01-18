# imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


# class
class MyWebDriver:
    _driver = None
    _wait = 1
    _page = None
    _web_elements = None
    _creator = 'Liron Revah and Baruh Shalumov'

    def __init__(self, game):
        self._page = game.get_info('url')
        self._web_elements = game.get_info('web_elem')
        self.load_game()

# Functions
    # do - return creator names
    def getMyCreator(self):
        return self._creator

    # do - load the game page
    def load_game(self):
        driver = self._driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(self._page)

    # output - return True if successful
    # do - if called refresh page of the browser
    def new_game(self):
        self._driver.refresh()
        return True

    # output - return True if successful
    # do - close the browser
    def close(self):
        self._driver.quit()
        return True

    # input - type as string, string as string
    # output - return element if found in '_wait' seconds, None otherwise
    def find_elem(self, elem_type, string):
        driver = self._driver
        delay = self._wait
        try:
            if elem_type is 'xpath':
                WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, string)))
                elem = driver.find_element_by_xpath(string)
            elif elem_type is 'id':
                WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, string)))
                elem = driver.find_element_by_id(string)

            return elem
        except:
            print('Could not find: '+ string)
            return None

    # input - elem as web element
    # output - return True if successful, False if not
    # do - select the elem
    def select_elem(self, elem, value):
        select = Select(elem)
        select.select_by_value(value)  # select_by_visible_text(value)
        return True, 'Selected the item'

    # input - elem as web element
    # output - return True if successful, False if not
    # do - click the elem
    def click_elem(self, elem):
        elem.click()
        return True, 'Clicked the item'

    # input - elem as web element, data as string
    # output - return True if successful, False if not
    # do - send the elem the data
    def send_data_to_elem(self, elem, data):
        elem.send_keys(data)
        return True, 'Inserted data'

    # input - elem as web element, data as string
    # output - return True if successful, False if not
    # do - send the elem the data
    def read_elem_text(self, elem):
        text = elem.get_attribute('textContent') # should i use this?
        # text = elem.text # should i use this?
        if text is not None:
            return True, text
        else:
            return False, None

    # input - command_string as string, data as string
    # output - return True + None if successful, False if not + massage
    # do - check if command is viable, if yes run it
    def get_command(self, command_string, data):
        exit_key_words = ['close game', 'i want to quit', 'quit']
        new_game_key_words = ['new game', 'refresh', 'restart']

        if command_string in new_game_key_words:
            return self.new_game()
        elif command_string in exit_key_words:
            return self.close()
        else:
            if command_string in self._web_elements.keys():
                return self.run_command(self._web_elements[command_string], data)
            return False, 'This command is not viable'

    # input - command_string as list of strings, data as string
    # output - return True + None if successful, False if not + massage
    # do - send data to be checked if viable, if yes lunch command
    def run_command(self, web_elem, data):
        name, command_type, string_type, string = web_elem.get_data()
        return self.execute_command(self, command_type, string_type, string, data)

    def execute_command(self, command_type, string_type, string, data):
        elem = self.find_elem(string_type, string)
        if command_type is 'click':
            return self.click_elem(elem)
        elif command_type is 'send':
            return self.send_data_to_elem(elem, data)
        elif command_type is 'read':
            return self.read_elem_text(elem)

    def alert_handle(self):
        obj = self._driver.switch_to.alert
        msg = obj.text
        obj.accept()
        self._driver.switch_to.default_content()
        return True
