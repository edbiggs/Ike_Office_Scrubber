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

import CurrentPole


load_dotenv()
class ScraperTools():

    def __init__(self):
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service)
        self.actions = ActionChains(self.driver)

        self.username = os.getenv("IKE_USERNAME")
        self.password = os.getenv("IKE_PASSWORD")
        self.job_name = os.getenv("JOB_NAME")

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

    fields_to_check = [
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

    def get_url(self):
        self.driver.get(
            "https://office.ikegps.com/#/login")

    def login(self):
        self.login = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.CLASS_NAME, "mdl-button--raised")))

        login_button = self.driver.find_element(
            By.CLASS_NAME, "mdl-button--raised")

        login_button.click()

        username_input = self.driver.find_element(
            By.CLASS_NAME, "input")

        username_input.send_keys(self.username + Keys.ENTER)

        password_input = self.driver.find_element(
            By.NAME, "password")

        password_input.send_keys(self.password + Keys.ENTER)

    def get_project(self):
        self.get_project = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "//span[@title='" + self.job_name + "']")))

        project = self.driver.find_element(
            By.XPATH, "//span[@title='" + self.job_name + "']")

        project.click()

        self.actions.send_keys(Keys.TAB * 2)
        self.actions.send_keys(Keys.ENTER)
        self.actions.perform()

    def get_pole_id_list(self):
        self.get_pole_list = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.CLASS_NAME, "c-CollectionCard__link")))

        poles = self.driver.find_elements(
            By.CLASS_NAME, "c-CollectionCard__link")

        pole_ids = [pole.get_attribute("title") for pole in poles]

        pole_ids.sort(key=lambda x: x[0])

        return pole_ids

    def get_next_pole(self, pole_id):
        next_pole = self.driver.find_element(
            By.XPATH, "//span[@title='" + pole_id + "']")

        next_pole.click()

    def check_missing_fields(self, pole_id):
        WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element(
            (By.CLASS_NAME, "c-CollectionEditTitle__Text"), pole_id))

        missing_fields = []

        page = CurrentPole.CurrentPole(pole_id)

        for field in self.fields_to_check:
            if field in self.xpath_map:
                xpath, data_type = self.xpath_map[field]
                try:
                    field_element = self.driver.find_element(By.XPATH, xpath)
                    if data_type == "value":
                        field_value = field_element.get_attribute(
                            "value")
                    elif data_type == "text":
                        field_value = field_element.text
                    setattr(page, field, field_value)
                except:
                    missing_fields.append(field)

        return missing_fields, page

    def generate_missing_fields_report(output_dict):
        for pole_id, fields in output_dict.items():
            print(f"{pole_id}:")
            for field in fields:
                print(f"{field}")
            print(" ")

    def debug(self, pole_id):
        try:
            ele = self.driver.find_element(
                By.XPATH,
                "//div[@title='Guys']"
                "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                "//div[contains(@class,'is-dirty')]"
                "//textarea").get_attribute("value")
        except:
            print(pole_id + ": N/A")
        else:
            print(pole_id + ": Guys: " + str(ele))


  
