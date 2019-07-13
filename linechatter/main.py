# -*- coding: utf-8 -*-
import os
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


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


def fill_linechat_form1(driver, start_url, img_sel_btn_id, avatar_img_path, name_input_name, friend_name):
    driver.get(start_url)

    # First need to select the avatar for the user.
    select = get_form_elements_by_id(driver, img_sel_btn_id)

    # Un-hide the file upload button before we can use it
    driver.execute_script("arguments[0].style.display = 'block';", select)

    # Now we can send it our avatar
    select.send_keys(avatar_img_path)

    # Next we have to enter a name.
    name_input = get_form_elements_by_name(driver, name_input_name)
    driver.execute_script("arguments[0].style.display = 'block';", name_input)
    name_input.send_keys(friend_name)

    # Next we have to select a round image avatar.
    get_form_elements_by_xpath(driver, '/html/body/section/div/div[2]/div/div/div/form/div[2]/div/label[2]').click()

    # And finally, submit
    get_form_elements_by_xpath(driver, '//*[@id="checkimg"]').click()


def get_writable_lines(script_fpath):
    with open(script_fpath, "r") as raw:
        chatlines = raw.readlines()

    writable_lines = []
    for line in chatlines:
        cooked = line.split(" ")
        writable_lines.append(cooked)

    return writable_lines


def main():
    # Variable assignments
    start_url = "http://sp.mojimaru.com/line/lineD.php?frame=line_long&backcolor=7292C1"
    avatar_img_path = "~/Desktop/car.jpg"
    friend_name = "バカ"
    img_sel_btn_id = "file1"
    name_input_name = "name"
    script_fpath = "script"
    person_sel_xp = "/html/body/section/div/div/div[2]/div/div[2]/div/div/div/div[1]/form[1]/div[1]/select"
    comment_xp = "/html/body/section/div/div/div[2]/div/div[2]/div/div/div/div[1]/form[1]/div[2]/textarea"
    time_xp = "/html/body/section/div/div/div[2]/div/div[2]/div/div/div/div[1]/form[1]/div[7]/input"

    driver = connect_firefox_webdriver()
    fill_linechat_form1(driver, start_url, img_sel_btn_id, avatar_img_path, name_input_name, friend_name)

    # Next page, we enter the actual chat.
    print(driver.current_url)

    # Read the script
    writable_lines = get_writable_lines(script_fpath)

    print(writable_lines)
    #for line in writable_lines:
    line = writable_lines[0]
    print(line)
    person_sel = get_form_elements_by_xpath(driver, person_sel_xp)
    person_sel_el = Select(person_sel)

    # A is other person, default is opponent.
    if [line[0] == 'B']:
        person_sel_el.select_by_value('me')

    # Add the comment
    comment_el = get_form_elements_by_xpath(driver, comment_xp)
    comment_el.send_keys(line[2])

    # Set time default time is 10:00 AM
    actions = ActionChains(driver)
    time_el = get_form_elements_by_xpath(driver, time_xp).click()
    actions.send_keys(Keys.ARROW_DOWN*4)
    actions.send_keys(Keys.TAB)
    actions.send_keys(Keys.ARROW_DOWN*2)
    actions.send_keys(Keys.TAB*2)
    actions.perform()
    # process the time for entering into the field.

    submit_btn = get_form_elements_by_id(driver, "checkimg").click()
    #driver.implicitly_wait(10)
    #driver.quit()

if __name__ == "__main__":
    main()
