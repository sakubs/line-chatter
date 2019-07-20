# -*- coding: utf-8 -*-
import os
import shutil
import sys
import time

import urllib3
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import Select

"""
Where this script is executing from.
"""
BASEDIR = os.path.abspath(os.path.dirname(__file__))

"""
A_LITTLE_LATER:
    Code meaning, combine 'ーーー' with the following line and send as one message
"""
A_LITTLE_LATER = '数時間後'

"""
INSERT_PIC:
    Code meaning, send a picture message
"""
INSERT_PIC = 2


CLOSING = 3

TRIPLE_HYPHEN = "ーーー"
RIGHT_PERS = 'B'
LEFT_PERS = 'A'
SONO_GOU = 'その後'
MISSED_CALL = '不在着信'
MIDNIGHT = '00:00'

img_sel_btn_id = "file1"
name_input_name = "name"
PERSON_SEL_XPATH = '//*[@id="create hidden"]/div/div/div[1]/form[1]/div[1]/select'
comment_xp = "/html/body/section/div/div/div[2]/div/div[2]/div/div/div/div[1]/form[1]/div[2]/textarea"
TIME_SEL_XPATH = "/html/body/section/div/div/div[2]/div/div[2]/div/div/div/div[1]/form[1]/div[7]/input"


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


def check_input_codes(input_line):
    """
    Checks for codes in the input

    :param msg:
    :return:
        - 0 for no codes
        - A_LITTLE_LATER
    """
    # if the length is not three, we know it is not a typical input
    if len(input_line) < 3:
        if str(input_line[0]) == TRIPLE_HYPHEN:
            return A_LITTLE_LATER
        elif str(input_line[0]) == SONO_GOU:
            return 0
    else:
        return 0


def is_line_msg(line):
    if line_startswith(line, LEFT_PERS):
        return True
    elif line_startswith(line, RIGHT_PERS):
        return True
    else:
        return False


def line_startswith(line, cmpstr):
    if line[0].strip().startswith(cmpstr):
        return True
    else:
        return False


def select_sender(driver, line):

    if line[0].strip() == LEFT_PERS:
        person_sel = driver.find_element_by_xpath(PERSON_SEL_XPATH)
        driver.execute_script("arguments[0].style.display = 'block';", person_sel)
        elem = Select(person_sel)
        elem.select_by_value('you')

    else:
        person_sel = driver.find_element_by_xpath(PERSON_SEL_XPATH)
        driver.execute_script("arguments[0].style.display = 'block';", person_sel)
        elem = Select(person_sel)
        elem.select_by_value('me')


def set_line_len(raw_msg):
    msg = ""
    if len(raw_msg) > 13:
        msg = insert_every_n(raw_msg)
    else:
        msg = raw_msg
    return msg


def set_msg_time(driver, line):
    print(line)
    actions = ActionChains(driver)
    get_form_elements_by_xpath(driver, TIME_SEL_XPATH).click()
    # Set hour
    hour = int(line[1][:2])
    set_hours(actions, hour)

    # Move to minutes field.
    press_tab(actions, 1)
    minutes = int(line[1][3:5].strip())
    set_minutes(actions, minutes)

    # Set AM/PM
    if hour > 12:
        press_tab(actions, 1)
        press_down(actions, 1)
    actions.perform()


def display_missed_call(driver):
    mc_btn_xpath = '/html/body/section/div/div/div[2]/div/div[2]/div/div/div/div[1]/form[1]/div[5]/div/div[1]/button'
    get_form_elements_by_xpath(driver, mc_btn_xpath).click()
    phone_txt_xpath = '/html/body/section/div/div/div[2]/div/div[2]/div/div/div/div[1]/form[1]/div[6]/input'
    phone_txt = get_form_elements_by_xpath(driver, phone_txt_xpath)
    phone_txt.send_keys(MISSED_CALL)
    return


def message_send(driver):
    get_form_elements_by_id(driver, "checkimg").click()
    return


def click_complete(driver):
    get_form_elements_by_xpath(
        driver,
        "/html/body/section/div/div/div[2]/div/div[2]/div/div/div/div[1]/form[2]/button").click()
    return


def download_chat_image(driver):
    final_img = driver.find_element_by_xpath('//*[@id="saveimg"]')
    src = final_img.get_attribute('src')
    http = urllib3.PoolManager()
    with http.request('GET', src, preload_content=False) as r, open('chatout.jpg', 'wb') as out_file:
        shutil.copyfileobj(r, out_file)


def send_regular_message(driver, line):
    # Uncheck auto line lengthbox
    get_form_elements_by_xpath(
        driver,
        '//*[@id="create hidden"]/div/div/div[1]/form[1]/div[9]/div/div/label/input').click()
    select_sender(driver, line)
    set_msg_time(driver, line)
    msg = set_line_len(line[2].strip())
    post_msg(driver, msg)
    return


def post_msg(driver, msg):
    comment_el = get_form_elements_by_xpath(driver, comment_xp)
    comment_el.send_keys(msg)
    return


def main():
    """
    """
    # Variable assignments
    start_url = "http://sp.mojimaru.com/line/lineD.php?frame=line_long&backcolor=7292C1"
    avatar_img_path = os.path.join(BASEDIR, "resources/profile.jpg")

    try:
        friend_name = sys.argv[1]
    except IndexError:
        print("you forgot to enter a name for the chat.")
        return

    # Load firefox and fill out chat start form.
    driver = connect_firefox_webdriver()
    fill_linechat_form1(driver, start_url, img_sel_btn_id, avatar_img_path, name_input_name, friend_name)

    # Read the script
    script_fpath = os.path.join(BASEDIR, "resources/script.txt")
    raw_lines = get_writable_lines(script_fpath)
    script_lines = len(raw_lines)
    current_line = 0

    # The script contains certain codes for special cases. Using a while loop allows reformatting message lines
    # and sending them back up to this first message sending case.
    while current_line < script_lines:
        # Magic number to wait for page load without issues.
        time.sleep(5)
        print(raw_lines[current_line])
        print("Processing line {} of {}".format(current_line, script_lines))
        time_left = (script_lines - current_line) * 5
        print("Approximate time to completion: {} seconds".format(time_left))

        # Check for regular message line
        if is_line_msg(raw_lines[current_line]):
            # Look for missed call message
            if MISSED_CALL in raw_lines[current_line][2]:

                # Send as a missed call instead of text
                display_missed_call(driver)
                set_msg_time(driver, raw_lines[current_line])
                message_send(driver)
                current_line += 1
                continue

            # Send regular text
            send_regular_message(driver, raw_lines[current_line])

            # Click send.
            message_send(driver)
            current_line += 1

        elif line_startswith(raw_lines[current_line], TRIPLE_HYPHEN):
            # Combine this line with the next line into one message posted by right person at 10:00
            # Everything after this is closing. Right person at 10:00
            newline = [
                RIGHT_PERS,
                '10:00',
                '\n'.join([raw_lines[current_line][0].strip(), raw_lines[current_line + 1][0].strip()])]
            raw_lines[current_line + 1] = newline

            # Increment to pass over the next line
            current_line += 1

        elif A_LITTLE_LATER in raw_lines[current_line][0]:
            # Look out for a little later message, modify message but don't increment counter.
            newline = [
                RIGHT_PERS,
                MIDNIGHT,
                raw_lines[current_line][0].strip()]
            raw_lines[current_line] = newline

        else:
            # If this case is found, must be a closing message, modify the message but don't increment
            newline = [
                RIGHT_PERS,
                '10:00',
                raw_lines[current_line][0].strip()
            ]
            raw_lines[current_line] = newline

    click_complete(driver)
    download_chat_image(driver)
    print("Done")


if __name__ == "__main__":
    main()
