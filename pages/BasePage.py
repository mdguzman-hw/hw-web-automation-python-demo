import time
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    def __init__(self, driver, language):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        self.language = language

    def click_element(self, by, locator):
        # 1: Find element
        element = self.wait.until(
            expected_conditions.presence_of_element_located((by, locator))
        )

        # 2: Scroll element into view
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )

        # 3: Wait for layout to stabilize
        self.wait.until(lambda d: element.is_displayed() and element.is_enabled())

        # 4: Small pause to allow any final reflows
        time.sleep(0.5)
        clickable_element = self.wait.until(
            expected_conditions.element_to_be_clickable((by, locator))
        )

        # 5: Click element
        clickable_element.click()
