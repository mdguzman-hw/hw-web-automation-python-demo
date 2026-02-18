from selenium.webdriver.support import expected_conditions
from pages.BasePage import BasePage


class HeaderAnon:
    EN = {
        "elements": {
            "buttons": {
                "sign_in": "btn-login"
            }
        },
        "paths": {
            "buttons": {
                "sign_in": "/en/login"
            }
        }
    }

    FR = {
        "elements": {
            "buttons": {
                "sign_in": "btn-login"
            }
        },
        "paths": {
            "buttons": {
                "sign_in": "/fr/login"
            }
        }
    }


class HeaderAuth:
    EN = {
        "elements": {
            "buttons": {
                "menu": "nav-account-toggle",
                "sign_out": "[aria-label=\"Sign out\"]"
            }
        },
        "paths": {
        }
    }

    FR = {
        "elements": {
            "buttons": {
                "menu": "nav-account-toggle",
                "sign_out": "[aria-label=\"Se déconnecter\"]"
            }
        },
        "paths": {
        }
    }


class HeaderCustomerPortal:
    EN = {
        "elements": {
            "buttons": {
                "menu": "nav-account-toggle",
                "sign_out": "[aria-label=\"Sign out\"]"
            }
        },
        "paths": {
        }
    }

    FR = {
        "elements": {
            "buttons": {
                "menu": "nav-account-toggle",
                "sign_out": ""
            }
        },
        "paths": {
        }
    }


class Header(BasePage):
    DOMAIN_MAP = {
        "homeweb": {"AUTH": HeaderAuth, "ANON": HeaderAnon},
        "customer_portal": {"AUTH": HeaderCustomerPortal, "ANON": HeaderAnon},
        "quantum_api": {"AUTH": HeaderAuth, "ANON": HeaderAnon},  # adjust if needed
    }

    def __init__(self, driver, language, domain="homeweb", user="ANON"):
        super().__init__(driver, language)
        self.type = HeaderAuth if user == "AUTH" else HeaderAnon
        self.domain = domain.lower()
        self.user = user.upper()

        domain_class = self.DOMAIN_MAP[self.domain][self.user]

        self.elements = domain_class.EN["elements"] if language == "en" else domain_class.FR["elements"]
        self.paths = domain_class.EN.get("paths", {}) if language == "en" else domain_class.FR.get("paths", {})

    def wait_for_account_menu(self):
        return self.wait.until(
            expected_conditions.visibility_of_element_located(
                ("css selector", "div.dropdown-menu.dropdown-account.show")
            )
        )

    def wait_for_insights_dropdown(self):
        return self.wait.until(
            expected_conditions.visibility_of_element_located(
                ("css selector", "ul.dropdown-menu.dropdown-insights.show")
            )
        )
