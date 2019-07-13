from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions

def connectChrome():
    """
    This function will setup and create a Chrome webbrowser driver.

    :return: webdriver.Crome object
    """
    options = ChromeOptions()
    options.add_argument("--headless")
    chromeDriverPath = "/usr/bin/chromedriver"
    driver = webdriver.Chrome(chromeDriverPath, chrome_options=options)
    return driver


def connect_firefox_webdriver():
    """
    This function will setup and create a Firefox webbrowser driver.

    :return: webdriver.Firefox object
    """
    options = FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(firefox_options=options)
    print("Firefox Headless Browser Invoked")
    return driver


def get_form_elements_by_id(driver, elemid):
    elem = driver.find_element_by_id(elemid)
    return elem


def get_form_elements_by_name(driver, elemname):
    elem = driver.find_element_by_name(elemname)
    return elem


def get_form_elements_by_xpath(driver, elemxpath):
    elem = driver.find_element_by_xpath(elemxpath)
    return elem