# imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# class
class MyWebDriver:
    _driver = webdriver.Chrome()
    _wait = 2
    _game = None
    _page = None
    _creator = 'Liron Revah and Baruh Shalumov'

    def __init__(self, game, page):
        m_game = game
        m_page = page

# Functions
    def getMyCreator(self):
        return self._creator

    def load_page(self):
        driver = self._driver
        driver.maximize_window()
        driver.get(self._page)

    # input - item as string
    # output - xpath as string
    def get_item_xpath(self, item):
        game = self._game
        item_dict = game.getElementsXpaths()
        return item_dict[item]

    # input - item as string
    # output - id as string
    def get_item_id(self, item):
        game = self._game
        item_dict = game.getElementsIDs()
        return item_dict[item]

    # input - xpath as string
    # output - return element if found in 5 seconds, None otherwise
    def findElemByXpath(self, Xpath):
        driver = self._driver
        delay = self._wait
        try:
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, Xpath)))
            return driver.find_element_by_xpath(Xpath)
        except:
            print('Could not find: '+ Xpath)
            return None

    # input - id as string
    # output - return element if found in 5 seconds, None otherwise
    def findElemByID(self, ID):
        driver = self._driver
        delay = self._wait
        try:
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, ID)))
            return driver.find_element_by_id(ID)
        except:
            print('Could not find: ' + ID)
            return None
