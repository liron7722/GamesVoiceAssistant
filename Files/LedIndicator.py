
class LedIndicator:
    _WebDriver = None

    def __init__(self, webDriver):
        self._WebDriver = webDriver

    def change_status(self, color):
        if color == "red":
            element = self._WebDriver._driver.find_element_by_id("led2")
            self._WebDriver._driver.execute_script("arguments[0].style.backgroundColor = 'red'", element)
            element = self._WebDriver._driver.find_element_by_id("led-indication")
            self._WebDriver._driver.execute_script("arguments[0].style.backgroundColor = 'red'", element)
        elif color == "green":
            element = self._WebDriver._driver.find_element_by_id("led2")
            self._WebDriver._driver.execute_script("arguments[0].style.backgroundColor = 'green'", element)
            element = self._WebDriver._driver.find_element_by_id("led-indication")
            self._WebDriver._driver.execute_script("arguments[0].style.backgroundColor = 'green'", element)
        elif color == "orange":
            element = self._WebDriver._driver.find_element_by_id("led2")
            self._WebDriver._driver.execute_script("arguments[0].style.backgroundColor = 'orange'", element)
            element = self._WebDriver._driver.find_element_by_id("led-indication")
            self._WebDriver._driver.execute_script("arguments[0].style.backgroundColor = 'orange'", element)
        elif color == "yellow":
            element = self._WebDriver._driver.find_element_by_id("led2")
            self._WebDriver._driver.execute_script("arguments[0].style.backgroundColor = 'yellow'", element)
            element = self._WebDriver._driver.find_element_by_id("led-indication")
            self._WebDriver._driver.execute_script("arguments[0].style.backgroundColor = 'yellow'", element)
        elif color == "blue":
            element = self._WebDriver._driver.find_element_by_id("led2")
            self._WebDriver._driver.execute_script("arguments[0].style.backgroundColor = 'blue'", element)
            element = self._WebDriver._driver.find_element_by_id("led-indication")
            self._WebDriver._driver.execute_script("arguments[0].style.backgroundColor = 'blue'", element)
        else:
            print("The color entered indicates nothing")
