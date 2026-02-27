################# BUILD ACCEPTANCE ################
############# SENTIO BETA - PROVIDER ##############
from selenium.webdriver.common.by import By


def test_bat_web_025(sentio_beta_provider, quantum):
    sentio_beta_provider.driver.get(sentio_beta_provider.base_url)
    assert quantum.base_url in sentio_beta_provider.current_url.lower()


def test_bat_web_026(sentio_beta_provider, quantum, credentials):
    quantum.login(credentials["personal"]["email"], credentials["personal"]["password"])
    assert sentio_beta_provider.wait_for_login()


def test_bat_web_027(sentio_beta_provider):
    assert sentio_beta_provider._is_authenticated

    # Login always navigates to EN, need to toggle to french manually after login
    header = sentio_beta_provider.header
    header_elements = header.elements
    if sentio_beta_provider.language == "fr":
        header.click_element(By.CSS_SELECTOR, ".btn.btn-nav-item.btn-language.btn-icon-spaced")

    assert sentio_beta_provider.wait_for_dashboard("classic")

    header.click_element(By.CSS_SELECTOR, header_elements["new"])
    assert sentio_beta_provider.wait_for_dashboard("new")


def test_bat_web_028(sentio_beta_provider, quantum):
    assert sentio_beta_provider._is_authenticated

    # 1: Test - Logout
    header = sentio_beta_provider.header
    header_buttons = header.elements["buttons"]
    header.click_element(By.CLASS_NAME, header_buttons["menu"])
    assert header.wait_for_account_menu(), "Menu not found"

    header.click_element(By.CSS_SELECTOR, header_buttons["menu_sign_out"])
    assert quantum.domain in sentio_beta_provider.current_url.lower()
