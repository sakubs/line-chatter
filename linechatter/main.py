# -*- coding: utf-8 -*-
import os
import sys
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from linechatter.constants import A_LITTLE_LATER
from linechatter.constants import BASEDIR
from linechatter.constants import IMG_SEL_BTN_ID
from linechatter.constants import MIDNIGHT
from linechatter.constants import MISSED_CALL
from linechatter.constants import NAME_INPUTBOX_NAME
from linechatter.constants import RIGHT_PERS
from linechatter.constants import TRIPLE_HYPHEN
from linechatter.formio import click_complete
from linechatter.formio import display_missed_call
from linechatter.formio import download_chat_image
from linechatter.formio import fill_linechat_form1
from linechatter.formio import message_send
from linechatter.formio import send_regular_message
from linechatter.formio import set_msg_time
from linechatter.ioformat import is_line_msg
from linechatter.ioformat import line_startswith


def connect_firefox_webdriver():
    """
    This function will setup and create a Firefox webbrowser driver.

    :return: webdriver.Firefox object
    """
    options = FirefoxOptions()
    driver = webdriver.Firefox(options=options)
    print("Firefox Headless Browser Invoked")
    return driver


def get_writable_lines(script_fpath):
    with open(script_fpath, "r") as raw:
        chatlines = raw.readlines()

    writable_lines = []
    for line in chatlines:
        cooked = line.split(" ")
        writable_lines.append(cooked)

    return writable_lines


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
    fill_linechat_form1(driver, start_url, IMG_SEL_BTN_ID, avatar_img_path, NAME_INPUTBOX_NAME, friend_name)

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
