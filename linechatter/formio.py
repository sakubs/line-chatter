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
