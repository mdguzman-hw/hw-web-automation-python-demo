from pages.Header import Header
from pages.Landing import LandingPage
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

class Homeweb:
    # Properties
    @property
    def title(self):
        return self.driver.title

    @property
    def current_url(self):
        return self.driver.current_url

    def __init__(self, driver, lang="EN"):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.lang = lang
        self.landing = LandingPage.EN if self.lang == "EN" else LandingPage.FR
        self._is_authenticated = False
        self._is_landing = False
        self.header = None
        self.update_header()

    # Methods
    def update_header(self):
        user_type = "AUTH" if self._is_authenticated else "ANON"
        self.header = Header(self.driver, self.lang, user_type)

    
    def navigate_landing(self):
        url = self.landing["base_url"]
        self.driver.get(url)

    def click_element(self, by, locator):
        # 1: Find element
        element = WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located((by, locator))
        )

        # 2: Scroll element into view and click
        ActionChains(self.driver).move_to_element(element).click().perform()

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

    def is_authenticated(self):
        return self._is_authenticated

    def is_landing(self):
        return self._is_landing

    def wait_for_dashboard(self):
        return self.wait.until(
            lambda d: "homeweb" in d.current_url.lower() and "/app/en/homeweb/dashboard" in d.current_url.lower()
        )

    def wait_for_resource_content(self):
        return self.wait.until(
            expected_conditions.visibility_of_element_located(("css selector", "#container-manager"))
        )

    def wait_for_sentio_transfer(self):
        return self.wait.until(
            lambda d: "sentioapp" in d.current_url.lower() and "/sso/token" in d.current_url.lower()
        )

    def wait_for_lifestage_transfer(self):
        return self.wait.until(
            lambda d: "lifestagecare" in d.current_url.lower()
        )

    def wait_for_lifestyle_transfer(self):
        return self.wait.until(
            lambda d: "healthycommunity" in d.current_url.lower()
        )

    def wait_for_modal(self):
        return self.wait.until(
            expected_conditions.visibility_of_element_located(("class name", "modal-content"))
        )

    def wait_for_course_content(self):
        return self.wait.until(
            expected_conditions.visibility_of_element_located(("class name", "iframeWrapper"))
        )

