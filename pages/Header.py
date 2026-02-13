from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import time


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
        element = self.wait.until(
            expected_conditions.element_to_be_clickable((by, locator))
        )

        # 2: Scroll element into view and click
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

        # 3: Wait for layout to stabilize
        self.wait.until(
            lambda d: element.is_displayed() and element.is_enabled()
        )

        # 4: Small pause to allow any final reflows
        time.sleep(0.5)

        # 5: Click
        element.click()

    def wait_for_dropdown(self):
        return self.wait.until(
            # expected_conditions.visibility_of_element_located(("css selector", "div.dropdown-menu.dropdown-account.show"))
            lambda d: "show" in d.find_element("css selector", "div.dropdown-menu.dropdown-account").get_attribute("class")
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
