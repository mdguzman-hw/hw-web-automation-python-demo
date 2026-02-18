from pages.Authenticated import Authenticated
from pages.BasePage import BasePage
from pages.Constants import HOMEWEB_BASE_URL, HOMEWEB_DOMAIN, SENTIO_DOMAIN, LIFESTAGE_DOMAIN, LIFESTYLE_DOMAIN
from pages.Header import Header
from pages.Landing import LandingPage
from selenium.webdriver.support import expected_conditions


class Homeweb(BasePage):
    # Properties
    @property
    def current_url(self):
        return self.driver.current_url

    def __init__(self, driver, language):
        super().__init__(driver, language)
        self.base_url = HOMEWEB_BASE_URL
        self.landing = LandingPage.EN if language == "en" else LandingPage.FR
        self._is_authenticated = False
        self._is_landing = False
        self.header = None
        self.authenticated = None
        self.update_header()

    # Methods
    def update_header(self):
        user_type = "AUTH" if self._is_authenticated else "ANON"
        self.header = Header(self.driver, domain="homeweb", language=self.language, user=user_type)

    def navigate_landing(self):
        self.driver.get(f"{self.base_url}/{self.language}")

    def go_back(self):
        self.driver.back()
        self.wait.until(
            lambda d: "homeweb.ca" in d.current_url
        )
        self.driver.execute_script("window.scrollBy(0, 0);")

    def set_landing(self, value):
        self._is_landing = value

    def set_authenticated(self, value):
        self._is_authenticated = value
        self.update_header()
        self.authenticated = Authenticated.EN if self.language == "en" else Authenticated.FR

    def is_authenticated(self):
        return self._is_authenticated

    def is_landing(self):
        return self._is_landing

    def wait_for_dashboard(self):
        expected_path = f"/app/{self.language}/homeweb/dashboard"

        return self.wait.until(
            lambda d: HOMEWEB_DOMAIN in d.current_url.lower() and expected_path in d.current_url.lower()
        )

    def wait_for_resource_content(self):
        return self.wait.until(
            expected_conditions.visibility_of_element_located(("css selector", "#container-manager"))
        )

    def wait_for_sentio_transfer(self):
        return self.wait.until(
            lambda d: SENTIO_DOMAIN in d.current_url.lower() and "/sso/token" in d.current_url.lower()
        )

    def wait_for_lifestage_transfer(self):
        return self.wait.until(
            lambda d: LIFESTAGE_DOMAIN in d.current_url.lower()
        )

    def wait_for_lifestyle_transfer(self):
        return self.wait.until(
            lambda d: LIFESTYLE_DOMAIN in d.current_url.lower()
        )

    def wait_for_modal(self):
        return self.wait.until(
            expected_conditions.visibility_of_element_located(("class name", "modal-content"))
        )

    def wait_for_course_content(self):
        # 1: Locate embed container
        self.wait.until(
            expected_conditions.visibility_of_element_located(("class name", "iframeWrapper"))
        )

        # 2: Locate and switch to iframe content
        iframe = self.wait.until(
            expected_conditions.presence_of_element_located(("tag name", "iframe"))
        )
        self.driver.switch_to.frame(iframe)

        # 3: Wait for content slides to load
        return self.wait.until(
            expected_conditions.presence_of_element_located(("id", "div_Slide"))
        )

