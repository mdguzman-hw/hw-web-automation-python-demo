from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

from pages.BasePage import BasePage
from pages.Header import Header
from pages.Login import LoginPage


class QuantumAPI(BasePage):
    @property
    def current_url(self):
        return self.driver.current_url

    def __init__(self, driver, language):
        super().__init__(driver, language)
        self.driver = driver
        self.elements = LoginPage.EN if language == "en" else LoginPage.FR
        self._is_authenticated = False
        self.header = None
        self.update_header()

    def login(self, email, password):
        inputs = self.elements["elements"]["inputs"]

        # Email step
        self.input(inputs["email_address"], email)
        self.submit()

        password_input = self.wait_for_password()
        assert password_input.is_displayed()

        # Password step
        self.input(inputs["password"], password)
        self.submit()

    def update_header(self):
        user_type = "AUTH" if self._is_authenticated else "ANON"
        self.header = Header(self.driver, domain="quantum_api", language=self.language, user=user_type)

    def set_authenticated(self, value):
        self._is_authenticated = value
        self.update_header()

    def is_authenticated(self):
        return self._is_authenticated

    def input(self, input_identifier, input_value):
        email_input = self.wait.until(
            expected_conditions.visibility_of_element_located((By.XPATH, input_identifier))
        )
        email_input.clear()
        email_input.send_keys(input_value)

    def submit(self):
        next_button = self.wait.until(
            expected_conditions.visibility_of_element_located((By.XPATH, self.elements["elements"]["buttons"]["next"]))
        )
        next_button.click()

    def wait_for_password(self):
        xpath = self.elements["elements"]["inputs"]["password"]
        return self.wait.until(expected_conditions.visibility_of_element_located((By.XPATH, xpath)))
