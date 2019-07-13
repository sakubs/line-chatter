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


def main():
    # Variable assignments
    start_url = "http://sp.mojimaru.com/line/lineD.php?frame=line_long&backcolor=7292C1"
    avatar_img_path = "~/Desktop/car.jpg"
    friend_name = "バカ"
    img__sel_btn_id = "file1"
    name_input_name = "name"

    driver = connect_firefox_webdriver()
    driver.get(start_url)

    # First need to select the avatar for the user.
    select_el = get_form_elements_by_id(driver, img__sel_btn_id)

    # Un-hide the file upload button before we can use it
    driver.execute_script("arguments[0].style.display = 'block';", select_el)

    # Now we can send it our avatar
    select_el.send_keys(avatar_img_path)

    # Next we have to enter a name.
    name_input_el = get_form_elements_by_name(driver, name_input_name)
    driver.execute_script("arguments[0].style.display = 'block';", name_input_el)
    name_input_el.send_keys(friend_name)

    # Next we have to select a round image avatar.
    driver.find_element_by_xpath('/html/body/section/div/div[2]/div/div/div/form/div[2]/div/label[2]').click()

    driver.find_element_by_xpath('//*[@id="checkimg"]').click()
    #driver.quit()


if __name__ == "__main__":
    main()