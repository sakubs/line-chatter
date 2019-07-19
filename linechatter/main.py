# -*- coding: utf-8 -*-
import sys
import time
import os
import flask
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

"""
Where this script is executing from.
"""
basedir = os.path.abspath(os.path.dirname(__file__))

"""
A_LITTLE_LATER:
    Code meaning, combine 'ーーー' with the following line and send as one message
"""
A_LITTLE_LATER = 1

"""
INSERT_PIC:
    Code meaning, send a picture message
"""
INSERT_PIC = 2


def connectChrome():
    """
    This function will setup and create a Chrome webbrowser driver.

    :return: webdriver.Crome object
    """
    options = ChromeOptions()
    chromeDriverPath = "/usr/bin/chromedriver"
    driver = webdriver.Chrome(chromeDriverPath, chrome_options=options)
    return driver


def connect_firefox_webdriver():
    """
    This function will setup and create a Firefox webbrowser driver.

    :return: webdriver.Firefox object
    """
    options = FirefoxOptions()
    driver = webdriver.Firefox(options=options)
    print("Firefox Headless Browser Invoked")
    return driver


def get_form_elements_by_id(driver, elemid):
    """
    Wrapper for find_element_by_id function from webdriver.
    :param driver:
    :param elemid:
    :return: if found, it returns the element object.
    """
    elem = driver.find_element_by_id(elemid)
    return elem


def get_form_elements_by_name(driver, elemname):
    """
    Wrapper for find_element_by_name function from webdriver.

    :param driver:
    :param elemname:
    :return: if found, it returns the element object.
    """
    elem = driver.find_element_by_name(elemname)
    return elem


def get_form_elements_by_xpath(driver, elemxpath):
    """
    Wrapper for find_element_by_xpath function from webdriver.
    :param driver:
    :param elemxpath:
    :return: if found, it returns the element object.
    """
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
    press_up(actions, m)


def insert_every_n(raw_string, group=13, char='\n'):
    return char.join(raw_string[i:i+group] for i in range(0, len(raw_string), group))


def check_input_codes(msg):
    """
    Checks for codes in the input

    :param msg:
    :return:
        - 0 for no codes
        - A_LITTLE_LATER
    """
    if str(msg) == "ーーー":
        return A_LITTLE_LATER
    else:
        return 0


def main():
    """
    """
    print(basedir)
    # Variable assignments
    start_url = "http://sp.mojimaru.com/line/lineD.php?frame=line_long&backcolor=7292C1"
    avatar_img_path = os.path.join(basedir, "resources/profile.jpg")

    try:
        friend_name = sys.argv[1]
    except IndexError:
        print("you forgot to enter a name for the chat.")
        return

    img_sel_btn_id = "file1"
    name_input_name = "name"
    script_fpath = os.path.join(basedir, "resources/script.txt")
    person_sel_xp = '//*[@id="create hidden"]/div/div/div[1]/form[1]/div[1]/select'
    comment_xp = "/html/body/section/div/div/div[2]/div/div[2]/div/div/div/div[1]/form[1]/div[2]/textarea"
    time_xp = "/html/body/section/div/div/div[2]/div/div[2]/div/div/div/div[1]/form[1]/div[7]/input"

    # Need to convert from nasty docx to txt to process
    driver = connect_firefox_webdriver()
    fill_linechat_form1(driver, start_url, img_sel_btn_id, avatar_img_path, name_input_name, friend_name)

    # Next page, we enter the actual chat.

    # Read the script
    writable_lines = get_writable_lines(script_fpath)

    # This variable is a placeholder for when codes require combining lines together.
    msg_before = ""
    flag_set = None

    for line in writable_lines:

        hour = int(line[1][:2])
        minutes = int(line[1][3:5])
        raw_msg = line[2].strip()
        msg = set_line_len(raw_msg)

        if flag_set == A_LITTLE_LATER:
            new_msg = [msg_before, msg]
            msg = '\n'.join(new_msg)
            flag_set = None
            print("Combined Message: {}".format(msg))

        input_code = check_input_codes(msg)
        if input_code > 0:
            if input_code == A_LITTLE_LATER:
                msg_before = msg
                flag_set = A_LITTLE_LATER
                continue
        print('Raw Line: {}'.format(line))

        try:
            # A is other person, default is opponent.
            select_sender(driver, line, person_sel_xp)
            time.sleep(1)

            # Add the comment
            post_msg(comment_xp, driver, msg)
            time.sleep(1)

            # Uncheck auto line lengthbox
            len_box = get_form_elements_by_xpath(driver, '//*[@id="create hidden"]/div/div/div[1]/form[1]/div[9]/div/div/label/input').click()
            time.sleep(1)

            # Need to calculate time via keystrokes from 10:00 AM
            set_msg_time(driver, hour, minutes, msg, time_xp)
            time.sleep(1)

            get_form_elements_by_id(driver, "checkimg").click()
        except NoSuchElementException:
            print('Problem found at: {}'.format(msg))
            print('check page loaded properly')
            driver.implicitly_wait(10)

    get_form_elements_by_xpath(driver, "/html/body/section/div/div/div[2]/div/div[2]/div/div/div/div[1]/form[2]/button").click()

        #driver.quit()


def set_line_len(raw_msg):
    msg = ""
    if len(raw_msg) > 13:
        msg = insert_every_n(raw_msg)
    else:
        msg = raw_msg
    return msg


def post_msg(comment_xp, driver, msg):
    comment_el = get_form_elements_by_xpath(driver, comment_xp)
    comment_el.send_keys(msg)


def set_msg_time(driver, hour, minutes, msg, time_xp):
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


def select_sender(driver, line, person_sel_xp):
    if line[0] == 'A':
        person_sel = driver.find_element_by_xpath(person_sel_xp)
        elem = Select(person_sel)
        elem.select_by_value('you')

    else:
        person_sel = driver.find_element_by_xpath(person_sel_xp)
        elem = Select(person_sel)
        elem.select_by_value('me')


if __name__ == "__main__":
    main()
