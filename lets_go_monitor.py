from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

EMAIL_BOX_XPATH = '//input[@name = "email"]'
PASSWORD_BOX_XPATH = '//input[@name = "pass"]'
LOGIN_BUTTON_XPATH = '//input[@value = "Log In"]'
MESSENGER_BUTTON_XPATH = '//a[@class = "jewelButton _3eo8"]'
OPEN_MESSENGER_BUTTON_XPATH = '//a[@class = "_4djt"]'
GROUPS_SEARCH_XPATH = '//input[@class = "_58al _7tpc"]'
SEARCH_RESULTS_CSS_SELECTOR = 'div._29hk'
GROUP_CHAT_CSS_SELECTOR = 'div._3q35'
FRIENDS_MESSAGES_CSS_SELECTOR = 'div._aok._7i2m'
REPLY_BUTTON_XPATH = '//span[@class = "_3-wv _7i2n"]'
MESSAGE_BOX_XPATH = '//div[@role="combobox"]'
SEND_BUTTON_XPATH = '//a[@class = "_30yy _38lh _7kpi"]'
REPLY = "LETS GOOOOOOOOOOOOOOOOO"
OPENING_MESSAGE = "\nWelcome to lets_go_monitor.py\n\nThis program will monitor your favourite facebook group chat to ensure you are always up for a night out even if you haven't seen the invite yet. The chat will be initially checked and if the program is left running it will continue to monitor the chat\n\nPrerequesits:\n You must have chromedriver installed on your computer (search chromedriver on google)\n You must have selenium installed (pip install selenium)\n"
CHROMEDRIVER_PROMPT = "Enter the path to your chromedriver.exe file: "
EMAIL_PROMPT = "Enter the email of your Facebook account: "
PASSWORD_PROMPT = "Enter the password of your Facebook account: "
GROUP_NAME_PROMPT = "Enter the name of your group chat: "
FACEBOOK_LINK = 'http://facebook.com'
WAIT_FOR_SEARCH_RESULTS = 5
DURATION_BETWEEN_CHECKS = 15

def get_element_using_xpath(xpath):
    return WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.XPATH, xpath)))

def get_element_using_css_selector(css_selector):
    return WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, css_selector)))

def log_in(email, password):
    email_box = get_element_using_xpath(EMAIL_BOX_XPATH)
    email_box.send_keys(email)

    password_box = get_element_using_xpath(PASSWORD_BOX_XPATH)
    password_box.send_keys(password)

    login_button = get_element_using_xpath(LOGIN_BUTTON_XPATH)
    login_button.click()

def find_group_chat(group_chat_name):
    messenger_button = get_element_using_xpath(MESSENGER_BUTTON_XPATH)
    messenger_button.click()

    open_messenger_button = get_element_using_xpath(OPEN_MESSENGER_BUTTON_XPATH)
    open_messenger_button.click()

    groups_search = get_element_using_xpath(GROUPS_SEARCH_XPATH)
    groups_search.send_keys(group_chat_name)

    time.sleep(WAIT_FOR_SEARCH_RESULTS)
    get_element_using_css_selector(SEARCH_RESULTS_CSS_SELECTOR)
    search_results = driver.find_elements_by_css_selector(SEARCH_RESULTS_CSS_SELECTOR)

    group_chat = search_results[2].find_element_by_css_selector(GROUP_CHAT_CSS_SELECTOR)
    group_chat.click()

def check_messages():
    previous_nights_out = [' ']
    while True:
        get_element_using_css_selector(FRIENDS_MESSAGES_CSS_SELECTOR)
        friends_messages = driver.find_elements_by_css_selector(FRIENDS_MESSAGES_CSS_SELECTOR)

        for message in friends_messages:
            print(message.text)
            message_text = message.text.lower()
            if ("night out" in message_text) and (message_text not in previous_nights_out):
                reply_to(message)
                previous_nights_out.append(message_text)
        time.sleep(DURATION_BETWEEN_CHECKS)

def reply_to(message):
    message.location_once_scrolled_into_view
    ActionChains(driver).move_to_element(message).perform()
    reply_button = get_element_using_xpath(REPLY_BUTTON_XPATH)
    reply_button.click()
    message_box = get_element_using_xpath(MESSAGE_BOX_XPATH)
    message_box.send_keys(REPLY)
    send_button = get_element_using_xpath(SEND_BUTTON_XPATH)
    send_button.click()


print(OPENING_MESSAGE)

chromedriver_path = input(CHROMEDRIVER_PROMPT)
email = input(EMAIL_PROMPT)
password = input(PASSWORD_PROMPT)
group_chat_name = input(GROUP_NAME_PROMPT)

driver_options = webdriver.ChromeOptions()
preferences = {"profile.default_content_setting_values.notifications" : 2}
driver_options.add_experimental_option("prefs", preferences)

driver = webdriver.Chrome(chromedriver_path, options=driver_options)
driver.maximize_window()
driver.get(FACEBOOK_LINK)

log_in(email, password)

find_group_chat(group_chat_name)

check_messages()
