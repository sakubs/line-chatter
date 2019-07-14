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


def get_form_elements_by_xpath(driver: object, elemxpath: object) -> object:
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


def press_down(actions, n):
    actions.send_keys(Keys.ARROW_DOWN * n)


def press_up(actions, n):
    actions.send_keys(Keys.ARROW_UP * n)


def press_tab(actions, n):
    actions.send_keys(Keys.TAB * n)


def set_hours(actions, h):
    if h < 13:
        press_down(actions, 10 - (h - 12))

    elif h > 10:
        press_up(actions, h - 10)

    elif h < 9:
        press_down(actions, 10 - h)


def set_minutes(actions, m):
    if m <= 30:
        press_up(actions, m)
    elif m > 30:
        press_down(actions, m)


def main():
    # Variable assignments
    start_url = "http://sp.mojimaru.com/line/lineD.php?frame=line_long&backcolor=7292C1"
    avatar_img_path = "~/Desktop/car.jpg"
    friend_name = "バカ"
    img_sel_btn_id = "file1"
    name_input_name = "name"
    script_fpath = "script.txt"
    person_sel_xp = "/html/body/section/div/div/div[2]/div/div[2]/div/div/div/div[1]/form[1]/div[1]/select"
    comment_xp = "/html/body/section/div/div/div[2]/div/div[2]/div/div/div/div[1]/form[1]/div[2]/textarea"
    time_xp = "/html/body/section/div/div/div[2]/div/div[2]/div/div/div/div[1]/form[1]/div[7]/input"

    # Need to convert from nasty docx to txt to process
    driver = connect_firefox_webdriver()
    fill_linechat_form1(driver, start_url, img_sel_btn_id, avatar_img_path, name_input_name, friend_name)

    # Next page, we enter the actual chat.

    # Read the script
    writable_lines = get_writable_lines(script_fpath)

    for line in writable_lines:

        hour = int(line[1][:2])
        minutes = int(line[1][3:5])
        msg = line[2]

        # A is other person, default is opponent.
        if line[0] == "Ｂ":
            person_sel = driver.find_element_by_xpath(person_sel_xp)
            elem = Select(person_sel)
            elem.select_by_value('me')

        # Add the comment
        comment_el = get_form_elements_by_xpath(driver, comment_xp)
        comment_el.send_keys(msg)

        # Need to calculate time via keystrokes from 10:00 AM
        actions = ActionChains(driver)
        get_form_elements_by_xpath(driver, time_xp).click()

        # Set hour
        set_hours(actions, hour)

        # Move to minutes field.
        press_tab(actions, 1)
        set_minutes(actions, minutes)

        # Set AM/PM
        if hour > 12:
            press_tab(actions, 1)
            press_down(actions, 1)

        actions.perform()

        get_form_elements_by_id(driver, "checkimg").click()
        time.sleep(3)

    get_form_elements_by_xpath(driver, "/html/body/section/div/div/div[2]/div/div[2]/div/div/div/div[1]/form[2]/button").click()
        #driver.implicitly_wait(10)
        #driver.quit()


if __name__ == "__main__":
    main()
