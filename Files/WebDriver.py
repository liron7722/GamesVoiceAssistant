# imports
from copy import copy
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException, \
    ElementNotVisibleException, ElementNotSelectableException, ElementNotInteractableException, NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class MyWebDriver:
    _driver = webdriver.Firefox()  # Web Driver
    _delay = 1  # Timer for finding web element
    _page = None  # Game starting page
    _web_elements = None  # Game buttons
    _logs = None  # Inside game log

    def __init__(self, game):
        self._page = game.get_info('url')
        self._web_elements = game.get_info('web_elem')
        self.load_game(self._driver, self._page)  # start game

    # Functions
    # input - driver as web driver, page as string
    # do - load the game page
    @staticmethod
    def load_game(driver, page):
        driver.fullscreen_window()  # Maximize browser window
        driver.get(page) # load page

    # output - return True if successful, False as stop flag, 'Game Refreshed' massage as string
    # do - refresh page of the browser
    def new_game(self):
        self._driver.refresh()
        return True, False, 'Game Refreshed'

    # output - return True if successful, False as stop flag, 'Game closed' massage as string
    # do - close the browser
    def close(self):
        self._driver.quit()
        return True, True, 'Game closed'

    # output - text as list of string
    # do - save new list of log, split new lines from old and send them
    def run_log(self):
        result, stop, log_text = self.get_command('log')
        if result:  # result true if there is text, otherwise false
            last_log = log_text.splitlines()  # split string to list of strings
            text = copy(last_log)  # make copy of the list
            if self._logs is not None:  # if we got old log
                for line in self._logs:
                    text.remove(line)
            self._logs = last_log  # save all of the new log
            return text  # return only new lines of the log

    # input - elem_type as string, string as string
    # output - return element if found in <delay> seconds, None otherwise
    def find_elem(self, elem_type, string):
        driver = self._driver
        delay = self._delay
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
        except TimeoutException as exception:  # did not found elem in time
            return None
        except NoSuchElementException as exception:  # did not found elem
            return None

    # input - elem as web element
    # output - return True if successful, False as stop flag, massage as string
    # do - hover the elem
    @staticmethod
    def hover_elem(driver, elem):
        try:
            hover = ActionChains(driver).move_to_element(elem)
            hover.perform()
            return True, False, 'done'
        except:
            return False, False, 'Could not hover that'

    # input - elem as web element, value as string, msg as string
    # output - return True if successful, False as stop flag, massage as string
    # do - select the option in elem
    @staticmethod
    def select_elem(elem, value, msg):
        if type(value) is not str:  # if value is number
            value = int(value)  # make sure value will be int and not float
        try:
            select = Select(elem)  # select the elem
            select.select_by_visible_text(str(value))  # select by text
            return True, False, msg
        except ElementNotSelectableException as exception:
            return False, False, 'Could not select that'

    # input - elem as web element, msg as string
    # output - return True if successful, False as stop flag, massage as string
    # do - click the elem
    @staticmethod
    def click_elem(elem, msg):
        try:
            elem.click()
            return True, False, msg
        except ElementClickInterceptedException as exception:
            return False, False, 'Could not click that'
        except ElementNotInteractableException as exception:
            return False, False, 'Could not click that'

    # input - elem as web element, data as string
    # output - return True if successful, False as stop flag, massage as string
    # do - send the text box elem string
    @staticmethod
    def send_data_to_elem(elem, data):
        try:
            elem.clear()  # clear text box
            elem.send_keys(data)  # type sting into text box
            return True, False, 'done'
        except:
            return False, False, 'Could not do that'

    # input - elem as web element
    # output - return True if successful, False as stop flag, massage as string
    # do - get the elem text
    @staticmethod
    def read_elem_text(elem):
        try:
            text = elem.text  # get elem text
            return True, False, text
        except:
            return False, False, ''

    # input - result as string
    # output - return True if successful, False as stop flag, massage as string
    # do - return massage if result none, accept alert if result accept so accept, if result dismiss so dismiss
    def alert_handle(self, result=None):
        driver = self._driver
        try:
            obj = driver.switch_to.alert  # driver focus on alert window
            msg = 'alert massage says: ' + obj.text  # take alert window massage
            if result == 'accept':
                obj.accept()  # accept alert window
            elif result == 'dismiss':
                obj.dismiss()  # dismiss alert window
            driver.switch_to.default_content()  # return to main window
            return True, False, msg
        except NoAlertPresentException as exception:
            return False, False, 'Did not find any alert'

    # input - command_string as string, data as dict of parameters, msg as string
    # output - return output of other function if command is found, else False as result, False as stop flag, massage as string
    # do - check if command is viable, if yes run it
    def get_command(self, command_string, data=None, msg=None):
        general_commands = {'new game': self.new_game, 'exit': self.close}

        if command_string in general_commands.keys():  # if command is on browser
            return general_commands[command_string]()
        else:
            if command_string in self._web_elements.keys():  # if command is on web elements
                return self.run_command(self._web_elements[command_string], data, msg)
            return False, False, 'did not found command'

    # input - web elem as WebElements, data as dict of parameters, msg as string
    # output - return execute_command output
    # do - if needed change location of the elem, then execute command
    def run_command(self, web_elem, data=None, msg=None):
        info = None
        name, command_type, string_type, string = web_elem.get_data()
        if data is not None:
            if 'number' in data.keys():
                string = string.replace('1', str(int(data['number'])))
            if 'label' in data.keys():
                string = string.replace('buy', data['label'])
            if 'data' in data.keys():
                info = data['data']
        return self.execute_command(command_type, string_type, string, info, msg)

    # input - command_type as string, string_type as string, string as string, data as string, msg as string
    # output - return output of called function
    # do - if needed change location of the elem, then execute command
    def execute_command(self, command_type, string_type, string, data=None, msg=None):
        if command_type == 'alert':
            return self.alert_handle(data)

        elem = self.find_elem(string_type, string)
        if elem is None:
            return False, False, 'Could not find web element'

        driver = self._driver
        if command_type == 'click':
            return self.click_elem(elem, msg)
        elif command_type == 'send':
            return self.send_data_to_elem(elem, data)
        elif command_type == 'read':
            return self.read_elem_text(elem)
        elif command_type == 'select':
            return self.select_elem(elem, data, msg)
        elif command_type == 'hover':
            return self.hover_elem(driver, elem)

        return False, False, 'I dont know how to handle command type: ' + command_type

