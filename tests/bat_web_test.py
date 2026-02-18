# Test Suite: Build Acceptance
from pages.Constants import HOMEWEB_DOMAIN, QUANTUM_API_DOMAIN


def test_bat_web_001(homeweb):
    # 1: Test - Navigate to Homeweb landing
    homeweb.navigate_landing()
    homeweb.set_landing(True)
    assert HOMEWEB_DOMAIN in homeweb.current_url.lower()
    f'Expected homeweb in URL, got: {homeweb.current_url}'

def test_bat_web_002(homeweb):
    assert homeweb.is_landing()
    resources = homeweb.landing["elements"]["resources"]
    paths = homeweb.landing["paths"]["resources"]

    # 1: Test - Resource 1
    homeweb.click_element("xpath", resources["emotional_intelligence"])
    assert paths["emotional_intelligence"] in homeweb.current_url.lower()
    assert homeweb.wait_for_resource_content()
    homeweb.go_back()

    # 2: Test - Resource 2
    homeweb.click_element("xpath", resources["anxiety"])
    assert paths["anxiety"] in homeweb.current_url.lower()
    assert homeweb.wait_for_resource_content()
    homeweb.go_back()

    # 3: Test - Resource 3
    homeweb.click_element("xpath", resources["letting_go"])
    assert paths["letting_go"] in homeweb.current_url.lower()
    assert homeweb.wait_for_resource_content()
    homeweb.go_back()

    # 4: Test - Resource 4
    homeweb.click_element("link text", resources["toolkit"])
    assert paths["toolkit"] in homeweb.current_url.lower()
    assert homeweb.wait_for_resource_content()
    homeweb.go_back()

def test_bat_web_003(homeweb, quantum, credentials):
    assert homeweb.is_landing()
    buttons = homeweb.landing["elements"]["buttons"]

    # 1: Test - Sign In - Button
    homeweb.click_element("xpath", buttons["sign_in"])
    assert QUANTUM_API_DOMAIN in quantum.current_url.lower()

    # 2: Test - Login - Homeweb - Personal
    quantum.login(credentials["personal"]["email"], credentials["personal"]["password"])
    assert homeweb.wait_for_dashboard()
    homeweb.set_authenticated(True)

# def test_bat_web_004(homeweb):
#     assert homeweb.is_authenticated()
#
#     # 1: Test - Navigate to resource
#     resource_target = HOMEWEB_BASE_URL + "/en/user/articles/56252b81e40e6f50062aa714"
#     homeweb.driver.get(resource_target)
#     assert homeweb.wait_for_resource_content()
#
# def test_bat_web_005(homeweb):
#     assert homeweb.is_authenticated()
#
#     # 1: Navigate to sentio resource
#     sentio_resource_target = HOMEWEB_BASE_URL + "/app/en/resources/62c5a1e929ed9c1608d0434b"
#     homeweb.driver.get(sentio_resource_target)
#     assert homeweb.wait_for_resource_content()
#
#     # 2: Test - Sentio transfer kickout
#     homeweb.click_element("class name", "btn-primary")
#     assert homeweb.wait_for_sentio_transfer()
#     homeweb.go_back()
#
# def test_bat_web_006(homeweb):
#     assert homeweb.is_authenticated()
#     header = homeweb.header
#     header_buttons = header.elements["buttons"]
#
#     # 1: Test - Menu dropdown
#     header.click_element("class name", header_buttons["menu"])
#     assert header.wait_for_account_menu()
#
#     # 2: Test - Logout
#     header.click_element("css selector", header_buttons["sign_out"])
#     assert "https://homeweb.ca/" in homeweb.current_url.lower()
#     assert homeweb.is_landing()
#     homeweb.set_authenticated(False)
#
# def test_bat_web_007(homeweb, quantum, credentials):
#     assert homeweb.is_landing()
#     header = homeweb.header
#     header_buttons = header.elements["buttons"]
#     paths = header.paths["buttons"]
#
#     # 1: Test - Sign In - Header
#     header.click_element("class name", header_buttons["sign_in"])
#     assert paths["sign_in"] in quantum.current_url.lower()
#
#     # 2: Test - Login - Homeweb - Demo
#     quantum.login(credentials["demo"]["email"], credentials["demo"]["password"])
#     assert homeweb.wait_for_dashboard()
#     homeweb.set_authenticated(True)
#
# def test_bat_web_008(homeweb):
#     assert homeweb.is_authenticated()
#     childcare_resource_target = HOMEWEB_BASE_URL + "/app/en/resources/579ba4db88db7af01fe6ddd4"
#     eldercare_resource_target = HOMEWEB_BASE_URL + "/app/en/resources/579ba49a88db7af01fe6ddc8"
#     hra_resource_target = HOMEWEB_BASE_URL + "/app/en/resources/579ba53088db7af01fe6dde6"
#
#     # 1: Test - ChildCare - Lifestage transfer kickout
#     homeweb.driver.get(childcare_resource_target)
#     assert homeweb.wait_for_resource_content()
#     homeweb.click_element("class name", "btn-primary")
#     assert homeweb.wait_for_lifestage_transfer()
#
#     # 2: Test - ElderCare - Lifestage transfer kickout
#     homeweb.driver.get(eldercare_resource_target)
#     assert homeweb.wait_for_resource_content()
#     homeweb.click_element("class name", "btn-primary")
#     assert homeweb.wait_for_lifestage_transfer()
#
#     # 3: Test - HRA - LifeStyles transfer kickout
#     homeweb.driver.get(hra_resource_target)
#     assert homeweb.wait_for_resource_content()
#     homeweb.click_element("class name", "btn-primary")
#     assert homeweb.wait_for_lifestyle_transfer()
#
# def test_bat_web_009(homeweb):
#     assert homeweb.is_authenticated()
#     header = homeweb.header
#     header_buttons = header.elements["buttons"]
#
#     # 1: Navigate to course
#     course_target = HOMEWEB_BASE_URL + "/app/en/resources/564a36083392100756dd3e32"
#     homeweb.driver.get(course_target)
#     assert homeweb.wait_for_resource_content()
#
#     # 2: Test - Open modal
#     homeweb.click_element("css selector", "[data-bs-toggle=\"modal\"]")
#     assert homeweb.wait_for_modal()
#
#     # 3: Test - Dismiss modal, display course content
#     homeweb.click_element("css selector", "[data-bs-dismiss=\"modal\"]")
#     assert homeweb.wait_for_course_content()
#     homeweb.wait_for_no_backdrop()
#     homeweb.wait_for_layout_idle()
#     homeweb.driver.switch_to.default_content()
#     homeweb.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
#
#     # 4: Test - Menu dropdown
#     header.click_element("class name", header_buttons["menu"])
#     assert header.wait_for_account_menu()
#
#     # 5: Test - Logout
#     header.click_element("css selector", header_buttons["sign_out"])
#     assert "https://homeweb.ca/" in homeweb.current_url.lower()
#     assert homeweb.is_landing()
#     homeweb.set_authenticated(False)
#
# def test_bat_web_010(homeweb):
#     resource_1_target = HOMEWEB_BASE_URL + "/summertime-and-your-health?embedded"
#     resource_2_target = HOMEWEB_BASE_URL + "/mental-health-benefits-of-exercise?embedded"
#     resource_3_target = HOMEWEB_BASE_URL + "/summer-beauty-from-the-inside-out?embedded"
#
#     # 1: Test - Embedded Resource - 1
#     homeweb.driver.get(resource_1_target)
#     assert homeweb.wait_for_resource_content()
#     homeweb.go_back()
#
#     # 2: Test - Embedded Resource - 2
#     homeweb.driver.get(resource_2_target)
#     assert homeweb.wait_for_resource_content()
#     homeweb.go_back()
#
#     # 3: Test - Embedded Resource - 3
#     homeweb.driver.get(resource_3_target)
#     assert homeweb.wait_for_resource_content()
#     homeweb.go_back()
#
# def test_bat_web_011(homeweb, quantum, customer_portal, credentials):
#     assert homeweb.is_landing()
#     paths = homeweb.landing["paths"]["buttons"]
#     header = customer_portal.header
#
#     # 1: Navigate to Customer Portal
#     homeweb.driver.get(CUSTOMER_PORTAL_BASE_URL)
#     assert paths["sign_in"] in quantum.current_url.lower()
#
#     # 2: Test - Login - Customer Portal - Personal
#     quantum.login(credentials["personal"]["email"], credentials["personal"]["password"])
#     assert customer_portal.wait_for_portal_login()
#     customer_portal.set_authenticated(True)
#
#     # 3: Test - Insights
#     assert customer_portal.wait_for_tableau_report()
#     customer_portal.driver.switch_to.default_content()
#
#     header.click_element("css selector", "[data-bs-toggle=\"dropdown\"]")
#     assert header.wait_for_insights_dropdown()
#     header.click_element("link text", "Equitable Dashboard")
#     assert customer_portal.wait_for_power_bi_report()
#     customer_portal.driver.switch_to.default_content()
#
#     header.click_element("css selector", "[data-bs-toggle=\"dropdown\"]")
#     assert header.wait_for_insights_dropdown()
#     header.click_element("link text", "Insights: Alberta Health Services")
#     assert customer_portal.wait_for_power_bi_report()
#     customer_portal.driver.switch_to.default_content()