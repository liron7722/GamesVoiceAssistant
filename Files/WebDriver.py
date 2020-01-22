# imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


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
        return True, False

    # output - return True if successful
    # do - close the browser
    def close(self):
        self._driver.quit()
        return True, False

    # input - type as string, string as string
    # output - return element if found in '_wait' seconds, None otherwise
    def find_elem(self, elem_type, string):
        driver = self._driver
        delay = self._wait
        elem=None
        #try:
        if elem_type is 'xpath':
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, string)))
            elem = driver.find_element_by_xpath(string)
        elif elem_type is 'id':
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, string)))
            elem = driver.find_element_by_id(string)

        return elem
        #except:
        #    print('Could not find: '+ string)
         #   return None

    # input - elem as web element
    # output - return True if successful, False if not
    # do - hover the elem
    def hover_elem(self, elem):
        hover = ActionChains(self._driver).move_to_element(elem)
        hover.perform()
        return True, 'item is hovered'

    # input - elem as web element
    # output - return True if successful, False if not
    # do - select the elem
    @staticmethod
    def select_elem(elem, value):
        select = Select(elem)
        select.select_by_visible_text(str(value))
        return True, False

    # input - elem as web element
    # output - return True if successful, False if not
    # do - click the elem
    @staticmethod
    def click_elem(elem):
        elem.click()
        return True, False

    # input - elem as web element, data as string
    # output - return True if successful, False if not
    # do - send the elem the data
    @staticmethod
    def send_data_to_elem(elem, data):
        elem.clear()
        elem.send_keys(data)
        return True, False

    # input - elem as web element, data as string
    # output - return True if successful, False if not
    # do - send the elem the data
    @staticmethod
    def read_elem_text(elem):
        text = elem.text()
        if text is not None:
            return True, False # TODO send text
        else:
            return None, False

    # input - command_string as string, data as string
    # output - return True + None if successful, False if not + massage
    # do - check if command is viable, if yes run it
    def get_command(self, command_string, data=None):
        general_commands = {'exit': self.new_game(),'new game': self.close()}
        if command_string in general_commands.keys():
            return general_commands[command_string]

        else:
            if command_string in self._web_elements.keys():
                return self.run_command(self._web_elements[command_string], data)
            return True, False

    # input - command_string as list of strings, data as string
    # output - return True + None if successful, False if not + massage
    # do - send data to be checked if viable, if yes lunch command
    def run_command(self, web_elem, data=None):
        name, command_type, string_type, string = web_elem.get_data()
        if data is not None:
            if 'number' in data.keys():
                string = string.replace('1', str(int(data['number'])))
            elif 'label' in data.keys():
                string = string.replace('buy', data['label'])
            if 'data' in data.keys():
                data = data['data']
        return self.execute_command(command_type, string_type, string, data)

    def execute_command(self, command_type, string_type, string, data=None):
        elem = self.find_elem(string_type, string)
        if elem is not None:
            if command_type is 'click':
                return self.click_elem(elem)
            elif command_type is 'send':
                return self.send_data_to_elem(elem, data)
            elif command_type is 'read':
                return self.read_elem_text(elem)
            elif command_type is 'select':
                return self.select_elem(elem, data)
            elif command_type is 'hover':
                return self.hover_elem(elem)
        return 'Could not find web element', False

    def alert_handle(self):
        obj = self._driver.switch_to.alert
        msg = obj.text
        obj.accept()
        self._driver.switch_to.default_content()
        return True
