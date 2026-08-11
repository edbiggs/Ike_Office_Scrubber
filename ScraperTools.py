from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from dotenv import load_dotenv
import os
import pandas as pd
import csv
from xpath_map import xpath_map


load_dotenv()

class ScraperTools():

    def __init__(self):

        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service)
        self.actions = ActionChains(self.driver)
        self.missing_fields = []
        self.output_dict = {}
        self.reel_id_map = {}
        self.inaccessible_span_lengths = {}


   # Startup functions
    #---------------------------------------------------------------------------------------------------------------
    def get_url(self):

        self.driver.get(
            "https://office.ikegps.com/#/login")


    def login(self, username, password):

        self.login = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.CLASS_NAME, "mdl-button--raised")))

        login_button = self.driver.find_element(
            By.CLASS_NAME, "mdl-button--raised")

        login_button.click()

        username_input = self.driver.find_element(
            By.CLASS_NAME, "input")

        username_input.send_keys(username + Keys.ENTER)

        password_input = self.driver.find_element(
            By.NAME, "password")

        password_input.send_keys(password + Keys.ENTER)


    def get_project(self, job_name):

        self.get_project = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "//span[@title='" + job_name + "']")))

        project = self.driver.find_element(
            By.XPATH, "//span[@title='" + job_name + "']")

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


# Data extraction functions
#---------------------------------------------------------------------------------------------------------------
    def extract_data(self, element, data_type, extracted_data=None):

        extractors = {
            "value": lambda el: el.get_attribute("value"),
            "text": lambda el: el.text,
            "slider": lambda el: el.is_selected(),
        }

        if data_type:
            extracted_data =  extractors[data_type](element)

        if not extracted_data:
            for extractor in extractors.values():
                try:
                    extracted_data = extractor(element)
                    if extracted_data:
                        return extracted_data
                except Exception:
                    continue

        return extracted_data


        
    def get_field_data(self, pole_id, field, field_xpath, data_type):  

        try:
            field_element = self.driver.find_element(
                By.XPATH, field_xpath)

            print(f"{pole_id}: Found field: {field}")

            data = self.extract_data(
                field_element, data_type)
            if not data:
                self.missing_fields.append(field)

        except Exception as e:
            print(f"{pole_id}: No field found: {field}: {str(e)}")
            self.missing_fields.append(field)


    def get_subform_field_data(self, pole_id, field, field_xpath, data_type):

        field_elements = self.driver.find_elements(
            By.XPATH, field_xpath)
        
        field_data = []

        for i, element in enumerate(field_elements):
            try:
                data = self.extract_data(element, data_type)
                print(f"{pole_id}: Found data for field {field} (element {i+1})")
                field_data.append(data)
                if not data:
                    self.missing_fields.append(field)

            except Exception as e:
                print(f"{pole_id}: No data found for field {field} (element {i+1}): {str(e)}")
                self.missing_fields.append(field)

        return field_data


    def process_data(self, pole_id, form_name, section, working_dict):
            
            field_data = {}
    
            for field, field_info in section["fields"].items():
                field_data[field] = self.get_subform_field_data(
                    pole_id, field, field_info["xpath"], field_info["data type"]
                )
    
            if form_name == "main":
                form_instance_count = 1
            else:
                form_count_field = f"{form_name}_count"
                form_count_info = section["fields"][form_count_field]
    
                form_instance_count = self.get_field_data(
                    pole_id, form_count_field, form_count_info["xpath"], form_count_info["data type"])
                form_instance_count = int(form_instance_count) if form_instance_count else 0
    
            for i in range(form_instance_count):
                instance_key = f"{form_name}{i + 1}"
                working_dict.setdefault(instance_key, {})
    
                for field, values in field_data.items():
                    working_dict[instance_key][field] = values[i] if i < len(values) else None
    
                for subform, subform_contents in section.get("subforms", {}).items():
                    working_dict[instance_key].setdefault(subform, {})
                    self.process_data(pole_id, subform, subform_contents, working_dict[instance_key][subform])
    
    
    def get_pole_data(self, pole_id):

        results = []
        self.missing_fields = []
        try:
            WebDriverWait(self.driver, 10).until(
                EC.text_to_be_present_in_element(
                    (By.CLASS_NAME, "c-CollectionEditTitle__Text"), pole_id
                )
            )
            print(f"Found pole: {pole_id}")
        except TimeoutException:
            print(f"Timeout waiting for pole: {pole_id}")
            return

        working_dict = {}
        for form_name, section in xpath_map.items():
            self.process_data(pole_id, form_name, section, working_dict)

        self.output_dict[pole_id] = working_dict

        if self.missing_fields:
            print(f"{pole_id}: Missing fields: {self.missing_fields}")
        else:
            print(f"{pole_id}: All fields found successfully!")

        print(f"working_dict: {working_dict}")
        return self.missing_fields, working_dict

    # Not yet functional
    def mid_span_correction(self, pole_id):

        try:
            WebDriverWait(self.driver, 10).until(
                EC.text_to_be_present_in_element(
                (By.CLASS_NAME, "c-CollectionEditTitle__Text"), 
                pole_id
                )
            )
        except TimeoutException:
            print(f"No pole info found (timeout)")

        try:
            mid_span_height = WebDriverWait(self.driver, 1).until(
            EC.presence_of_element_located((By.XPATH, xpath_map["communication_mid_span_height"]["xpath"]))
            )

            mid_span_clearance = WebDriverWait(self.driver, 1).until(
            EC.presence_of_element_located((By.XPATH, xpath_map["communication_ms_clearance"]["xpath"]))
            )

            if mid_span_clearance and not mid_span_height:
                mid_span_height.click()
                mid_span_height.send_keys(mid_span_clearance)
                self.actions.key_down(Keys.CONTROL).send_keys(
                    's').key_up(Keys.CONTROL).perform()
                self.actions.reset_actions()
        except:
            pass

        
    # Reel ID functions
    #---------------------------------------------------------------------------------------------------------------
    def create_reel_id_map(self, reel_id_file):

        with open(reel_id_file) as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.reel_id_map.setdefault(
                    row["Reel ID"], []).append(row["ID"])

    def insert_reel_id(self):

        for reel_id, poles in self.reel_id_map.items():
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, xpath_map["reel_id"]["xpath"])))
            

            pole_id_list = self.get_pole_id_list()
            not_found = []

            for pole in poles:
                if pole in pole_id_list:
                    self.get_next_pole(pole)

                    reel_id_page_element = self.driver.find_element(
                        By.XPATH, xpath_map["reel_id"]["xpath"])

                    reel_id_page_element.click()

                    self.actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform
                    self.actions.send_keys(Keys.DELETE)
                    self.actions.send_keys(reel_id)
                    self.actions.key_down(Keys.CONTROL).send_keys(
                        's').key_up(Keys.CONTROL).perform()
                    self.actions.reset_actions()

                    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                        (By.XPATH, xpath_map["no_changes"]["xpath"])))
                    print("Found: " + pole)
                else:
                    not_found.append(pole)

            for pole in not_found:
                print("Not found: " + pole)
                
            
    # Final sag: D = (W * L^2) / (8 * H)
    # D = sag (ft)
    # W = unit weigth (lbs/ft)
    # L = span length (ft)
    # H = horizontal tension (lbs)
    #---------------------------------------------------------------------------------------------------------------
    def calculate_final_sag(self, pole_id, pole_dict):
        for key, value in pole_dict.items():
            if key.startswith("span") and key != "span_type": 
                span_length_ft = value.get("span_length_ft")
                span_length_in = value.get("span_length_in")

                if span_length_ft is None:
                    print(f"Inaccessible value: {pole_id} {key}")
                    return "Inaccessible span length"

                else:
                    span_length = float(span_length_ft) + (float(span_length_in)/12)

                    L = span_length
                    W = 0.09316
                    H = 7.795 * (L ** 0.8258)
                    D = (W * L ** 2) / (8 * H)

                    print(f"Comm 1:\nL = {L}\nW = {W}\nH = {H}\nD = {D}")

                    return D
                
    # Outputs
    #---------------------------------------------------------------------------------------------------------------
    def generate_missing_fields_report(self, output_dict):
        for pole_id, fields in output_dict.items():
            print(f"{pole_id}:")
            for field in fields:
                print(f"{field}")
            print(" ")

    def export_final_sag(self, job_name, output_path=None):

        output_path = f"{job_name}_final_sag.xlsx"

        results = []

        for pole_id, pole_dict in self.output_dict.items():
            final_sag = self.calculate_final_sag(pole_id, pole_dict)
            results.append((pole_id, final_sag))

        df = pd.DataFrame(results, columns=["Pole ID", "Final Sag (ft)"])
        df.to_excel(output_path, index=False)