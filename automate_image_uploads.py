from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from random import random
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
from shutil import copyfile
import re
import sys

def kill_session():
    #assuming we are logged in
    driver.get('https://www.redbubble.com/auth/logout?ref=account-nav-dropdown')
    logging_out_button = driver.find_element(By.XPATH,'//*[@id="logout-form"]/form/input[3]')
    logging_out_button.click()
    driver.quit()
    # close the program
    sys.exit()

def get_tags_as_single_string(path):
    f = open(path, "r")
    temp = f.readlines()
    words = []
    while len(words) < 50 and len(temp) != 0:
        value = temp.pop(int(random() * len(temp)))
        words.append(value.split("\n")[0])
    final_string = ", ".join(words)
    return final_string

def get_desc_as_single_string(path):
    f = open(path, "r")
    final_string = f.read()
    return final_string


image_directory_plus_file_excluding_file_type = "D:/python_projects/create_svg_based_designs/png/"
image_directory_text = "D:/python_projects/create_svg_based_designs/text_tags/"
image_directory_desc = "D:/python_projects/create_svg_based_designs/text_desc/"
path_images_uploaded = "D:/python_projects/create_svg_based_designs/send_to_redbubble/"
'''
creating directories
'''
for _ in [image_directory_plus_file_excluding_file_type, image_directory_text, path_images_uploaded, image_directory_desc]:
    if not os.path.isdir(_):
        os.mkdir(_)
'''
starting up core driver settings
'''
chrome_options = Options()
chrome_options.add_argument('--deny-permission-prompts')
chrome_options.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])
driver = webdriver.Chrome(options=chrome_options,  executable_path=ChromeDriverManager().install())
driver.get("https://www.redbubble.com/")
login_button = driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/div/div[2]/div/div/div/header/div[1]/a[2]')
login_button.click()

'''
this part wait for you to login
'''

# login and check the boxes to prove you are not a bot
print("stop")
flag = True
while(flag):
    try:
        driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/div/div[2]/div/div/div/header/div[3]/div[1]/div/div/div/div[1]/div/div/div/button')
        break
    except Exception as e:
        print("not logged in yet")
        time.sleep(2)

    # creating directory to hold files we have uploaded


set_of_files = set()
files_list = os.listdir(path_images_uploaded)
for file in files_list:
    id = re.split("\.", file)[0]
    set_of_files.add(id)


counter = 0
list_of_files = os.listdir(image_directory_plus_file_excluding_file_type)
for index in range(0 ,len(list_of_files)):
    file_with_ending = list_of_files[index]

    file_stripped = re.split("\.", file_with_ending)[0]
    if file_stripped in set_of_files:
        continue

    # checking if tag files have been made for this
    text_for_tags = None
    while (True):
        try:
            path = image_directory_text + file_stripped + ".txt"
            text_for_tags = get_tags_as_single_string(path=path)
            break
        except Exception as e:
            print(e, "text for tag file has not been created yet and so are are waiting")
            time.sleep(60)
    # checking if tag files have been made for this


    # checking if desc files have been made for this
    text_for_desc = None
    try:
        path = image_directory_desc + file_stripped + ".txt"
        text_for_desc = get_desc_as_single_string(path=path)
    except Exception as e:
        print(e, "text file for desc has not been created")
    # checking if desc files have been made for this

    file = file_stripped+'.png'
    flag = True
    while(flag):

            counter += 1

            if counter > 60:
                # redbubble has a limit of 60 works per day - if we have gone pass that sign out and exit page
                kill_session()
            try:
                # after login
                driver.get('https://www.redbubble.com/portfolio/images/new')
                # this is so the leaving page popup is disabled
                driver.execute_script("window.onbeforeunload = function() {};")
                # uploading_an_image
                time.sleep(10)
                find_image_button = driver.find_element(By.XPATH,'//*[@id="select-image-single"]')
                find_image_button.send_keys(image_directory_plus_file_excluding_file_type+file)

                time.sleep(5)
                '''
                setting name/tag/desc
                '''
                name_of_work_text_box = driver.find_element(By.XPATH,'//*[@id="work_title_en"]')
                name_of_work = file_stripped
                name_of_work_text_box.send_keys(name_of_work)
                time.sleep(0.5)
                tag_text = driver.find_element(By.XPATH,'//*[@id="work_tag_field_en"]')

                tag_text.send_keys(text_for_tags)
                time.sleep(0.5)
                description_text = driver.find_element(By.XPATH,'//*[@id="work_description_en"]')
                # if no file can be found for a desc then default will be given
                if text_for_desc == None:
                    extra = "Desc"
                else:
                    extra = text_for_desc
                description_text.send_keys(extra)

                time.sleep(1)
                '''
                make graphic t-shirt default
                '''
                clicking_graphic_T_shirt_as_main_item = driver.find_element(By.XPATH,'//*[@id="work_default_product"]/option[30]')
                clicking_graphic_T_shirt_as_main_item.click()

                time.sleep(0.5)

                check_box_photography = driver.find_element(By.XPATH,'//*[@id="media_photography"]')
                check_box_photography.click()

                time.sleep(0.5)

                check_box_dig_art = driver.find_element(By.XPATH,'//*[@id="media_digital"]')
                check_box_dig_art.click()

                time.sleep(0.5)

                ratio_button_no_adult = driver.find_element(By.XPATH,'//*[@id="work_safe_for_work_true"]')
                ratio_button_no_adult.click()

                time.sleep(0.5)

                check_box_have_rights = driver.find_element(By.XPATH,'//*[@id="rightsDeclaration"]')
                check_box_have_rights.click()

                time.sleep(2)
                flag_1 = True
                while(flag_1):
                    progress_bar = driver.find_element(By.XPATH,'//*[@id="add-new-work"]/div/div[1]/div[1]/div[1]')
                    time.sleep(20)
                    progress_bar_value = int(progress_bar.get_attribute("data-value"))
                    if (progress_bar_value == 100 or progress_bar_value == 0):
                        break

                # selecting work that will be available to sell
                flag_2 = True
                time.sleep(10)
                while(flag_2):
                    try:
                        buttons = driver.find_elements_by_xpath('//div[contains(@class,"rb-button enable-all")]')
                        for button in buttons:
                            try:
                                button.click()
                            except Exception as e:
                                print("already had been pressed")
                            time.sleep(0.5)
                        time.sleep(2)
                        break
                    except Exception as e:
                        print('error in making work available')
                        break
                '''
                submitting work
                '''
                flag_3 = True
                while(flag_3):
                    try:
                        submit_button_work = driver.find_element(By.XPATH,'//*[@id="submit-work"]')
                        submit_button_work.click()
                        time.sleep(2)
                    except Exception as e:
                        print('sumbmit button has been pressed')
                        break

                manage_your_work_button = None

                time.sleep(30)

                flag_4 = True
                while(flag_4):
                    try:
                        manage_your_work_button = driver.find_element(By.XPATH,'//*[@id="app"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[1]/a/p')
                        break
                    except Exception as e:
                        print("item not found yet")
                        '''
                        working with error whilst uploading, if error is too big retry upload from start
                        '''
                        try:
                            element_for_server_error_500 = driver.find_element(By.XPATH, '//*[@id="wrap"]/h1')
                            message = element_for_server_error_500.text
                            if "Computer says 'No'." in message:
                                print("we have been signed out or the page has crashed")
                                driver.get("https://www.redbubble.com/")
                                driver.get("https://www.redbubble.com/portfolio/images")
                                break
                        except Exception as e:
                            print(e, " this means the we are still waiting for the work to be uploaded")


                        time.sleep(2)
                try:
                    manage_your_work_button.click()
                    '''
                    copy work into send folder
                    '''
                    src = image_directory_plus_file_excluding_file_type + file
                    dst = path_images_uploaded + file
                    copyfile(src, dst)


                    break
                except Exception as e:
                    print("exception")
            except Exception as e:
                # kill_session()
                print(e, "try task again")
                counter -= 1



kill_session()


