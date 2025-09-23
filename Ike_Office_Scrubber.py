from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time


service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)
actions = ActionChains(driver)

print("START")

driver.get("https://office.ikegps.com/#/login")

# Login credentials
username = "edward.biggs@rivercityinc.net"
password = "k5c8QUQSc6*DtcMG"

# Project to be sorted
target = "wwk-pry"

# Click Login button
WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    (By.CLASS_NAME, "mdl-button--raised")))

login_button = driver.find_element(
    By.CLASS_NAME, "mdl-button--raised")

login_button.click()

# Insert username
username_input = driver.find_element(
    By.CLASS_NAME, "input")

username_input.send_keys(username + Keys.ENTER)


# Insert password
password_input = driver.find_element(
    By.NAME, "password")

password_input.send_keys(password + Keys.ENTER)

# Select Project
WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    (By.XPATH, "//span[@title='" + target + "']")))


project = driver.find_element(By.XPATH, "//span[@title='" + target + "']")

project.click()

actions.send_keys(Keys.TAB * 2)
actions.send_keys(Keys.ENTER)
actions.perform()


# Create list of pole IDs and sort in ascending order
WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    (By.CLASS_NAME, "c-CollectionCard__link")))


poles = driver.find_elements(By.CLASS_NAME, "c-CollectionCard__link")

pole_ids = [(id.get_attribute("title"), id) for id in poles]

# pole_ids.sort(key=lambda x: x[0])


# Iterate through poles, update status
for id in pole_ids:
    next_pole = driver.find_element(By.XPATH, "//span[@title='" + id[0] + "']")
    next_pole.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.CLASS_NAME, "c-MultiListInput__button")))

    # Check current status
    status_label = driver.find_element(
        By.CLASS_NAME, "c-MultiListInput__button")

    current_status = status_label.text
    print(current_status)

    if current_status.__contains__("Delivery") != True:
        # Click status bar
        status_bar = driver.find_element(
            By.CLASS_NAME, "c-MultiListInput__button")
        status_bar.click()

        # Generate a list of status'
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.CLASS_NAME, "c-MultiListChooser__groupSelect")))

        status_options = driver.find_elements(
            By.CLASS_NAME, "c-MultiListChooser__groupSelect")

        status_list = [(status.get_attribute("id"), status)
                       for status in status_options]

        # Select 'Delivery' status using index from status_list
        delivery = driver.find_element(
            By.XPATH, "//div[@id='" + status_list[12][0] + "']")

        delivery.click()

        # Select 'Ok' and save changes
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.CLASS_NAME, "c-Modal-Actions__Ok")))

        ok_button = driver.find_element(
            By.CLASS_NAME, "c-Modal-Actions__Ok")
        ok_button.click()

        actions.key_down(Keys.CONTROL).send_keys(
            "s").key_up(Keys.CONTROL).perform()

        time.sleep(2)


time.sleep(10)

print("FICNISH")
driver.quit()
