from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

print("\nWelcome to lets_go_monitor.py\n\nThis program will monitor your favourite facebook group chat to ensure you are always up for a night out even if you haven't seen the invite yet. The chat will be initially checked and if the program is left running it will continue to monitor the chat\n\nPrerequesits:\n You must have chromedriver installed on your computer (search chromedriver on google)\n You must have selenium installed (pip install selenium)\n")

chromedriver_path = input("Enter the path to your chromedriver.exe file: ")
email = input("Enter the email of your Facebook account: ")
password = input("Enter the password of your Facebook account: ")
group_chat_name = input("Enter the name of your group chat: ")

driver_options = webdriver.ChromeOptions()
preferences = {"profile.default_content_setting_values.notifications" : 2}
driver_options.add_experimental_option("prefs", preferences)

driver = webdriver.Chrome(chromedriver_path, options=driver_options)
driver.implicitly_wait(10)
driver.maximize_window()
driver.get('http://facebook.com')

email_box = driver.find_element_by_xpath('//input[@name = "email"]')
email_box.send_keys(email)

password_box = driver.find_element_by_xpath('//input[@name = "pass"]')
password_box.send_keys(password)

login_button = driver.find_element_by_xpath('//input[@value = "Log In"]')
login_button.click()

messenger_button = WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.XPATH, '//a[@class = "jewelButton _3eo8"]')))
messenger_button.click()

open_messenger_button = WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.XPATH, '//a[@class = "_4djt"]')))
open_messenger_button.click()

groups_search = WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.XPATH, '//input[@class = "_58al _7tpc"]')))
groups_search.send_keys(group_chat_name)

group_chat = WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, 'div._3q35')))
group_chat.click()

previous_nights_out = [' ']

while True:
    WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, 'div._aok._7i2m')))
    friends_messages = driver.find_elements_by_css_selector('div._aok._7i2m')

    for message in friends_messages:
        print(message.text)
        if ("night out" in message.text.lower()) and (message.text.lower() not in previous_nights_out):
            message.location_once_scrolled_into_view
            ActionChains(driver).move_to_element(message).perform()
            reply_button = WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.XPATH, '//span[@class = "_3-wv _7i2n"]')))
            reply_button.click()
            message_box = WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.XPATH, '//div[@role="combobox"]')))
            message_box.send_keys("LETS GOOOOOOOOOOOOOOOOO")
            send_button = WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.XPATH, '//a[@class = "_30yy _38lh _7kpi"]')))
            send_button.click()
            previous_nights_out.append(message.text.lower())
    time.sleep(15)
