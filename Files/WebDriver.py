# imports
from copy import copy
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException, \
    ElementNotVisibleException, ElementNotSelectableException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class MyWebDriver:
    _driver = webdriver.Firefox()
    _wait = 1
    _page = None
    _web_elements = None
    _logs = None

    def __init__(self, game):
        self._page = game.get_info('url')
        self._web_elements = game.get_info('web_elem')
        self.load_game(self._driver, self._page)

    # Functions
    # do - load the game page
    @staticmethod
    def load_game(driver, page):
        driver.fullscreen_window()
        driver.get(page)

    # output - return True if successful
    # do - if called refresh page of the browser
    def new_game(self):
        self._driver.refresh()
        return True, False, 'Game Refreshed'

    # output - return True if successful
    # do - close the browser
    def close(self):
        self._driver.quit()
        return True, True, 'Game closed'

    def run_log(self):
        result, stop, log_text = self.get_command('log')
        if result:  # result true if there is text, otherwise false
            last_log = log_text.splitlines()
            text = copy(last_log)
            if self._logs is not None:
                for line in self._logs:
                    text.remove(line)
            self._logs = last_log
            return text

    # input - type as string, string as string
    # output - return element if found in '_wait' seconds, None otherwise
    def find_elem(self, elem_type, string):
        driver = self._driver
        delay = self._wait
        try:
            elem = None
            if elem_type == 'xpath':
                WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, string)))
                elem = driver.find_element_by_xpath(string)
            elif elem_type == 'id':
                WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, string)))
                elem = driver.find_element_by_id(string)
            else:
                print('find_elem function need to have: ' + elem_type)
            return elem
        except TimeoutException as exception:
            return None
        except NoSuchElementException as exception:
            return None

    # input - elem as web element
    # output - return True if successful, False if not
    # do - hover the elem
    def hover_elem(self, elem):
        driver = self._driver
        try:
            hover = ActionChains(driver).move_to_element(elem)
            hover.perform()
            return True, False, 'done'
        except:
            return False, False, 'Could not hover that'

    # input - elem as web element
    # output - return True if successful, False if not
    # do - select the elem
    @staticmethod
    def select_elem(elem, value, msg):
        if type(value) is not str:
            value = int(value)
        try:
            select = Select(elem)
            select.select_by_visible_text(str(value))
            return True, False, msg
        except ElementNotSelectableException as exception:
            return False, False, 'Could not select that'

    # input - elem as web element
    # output - return True if successful, False if not
    # do - click the elem
    def click_elem(self, elem, msg):
        try:
            elem.click()
            #if alert:
                #self.alert_handle()
            return True, False, msg
        except ElementClickInterceptedException as exception:
            return False, False, 'Could not click that'
        except ElementNotInteractableException as exception:
            return False, False, 'Could not click that'

    # input - elem as web element, data as string
    # output - return True if successful, False if not
    # do - send the elem the data
    @staticmethod
    def send_data_to_elem(elem, data):
        try:
            elem.clear()
            elem.send_keys(data)
            return True, False, 'done'
        except:
            return False, False, 'Could not do that'

    # input - elem as web element, data as string
    # output - return True if successful, False if not
    # do - send the elem the data
    @staticmethod
    def read_elem_text(elem):
        try:
            text = elem.text
            return True, False, text
        except:
            return False, False, ''

    # input - command_string as string, data as string
    # output - return True + None if successful, False if not + massage
    # do - check if command is viable, if yes run it
    def get_command(self, command_string, data=None, msg=None):
        general_commands = {'new game': self.new_game, 'exit': self.close}

        if command_string in general_commands.keys():
            return general_commands[command_string]()
        else:
            if command_string in self._web_elements.keys():
                return self.run_command(self._web_elements[command_string], data, msg)
            return False, False, 'did not found command'

    # input - command_string as list of strings, data as string
    # output - return True + None if successful, False if not + massage
    # do - send data to be checked if viable, if yes lunch command
    def run_command(self, web_elem, data=None, msg=None):
        info = None
        name, command_type, string_type, string = web_elem.get_data()
        if data is not None:
            if 'number' in data.keys():
                string = string.replace('1', str(int(data['number'])))
            elif 'label' in data.keys():
                string = string.replace('buy', data['label'])
            if 'data' in data.keys():
                info = data['data']
        return self.execute_command(command_type, string_type, string, info, msg)

    def execute_command(self, command_type, string_type, string, data=None, msg=None):
        elem = self.find_elem(string_type, string)
        if elem is None:
            return False, False, 'Could not find web element'

        if command_type == 'click':
            return self.click_elem(elem, msg)
        elif command_type == 'send':
            return self.send_data_to_elem(elem, data)
        elif command_type == 'read':
            return self.read_elem_text(elem)
        elif command_type == 'select':
            return self.select_elem(elem, data, msg)
        elif command_type == 'hover':
            return self.hover_elem(elem)

    def alert_handle(self):
        driver = self._driver
        obj = driver.switch_to.alert
        msg = 'alert massage says: ' + obj.text
        obj.accept()
        driver.switch_to.default_content()
        return True, False, msg
