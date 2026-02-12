from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from pages.Login import LoginPage


class QuantumAPI:
    URL = "https://api.homewoodhealth.io/en/login"

    @property
    def current_url(self):
        return self.driver.current_url

    def __init__(self, driver, lang="EN"):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.login = LoginPage.EN if lang == "EN" else LoginPage.FR

    def open(self):
        self.driver.get(self.URL)

    def input(self, input_identifier, input_value):
        email_input = self.wait.until(
            expected_conditions.visibility_of_element_located((By.XPATH, input_identifier))
        )
        email_input.clear()
        email_input.send_keys(input_value)

    def submit(self):
        next_button = self.wait.until(
            expected_conditions.visibility_of_element_located((By.XPATH, self.login["elements"]["buttons"]["next"]))
        )
        next_button.click()

    def wait_for_password(self):
        xpath = self.login["elements"]["inputs"]["password"]
        return self.wait.until(expected_conditions.visibility_of_element_located((By.XPATH, xpath)))



