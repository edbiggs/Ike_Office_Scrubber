from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv
import os
import time


# ──────────────── Login credentials ────────────────
load_dotenv()
username = os.getenv("IKE_USERNAME")
password = os.getenv("IKE_PASSWORD")

# ──────────────── Project name being targeted ────────────────
target = os.getenv("JOB_NAME")


# ─── Configuration for check_for_empty_fields() function ────────────────
check_fields = [
    "pole_id",
    "pole_type",
    "tip",
    "latitude",
    "longtitude",
    "mf_hdw",
    "ms_height",
    "ms_clearance"
]

# Locators to identify elements on page
xpath_locators = {
    "pole_id": "//div[contains(@class,'c-Input--id') and contains(@class,'is-dirty')]"
    "//input",
    "pole_type": "//div[@title='Type']"
    "[not(ancestor::div[contains(@class,'c-SubFormInstance')])]"
    "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
    "//span[contains(@class,'c-MultiListInput__label')]",
    "tip": "//div[@title='Tip']"
    "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
    "//div[contains(@class,'c-Input--ft') and contains(@class,'is-dirty')]"
    "//input",
    "latitude": "//div[contains(@class,'c-Input--lat') and contains(@class,'is-dirty')]"
    "//input",
    "longtitude": "//div[contains(@class,'c-Input--lng') and contains(@class,'is-dirty')]"
    "//input",
    "mf_hdw": "//div[@title='M/F Hdw.']"
    "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
    "//div[contains(@class,'is-dirty')]"
    "//textarea",
    "ms_height": "//div[contains(@class,'c-SubFormInstance')]"
    "[.//span[contains(@class,'c-MultiListInput__label') and contains(text(),'Fiber')]]"
    "//div[@title='Mid Span Height']"
    "/following-sibling::div"
    "//div[contains(@class,'c-PMLink')]",
    "ms_clearance": "//div[contains(@class,'c-SubFormInstance')]"
    "[.//span[contains(@class,'c-MultiListInput__label') and contains(text(),'Fiber')]]"
    "//div[@title='MS Clearance ']"
    "/following-sibling::div"
    "//div[contains(@class,'c-PMLink')]"

}


# ChromeDriver and Selenium variables
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

actions = ActionChains(driver)


def check_for_empty_fields(id):

    missing = []

    try:
        pole_id = driver.find_element(
            By.XPATH,
            "//div[@title='ID']"
            "[not(ancestor::div[contains(@class,'c-SubFormInstance')])]"
            "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
            "//div[contains(@class,'is-dirty')]"
            "//textarea"
        ).get_attribute("value")
    except:
        pole_id = None
        missing.append("Pole ID")

    try:
        pole_type = driver.find_element(
            By.XPATH,
            "//div[@title='Type']"
            "[not(ancestor::div[contains(@class,'c-SubFormInstance')])]"
            "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
            "//span[contains(@class,'c-MultiListInput__label')]"
        ).text
    except:
        pole_type = None
        missing.append("Pole Type")

    try:
        tip = driver.find_element(
            By.XPATH,
            "//div[@title='Tip']"
            "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
            "//div[contains(@class,'c-Input--ft') and contains(@class,'is-dirty')]"
            "//input"
        ).get_attribute("value")
    except:
        tip = None
        missing.append("Tip")

    try:
        latitude = driver.find_element(
            By.XPATH,
            "//div[contains(@class,'c-Input--lat') and contains(@class,'is-dirty')]"
            "//input"
        ).get_attribute("value")
    except:
        latitude = None
        missing.append("Latitude")

    try:
        longitude = driver.find_element(
            By.XPATH,
            "//div[contains(@class,'c-Input--lng') and contains(@class,'is-dirty')]"
            "//input"
        ).get_attribute("value")
    except:
        longitude = None
        missing.append("Longitude")

    try:
        mf_hdw = driver.find_element(
            By.XPATH,
            "//div[@title='M/F Hdw.']"
            "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
            "//div[contains(@class,'is-dirty')]"
            "//textarea"
        ).get_attribute("value")
    except:
        mf_hdw = None
        missing.append("M/F Hdw.")

    try:
        ms_height = driver.find_element(
            By.XPATH,
            "//div[contains(@class,'c-SubFormInstance')]"
            "[.//span[contains(@class,'c-MultiListInput__label') and contains(text(),'Fiber')]]"
            "//div[@title='Mid Span Height']"
            "/following-sibling::div"
            "//div[contains(@class,'c-PMLink')]"
        ).text
    except:
        ms_height = None
        missing.append("Mid Span Height")

    try:
        ms_clearance = driver.find_element(
            By.XPATH,
            "//div[contains(@class,'c-SubFormInstance')]"
            "[.//span[contains(@class,'c-MultiListInput__label') and contains(text(),'Fiber')]]"
            "//div[@title='MS Clearance ']"
            "/following-sibling::div"
            "//div[contains(@class,'c-PMLink')]"
        ).text
    except:
        ms_clearance = None
        missing.append("MS Clearance")

    return missing


def debug(id):
    try:
        mf_hdw = driver.find_element(
            By.XPATH,
            "//div[@title='M/F Hdw.']"
            "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
            "//div[contains(@class,'is-dirty')]"
            "//textarea"
        ).get_attribute("value")
    except:
        mf_hdw = None
        print("M/F Hdw.")
    else:
        print(mf_hdw)


def generate_output(output_dict):
    for pole_id, fields in output_dict.items():
        print(f"{pole_id}:")
        for field in fields:
            print(f"{field}")
        print(" ")


# ────────────────────── Main Script ─────────────────────────

def main():

    print("START")

    driver.get("https://office.ikegps.com/#/login")

    # Locate and click Login button
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.CLASS_NAME, "mdl-button--raised")))

    login_button = driver.find_element(
        By.CLASS_NAME, "mdl-button--raised")

    login_button.click()

    # Insert username/password
    username_input = driver.find_element(
        By.CLASS_NAME, "input")

    username_input.send_keys(username + Keys.ENTER)

    password_input = driver.find_element(
        By.NAME, "password")

    password_input.send_keys(password + Keys.ENTER)

    # Locate and select Project
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

    pole_ids = [pole.get_attribute("title") for pole in poles]

    pole_ids.sort(key=lambda x: x[0])

    # Iterate through poles, check for missing fields and add them to output dict
    missing_data = {}

    for id in pole_ids:

        next_pole = driver.find_element(
            By.XPATH, "//span[@title='" + id + "']")

        next_pole.click()

        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element(
            (By.CLASS_NAME, "c-CollectionEditTitle__Text"), id))

        missing = check_for_empty_fields(id)

        if missing:
            missing_data[id] = missing

        # debug(id)

    generate_output(missing_data)

    print("FINISH")
    driver.quit()


main()
