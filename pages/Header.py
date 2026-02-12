from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class Header:
    def __init__(self,  driver, lang="EN", user="ANON"):
        self.driver = driver
        self.lang = lang
        self.wait = WebDriverWait(driver, 10)
        self.type = HeaderAuth if user == "AUTH" else HeaderAnon
        self.elements = self.type.EN["elements"] if lang == "EN" else self.type.FR["elements"]
        self.paths = self.type.EN["paths"] if lang == "EN" else self.type.FR["paths"]

    def click_element(self, by, locator):
        # 1: Find element
        element = WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located((by, locator))
        )

        # 2: Scroll element into view and click
        ActionChains(self.driver).move_to_element(element).click().perform()

    def wait_for_dropdown(self):
        return self.wait.until(
            expected_conditions.visibility_of_element_located(("css selector", "div.dropdown-menu.dropdown-account.show"))
        )

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
                "sign_out": ""
            }
        },
        "paths": {
        }
    }
