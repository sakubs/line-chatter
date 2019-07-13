from browser.webforms import connect_firefox_webdriver
from browser.webforms import get_form_elements_by_id as form_el_id
from browser.webforms import get_form_elements_by_name as form_el_name
from browser.webforms import get_form_elements_by_xpath as form_el_xp

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
    select_el = form_el_id(driver, img__sel_btn_id)

    # Un-hide the file upload button before we can use it
    driver.execute_script("arguments[0].style.display = 'block';", select_el)

    # Now we can send it our avatar
    select_el.send_keys(avatar_img_path)

    # Next we have to enter a name.
    name_input_el = form_el_name(driver, name_input_name)
    driver.execute_script("arguments[0].style.display = 'block';", name_input_el)
    name_input_el.send_keys(friend_name)

    # Next we have to select a round image avatar.
    driver.form_el_xp('/html/body/section/div/div[2]/div/div/div/form/div[2]/div/label[2]').click()

    driver.form_el_xp('//*[@id="checkimg"]').click()
    #driver.quit()


if __name__ == "__main__":
    main()