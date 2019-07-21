import shutil

import urllib3
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from linechatter.constants import COMMENT_INPUT_XP
from linechatter.constants import LEFT_PERS
from linechatter.constants import MISSED_CALL
from linechatter.constants import PERSON_SEL_XPATH
from linechatter.constants import TIME_SEL_XPATH
from linechatter.ioformat import set_line_len


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
    comment_el = get_form_elements_by_xpath(driver, COMMENT_INPUT_XP)
    comment_el.send_keys(msg)
    return
