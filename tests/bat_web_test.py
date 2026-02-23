# Test Suite: Build Acceptance
import random

from selenium.webdriver.common.by import By


###################### HOMEWEB #####################
def test_bat_web_001(homeweb):
    # 1: Test - Navigate to Homeweb landing
    homeweb.navigate_landing()
    assert homeweb.domain in homeweb.current_url.lower()
    homeweb.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")


def test_bat_web_002(homeweb):
    assert homeweb.is_landing()
    resources = homeweb.public["elements"]["resources"]
    paths = homeweb.public["paths"]["resources"]

    # 1: Test - Resource 1
    homeweb.click_element(By.XPATH, resources["emotional_intelligence"])
    assert paths["emotional_intelligence"] in homeweb.current_url.lower()
    assert homeweb.wait_for_resource_content()
    homeweb.go_back()

    # 2: Test - Resource 2
    homeweb.click_element(By.XPATH, resources["anxiety"])
    assert paths["anxiety"] in homeweb.current_url.lower()
    assert homeweb.wait_for_resource_content()
    homeweb.go_back()

    # 3: Test - Resource 3
    homeweb.click_element(By.XPATH, resources["letting_go"])
    assert paths["letting_go"] in homeweb.current_url.lower()
    assert homeweb.wait_for_resource_content()
    homeweb.go_back()

    # 4: Test - Resource 4
    homeweb.click_element(By.LINK_TEXT, resources["toolkit"])
    assert paths["toolkit"] in homeweb.current_url.lower()
    assert homeweb.wait_for_resource_content()
    homeweb.go_back()


def test_bat_web_003(homeweb, quantum, credentials):
    assert homeweb.is_landing()
    buttons = homeweb.public["elements"]["buttons"]

    # 1: Test - Sign In - Button
    homeweb.click_element(By.XPATH, buttons["sign_in"])
    assert quantum.domain in quantum.current_url.lower()

    # 2: Test - Login - Homeweb - Personal
    quantum.login(credentials["personal"]["email"], credentials["personal"]["password"])
    assert homeweb.wait_for_dashboard()


def test_bat_web_004(homeweb):
    assert homeweb.is_authenticated()

    # 1: Test - Navigate to resource
    resource_target = homeweb.base_url + "/" + homeweb.language + "/user/articles/56252b81e40e6f50062aa714"
    homeweb.driver.get(resource_target)
    assert homeweb.wait_for_resource_content()


def test_bat_web_005(homeweb):
    assert homeweb.is_authenticated()

    # 1: Navigate to sentio resource
    sentio_resource_target = homeweb.base_url + "/app/" + homeweb.language + "/resources/62c5a1e929ed9c1608d0434b"
    homeweb.driver.get(sentio_resource_target)
    assert homeweb.wait_for_resource_content()

    # 2: Test - Sentio transfer kickout
    homeweb.click_element(By.CLASS_NAME, "btn-primary")
    assert homeweb.wait_for_sentio_transfer()
    homeweb.go_back()


def test_bat_web_006(homeweb):
    assert homeweb.is_authenticated()
    header = homeweb.header
    header_buttons = header.elements["buttons"]

    # 1: Test - Menu dropdown
    header.click_element(By.CLASS_NAME, header_buttons["menu"])
    assert header.wait_for_account_menu(), "Menu not found"

    # 2: Test - Logout
    header.click_element(By.CSS_SELECTOR, header_buttons["sign_out"])
    assert homeweb.wait_for_logout()

    # KNOWN ISSUE 1 - Workaround: Manually navigate back to landing (locale-aware)
    homeweb.navigate_landing()


def test_bat_web_007(homeweb, quantum, credentials):
    assert homeweb.is_landing()
    header = homeweb.header
    header_buttons = header.elements["buttons"]
    paths = header.paths["buttons"]

    # 1: Test - Sign In - Header
    header.click_element(By.CLASS_NAME, header_buttons["sign_in"])
    assert paths["sign_in"] in quantum.current_url.lower()

    # 2: Test - Login - Homeweb - Demo
    quantum.login(credentials["demo"]["email"], credentials["demo"]["password"])
    assert homeweb.wait_for_dashboard()


def test_bat_web_008(homeweb):
    assert homeweb.is_authenticated()
    childcare_resource_target = homeweb.base_url + "/app/" + homeweb.language + "/resources/579ba4db88db7af01fe6ddd4"
    eldercare_resource_target = homeweb.base_url + "/app/" + homeweb.language + "/resources/579ba49a88db7af01fe6ddc8"
    hra_resource_target = homeweb.base_url + "/app/" + homeweb.language + "/resources/579ba53088db7af01fe6dde6"

    # 1: Test - ChildCare - Lifestage transfer kickout
    homeweb.driver.get(childcare_resource_target)
    assert homeweb.wait_for_resource_content()
    homeweb.click_element(By.CLASS_NAME, "btn-primary")
    assert homeweb.wait_for_lifestage_transfer()

    # 2: Test - ElderCare - Lifestage transfer kickout
    homeweb.driver.get(eldercare_resource_target)
    assert homeweb.wait_for_resource_content()
    homeweb.click_element(By.CLASS_NAME, "btn-primary")
    assert homeweb.wait_for_lifestage_transfer()

    # 3: Test - HRA - LifeStyles transfer kickout
    homeweb.driver.get(hra_resource_target)
    assert homeweb.wait_for_resource_content()
    homeweb.click_element(By.CLASS_NAME, "btn-primary")
    assert homeweb.wait_for_lifestyle_transfer()


def test_bat_web_009(homeweb):
    assert homeweb.is_authenticated()
    header = homeweb.header
    header_buttons = header.elements["buttons"]

    # 1: Navigate to course
    course_target = homeweb.base_url + "/app/" + homeweb.language + "/resources/564a36083392100756dd3e32"
    homeweb.driver.get(course_target)
    assert homeweb.wait_for_resource_content()

    # 2: Test - Open modal
    homeweb.click_element(By.CSS_SELECTOR, "[data-bs-toggle=\"modal\"]")
    assert homeweb.wait_for_modal()

    # 3: Test - Dismiss modal, display course content
    homeweb.click_element(By.CSS_SELECTOR, "[data-bs-dismiss=\"modal\"]")
    # assert homeweb.wait_for_course_content()
    assert homeweb.wait_for_course_content(), "iframe content issue"

    # 4: Test - Menu dropdown
    header.click_element(By.CLASS_NAME, header_buttons["menu"])
    assert header.wait_for_account_menu(), "Menu not found"

    # 5: Test - Logout
    header.click_element(By.CSS_SELECTOR, header_buttons["sign_out"])
    assert homeweb.wait_for_logout()

    # KNOWN ISSUE 1 - Workaround: Manually navigate back to landing (locale-aware)
    homeweb.navigate_landing()


def test_bat_web_010(homeweb):
    lang_prefix = "" if homeweb.language.lower() == "en" else f"/{homeweb.language}"

    resource_1_target = homeweb.base_url + lang_prefix + "/summertime-and-your-health?embedded"
    resource_2_target = homeweb.base_url + lang_prefix + "/mental-health-benefits-of-exercise?embedded"
    resource_3_target = homeweb.base_url + lang_prefix + "/summer-beauty-from-the-inside-out?embedded"

    # 1: Test - Embedded Resource - 1
    homeweb.driver.get(resource_1_target)
    assert homeweb.wait_for_resource_content()
    homeweb.go_back()

    # 2: Test - Embedded Resource - 2
    homeweb.driver.get(resource_2_target)
    assert homeweb.wait_for_resource_content()
    homeweb.go_back()

    # 3: Test - Embedded Resource - 3
    homeweb.driver.get(resource_3_target)
    assert homeweb.wait_for_resource_content()
    homeweb.go_back()


################## CUSTOMER PORTAL #################
def test_bat_web_011(homeweb, quantum, customer_portal, credentials, language):
    assert homeweb.is_landing()

    # 1: Navigate to Customer Portal - Always EN
    homeweb.driver.get(customer_portal.base_url)
    assert quantum.base_url in quantum.current_url.lower()

    # 2: Test - Login - Customer Portal - Personal
    quantum.login(credentials["personal"]["email"], credentials["personal"]["password"])
    assert customer_portal.wait_for_portal_login()
    customer_portal.set_authenticated(True)

    # 2.1: Login always navigates to EN, need to toggle to french manually after login
    header = customer_portal.header
    header_buttons = header.elements["buttons"]
    header_dropdown = header.elements["dropdown"]
    if language == "fr":
        header.click_element("css selector", ".btn.btn-nav-item.btn-language.btn-icon-spaced")
        assert "fr" in customer_portal.current_url.lower()

    # 3: Test - Insights
    assert customer_portal.wait_for_tableau_report()

    header.click_element(By.CSS_SELECTOR, "[data-bs-toggle=\"dropdown\"]")
    assert header.wait_for_insights_dropdown()
    header.click_element(By.LINK_TEXT, header_dropdown["dropdown_eq"])
    assert customer_portal.wait_for_power_bi_report()

    header.click_element(By.CSS_SELECTOR, "[data-bs-toggle=\"dropdown\"]")
    assert header.wait_for_insights_dropdown()
    header.click_element(By.LINK_TEXT, header_dropdown["dropdown_ahs"])
    assert customer_portal.wait_for_power_bi_report()

    # 4: Test - Logout
    header.click_element(By.CLASS_NAME, header_buttons["menu"])
    assert header.wait_for_account_menu(), "Menu not found"

    header.click_element(By.CSS_SELECTOR, header_buttons["menu_sign_out"])
    assert header.wait_for_sign_out_group()

    header.click_element(By.LINK_TEXT, header_buttons["menu_sign_out_all"])
    assert quantum.domain in quantum.current_url.lower()


############### SENTIO BETA - CLIENT ###############
def test_bat_web_012(sentio_beta_client):
    sentio_beta_client.navigate_landing()
    assert sentio_beta_client.landing_url in sentio_beta_client.current_url.lower()


def test_bat_web_013(sentio_beta_client, quantum, credentials):
    assert sentio_beta_client._is_landing
    elements = sentio_beta_client.landing_elements

    sentio_beta_client.click_element(By.LINK_TEXT, elements["get_started"])
    assert quantum.base_url + "/" + sentio_beta_client.language + "/login" in sentio_beta_client.current_url.lower()

    sentio_beta_client.go_back()
    sentio_beta_client.click_element(By.LINK_TEXT, elements["login"])
    assert quantum.base_url + "/" + sentio_beta_client.language + "/login" in sentio_beta_client.current_url.lower()

    quantum.login(credentials["sentio"]["email"], credentials["sentio"]["password"])
    assert sentio_beta_client.wait_for_dashboard()


def test_bat_web_014(sentio_beta_client):
    assert sentio_beta_client._is_authenticated

    programs = sentio_beta_client.available_programs
    assert programs

    # Filter programs that are Completed or None
    valid_programs = [
        p for p in programs
        if p.status is None or p.status.lower() == "completed"
    ]

    assert valid_programs, "No completed or unstarted programs available"

    # Can modify this to be a specific program, if required
    test_program = random.choice(valid_programs)

    sentio_beta_client.navigate_overview(test_program.title)
    assert test_program.href in sentio_beta_client.current_url.lower()

    sentio_beta_client.navigate_assessment()
    assert "/assessments" and "take" in sentio_beta_client.current_url.lower()

    sentio_beta_client.complete_assessment()
    assert "/assessments" and "results" in sentio_beta_client.current_url.lower()

    tiers = sentio_beta_client.available_tiers
    provinces = sentio_beta_client.available_provinces
    assert tiers
    assert provinces

    # Can modify to be a specific tier and province, if required
    test_tier = random.choice(tiers)
    test_province = random.choice(provinces)
    sentio_beta_client.start_program(test_tier, test_province)


def test_bat_web_015(sentio_beta_client):
    assert sentio_beta_client._is_authenticated
    sentio_beta_client.navigate_dashboard()
    in_progress_programs = sentio_beta_client.in_progress_programs
    assert in_progress_programs, "No in_progress programs available"

    # Can modify to be a specific program, if required
    valid_program = random.choice(in_progress_programs)

    sentio_beta_client.continue_program(valid_program.title)
    assert valid_program.href_toc in sentio_beta_client.current_url.lower()


def test_bat_web_024(sentio_beta_client):
    assert sentio_beta_client._is_authenticated

    header = sentio_beta_client.header
    header_buttons = header.elements["buttons"]
    # 4: Test - Menu dropdown
    header.click_element(By.CLASS_NAME, header_buttons["menu"])
    assert header.wait_for_account_menu(), "Menu not found"

    # 5: Test - Logout
    header.click_element(By.CSS_SELECTOR, header_buttons["menu_sign_out"])
    assert sentio_beta_client.base_url in sentio_beta_client.current_url.lower()

############### SENTIO BETA - PROVIDER ###############
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
