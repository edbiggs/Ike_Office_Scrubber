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
            "subform": None,
        },
        "pole_id": {
            "xpath": "//div[@title='ID']"
                     "[not(ancestor::div[contains(@class,'c-SubFormInstance')])]"
                     "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                     "//div[contains(@class,'is-dirty')]"
                     "//textarea",
            "data type": "value",
            "subform": None,
        },
        "pole_type": {
            "xpath": "//div[@title='Type']"
                     "[not(ancestor::div[contains(@class,'c-SubFormInstance')])]"
                     "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                     "//span[contains(@class,'c-MultiListInput__label')]",
            "data type": "text",
            "subform": None,
        },
        "tip": {
            "xpath": "//div[@title='Tip']"
                     "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                     "//div[contains(@class,'c-Input--ft') and contains(@class,'is-dirty')]"
                     "//input",
            "data type": "value",
            "subform": None,
        },
        "latitude": {
            "xpath": "//div[contains(@class,'c-Input--lat') and contains(@class,'is-dirty')]"
                     "//input",
            "data type": "value",
            "subform": None,
        },
        "longitude": {
            "xpath": "//div[contains(@class,'c-Input--lng') and contains(@class,'is-dirty')]"
                     "//input",
            "data type": "value",
            "subform": None,
        },
        # Not verified
        "pla_result": {
            "xpath": "//div[@title='PLA Result']"
                     "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                     "//textarea",
            "data type": "text",
            "subform": None,
        },
        "pole_tag": {
            "xpath": "//div[@title='Pole Tag']"
                     "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                     "//input[contains(@class,'c-SwitchInput__input')]",
            "data type": "slider",
            "subform": None,
        },
        "facility_id_slider": {
            "xpath": "//div[@title='Facility ID']"
                     "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                     "//input[contains(@class,'c-SwitchInput__input')]",
            "data type": "slider",
            "subform": None,
        },
        "facility_id_text": {
            "xpath": "//div[@title='Facility ID Number']"
                     "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                     "//div[contains(@class,'is-dirty')]"
                     "//textarea",
            "data type": "value",
            "subform": None,
        },
        "mf_hdw": {
            "xpath": "//div[@title='M/F Hdw.']"
                     "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                     "//div[contains(@class,'is-dirty')]"
                     "//textarea",
            "data type": "value",
            "subform": None,
        },
        "anchor_count": {
            "xpath": "//div[@title='Anchor']"
                     "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                     "//div[contains(@class,'is-dirty')]"
                     "//textarea",
            "data type": "value",
            "subform": None,
        },
        "riser_count": {
            "xpath": "//div[@title='Riser']"
                     "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                     "//div[contains(@class,'is-dirty')]"
                     "//textarea",
            "data type": "value",
            "subform": None,
        },
        "splice_point_slider": {
            "xpath": "//div[@title='Splice Point']"
                     "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                     "//input[contains(@class,'c-SwitchInput__input')]",
            "data type": "slider",
            "subform": None,
        },
        # Not verified
        "splice_type": {
            "xpath": "//div[@title='Splice Type']"
                     "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                     "//div[contains(@class,'is-dirty')]"
                     "//textarea",
            "data type": "value",
            "subform": None,
        },
        "slack_loop": {
            "xpath": "//div[@title='Slack Loop']"
                     "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                     "//input[contains(@class,'c-SwitchInput__input')]",
            "data type": "slider",
            "subform": None,
        },
        "storage_type": {
            "xpath": "//div[@title='Storage Type']"
                     "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                     "//div[contains(@class,'is-dirty')]"
                     "//textarea",
            "data type": "value",
            "subform": None,
        },
        # Not verified
        "strand": {
            "xpath": "//div[@title='Strand']"
                     "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                     "//textarea",
            "data type": "value",
            "subform": None,
        },
        "vault": {
            "xpath": "//div[@title='Vault']"
                     "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                     "//input[contains(@class,'c-SwitchInput__input')]",
            "data type": "slider",
            "subform": None,
        },
        "reel_id": {
            "xpath": "//div[@title='Reel ID']"
                     "/following-sibling::div[contains(@class, 'c-CollectionField__Value')]"
                     "//textarea",
            "data type": "value",
            "subform": None,
        },
        "equipment_subform_count": {
            "xpath": "//div[contains(@class,'c-SubForm__TitleName') and @title='Equipment']"
                     "/following-sibling::div[contains(@class,'c-SubForm__TitleCount')]",
            "data type": "text",
            "subform": {
                "equipment_type": {
                    "xpath": "//div[contains(@id,'ipf_equipmentType')]"
                     "//span[contains(@class,'c-MultiListInput__label')]",
                    "data type": "text",
                    "subform": None,
                },
                "equipment_orientation": {
                    "xpath": "//div[contains(@id,'ipf_equipmentOrientation')]"
                    "//div[contains(@class,'c-Input--is-dirty')]"
                    "//input",
                    "data type": "value",
                    "subform": None,
                },
                "equipment_attachment_height_ft": {
                    "xpath": "//div[contains(@id,'ipf_equipmentAttachmentHeight')]"
                    "//div[contains(@class,'c-Input--ft') and contains(@class,'is-dirty')]"
                    "//input",
                    "data type": "value",
                    "subform": None,
                },
                "equipment_attachment_height_in": {
                    "xpath": "//div[contains(@id,'ipf_equipmentAttachmentHeight')]"
                    "//div[contains(@class,'c-Input--in') and contains(@class,'is-dirty')]"
                    "//input",
                    "data type": "value",
                    "subform": None
                }
            }
        },
        "anchor_subform_count": {
            "xpath": "//div[contains(@class,'c-SubForm__TitleName') and @title='Anchor']"
                     "/following-sibling::div[contains(@class,'c-SubForm__TitleCount')]",
            "data type": "text",
            "subform": {
                "anchor_lead_length_ft": {
                    "xpath": "//div[contains(@id,'ipf_anchorLeadLength')]"
                     "//div[contains(@class,'c-VectorInput__leftInput')]"
                     "//div[contains(@class,'c-Input--ft') and contains(@class,'is-dirty')]"
                     "//input",
                    "data type": "value",
                    "subform": None,
                },
                "anchor_lead_length_in": {
                    "xpath": "//div[contains(@id,'ipf_anchorLeadLength')]"
                    "//div[contains(@class,'c-VectorInput__leftInput')]"
                    "//div[contains(@class,'c-Input--in') and contains(@class,'is-dirty')]"
                    "//input",
                    "data type": "value",
                    "subform": None,
                },
                "anchor_lead_orientation": {
                    "xpath": "//div[contains(@id,'ipf_anchorLeadLength')]"
                    "//div[contains(@class,'c-Input--bearing') and contains(@class,'is-dirty')]"
                    "//input",
                    "data type": "value",
                    "subform": None,
                },
                "guy_subform_count": {
                    "xpath": "//div[@title='Guys']"
                    "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                    "//div[contains(@class,'is-dirty')]"
                    "//textarea",
                    "data type": "value",
                    "subform": {
                        "guy_size": {
                            "xpath": "//div[contains(@id,'ipf_anchorGuySize')]"
                            "//span[contains(@class,'c-MultiListInput__label')]",
                            "data type": "text",
                            "subform": None,
                        },
                        "guy_attachment_height_ft": {
                            "xpath": "//div[contains(@id,'ipf_anchorGuyAttachmentHeight')]"
                            "//div[contains(@class,'c-Input--ft') and contains(@class,'is-dirty')]"
                            "//input",
                            "data type": "value",
                            "subform": None,
                        },
                        "guy_attachment_height_in": {
                            "xpath": "//div[contains(@id,'ipf_anchorGuyAttachmentHeight')]"
                            "//div[contains(@class,'c-Input--in') and contains(@class,'is-dirty')]"
                            "//input",
                            "data type": "value",
                            "subform": None,
                        },
                    }
                }
            }
        },
        "span_subform_count": {
            "xpath": "//div[contains(@class,'c-SubForm__TitleName') and @title='Span']"
                     "/following-sibling::div[contains(@class,'c-SubForm__TitleCount')]",
            "data type": "text",
            "subform": {
                "span_length": {
                    "xpath": "//div[contains(@id,'ipf_spanLength')]"
                     "//div[contains(@class,'c-Input')]/span",
                    "data type": "text",
                    "subform": None,
                },
                "span_type": {
                    "xpath": "//div[contains(@id,'ipf_spanType')]"
                    "//span[contains(@class,'c-MultiListInput__label')]",
                    "data type": "text",
                    "subform": None,
                },
                "span_mid_span_ike_photo": {
                    "xpath": "//div[contains(@id,'ipf_spanMidSpanIkePhoto')]"
                    "//div[contains(@class,'c-CollectionField__Value')]",
                    "data type": "text",
                    "subform": None,
                },
                "power_circuit_subform_count": {
                    "xpath": "//div[contains(@class,'c-SubForm__TitleName') and @title='Power Circuit']"
                    "/following-sibling::div[contains(@class,'c-SubForm__TitleCount')]",
                    "data type": "text",
                    "subform": {
                        "power_circuit_type": {
                            "xpath": "//div[contains(@id,'ipf_spanPowerCircuitType')]"
                            "//span[contains(@class,'c-MultiListInput__label')]",
                            "data type": "text",
                            "subform": None,
                        },
                        "power_circuit_primary_conductor": {
                            "xpath": "//div[contains(@id,'ipf_spanPowerCircuitPrimaryConductor')]"
                            "//span[contains(@class,'c-MultiListInput__label')]",
                            "data type": "text",
                            "subform": None,
                        },
                        "power_circuit_primary_framing": {
                            "xpath": "//div[contains(@id,'ipf_spanPowerCircuitPrimaryFraming')]"
                            "//span[contains(@class,'c-MultiListInput__label')]",
                            "data type": "text",
                            "subform": None,
                        },
                        "power_circuit_primary_phase_a_height_ft": {
                            "xpath": "//div[contains(@id,'ipf_spanPowerCircuitPrimaryPhaseAHeight')]"
                            "//div[contains(@class,'c-Input--ft') and contains(@class,'is-dirty')]"
                            "//input",
                            "data type": "value",
                            "subform": None,
                        },
                        "power_circuit_primary_phase_a_height_in": {
                            "xpath": "//div[contains(@id,'ipf_spanPowerCircuitPrimaryPhaseAHeight')]"
                            "//div[contains(@class,'c-Input--in') and contains(@class,'is-dirty')]"
                            "//input",
                            "data type": "value",
                            "subform": None,
                        },
                        "power_circuit_primary_phase_b_height_ft": {
                            "xpath": "//div[contains(@id,'ipf_spanPowerCircuitPrimaryPhaseBHeight')]"
                            "//div[contains(@class,'c-Input--ft') and contains(@class,'is-dirty')]"
                            "//input",
                            "data type": "value",
                            "subform": None,
                        },
                        "power_circuit_primary_phase_b_height_in": {
                            "xpath": "//div[contains(@id,'ipf_spanPowerCircuitPrimaryPhaseBHeight')]"
                            "//div[contains(@class,'c-Input--in') and contains(@class,'is-dirty')]"
                            "//input",
                            "data type": "value",
                            "subform": None,
                        },
                        "power_circuit_primary_phase_c_height_ft": {
                            "xpath": "//div[contains(@id,'ipf_spanPowerCircuitPrimaryPhaseCHeight')]"
                            "//div[contains(@class,'c-Input--ft') and contains(@class,'is-dirty')]"
                            "//input",
                            "data type": "value",
                            "subform": None,
                        },
                        "power_circuit_primary_phase_c_height_in": {
                            "xpath": "//div[contains(@id,'ipf_spanPowerCircuitPrimaryPhaseCHeight')]"
                            "//div[contains(@class,'c-Input--in') and contains(@class,'is-dirty')]"
                            "//input",
                            "data type": "value",
                            "subform": None,
                        },
                        "power_circuit_neutral_conductor": {
                            "xpath": "//div[contains(@id,'ipf_spanPowerCircuitNeutralConductor')]"
                            "//span[contains(@class,'c-MultiListInput__label')]",
                            "data type": "text",
                            "subform": None,
                        },
                        "power_circuit_neutral_framing": {
                            "xpath": "//div[contains(@id,'ipf_spanPowerCircuitNeutralFraming')]"
                            "//span[contains(@class,'c-MultiListInput__label')]",
                            "data type": "text",
                            "subform": None,
                        },
                        "power_circuit_neutral_height_ft": {
                            "xpath": "//div[contains(@id,'ipf_spanPowerCircuitNeutralHeight')]"
                            "//div[contains(@class,'c-Input--ft') and contains(@class,'is-dirty')]"
                            "//input",
                            "data type": "value",
                            "subform": None,
                        },
                        "power_circuit_neutral_height_in": {
                            "xpath": "//div[contains(@id,'ipf_spanPowerCircuitNeutralHeight')]"
                            "//div[contains(@class,'c-Input--in') and contains(@class,'is-dirty')]"
                            "//input",
                            "data type": "value",
                            "subform": None,
                        }
                    }
                }
            },
            "communication_subform_count": {
                "xpath": "//div[contains(@class,'c-SubForm__TitleName') and @title='Communication']"
                "/following-sibling::div[contains(@class,'c-SubForm__TitleCount')]",
                "data type": "text",
                "subform": {
                    "communication_mid_span_height": {
                        "xpath": "//div[contains(@id,'ipf_spanCommunicationMidSpanHeight')]"
                        "//div[contains(@class,'c-PMLink')]",
                        "data type": "text",
                        "subform": None,
                    },
                    "communication_size": {
                        "xpath": "//div[contains(@id,'ipf_spanCommunicationSize')]"
                        "//span[contains(@class,'c-MultiListInput__label')]",
                        "data type": "text",
                        "subform": None,
                    },
                    "communication_owner": {
                        "xpath": "//div[contains(@id,'ipf_spanCommunicationOwner')]"
                        "//span[contains(@class,'c-MultiListInput__label')]",
                        "data type": "text",
                        "subform": None,
                    },
                    "communication_horizontal_offset": {
                        "xpath": "//div[contains(@id,'ipf_spanCommunicationHorizOffset')]"
                        "//div[contains(@class,'c-Input--is-dirty')]"
                        "//input",
                        "data type": "value",
                        "subform": None,
                    },
                    "communication_attachment_height": {
                        "xpath": "//div[contains(@id,'ipf_spanCommunicationAttachmentHeight')]"
                        "//div[contains(@class,'c-PMLink') and not(contains(@class,'c-PMLink--inputs'))]",
                        "data type": "text",
                        "subform": None,
                    },
                    "communication_attachment_height_ft": {
                        "xpath": "//div[contains(@id,'ipf_spanCommunicationAttachmentHeight')]"
                        "//div[contains(@class,'c-Input--ft') and contains(@class,'is-dirty')]"
                        "//input",
                        "data type": "value",
                        "subform": None,
                    },
                    "communication_attachment_height_in": {
                        "xpath": "//div[contains(@id,'ipf_spanCommunicationAttachmentHeight')]"
                        "//div[contains(@class,'c-Input--in') and contains(@class,'is-dirty')]"
                        "//input",
                        "data type": "value",
                        "subform": None,
                    },
                    "communication_ms_clearance": {
                        "xpath": "//div[@title='MS Clearance ']"
                        "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                        "//div[contains(@class,'c-PMLink')]",
                        "data type": "text",
                        "subform": None,
                    },
                    "communication_midspan_ike_photo": {
                        "xpath": "//div[@title='MidSpan IKE Photo']"
                        "/following-sibling::div[contains(@class,'c-CollectionField__Value')]",
                        "data type": "text",
                        "subform": None,
                    },
                    "communication_joint_use": {
                        "xpath": "//div[@title='Joint Use']"
                        "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                        "//input[contains(@class,'c-SwitchInput__input')]",
                        "data type": "slider",
                        "subform": None,
                    },
                    "ms_height": {
                        "xpath": "//div[contains(@class,'c-SubFormInstance')]"
                        "[.//span[contains(@class,'c-MultiListInput__label') and contains(text(),'Fiber')]]"
                        "//div[@title='Mid Span Height']"
                        "/following-sibling::div"
                        "//div[contains(@class,'c-PMLink')]",
                        "data type": "text",
                        "subform": None,
                    },
                    "ms_clearance": {
                        "xpath": "//div[contains(@class,'c-SubFormInstance')]"
                        "[.//span[contains(@class,'c-MultiListInput__label') and contains(text(),'Fiber')]]"
                        "//div[@title='MS Clearance ']"
                        "/following-sibling::div"
                        "//div[contains(@class,'c-PMLink')]",
                        "data type": "text",
                        "subform": None,
                    }
                }
            }
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

    def extract_data(self, element, data_type):
        if data_type == "value":
            return element.get_attribute("value")
        elif data_type == "text":
            return element.text
        elif data_type == "slider":
            return element.is_selected()

    def get_data_recursion(self, field_dict, current_class, subform_level, sub_classes):
        for field, field_info in field_dict.items():
            if field_info["subform"] == None:
                try:
                    field_element = self.driver.find_element(
                        By.XPATH, field_info["xpath"])
                    setattr(current_class, field_element.extract_data(
                        field_element, field_info["data type"]
                    ))
                    print(field_info)
                except:
                    return field
            else:
                sub_class_key = f"{field} " + str(subform_level)
                subform_level += 1
                sub_classes[sub_class_key] = getattr(current_class, f"{field}")
                current_class = sub_classes[sub_class_key]
                self.get_data_recursion(
                    field, field_info["subform"], current_class, subform_level, sub_classes)

    def get_field_data(self, pole_id):
        WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element(
            (By.CLASS_NAME, "c-CollectionEditTitle__Text"), pole_id))

        page = CurrentPole.CurrentPole(pole_id)

        current_class = page

        subform_class = None

        subform_level = 0

        missing_fields = []

        sub_classes = {
        }

        for field, field_info in self.xpath_map.items():
            missing_fields.append(self.get_data_recursion(
                self.xpath_map, current_class, subform_level, sub_classes))
            print(missing_fields)
            # if field_info["subform"] == None:
            #     try:
            #         field_element = self.driver.find_element(
            #             By.XPATH, field_info["xpath"])
            #         setattr(current_class, field_element.extract_data(
            #             field_element, field_info["data type"]
            #         ))
            #     except:
            #         missing_fields.append(field)

            # else:
            #     sub_class_key = f"{field} " + subform_level
            #     sub_classes[sub_class_key] = getattr(current_class, f"{field}")()
            #     current_class = sub_classes[sub_class_key]
            #     self.get_data_recursion(field, field_info, current_class, subform_level, sub_classes)

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
