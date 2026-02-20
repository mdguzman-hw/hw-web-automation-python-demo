from pages.BasePage import BasePage
from pages.Constants import SENTIO_BETA_CLIENT_BASE_URL, SENTIO_BETA_DOMAIN
from pages.Header import Header


class SentioBetaClient(BasePage):
    # Properties
    @property
    def current_url(self):
        return self.driver.current_url

    @property
    def base_url(self):
        return SENTIO_BETA_CLIENT_BASE_URL

    @property
    def landing_url(self):
        return self.base_url + "/" + self.language

    @property
    def domain(self):
        return SENTIO_BETA_DOMAIN

    @property
    def dashboard_endpoint(self):
        return "/app/" + self.language + "/dashboard"

    @property
    def is_landing(self):
        return self._is_landing

    @property
    def landing_elements(self):
        return SentioLanding.EN["elements"] if self.language == "en" else SentioLanding.FR["elements"]

    def __init__(self, driver, language):
        super().__init__(driver, language)
        # self.domain = SENTIO_BETA_DOMAIN
        # self.base_url = SENTIO_BETA_CLIENT_BASE_URL
        # self.landing_url = self.base_url + "/" + self.language
        self._is_authenticated = False
        self._is_landing = False
        self.header = None
        self.update_header()

    def update_header(self):
        user_type = "AUTH" if self._is_authenticated else "ANON"
        self.header = Header(self.driver, domain="sentio_beta_client", language=self.language, user=user_type)

    def set_authenticated(self, value):
        self._is_authenticated = value
        self.update_header()

    def navigate_landing(self):
        self.driver.get(self.landing_url)
        self._is_landing = True
    def go_back(self):
        self.driver.back()
        self.wait.until(
            lambda d: self.domain in d.current_url
        )
        self.driver.execute_script("window.scrollBy(0, 0);")

    def wait_for_dashboard(self):

        self._is_landing = False

        self.set_authenticated(True)

        return self.wait.until(
            lambda d: self.dashboard_endpoint in d.current_url.lower()
        )

class SentioLanding:
    EN = {
        "elements": {
            "get_started": "Get Started",
            "login": "Login"
        }
    }

    FR = {
        "elements": {
            "get_started": "Commencer",
            "login": "Ouvrir une session"
        }
    }






