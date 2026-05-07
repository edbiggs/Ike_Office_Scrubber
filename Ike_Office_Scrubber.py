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
    "longitude",
    "pla_result",
    "pole_tag",
    "facility_id_slider",
    "facility_id_text",
    "mf_hdw",
    "anchor_count",
    "riser_count",
    "splice_point_slider",
    "splice_type",
    "slack_loop",
    "storage_type",
    "strand",
    "vault",
    "guys",
    "anchor_subsection_count",
    "ms_height",
    "ms_clearance"
]


# ChromeDriver and Selenium variables
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

actions = ActionChains(driver)


# Locators to identify elements on page
xpath_map = {
    "pole_id": [
        "//div[@title='ID']"
        "[not(ancestor::div[contains(@class,'c-SubFormInstance')])]"
        "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
        "//div[contains(@class,'is-dirty')]"
        "//textarea",
        "value"
    ],
    "pole_type": [
        "//div[@title='Type']"
        "[not(ancestor::div[contains(@class,'c-SubFormInstance')])]"
        "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
        "//span[contains(@class,'c-MultiListInput__label')]",
        "text"
    ],
    "tip": [
        "//div[@title='Tip']"
        "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
        "//div[contains(@class,'c-Input--ft') and contains(@class,'is-dirty')]"
        "//input",
        "value"
    ],
    "latitude": [
        "//div[contains(@class,'c-Input--lat') and contains(@class,'is-dirty')]"
        "//input",
        "value"
    ],
    "longitude": [
        "//div[contains(@class,'c-Input--lng') and contains(@class,'is-dirty')]"
        "//input",
        "value"
    ],
    # Not verified
    "pla_result": [
        "//div[@title='PLA Result']"
        "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
        "//textarea", "text"
    ],
    "pole_tag": [
        "//div[@title='Pole Tag']"
        "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
        "//input[contains(@class,'c-SwitchInput__input')]",
        "slider"
    ],
    "facility_id_slider": [
        "//div[@title='Facility ID']"
        "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
        "//input[contains(@class,'c-SwitchInput__input')]",
        "slider"
    ],
    "facility_id_text": [
        "//div[@title='Facility ID Number']"
        "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
        "//div[contains(@class,'is-dirty')]"
        "//textarea",
        "value"
    ],
    "mf_hdw": [
        "//div[@title='M/F Hdw.']"
        "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
        "//div[contains(@class,'is-dirty')]"
        "//textarea",
        "value"
    ],
    "anchor_count": [
        "//div[@title='Anchor']"
        "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
        "//div[contains(@class,'is-dirty')]"
        "//textarea",
        "value"
    ],
    "riser_count": [
        "//div[@title='Riser']"
        "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
        "//div[contains(@class,'is-dirty')]"
        "//textarea",
        "value"
    ],
    "splice_point_slider": [
        "//div[@title='Splice Point']"
        "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
        "//input[contains(@class,'c-SwitchInput__input')]",
        "slider"
    ],
    # Not verified
    "splice_type": [
        "//div[@title='Splice Type']"
        "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
        "//div[contains(@class,'is-dirty')]"
        "//textarea",
        "value"
    ],
    "slack_loop": [
        "//div[@title='Slack Loop']"
        "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
        "//input[contains(@class,'c-SwitchInput__input')]",
        "slider"
    ],
    "storage_type": [
        "//div[@title='Storage Type']"
        "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
        "//div[contains(@class,'is-dirty')]"
        "//textarea",
        "value"
    ],
    # Not verified
    "strand": [
        "//div[@title='Strand']"
        "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
        "//textarea",
        "value"
    ],
    "vault": [
        "//div[@title='Vault']"
        "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
        "//input[contains(@class,'c-SwitchInput__input')]",
        "slider"
    ],
    "guys": [
        "//div[@title='Guys']"
        "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
        "//div[contains(@class,'is-dirty')]"
        "//textarea",
        "value"
    ],
    "anchor_subsection_count": [
        "//div[contains(@class,'c-SubForm__TitleName') and @title='Anchor']"
        "/following-sibling::div[contains(@class,'c-SubForm__TitleCount')]",
        "text"
    ],
    "ms_height": [
        "//div[contains(@class,'c-SubFormInstance')]"
        "[.//span[contains(@class,'c-MultiListInput__label') and contains(text(),'Fiber')]]"
        "//div[@title='Mid Span Height']"
        "/following-sibling::div"
        "//div[contains(@class,'c-PMLink')]",
        "text"
    ],
    "ms_clearance": [
        "//div[contains(@class,'c-SubFormInstance')]"
        "[.//span[contains(@class,'c-MultiListInput__label') and contains(text(),'Fiber')]]"
        "//div[@title='MS Clearance ']"
        "/following-sibling::div"
        "//div[contains(@class,'c-PMLink')]",
        "text"
    ],
}

# ──────────────── Debug Mode ────────────────


def debug(pole_id):
    try:
        ele = driver.find_element(
            By.XPATH,
            "//div[@title='Guys']"
            "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
            "//div[contains(@class,'is-dirty')]"
            "//textarea").get_attribute("value")
    except:
        print(pole_id + ": N/A")
    else:
        print(pole_id + ": Guys: " + str(ele))


debug_mode = True


# ──────────────────────────────────────────────


class CurrentPage():

    def __init__(self):
        self.pole_id = None
        self.pole_type = None
        self.tip = None
        self.latitude = None
        self.longitude = None
        self.pla_result = None
        self.pole_tag = None
        self.facility_id_slider = None
        self.facility_id_text = None
        self.mf_hdw = None
        self.anchor_count = None
        self.riser_count = None
        self.splice_point_slider = None
        self.splice_type = None
        self.slack_loop = None
        self.storage_type = None
        self.strand = None
        self.vault = None
        self.guys = None
        self.anchor_subsection_count = None
        self.ms_height = None
        self.ms_clearance = None


def check_missing_fields(pole_id):
    missing_fields = []

    pole_id = CurrentPage()

    for field in check_fields:
        if field in xpath_map:
            xpath, data_type = xpath_map[field]
            try:
                field_element = driver.find_element(By.XPATH, xpath)
                if data_type == "value":
                    field_value = field_element.get_attribute(
                        "value")
                elif data_type == "text":
                    field_value = field_element.text
                setattr(pole_id, field, field_value)
            except:
                missing_fields.append(field)

    return [missing_fields, pole_id]


def generate_missing_fields_report(output_dict):
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

    # Generate list of pole IDs and sort in ascending order
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.CLASS_NAME, "c-CollectionCard__link")))

    poles = driver.find_elements(By.CLASS_NAME, "c-CollectionCard__link")

    pole_ids = [pole.get_attribute("title") for pole in poles]

    pole_ids.sort(key=lambda x: x[0])

    # Iterate through poles, check for missing_fields fields and add them to output dict
    missing_data = {}

    for pole_id in pole_ids:

        next_pole = driver.find_element(
            By.XPATH, "//span[@title='" + pole_id + "']")

        next_pole.click()

        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element(
            (By.CLASS_NAME, "c-CollectionEditTitle__Text"), pole_id))

        if debug_mode == True:
            debug(pole_id)
        else:
            output = check_missing_fields(pole_id)

            if output:
                missing_data[pole_id] = output[0]

    if missing_data:
        generate_missing_fields_report(missing_data)

    print("FINISH")
    driver.quit()


main()
