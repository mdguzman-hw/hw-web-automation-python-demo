"""
Pytest configuration and shared fixtures
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.Homeweb import Homeweb
from pages.QuantumAPI import QuantumAPI


@pytest.fixture(scope="session")
def driver():
    # 1: Configure Chrome options
    chrome_options = Options()
    # chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    # 2: Launch Browser
    driver_instance = webdriver.Chrome(options=chrome_options)

    # 3. YIELD - give driver to the tests
    yield driver_instance

    # 4: Close Browser
    driver_instance.quit()

@pytest.fixture(scope="session")
def homeweb(driver):
    homeweb = Homeweb(driver)
    return homeweb

@pytest.fixture(scope="session")
def quantum(driver):
    quantum = QuantumAPI(driver)
    return quantum

