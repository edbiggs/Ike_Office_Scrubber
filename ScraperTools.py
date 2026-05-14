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
import re
import pandas as pd
import csv
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

    # Each entry: {"field", "xpath", "data type", "section", "subform"}
    # subform value = None for single-instance fields on the main page
    # subform value = "Equipment"/"Anchor"/etc. for multi-instance fields inside that subform
    # subform value = "Anchor>Guy"/"Span>PowerCircuit"/"Span>Communication" for nested subforms
    xpath_map = {
        "no_changes": {
            "xpath": "//a[@title='No changes']",
            "data type": "slider",
            "section": "main",
            "subform": None,
        },
        "pole_id": {
            "xpath": "//div[@title='ID']"
                     "[not(ancestor::div[contains(@class,'c-SubFormInstance')])]"
                     "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                     "//div[contains(@class,'is-dirty')]"
                     "//textarea",
            "data type": "value",
            "section": "main",
            "subform": None,
        },
        "pole_type": {
            "xpath": "//div[@title='Type']"
                     "[not(ancestor::div[contains(@class,'c-SubFormInstance')])]"
                     "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                     "//span[contains(@class,'c-MultiListInput__label')]",
            "data type": "text",
            "section": "main",
            "subform": None,
        },
        "tip": {
            "xpath": "//div[@title='Tip']"
                     "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                     "//div[contains(@class,'c-Input--ft') and contains(@class,'is-dirty')]"
                     "//input",
            "data type": "value",
            "section": "main",
            "subform": None,
        },
        "latitude": {
            "xpath": "//div[contains(@class,'c-Input--lat') and contains(@class,'is-dirty')]"
                     "//input",
            "data type": "value",
            "section": "main",
            "subform": None,
        },
        "longitude": {
            "xpath": "//div[contains(@class,'c-Input--lng') and contains(@class,'is-dirty')]"
                     "//input",
            "data type": "value",
            "section": "main",
            "subform": None,
        },
        # Not verified
        "pla_result": {
            "xpath": "//div[@title='PLA Result']"
                     "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                     "//textarea",
            "data type": "text",
            "section": "main",
            "subform": None,
        },
        "pole_tag": {
            "xpath": "//div[@title='Pole Tag']"
                     "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                     "//input[contains(@class,'c-SwitchInput__input')]",
            "data type": "slider",
            "section": "main",
            "subform": None,
        },
        "facility_id_slider": {
            "xpath": "//div[@title='Facility ID']"
                     "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                     "//input[contains(@class,'c-SwitchInput__input')]",
            "data type": "slider",
            "section": "main",
            "subform": None,
        },
        "facility_id_text": {
            "xpath": "//div[@title='Facility ID Number']"
                     "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                     "//div[contains(@class,'is-dirty')]"
                     "//textarea",
            "data type": "value",
            "section": "main",
            "subform": None,
        },
        "mf_hdw": {
            "xpath": "//div[@title='M/F Hdw.']"
                     "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                     "//div[contains(@class,'is-dirty')]"
                     "//textarea",
            "data type": "value",
            "section": "main",
            "subform": None,
        },
        "anchor_count": {
            "xpath": "//div[@title='Anchor']"
                     "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                     "//div[contains(@class,'is-dirty')]"
                     "//textarea",
            "data type": "value",
            "section": "main",
            "subform": None,
        },
        "riser_count": {
            "xpath": "//div[@title='Riser']"
                     "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                     "//div[contains(@class,'is-dirty')]"
                     "//textarea",
            "data type": "value",
            "section": "main",
            "subform": None,
        },
        "splice_point_slider": {
            "xpath": "//div[@title='Splice Point']"
                     "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                     "//input[contains(@class,'c-SwitchInput__input')]",
            "data type": "slider",
            "section": "main",
            "subform": None,
        },
        # Not verified
        "splice_type": {
            "xpath": "//div[@title='Splice Type']"
                     "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                     "//div[contains(@class,'is-dirty')]"
                     "//textarea",
            "data type": "value",
            "section": "main",
            "subform": None,
        },
        "slack_loop": {
            "xpath": "//div[@title='Slack Loop']"
                     "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                     "//input[contains(@class,'c-SwitchInput__input')]",
            "data type": "slider",
            "section": "main",
            "subform": None,
        },
        "storage_type": {
            "xpath": "//div[@title='Storage Type']"
                     "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                     "//div[contains(@class,'is-dirty')]"
                     "//textarea",
            "data type": "value",
            "section": "main",
            "subform": None,
        },
        # Not verified
        "strand": {
            "xpath": "//div[@title='Strand']"
                     "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                     "//textarea",
            "data type": "value",
            "section": "main",
            "subform": None,
        },
        "vault": {
            "xpath": "//div[@title='Vault']"
                     "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                     "//input[contains(@class,'c-SwitchInput__input')]",
            "data type": "slider",
            "section": "main",
            "subform": None,
        },
        "reel id": {
            "xpath": "//div[@title='Reel ID']"
                     "/following-sibling::div[contains(@class, 'c-CollectionField__Value')]"
                     "//textarea",
            "data type": "value",
            "section": "main",
            "subform": None,
        },
        "equipment_subform_count": {
            "xpath": "//div[contains(@class,'c-SubForm__TitleName') and @title='Equipment']"
                     "/following-sibling::div[contains(@class,'c-SubForm__TitleCount')]",
            "data type": "text",
            "section": "main",
            "subform": None,
        },
        "equipment_type": {
            "xpath": "//div[contains(@id,'ipf_equipmentType')]"
                     "//span[contains(@class,'c-MultiListInput__label')]",
            "data type": "text",
            "section": "equipment",
            "subform": None,
        },
        "equipment_orientation": {
            "xpath": "//div[contains(@id,'ipf_equipmentOrientation')]"
                     "//div[contains(@class,'c-Input--is-dirty')]"
                     "//input",
            "data type": "value",
            "section": "equipment",
            "subform": None,
        },
        "equipment_attachment_height_ft": {
            "xpath": "//div[contains(@id,'ipf_equipmentAttachmentHeight')]"
                     "//div[contains(@class,'c-Input--ft') and contains(@class,'is-dirty')]"
                     "//input",
            "data type": "value",
            "section": "equipment",
            "subform": None,
        },
        "equipment_attachment_height_in": {
            "xpath": "//div[contains(@id,'ipf_equipmentAttachmentHeight')]"
                     "//div[contains(@class,'c-Input--in') and contains(@class,'is-dirty')]"
                     "//input",
            "data type": "value",
            "section": "equipment",
            "subform": None,
        },
        "anchor_lead_length_ft": {
            "xpath": "//div[contains(@id,'ipf_anchorLeadLength')]"
                     "//div[contains(@class,'c-VectorInput__leftInput')]"
                     "//div[contains(@class,'c-Input--ft') and contains(@class,'is-dirty')]"
                     "//input",
            "data type": "value",
            "section": "anchor",
            "subform": None,
        },
        "anchor_lead_length_in": {
            "xpath": "//div[contains(@id,'ipf_anchorLeadLength')]"
                     "//div[contains(@class,'c-VectorInput__leftInput')]"
                     "//div[contains(@class,'c-Input--in') and contains(@class,'is-dirty')]"
                     "//input",
            "data type": "value",
            "section": "anchor",
            "subform": None,
        },
        "anchor_lead_orientation": {
            "xpath": "//div[contains(@id,'ipf_anchorLeadLength')]"
                     "//div[contains(@class,'c-Input--bearing') and contains(@class,'is-dirty')]"
                     "//input",
            "data type": "value",
            "section": "anchor",
            "subform": None,
        },
        "guy_count": {
            "xpath": "//div[@title='Guys']"
                     "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                     "//div[contains(@class,'is-dirty')]"
                     "//textarea",
            "data type": "value",
            "section": "main",
            "subform": None,
        },
        "guy_size": {
            "xpath": "//div[contains(@id,'ipf_anchorGuySize')]"
                     "//span[contains(@class,'c-MultiListInput__label')]",
            "data type": "text",
            "section": "anchor",
            "subform": "guy",
        },
        "guy_attachment_height_ft": {
            "xpath": "//div[contains(@id,'ipf_anchorGuyAttachmentHeight')]"
                     "//div[contains(@class,'c-Input--ft') and contains(@class,'is-dirty')]"
                     "//input",
            "data type": "value",
            "section": "anchor",
            "subform": "guy",
        },
        "guy_attachment_height_in": {
            "xpath": "//div[contains(@id,'ipf_anchorGuyAttachmentHeight')]"
                     "//div[contains(@class,'c-Input--in') and contains(@class,'is-dirty')]"
                     "//input",
            "data type": "value",
            "section": "anchor",
            "subform": "guy",
        },
        "span_subform_count": {
            "xpath": "//div[contains(@class,'c-SubForm__TitleName') and @title='Span']"
                     "/following-sibling::div[contains(@class,'c-SubForm__TitleCount')]",
            "data type": "text",
            "section": "main",
            "subform": None,
        },
        "communication_mid_span_height": {
            "xpath": "//div[contains(@id,'ipf_spanCommunicationMidSpanHeight')]"
                     "//div[contains(@class,'c-PMLink')]",
            "data type": "text",
            "section": "span",
            "subform": "communication",
        },
        "communication_size": {
            "xpath": "//div[contains(@id,'ipf_spanCommunicationSize')]"
                     "//span[contains(@class,'c-MultiListInput__label')]",
            "data type": "text",
            "section": "span",
            "subform": "communication",
        },
        "communication_owner": {
            "xpath": "//div[contains(@id,'ipf_spanCommunicationOwner')]"
                     "//span[contains(@class,'c-MultiListInput__label')]",
            "data type": "text",
            "section": "span",
            "subform": "communication",
        },
        "communication_horizontal_offset": {
            "xpath": "//div[contains(@id,'ipf_spanCommunicationHorizOffset')]"
                     "//div[contains(@class,'c-Input--is-dirty')]"
                     "//input",
            "data type": "value",
            "section": "span",
            "subform": "communication",
        },
        # PMLink form — only matches when attachment height is a linked value
        "communication_attachment_height": {
            "xpath": "//div[contains(@id,'ipf_spanCommunicationAttachmentHeight')]"
                     "//div[contains(@class,'c-PMLink') and not(contains(@class,'c-PMLink--inputs'))]",
            "data type": "text",
            "section": "span",
            "subform": "communication",
        },
        # Manual ft/in form — only matches when attachment height is hand-entered
        "communication_attachment_height_ft": {
            "xpath": "//div[contains(@id,'ipf_spanCommunicationAttachmentHeight')]"
                     "//div[contains(@class,'c-Input--ft') and contains(@class,'is-dirty')]"
                     "//input",
            "data type": "value",
            "section": "span",
            "subform": "communication",
        },
        "communication_attachment_height_in": {
            "xpath": "//div[contains(@id,'ipf_spanCommunicationAttachmentHeight')]"
                     "//div[contains(@class,'c-Input--in') and contains(@class,'is-dirty')]"
                     "//input",
            "data type": "value",
            "section": "span",
            "subform": "communication",
        },
        "communication_ms_clearance": {
            "xpath": "//div[@title='MS Clearance ']"
                     "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                     "//div[contains(@class,'c-PMLink')]",
            "data type": "text",
            "section": "span",
            "subform": "communication",
        },
        "communication_midspan_ike_photo": {
            "xpath": "//div[@title='MidSpan IKE Photo']"
                     "/following-sibling::div[contains(@class,'c-CollectionField__Value')]",
            "data type": "text",
            "section": "span",
            "subform": "communication",
        },
        "communication_joint_use": {
            "xpath": "//div[@title='Joint Use']"
                     "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                     "//input[contains(@class,'c-SwitchInput__input')]",
            "data type": "slider",
            "section": "span",
            "subform": "communication",
        },
        "ms_height": {
            "xpath": "//div[contains(@class,'c-SubFormInstance')]"
                     "[.//span[contains(@class,'c-MultiListInput__label') and contains(text(),'Fiber')]]"
                     "//div[@title='Mid Span Height']"
                     "/following-sibling::div"
                     "//div[contains(@class,'c-PMLink')]",
            "data type": "text",
            "section": "span",
            "subform": "communication",
        },
        "ms_clearance": {
            "xpath": "//div[contains(@class,'c-SubFormInstance')]"
                     "[.//span[contains(@class,'c-MultiListInput__label') and contains(text(),'Fiber')]]"
                     "//div[@title='MS Clearance ']"
                     "/following-sibling::div"
                     "//div[contains(@class,'c-PMLink')]",
            "data type": "text",
            "section": "span",
            "subform": "communication",
        },
        "span_length": {
            "xpath": "//div[contains(@id,'ipf_spanLength')]"
                     "//div[contains(@class,'c-Input')]/span",
            "data type": "text",
            "section": "span",
            "subform": "communication",
        },
        "span_type": {
            "xpath": "//div[contains(@id,'ipf_spanType')]"
                     "//span[contains(@class,'c-MultiListInput__label')]",
            "data type": "text",
            "section": "span",
            "subform": "communication",
        },
        "span_mid_span_ike_photo": {
            "xpath": "//div[contains(@id,'ipf_spanMidSpanIkePhoto')]"
                     "//div[contains(@class,'c-CollectionField__Value')]",
            "data type": "text",
            "section": "span",
            "subform": "communication",
        },
        "power_circuit_type": {
            "xpath": "//div[contains(@id,'ipf_spanPowerCircuitType')]"
                     "//span[contains(@class,'c-MultiListInput__label')]",
            "data type": "text",
            "section": "span",
            "subform": "power_circuit",
        },
        "power_circuit_primary_conductor": {
            "xpath": "//div[contains(@id,'ipf_spanPowerCircuitPrimaryConductor')]"
                     "//span[contains(@class,'c-MultiListInput__label')]",
            "data type": "text",
            "section": "span",
            "subform": "power_circuit",
        },
        "power_circuit_primary_framing": {
            "xpath": "//div[contains(@id,'ipf_spanPowerCircuitPrimaryFraming')]"
                     "//span[contains(@class,'c-MultiListInput__label')]",
            "data type": "text",
            "section": "span",
            "subform": "power_circuit",
        },
        "power_circuit_primary_phase_a_height_ft": {
            "xpath": "//div[contains(@id,'ipf_spanPowerCircuitPrimaryPhaseAHeight')]"
                     "//div[contains(@class,'c-Input--ft') and contains(@class,'is-dirty')]"
                     "//input",
            "data type": "value",
            "section": "span",
            "subform": "power_circuit",
        },
        "power_circuit_primary_phase_a_height_in": {
            "xpath": "//div[contains(@id,'ipf_spanPowerCircuitPrimaryPhaseAHeight')]"
                     "//div[contains(@class,'c-Input--in') and contains(@class,'is-dirty')]"
                     "//input",
            "data type": "value",
            "section": "span",
            "subform": "power_circuit",
        },
        "power_circuit_primary_phase_b_height_ft": {
            "xpath": "//div[contains(@id,'ipf_spanPowerCircuitPrimaryPhaseBHeight')]"
                     "//div[contains(@class,'c-Input--ft') and contains(@class,'is-dirty')]"
                     "//input",
            "data type": "value",
            "section": "span",
            "subform": "power_circuit",
        },
        "power_circuit_primary_phase_b_height_in": {
            "xpath": "//div[contains(@id,'ipf_spanPowerCircuitPrimaryPhaseBHeight')]"
                     "//div[contains(@class,'c-Input--in') and contains(@class,'is-dirty')]"
                     "//input",
            "data type": "value",
            "section": "span",
            "subform": "power_circuit",
        },
        "power_circuit_primary_phase_c_height_ft": {
            "xpath": "//div[contains(@id,'ipf_spanPowerCircuitPrimaryPhaseCHeight')]"
                     "//div[contains(@class,'c-Input--ft') and contains(@class,'is-dirty')]"
                     "//input",
            "data type": "value",
            "section": "span",
            "subform": "power_circuit",
        },
        "power_circuit_primary_phase_c_height_in": {
            "xpath": "//div[contains(@id,'ipf_spanPowerCircuitPrimaryPhaseCHeight')]"
                     "//div[contains(@class,'c-Input--in') and contains(@class,'is-dirty')]"
                     "//input",
            "data type": "value",
            "section": "span",
            "subform": "power_circuit",
        },
        "power_circuit_neutral_conductor": {
            "xpath": "//div[contains(@id,'ipf_spanPowerCircuitNeutralConductor')]"
                     "//span[contains(@class,'c-MultiListInput__label')]",
            "data type": "text",
            "section": "span",
            "subform": "power_circuit",
        },
        "power_circuit_neutral_framing": {
            "xpath": "//div[contains(@id,'ipf_spanPowerCircuitNeutralFraming')]"
                     "//span[contains(@class,'c-MultiListInput__label')]",
            "data type": "text",
            "section": "span",
            "subform": "power_circuit",
        },
        "power_circuit_neutral_height_ft": {
            "xpath": "//div[contains(@id,'ipf_spanPowerCircuitNeutralHeight')]"
                     "//div[contains(@class,'c-Input--ft') and contains(@class,'is-dirty')]"
                     "//input",
            "data type": "value",
            "section": "span",
            "subform": "power_circuit",
        },
        "power_circuit_neutral_height_in": {
            "xpath": "//div[contains(@id,'ipf_spanPowerCircuitNeutralHeight')]"
                     "//div[contains(@class,'c-Input--in') and contains(@class,'is-dirty')]"
                     "//input",
            "data type": "value",
            "section": "span",
            "subform": "power_circuit",
        }
    }

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

    def get_data_type(self, element, data_type):
        if data_type == "value":
            return element.get_attribute("value")
        elif data_type == "text":
            return element.text
        elif data_type == "slider":
            return element.is_selected()

    def get_field_data(self, pole_id):
        WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element(
            (By.CLASS_NAME, "c-CollectionEditTitle__Text"), pole_id))

        page = CurrentPole.CurrentPole(pole_id)

        missing_fields = []

        processed_fields = []

        for field, info in self.xpath_map.items():
            print(info["section"], info["subform"], info["xpath"])
        #     if subform is None:
        #         try:
        #             field_element = self.driver.find_element(By.XPATH, xpath)
        #             setattr(page, field, self.get_data_type(
        #                 field_element, data_type))
        #             processed_fields.append(field)
        #         except:
        #             missing_fields.append(field)
        #             processed_fields.append(field)
        #     else:
        #         form_count = 0
        #         parent_form_key = form_info["subform"]
        #         subforms = [
        #             name for name, (xpath, dtype, info) in self.xpath_map.items()
        #             if info["subform"] == parent_form_key
        #         ]

        #         try:
        #             field_element = self.driver.find_element(
        #                 By.XPATH, xpath)
        #             setattr(page, field + form_count, self.get_data_type(
        #                 field_element, data_type))
        #             processed_fields.append(field)
        #         except:
        #             missing_fields.append(field)
        #             processed_fields.append(field)
        #         for field in subforms:
        #             try:
        #                 field_element = self.driver.find_element(
        #                     By.XPATH, xpath)
        #                 setattr(page, field, self.get_data_type(
        #                     field_element, data_type))
        #                 processed_fields.append(field)
        #             except:
        #                 missing_fields.append(field)
        #                 processed_fields.append(field)

        # for attribute, value in vars(page).items():
        #     print(f"{attribute}: {value}")
        # for field in missing_fields:
        #     print("Missing: " + field)

    def get_subform_instances(self, title, scope=None):

        xpath = (
            f"//div[contains(@class,'c-SubForm__TitleName') and @title='{title}']"
            "/ancestor::div[contains(@class,'c-SubForm__Header')]"
            "/following-sibling::div[contains(@class,'c-SubFormInstance')]"
        )
        if scope is not None:
            return scope.find_elements(By.XPATH, "." + xpath)
        return self.driver.find_elements(By.XPATH, xpath)

    def to_snake_case(self, name):
        """PascalCase -> snake_case (PowerCircuit -> 'power_circuit')."""
        return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()

    def subform_title(self, name):
        """PascalCase -> space-separated title (PowerCircuit -> 'Power Circuit')."""
        return re.sub(r'(?<!^)(?=[A-Z])', ' ', name)

    def claude_version_get_field_data(self, pole_id):
        WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element(
            (By.CLASS_NAME, "c-CollectionEditTitle__Text"), pole_id))

        page = CurrentPole.CurrentPole(pole_id)
        missing_fields = []
        processed_fields = []

        # Keep WebElement for each top-level instance so Phase C can scope into it.
        # { "Anchor": [(anchor_obj_1, anchor_el_1), ...], ... }
        parent_instances = {}

        # ───── Phase A: pole-level fields (subform is None) ─────
        for field, (xpath, data_type, subform_info) in self.xpath_map.items():
            if subform_info["subform"] is None:
                try:
                    field_element = self.driver.find_element(By.XPATH, xpath)
                    setattr(page, field, self.get_data_type(
                        field_element, data_type))
                except:
                    missing_fields.append(field)
                processed_fields.append(field)

        # ───── Phase B: top-level subforms (no '>') ─────
        top_level_subforms = {
            info["subform"] for (_, _, info) in self.xpath_map.values()
            if info["subform"] is not None and ">" not in info["subform"]
        }

        for subform in top_level_subforms:
            inner_class = getattr(CurrentPole.CurrentPole, subform)
            title = self.subform_title(subform)
            attr_prefix = self.to_snake_case(subform)

            subform_fields = [
                (name, xp, dt) for name, (xp, dt, info) in self.xpath_map.items()
                if info["subform"] == subform
            ]

            instances = self.get_subform_instances(title)

            for form_count, inst_el in enumerate(instances, start=1):
                obj = inner_class()
                for name, xp, dt in subform_fields:
                    try:
                        el = inst_el.find_element(By.XPATH, "." + xp)
                        setattr(obj, name, self.get_data_type(el, dt))
                    except:
                        missing_fields.append(
                            f"{attr_prefix}_{form_count}.{name}")
                    processed_fields.append(name)
                setattr(page, f"{attr_prefix}_{form_count}", obj)
                parent_instances.setdefault(subform, []).append((obj, inst_el))

        # ───── Phase C: nested subforms (markers with '>') ─────
        nested_subforms = {
            info["subform"] for (_, _, info) in self.xpath_map.values()
            if info["subform"] is not None and ">" in info["subform"]
        }

        for subform in nested_subforms:
            parent_name, child_name = subform.split(">", 1)
            # Walk getattr chain: CurrentPole.Anchor.Guy
            inner_class = getattr(CurrentPole.CurrentPole, parent_name)
            inner_class = getattr(inner_class, child_name)
            child_title = self.subform_title(child_name)
            parent_prefix = self.to_snake_case(parent_name)
            child_prefix = self.to_snake_case(child_name)

            child_fields = [
                (name, xp, dt) for name, (xp, dt, info) in self.xpath_map.items()
                if info["subform"] == subform
            ]

            for p_idx, (parent_obj, parent_el) in enumerate(
                parent_instances.get(parent_name, []), start=1
            ):
                child_instances = self.get_subform_instances(
                    child_title, scope=parent_el)
                for form_count, child_el in enumerate(child_instances, start=1):
                    obj = inner_class()
                    for name, xp, dt in child_fields:
                        try:
                            el = child_el.find_element(By.XPATH, "." + xp)
                            setattr(obj, name, self.get_data_type(el, dt))
                        except:
                            missing_fields.append(
                                f"{parent_prefix}_{p_idx}.{child_prefix}_{form_count}.{name}"
                            )
                        processed_fields.append(name)
                    setattr(parent_obj, f"{child_prefix}_{form_count}", obj)

        for attribute, value in vars(page).items():
            print(f"{attribute}: {value}")
        for field in missing_fields:
            print("Missing: " + field)

    def generate_missing_fields_report(self, output_dict):
        for pole_id, fields in output_dict.items():
            print(f"{pole_id}:")
            for field in fields:
                print(f"{field}")
            print(" ")

    def debug(self, debug_field_name, debug_xpath, debug_data_type, pole_id):
        WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element(
            (By.CLASS_NAME, "c-CollectionEditTitle__Text"), pole_id))

        try:
            debug_field_element = self.driver.find_element(
                By.XPATH, debug_xpath)
            debug_field_element.click()
            if debug_data_type == "value":
                print(pole_id + ": " + debug_field_name +
                      " " + debug_field_element.get_attribute(
                          "value"))
            elif debug_data_type == "text":
                print(pole_id + ": " + debug_field_name +
                      " " + debug_field_element.text)
        except:
            print(pole_id + ": " + debug_field_name + " N/A")

    def create_reel_id_map(self, reel_id_file):
        reel_id_map = {}

        with open(reel_id_file) as file:
            reader = csv.DictReader(file)
            for row in reader:
                reel_id_map.setdefault(row["Reel ID"], []).append(row["ID"])
        return reel_id_map

    def insert_reel_id(self, pole_id):
        WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element(
            (By.CLASS_NAME, "c-CollectionEditTitle__Text"), pole_id))

        for reel_id, poles in self.reel_id_map.items():
            if pole_id in poles:
                reel_id_page_element = self.driver.find_element(
                    By.XPATH, self.xpath_map["reel id"][0])

                reel_id_page_element.click()

                self.actions.send_keys(reel_id)
                self.actions.key_down(Keys.CONTROL).send_keys(
                    's').key_up(Keys.CONTROL).perform()
                self.actions.reset_actions()
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                    (By.XPATH, self.xpath_map["no_changes"][0])))
